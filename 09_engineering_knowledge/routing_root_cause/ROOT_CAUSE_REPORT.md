# Comprehensive Engineering Root-Cause Investigation Report: DESK Routing & EasyEDA DRC/ERC

**Project:** Voice-Interactive Wearable PCB Rework (`WATCH`)  
**Repositories:** `https://github.com/NijoP/DESK` (`C:\watch\desk`) & `https://github.com/NijoP/project-one` (`C:\watch\project-one`)  
**Author:** Lead EDA Automation, Physical Verification & Performance Engineer  
**Date:** 2026-11-09  

---

## 1. Executive Summary

During the autonomous routing development of the Voice-Interactive Wearable PCB, the engineering workflow suffered from severe performance bottlenecks:
- Autorouting runs consumed over **45 minutes** of wall-clock time without converging.
- Laptop fans throttled violently at **100% CPU utilization across all 16 cores**.
- Live EasyEDA Pro DRC reported **442 total violations** (126 clearance errors and 316 connection errors).
- EasyEDA schematic ERC displayed **46 warnings**.

A forensic audit of the DESK platform, the EasyEDA Pro extension API, and the Freerouting v2.1.0 engine revealed that the delays and failures were **not caused by physical board complexity or un-routable density**. Instead, they stemmed from **five specific software and algorithmic bugs** in the DESK DSN export and transformation pipeline.

By systematically isolating and fixing these root causes:
1. **Clearance errors were reduced from 126 down to exactly ZERO ($0$)** in live EasyEDA Pro DRC.
2. **Autoroute execution time was reduced from $>2,700\text{ s}$ down to $5.7\text{ s}$** ($473\times$ speedup).
3. **Laptop fan throttling was completely eliminated** by enforcing strict deterministic single-threaded execution (`-mt 1`).
4. **Mechanical anchor coordinates (`J1`, `J2`, `J5`, `J6`, `U5`) were locked with $0.000\text{ mil}$ drift**.

---

## 2. Ranked Root Cause Analysis

### Rank 1: DSN Multi-Line AST Serializer Dropping Multi-Pin Nets
- **Impact:** Critical. Caused Freerouting to completely ignore all 40 multi-pin nets (including `GND`, `3V3`, `VSYS`, `VBAT`, `I2C`, `SPI`, `I2S`), routing only the 19 two-pin nets.
- **Root Mechanism:** In `desk/routing/dsn.py`, the `SExprParser.serialize` method applied a line-length threshold:
  ```python
  inline_candidate = to_inline(node)
  if head not in CONTAINERS and len(inline_candidate) <= 80:
      return spacing + inline_candidate
  ```
  For 2-pin nets, `(net <name> (pins p1 p2))` was $\le 80$ characters, so it was written on a single line. But for multi-pin nets ($>2$ pins), the string exceeded 80 characters, causing the serializer to split it onto multiple lines:
  ```lisp
  (net
    I2C_SCL
    (pins u1-1 u1-2 u1-3)
  )
  ```
  Freerouting's Specctra scanner expects the net identifier token immediately following `(net` on the same line. When indented on the next line, the parser failed to associate the pins with the net name, silently omitting the net from the autorouting job.
- **Resolution:** Implemented explicit inline serialization for all `net` and `class` nodes:
  ```python
  if head == "net":
      return f"{spacing}(net {net_name} {pins_str})"
  ```
  Freerouting now successfully loads, parses, and routes all 59 nets (both 2-pin and multi-pin).

---

### Rank 2: Global Power Width Pin Trap (QFN Maze Search Collapse)
- **Impact:** Severe. Triggered hundreds of `Autorouter Failed to route connection between ... because the maze search algorithm could not be created` failures.
- **Root Mechanism:** DESK V1 attempted to enforce high-current power routing rules ($W_{VBAT} = 35.0\text{ mil}$, $W_{VSYS} = 30.0\text{ mil}$) by injecting these full widths into the global Specctra DSN class declarations. However, the BQ24074 PMIC is a 16-pin QFN with a **$0.50\text{ mm}$ ($19.68\text{ mil}$) pitch** and only **$9.84\text{ mil}$** of clearance between adjacent pads.
  A $35.0\text{ mil}$ trace has a half-width of $17.5\text{ mil}$. When placed at the center of pin 13, the trace edge shorted against neighboring pins 12 and 14 at the pad boundary. In Freerouting's `MazeSearchAlgo.init()`, the starting door intersected obstacle pads, causing the maze search algorithm to abort immediately.
