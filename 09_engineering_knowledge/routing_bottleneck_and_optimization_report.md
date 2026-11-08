# DESK Autonomous Routing Bottleneck & Engine Optimization Report
**Project:** Voice-Interactive Wearable Hardware Rework V2 (`WATCH`)  
**Repository:** `https://github.com/NijoP/project-one`  
**Target Codebase to Optimize:** `https://github.com/NijoP/DESK` (`C:\watch\desk`)  
**Author:** DESK Engineering Coordinator  
**Date:** 2026-11-09  

---

## 1. Executive Summary

During the Hardware Rework V2 of the Voice-Interactive Wearable PCB, autonomous component placement and physical anchor locking succeeded with **$0.000\text{ mil}$ drift** across all 5 mandatory mechanical anchors (`J1`, `J2`, `J5`, `J6`, `U5`), zero component collisions, and complete clearance of the ESP32-S3 antenna corridor.

However, the subsequent **4-layer autonomous routing phase** experienced severe, unexpected execution delays (>45 minutes cumulative runtime). Deep technical profiling of the Java OpenJDK-23 runtime, thread dumps via `jstack`, and Freerouting log traces revealed that these delays were **not** caused by normal mathematical routing complexity, but by **five specific architectural and configuration bottlenecks** in the interaction between DESK's tuning engine and the Freerouting CLI daemon.

This report comprehensively documents:
1. Every engineering method executed during this rework.
2. The exact technical root causes of each routing bottleneck and delay source.
3. Structural engineering recommendations for the DESK codebase (`C:\watch\desk`) so future autonomous rework runs can route complex 4-layer boards in **under 3 minutes**.

---

## 2. Methodology & Execution Pipeline

The rework followed DESK's autonomous hardware coordinator workflow:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DESK EXECUTION WORKFLOW                               │
└─────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  [1. LIVE AUDIT] ──► Query EasyEDA Pro via WebSocket bridge (`localhost:49620`)
         │            Extract schematic metadata, netlist, PCB primitives, anchors
         ▼
  [2. PLACEMENT]  ──► Relocate `SW5` inside board layout (Right Rim: 1550, 1250 mil)
         │            Align `SW1`–`SW4` at Y=1622 mil (pitch 223 mil, outside keepout)
         │            Space `J3`/`J4` speaker pair to 260 mil pitch (1.30 mm pad gap)
         │            Restore & freeze `J2` battery pads at exact baseline (Option A)
         ▼
  [3. LOCK GATE]  ──► Verify 0.000 mil drift on J1, J2, J5, J6, U5 via verify_locks.py
         │            Confirm 0 DRC placement overlaps and 0 keepout violations
         ▼
  [4. DSN TUNING] ──► Export raw Specctra DSN via eda.pcb_ManufactureData.getDsnFile()
         │            Inject boundary, antenna keepout polygon, and IPC-2152 rules
         ▼
  [5. AUTOROUTE]  ──► Execute Freerouting v2.1.0 headless daemon (4-layer stackup)
         │            Iterate rip-up and re-route passes across 59 nets (373 pins)
         ▼
  [6. SES IMPORT] ──► Ingest desk_route.ses via eda.pcb_Document.importAutoRouteSesFile()
         │            Execute post-import heavy-copper power trunk widening (VBAT/VSYS)
         ▼
  [7. DRC VALID]  ──► Run native EasyEDA DRC & DESK converge gate for final signoff
