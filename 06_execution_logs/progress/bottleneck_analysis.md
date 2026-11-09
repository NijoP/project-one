# DESK Execution Bottleneck & Latency Analysis

**Log Location:** `C:\watch\desk\field\progress\bottleneck_analysis.md`  
**Purpose:** Identify, investigate, and eliminate execution bottlenecks, high-latency operations, and inefficient tool patterns across DESK.

---

## 1. Bottleneck Summary Table

| Bottleneck ID | Task Name | Baseline | Measured Time | Delay Source | Optimization Status |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **BN-001** | Schematic Primitive Extraction | `~3.0s` | `32.8s` | IPC Gateway Mismatch & Tab Focus | **FIXED & MEASURED (1.8s)** |
| **BN-002** | PCB Primitive Batch Dump | `~1.5s` | `5.8s` | Sequential 40-item chunking without pipelining | **MONITORED** |
| **BN-003** | PowerShell Cmdlet Parameter Exception | `<0.5s` | `2.8s` | Command parameter binding mismatch | **FIXED** |
| **BN-004** | Headless Freerouting Modal Dialog Hang | `<120s` | `>980s` | Freerouting modal GUI dialog waiting on input | **FIXED (--gui.enabled=false)** |
| **BN-005** | Fine-Pitch IC Escape / Maze Search Trap | `~60s` | `~600s` | 35 mil trace forced into 9.8 mil QFN pad | **FIXED (Decoupled escape)** |
| **BN-006** | 0.25 mil Search Grid Space Explosion | `~90s` | `~450s` | 16x search node multiplication hitting step limit | **FIXED (Locked 1.25 mil grid)** |

---

## 2. In-Depth Bottleneck Investigations

### Bottleneck BN-001: Schematic Primitive Extraction Latency & Method Mismatches
1. **Task Name:** `T-009`: Live Schematic Primitive & MPN Extraction
2. **Expected Duration (Baseline):** `~3.0s` for an 89-component schematic query.
3. **Actual Duration:** `32.8s`
4. **Excess Time Consumed:** `+29.8s` (9.9x over expected baseline).
5. **What Happened During Execution:**
   - Attempt 1 called `guard(sheet_uuid)` which executed `eda.dmt_EditorControl.openDocument(sheet_uuid)`. Because `P1.Schematic1` was already open in a split-screen tab, `openDocument` did not trigger an active document focus event within the 600ms guard sleep window. The script timed out waiting for the sheet to become active.
   - Attempt 2 invoked `eda.sch_PrimitiveComponent.getAllPrimitiveId()`, which threw a runtime JavaScript `TypeError: getAllPrimitiveId is not a function` because schematic components implement `getAll()` rather than `getAllPrimitiveId()`.
   - Attempt 3 successfully brought the tab to focus using `eda.dmt_EditorControl.activateDocument(tabId)` and retrieved components with `getAll()`.
6. **Why It Took So Long:**
   - Sequential exception propagation and IPC retry timeouts over the WebSocket bridge.
   - Trial-and-error reflection against unverified schematic methods.
7. **Delay Breakdown:**
   - EasyEDA IPC Waiting & Retries: `18.5s`
   - Script Execution & Reflection: `8.4s`
   - IPC Roundtrip Latency: `5.9s`
8. **Root Cause:**
   - Incomplete knowledge of the EasyEDA Pro 3.2.149 split-screen document activation model (`activateDocument` vs `openDocument`).
   - Assuming API symmetry between PCB and Schematic components.
9. **Suggested Optimization:**
   - Cache active `tabId` directly in `ProjectBinding`.
   - Use `eda.dmt_EditorControl.activateDocument(tabId)` directly when switching sheets.
   - Query all schematic attributes in a single vectorised JavaScript payload rather than querying component properties individually.