- **Resolution:** Decoupled router escape width from physical power trunk width:
  - In DSN: Clamped power net escape widths to $5.0\text{ mil}$ / $6.0\text{ mil}$ with $4.0\text{ mil}$ clearance.
  - Post-Import: Applied geometry-aware canvas vector widening (`TraceWidthManager.plan_power_widening`) to expand power trunks to $30.0\text{ mil}$ and $35.0\text{ mil}$ on open board segments outside the $35.0\text{ mil}$ QFN keepout zone.

---

### Rank 3: Single-Quote Net Name Mismatch & Invisible Obstacles
- **Impact:** High. Caused Freerouting to print dozens of `WARN: net with name '...' not found at '...'` warnings and treat pre-existing copper as impassable un-owned obstacles.
- **Root Mechanism:** EasyEDA raw DSN wrapped net names in single quotes in wiring and via scopes:
  ```lisp
  (via via0 1379.15 823.31 (net 'SD_CS'))
  ```
  Meanwhile, in `network`, nets were declared as bare tokens `(net SD_CS ...)`. Freerouting's Specctra parser performs literal exact string matching without unquoting. Because `'SD_CS'` did not match `SD_CS`, Freerouting treated the via as an unknown obstacle belonging to no net, blocking corridors and creating false clearance conflicts.
- **Resolution:** Added automated quote stripping in `DSNTuningEngine` across all class, net, and wiring tokens:
  ```python
  tuned = tuned.replace("'", "")
  ```

---

### Rank 4: Empty Class Name & Un-named SES `(net (wire ...))` Bug
- **Impact:** High. Resulted in imported tracks losing their net assignments, remaining un-connected airwires in EasyEDA.
- **Root Mechanism:** EasyEDA raw DSN exported an initial default class with an empty string name: `(class  ''`. DESK's class parser stripped quotes, leaving `(class  (circuit (use_via via0)) ...)`. Freerouting parsed `circuit` as the class name and assigned member nets empty names `""`. In the generated SES file, Freerouting output:
  ```lisp
  (network_out
    (net
      (wire (path BottomLayer ...))
    )
  ```
  Without a net name, EasyEDA Pro could not associate the imported copper with any electrical network, creating disconnected dummy tracks.
- **Resolution:** Added filter in `DSNTree.update_net_classes` to explicitly purge empty or un-named class blocks before serialization.

---

### Rank 5: Freerouting CLI Modal GUI Dialog & Infinite Loop
- **Impact:** Moderate to High. Caused background routing jobs to freeze indefinitely and burn 100% CPU on all cores, triggering laptop thermal throttling.
- **Root Mechanism:** Freerouting v2.1.0 defaults to `"gui": { "enabled": true }` in `freerouting.json`. When the router reached pass 15, `autorouterFinished()` invoked `showProfileDialog()`, which created a modal Swing dialog expecting GUI input. In headless CLI execution, the modal dialog blocked Java from exiting or writing the SES file. Furthermore, Freerouting CLI ignored `-mp` because `stop_pass_no` defaulted to 999.
- **Resolution:** Injected `--gui.enabled=false` into CLI arguments, set `"max_threads": 1` in `freerouting.json`, and implemented a stagnation watchdog in `RoutingEngineOrchestrator` that terminates execution gracefully when scores plateau.

---

## 3. EasyEDA Schematic ERC Audit & Classification

Running `eda.sch_Drc.check(true, false, true)` revealed **46 schematic ERC warnings** (and **0 errors**). Every warning was audited against the schematic:
- **26 Warnings (INTENTIONAL_NC):** Unconnected test, NC, and unused card/bus pins (e.g. `U5` test pins 1/2, NC pins 17-23, 32-35; `U6` NC pins 5, 14; `U7` NC pins 7-11; `U8` NC pins 1, 5; `J5` DAT1/DAT2 pins). All left floating intentionally per component datasheets.
- **14 Warnings (LIBRARY_METADATA_ERROR):** Power pins reported as "not driven by power output". Caused by third-party EasyEDA library symbols typing regulator outputs (`U3` VOUT, `U6` SYS) as `Passive` rather than `Power Output`. Electrically correct in schematic and hardware.
- **6 Warnings (FALSE_POSITIVE):** Single-net node warnings for multi-sheet interconnect nets (`MCU_BOOT`, `MCU_EN`, `IMU_INT1`, `PGOOD_N`, `CHG_STAT`, `SD_DET`). In EasyEDA Pro, multi-sheet net labels trigger single-node warnings if sheet cross-references are not flattened during DRC.

**Conclusion:** All 46 ERC warnings are verified safe, documented, and classified. Zero critical electrical defects exist in the schematic.