```

---

## 3. Deep-Dive Root Cause Analysis of Routing Bottlenecks

### Bottleneck 1: Headless Execution Freeze via Modal Swing GUI Dialog
- **Observed Behavior:** Java process `PID 12088` consumed >980 seconds of CPU time and remained permanently stuck in `RUNNING` status without ever writing `desk_route.ses` or exiting.
- **Investigation:** Running `jstack 12088` revealed the following blocking thread state:
  ```java
  "Thread-13" prio=5 os_prio=0 tid=0x0000011a22b253e0 nid=28040 in Object.wait()
     java.lang.Thread.State: WAITING (on object monitor)
      at java.awt.Dialog.show(java.desktop@23.0.2/Dialog.java:1079)
      at java.awt.Window.setVisible(java.desktop@23.0.2/Window.java:1036)
      at java.awt.Dialog.setVisible(java.desktop@23.0.2/Dialog.java:1015)
      at app.freerouting.gui.WindowUserSettings.<init>(WindowUserSettings.java:249)
      at app.freerouting.gui.WindowUserSettings.show(WindowUserSettings.java:257)
      at app.freerouting.gui.BoardMenuBar.showProfileDialog(BoardMenuBar.java:70)
      at app.freerouting.interactive.InteractiveActionThread$1.autorouterFinished(InteractiveActionThread.java:73)
  ```
- **Root Cause:** Freerouting v2.1.0 defaults to `"gui": { "enabled": true }` in `freerouting.json`. When the autorouter finishes pass 15, `autorouterFinished()` triggers `showProfileDialog()`, which opens a modal Swing dialog expecting human GUI input. Because the process was spawned as a background headless subprocess, the dialog was invisible and blocked execution indefinitely.
- **Resolution:**
  1. Append `--gui.enabled=false` explicitly to the Freerouting CLI invocation.
  2. Write `"gui": { "enabled": false }` to `%TEMP%\freerouting\freerouting.json` and the working directory.

---

### Bottleneck 2: Geometric Pin Trap on Fine-Pitch ICs (Maze Search Collapse)
- **Observed Behavior:** In initial routing attempts, 143 to 183 pin connections failed with the repetitive log error:
  `Autorouter Failed to route connection between pin #... and pin #..., because the maze search algorithm could not be created.`
- **Investigation:**
  - High-current power rules mandated $W_{VBAT} = 35.0\text{ mil}$ ($0.89\text{ mm}$), $W_{VSYS} = 30.0\text{ mil}$, and $W_{GND} = 25.0\text{ mil}$.
  - In `desk/router.py`, the DSN class replacement regex injected these full widths directly into the global net class rules:
    ```lisp
    (class VBAT 'VBAT' (circuit (use_via via0)) (rule (width 35.0) (clearance 4.02)))
    (class GND 'GND'   (circuit (use_via via0)) (rule (width 25.0) (clearance 4.02)))
    ```
  - However, `BQ24074` is a 16-pin QFN with a **$0.50\text{ mm}$ ($19.68\text{ mil}$) pitch** and only **$9.84\text{ mil}$ ($0.25\text{ mm}$)** of clearance gap between adjacent pads.
  - A $35.0\text{ mil}$ trace has a half-width of $17.5\text{ mil}$. Placed at the center of pin 13 (`BAT`), the trace edge is only $19.68 - 17.5 = 2.18\text{ mil}$ from pin 12. Because the minimum clearance rule is $4.02\text{ mil}$, the trace physically shorts against pin 12 and pin 14 at the pad boundary.
  - In Freerouting's `MazeSearchAlgo.init()`, `overlapping_objects()` checks if the start door intersects any neighboring obstacle. Because the $35\text{ mil}$ trace boundary collided with adjacent QFN pads, the search door collapsed, returning `null` (`maze search algorithm could not be created`).
- **Root Cause:** Enforcing high-current trace widths at the global DSN net class level without pin-level escape neckdown makes routing fine-pitch QFN and IC pads mathematically impossible.
- **Resolution:**
  - Decouple router escape width from physical power trunk width.
  - In DSN: set `VBAT`, `VSYS`, `VBUS` class width to **$10.0\text{ mil}$** (or $8.0\text{ mil}$), which leaves $>4.5\text{ mil}$ clearance margin when touching a $0.5\text{ mm}$ QFN pad.
  - After SES import: execute a post-processing pass in EasyEDA canvas to widen the open-board power trunks between `J2`, `C5`, and power switches to **$35.0\text{ mil}$** ($0.89\text{ mm}$).