10. **Whether the Issue Was Fixed:** **YES.** The optimized script [`scratch/dump_sch_meta.py`](file:///C:/watch/desk/scratch/dump_sch_meta.py) was written and verified.
11. **Before-and-After Execution Time:**
    - **Before:** `32.8s` (3 attempts with timeouts)
    - **After:** `1.8s` (single roundtrip vectorised query for all 89 parts)
    - **Performance Gain:** **18.2x faster (94.5% latency reduction)**.

---

### Bottleneck BN-002: PCB Primitive Batch Chunking
1. **Task Name:** `T-008`: PCB Component Dump (`tools/pcb_dump.py`)
2. **Expected Duration (Baseline):** `~1.5s`
3. **Actual Duration:** `5.8s`
4. **Excess Time Consumed:** `+4.3s`
5. **What Happened During Execution:**
   - `tools/pcb_dump.py` chunks 89 components into groups of 40:
     - Chunk 1: 40 parts (`1.9s`)
     - Chunk 2: 40 parts (`2.1s`)
     - Chunk 3: 9 parts (`1.8s`)
   - Each chunk performs synchronous IPC roundtrips: `eda.pcb_PrimitiveComponent.get(id)`, `getAllPinsByPrimitiveId(id)`, and `getPrimitivesBBox([id])`.
6. **Why It Took So Long:**
   - For every single component, individual bounding box and pin queries are evaluated serially inside the EasyEDA JavaScript worker thread.
7. **Delay Breakdown:**
   - EasyEDA JS DOM Evaluation: `3.8s`
   - IPC WebSocket Transfer: `1.2s`
   - Python JSON Serialization: `0.8s`
8. **Root Cause:**
   - Architectural limitation in EasyEDA Pro's extension IPC sandbox: executing too many primitive lookups in a single call blocks the browser UI rendering loop, requiring 40-item chunking.
9. **Suggested Optimization:**
   - Retain 40-item chunking for mutation safety, but pipeline the chunks asynchronously or pre-filter unneeded pin geometries when only position locks are being queried.
10. **Status:** **MONITORED.** Execution time of 5.8s is acceptable for an 89-component full board dump, well within the 5-minute routine threshold.

---

### Bottleneck BN-004: Headless Freerouting Modal Dialog Hang
1. **Task Name:** `T-015`: 4-Layer Autonomous Routing Execution (`tools/route.py`)
2. **Expected Duration (Baseline):** `~120s` for a 4-layer 59-net board.
3. **Actual Duration:** `>980s` (Process PID `12088` stuck indefinitely).
4. **Excess Time Consumed:** `+860s`
5. **What Happened During Execution:**
   - Freerouting completed pass #15 in 81.3 seconds.
   - However, because `--gui.enabled=false` was not supplied on CLI, Freerouting opened a modal Swing `WindowUserSettings` dialog asking for user confirmation.
   - The process blocked on `java.awt.Dialog.show()` and never wrote `desk_route.ses` or exited.
6. **Root Cause:** Incomplete CLI argument configuration in `tools/route.py`.
7. **Suggested Optimization:** Append `--gui.enabled=false` to Freerouting invocations and configure `gui.enabled = false` in `freerouting.json`.
8. **Status:** **FIXED.**

---

### Bottleneck BN-005: Fine-Pitch IC Escape / Maze Search Trap
1. **Task Name:** `T-015`: Autonomous Net Routing Convergence
2. **Expected Duration (Baseline):** `~60s`
3. **Actual Duration:** `~600s`
4. **Excess Time Consumed:** `+540s`
5. **What Happened During Execution:**
   - 143+ pin connections repeatedly failed with `maze search algorithm could not be created`.
   - Power nets were assigned high-current widths ($W_{VBAT} = 35\text{ mil}$, $W_{VSYS} = 30\text{ mil}$) at the global DSN class level.
   - When touching `BQ24074` pin 13 (QFN $0.5\text{ mm}$ pitch, $9.8\text{ mil}$ gap to adjacent pins), a $35\text{ mil}$ trace physically collided with pins 12 and 14, causing the maze search door to collapse.
6. **Root Cause:** Enforcing high-current trace widths at the global DSN net class level without pin-level escape neckdown.
7. **Suggested Optimization:** Set DSN class widths to escape-friendly dimensions ($\le 10\text{ mil}$) and execute a post-import vectorised JavaScript pass in EasyEDA canvas to widen open-board power trunks to $35\text{ mil}$ / $30\text{ mil}$.
8. **Status:** **FIXED.**

---

### Bottleneck BN-006: 0.25 mil Search Grid Space Explosion
1. **Task Name:** `T-015`: Fine-Grid Routing Convergence
2. **Expected Duration (Baseline):** `~90s`
3. **Actual Duration:** `~450s`
4. **Excess Time Consumed:** `+360s`
5. **What Happened During Execution:**
   - Coarsening/fine-graining the DSN wire grid to $0.25\text{ mil}$ multiplied the search graph by $16\times$ ($>50\text{ million}$ nodes).
   - Long cross-board traces (SPI, I2S, LCD) repeatedly timed out against Freerouting's internal `TIME_LIMIT_TO_PREVENT_ENDLESS_LOOP`.
6. **Root Cause:** Excessively fine search grid for a $45\text{ mm}$ board.
7. **Suggested Optimization:** Lock the DSN routing grid to $1.25\text{ mil}$ for boards $>30\text{ mm}$.
8. **Status:** **FIXED.**

---

## 3. High-Watermark Threshold Compliance

- **Routine Operations Threshold (5 Minutes / 300s):**
  - All routine tasks to date completed between `2.1s` and `32.8s`.
- **Major Operations Threshold (15 Minutes / 900s):**
  - Freerouting execution exceeded 15 minutes in initial runs due to `BN-004` (headless dialog hang) and `BN-005` (geometric pin trap).
  - Both root causes are now identified, documented, and resolved.


---

### Bottleneck BN-007: Freerouting CLI 999-Pass Hardcode Loop
1. **Task Name:** `T-015`: Autonomous Router Pass Budget Control (`-mp`)
2. **Expected Duration (Baseline):** `~60s` for 15 passes (3.6s / pass).
3. **Actual Duration:** `>1200s` (Process ran beyond 290+ passes).
4. **Excess Time Consumed:** `+1140s`
5. **What Happened During Execution:**
   - In `tools/route.py`, `--passes 15` passed `-mp 15` to Java.
   - However, Freerouting v2.1.0 continued running passes indefinitely (Pass #100, #200, #291...).
6. **Root Cause:**
   - Bytecode disassembly of `app.freerouting.settings.RouterSettings` and `BatchAutorouter` revealed:
     - `RouterSettings.stop_pass_no` is hardcoded to `999` in the constructor (`102: sipush 999; 105: putfield stop_pass_no:I`).
     - CLI parser `-mp` only sets `maxPasses` in `RouterSettings`.
     - But `BatchAutorouter.runBatchLoop()` checks `settings.get_stop_pass_no()`, NOT `maxPasses`!
     - In CLI mode, `stop_pass_no` is never updated from `maxPasses`, causing the batch router to iterate up to 999 passes unless 100% completion is reached.
7. **Suggested Optimization:**
   - Direct heap extraction or background monitor script that captures `RoutingJob.output.dataBytes` as Specctra SES snapshots upon target pass completion.
8. **Status:** **DOCUMENTED & WORKAROUND IMPLEMENTED.**

---

### Bottleneck BN-008: Freerouting Silent SES Drop on Non-100% Exit
1. **Task Name:** `T-015`: Specctra SES File Persistence
2. **Expected Duration (Baseline):** `~2s` file write upon timeout or stop.
3. **Actual Duration:** Infinite wait (File never written to disk).
4. **Excess Time Consumed:** `+600s`
5. **What Happened During Execution:**
   - Even when Freerouting completed 200+ passes or when job timeout expired, `desk_route.ses` was never generated on disk.
6. **Root Cause:**
   - Disassembly of `app.freerouting.Freerouting.InitializeCLI()` revealed lines 261-268:
     ```
     261: aload_2
     262: getfield app/freerouting/core/RoutingJob.state
     265: getstatic app/freerouting/core/RoutingJobState.COMPLETED
     268: if_acmpne 324  // SKIPS FILE WRITE IF STATE != COMPLETED!
     271: // java.nio.file.Files.write(design_output_filename, ...)
     ```
   - When a routing job times out or is interrupted, `job.state` is set to `TERMINATED` (not `COMPLETED`).
   - Consequently, line 268 skips `Files.write`, and the process terminates without saving any routed copper to disk, throwing away all completed tracks!
7. **Suggested Optimization:**
   - Extract `RoutingJob.output.dataBytes` directly from the JVM heap (`GC.heap_dump`) via Python, or patch `freerouting.jar` to write output unconditionally on `TERMINATED`.
8. **Status:** **RESOLVED VIA HEAP EXTRACTION PIPELINE.**

---

### Bottleneck BN-009: EasyEDA Pro API Namespace Discrepancy (`pcb_Device` vs `pcb_PrimitiveComponent`)
1. **Task Name:** `T-015`: Post-Routing Verification & Component Audit
2. **Expected Duration (Baseline):** `~1s`
3. **Actual Duration:** `~30s` (HTTP 500 error debugging).
4. **Excess Time Consumed:** `+29s`
5. **What Happened During Execution:**
   - Queries to `eda.pcb_Device.getAll()` failed with `HTTP 500: Cannot read properties of undefined (reading 'getAll')`.
6. **Root Cause:**
   - In EasyEDA Pro JavaScript API, placed board components are registered under `eda.pcb_PrimitiveComponent`, while `eda.pcb_Device` is exclusive to schematic or non-existent in PCB workspace.
7. **Suggested Optimization:**
   - Standardize all component queries on `eda.pcb_PrimitiveComponent.getAll()`.
8. **Status:** **FIXED.**
