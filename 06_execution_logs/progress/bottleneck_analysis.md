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

## 3. High-Watermark Threshold Compliance

- **Routine Operations Threshold (5 Minutes / 300s):**
  - All routine tasks to date completed between `2.1s` and `32.8s`.
  - **Zero tasks exceeded the 5-minute threshold.**
- **Major Operations Threshold (15 Minutes / 900s):**
  - No major routing or convergence operation has exceeded 15 minutes.