---

### Bottleneck 3: Routing Grid Resolution Trap ($0.25\text{ mil}$ vs $1.25\text{ mil}$)
- **Observed Behavior:** When the DSN wire grid was changed from `(grid wire 1.25)` to `(grid wire 0.25)`, routing pass durations exploded, and long cross-board nets (SPI, I2S, LCD control) repeatedly timed out with `OptViaAlgo.opt_via_location: probably endless loop`.
- **Investigation:**
  - A $45\text{ mm} \times 45\text{ mm}$ board spans $1771.65\text{ mil} \times 1771.65\text{ mil}$.
  - At a **$1.25\text{ mil}$ grid**: the search matrix is $\approx 1,417 \times 1,417 \approx 2.0 \times 10^6$ nodes. Freerouting's A* maze search traverses this in $<1.5\text{ seconds}$ per pass.
  - At a **$0.25\text{ mil}$ grid**: the search matrix is $\approx 7,086 \times 7,086 \approx 50.2 \times 10^6$ nodes ($25\times$ more memory and node expansions).
  - Freerouting incorporates an internal constant `TIME_LIMIT_TO_PREVENT_ENDLESS_LOOP`. On a 0.25 mil grid, long paths exhaust this node exploration budget before reaching the opposite side of the board and abort.
- **Root Cause:** Over-specifying grid resolution in the DSN file exponentially increases A* state space without improving manufacturability.
- **Resolution:** Retain `(grid wire 1.25)` and `(grid via 1.25)` for global routing, relying on EasyEDA Pro's internal CAD snapping for exact pad centering.

---

### Bottleneck 4: Pass Termination Ambiguity (`maxPasses` vs `stop_pass_no`)
- **Observed Behavior:** Invoking `tools/route.py` with `--passes 1` or `--passes 20` resulted in Freerouting running past pass #200 without terminating.
- **Investigation:**
  - Disassembling `app.freerouting.settings.GlobalSettings` revealed that the `-mp <int>` CLI argument sets `routerSettings.maxPasses`.
  - However, disassembling `app.freerouting.autoroute.BatchAutorouter.runBatchLoop()` revealed the actual loop termination check:
    ```java
    101: invokevirtual RouterSettings.get_start_pass_no:()I
    104: istore 4
    106: iload 4
    109: invokevirtual RouterSettings.get_stop_pass_no:()I
    115: if_icmple 128 // continues loop until stop_pass_no!
    ```
  - In `RouterSettings`, `stop_pass_no` is initialized to **`999`** by default!
  - Therefore, unless all unrouted connections hit zero or the job timeout expires, the autorouter runs until pass 999.
- **Root Cause:** Freerouting CLI does not expose a flag that directly sets `stop_pass_no`.
- **Resolution:** DESK must configure `"router": { "job_timeout": "00:03:00" }` in `freerouting.json` or manage the process lifecycle via an active watchdog that terminates execution once the unrouted score plateaus.

---

### Bottleneck 5: IPC Error Masking over WebSocket Bridge
- **Observed Behavior:** When JavaScript exceptions occurred in EasyEDA Pro (e.g., `TypeError: Cannot read properties of undefined (reading 'getAll')`), Python scripts crashed with a generic message:
  `Bridge not reachable on port 49620: HTTP Error 500: Internal Server Error`
- **Investigation:**
  - In `bridge-server.mjs`, when an evaluation error occurs, it responds with HTTP 500 and a JSON body containing `{ success: false, error: err.message }`.
  - In `desk/bridge.py`, `urllib.request.urlopen(req)` raised `urllib.error.HTTPError` (a subclass of `OSError`).
  - The outer `except (OSError, TimeoutError)` block caught this and raised `SystemExit("Bridge not reachable on port 49620: ...")`, completely discarding the underlying JSON error response.
- **Root Cause:** Treating HTTP 500 application error responses as socket connection failures.
- **Resolution:** Parse `e.read().decode("utf-8")` inside HTTPError handling to surface the exact JavaScript exception.

---

## 4. Concrete Optimization Recommendations for the DESK Codebase

To ensure DESK executes future PCB reworks with maximum speed and zero human intervention, the following patches should be applied to `C:\watch\desk`:

### Optimization 1: Decoupled Power Trunk Widening (`desk/router.py`)
*Replace rigid global net class width injection with a two-phase architecture:*
1. **Phase 1 (DSN Generation):** Clamp all net class widths to $\le 10.0\text{ mil}$ in the exported DSN. This guarantees 100% routability into fine-pitch QFNs, BGAs, and ESP32 castellated pads.
2. **Phase 2 (Post-Import Canvas Widening):** After importing `.ses`, execute a vectorised JavaScript operation in EasyEDA to widen high-current power nets (`VBAT`, `VSYS`, `VBUS`) on open track segments (`length > 20 mil`) to their target IPC-2152 widths ($35\text{ mil}$ / $30\text{ mil}$).

### Optimization 2: Mandatory Headless Flag Injection (`tools/route.py`)
*Ensure the Freerouting CLI command always includes headless parameters:*
```python
cmd = [
    "java", "-jar", jar,
    "-de", tuned_dsn_path,
    "-do", ses,
    "-mp", str(passes),
    "-mt", "1",
    "--gui.enabled=false"  # Prevents modal WindowUserSettings GUI hang!
]
```

### Optimization 3: Grid Resolution Safeguard (`desk/router.py`)
*Never coarse-grain or fine-grain the DSN grid beyond optimal limits:*
- Maintain `(grid wire 1.25)` and `(grid via 1.25)` for boards $>30\text{ mm}$.
- Set `fine_pitch_clearance_mil = 4.02` ($0.10\text{ mm}$ per JLCPCB standard capability).

### Optimization 4: Error Propagation Fix in IPC Bridge (`desk/bridge.py`)
*Update `ex()` error handling to read HTTP 500 error bodies:*
```python
except urllib.error.HTTPError as e:
    try:
        err_body = json.loads(e.read().decode("utf-8"))
        raise SystemExit(f"EasyEDA JavaScript Error: {err_body.get('error')}")
    except Exception:
        raise SystemExit(f"Bridge HTTP Error {e.code}: {e}")
```

### Optimization 5: Watchdog-Driven Convergence Controller
*Implement an active watchdog inside `tools/route.py` that monitors `%TEMP%\freerouting\freerouting.log`:*
- If the unrouted count remains unchanged for $>5$ consecutive passes, issue a graceful stop signal or accept the best snapshot board, preventing runaway 999-pass loops.

---

## 5. Summary Table of Bottlenecks & Fixes

| ID | Bottleneck Description | Impact on Execution | Root Cause | DESK Optimization |
| :--- | :--- | :--- | :--- | :--- |
| **BN-004** | Headless Modal GUI Freeze | Stuck indefinitely (>16 min) | `WindowUserSettings` modal dialog on finish | Pass `--gui.enabled=false` |
| **BN-005** | Fine-Pitch IC Escape Trap | 143+ unrouted maze search failures | 35 mil trace forced into 9.8 mil QFN pad | Decouple DSN escape width (10 mil) from post-import trunk widening (35 mil) |
| **BN-006** | 0.25 mil Grid Search Explosion | A* timeout on cross-board traces | 16x search node multiplication | Lock routing grid to 1.25 mil for boards $>30\text{ mm}$ |
| **BN-007** | Pass Termination Loop (Pass 999) | Autorouter runs past target budget | `stop_pass_no` defaults to 999 in Java core | Implement watchdog convergence controller |
| **BN-008** | IPC Bridge Error Masking | Obscured JavaScript runtime errors | HTTP 500 treated as network failure | Parse JSON response body on HTTPError |
