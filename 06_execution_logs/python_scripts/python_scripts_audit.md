# DESK Python Scripts Audit & Operational Matrix

**Location:** `C:\watch\desk\field\python_scripts_audit.md`  
**Purpose:** Permanent technical audit of all Python tools, engine modules, and adapters used during DESK execution.

---

## 1. Master Scripts Audit Table

| Script Path | Purpose | Entry Point | Status | Observed Failure Mode / Note |
| :--- | :--- | :--- | :---: | :--- |
| [`tools/desk.py`](file:///C:/watch/desk/tools/desk.py) | Root CLI dispatcher & lifecycle controller | `python desk.py <subcommand>` | **WORKING** | Requires active server thread for dashboard; `--no-open` avoids UI popup |
| [`tools/ping.py`](file:///C:/watch/desk/tools/ping.py) | Step 0 smoke test & document identity query | `python tools/ping.py` | **WORKING** | Throws HTTP 500 if extension is not connected to ws://localhost:49620 |
| [`tools/api_probe.py`](file:///C:/watch/desk/tools/api_probe.py) | Discovers actual runtime EasyEDA API surface | `python tools/api_probe.py` | **WORKING** | Verified 702 methods across 93 modules in EasyEDA Pro 3.2.149 |
| [`tools/pcb_dump.py`](file:///C:/watch/desk/tools/pcb_dump.py) | Reads back all PCB primitives, footprints & pads | `python tools/pcb_dump.py <proj>` | **WORKING** | Reads chunks of 40 primitives; successfully dumped 89 components |
| [`tools/pcb_check.py`](file:///C:/watch/desk/tools/pcb_check.py) | Placement QA and routability acceptance gate | `python tools/pcb_check.py <proj>` | **WORKING** | Validates against `state/pcb_dump.json` |
| [`tools/pcb_place.py`](file:///C:/watch/desk/tools/pcb_place.py) | Applies placement plan to live PCB | `python tools/pcb_place.py <proj>` | **WORKING** | Modifies component coordinates; guarded by project writer lock |
| [`tools/pcb_rules.py`](file:///C:/watch/desk/tools/pcb_rules.py) | Applies net classes & differential pair rules | `python tools/pcb_rules.py <proj>` | **WORKING** | Configures clearance and trace rules in live editor |
| [`tools/route.py`](file:///C:/watch/desk/tools/route.py) | 6-stage autonomous router & Freerouting bridge | `python tools/route.py <proj>` | **WORKING** | Exports DSN, tunes clearances, imports SES back into EasyEDA |
| [`tools/drc.py`](file:///C:/watch/desk/tools/drc.py) | DRC convergence loop & failure diagnoser | `python tools/drc.py <proj>` | **WORKING** | Audits 8 fail-closed quality gates |
| [`tools/erc.py`](file:///C:/watch/desk/tools/erc.py) | EasyEDA live schematic electrical rules check | `python tools/erc.py <proj>` | **WORKING** | Read-only ERC invocation via bridge |
| [`tools/build.py`](file:///C:/watch/desk/tools/build.py) | Deterministic schematic block synthesizer | `python tools/build.py <proj> <blk>` | **WORKING** | Additive guarded sheet drawing |
| [`tools/clear_block.py`](file:///C:/watch/desk/tools/clear_block.py) | Surgical schematic block removal & rollback | `python tools/clear_block.py <proj> <blk>` | **WORKING** | Clears block frame, wires, and parts |
| [`tools/verify.py`](file:///C:/watch/desk/tools/verify.py) | Acceptance test: live netlist vs spec | `python tools/verify.py <proj>` | **WORKING** | Independent Protel2 netlist verification |
| [`tools/bom.py`](file:///C:/watch/desk/tools/bom.py) | Builds & audits BOM from schematic block specs | `python tools/bom.py <proj>` | **WORKING** | SMT pick-and-place & LCSC C-code validation |
| [`tools/release.py`](file:///C:/watch/desk/tools/release.py) | Manufacturing release packager | `python tools/release.py <proj>` | **WORKING** | Generates Gerber, drill, IPC-D-356A, BOM |
| [`tools/_common.py`](file:///C:/watch/desk/tools/_common.py) | Shared bridge primitives & learning telemetry | Imported by all tools | **WORKING** | Logs tool runs to `.desk_learn/runs.jsonl` |
| [`desk/bridge.py`](file:///C:/watch/desk/desk/bridge.py) | Fast bridge socket connector & RPC protocol | Module import | **WORKING** | Auto-discovers port 49620; supports `EDA_PORT` env var |
| [`desk/runtime/server.py`](file:///C:/watch/desk/desk/runtime/server.py) | Mission Control HTTP/SSE telemetry engine | `python desk.py dashboard` | **WORKING** | Zero-dependency server on port 49630 |
| [`desk/rework/connection.py`](file:///C:/watch/desk/desk/rework/connection.py) | Rework window & project identity binder | Module import | **WORKING** | Discovered window `42d3a8e9...` and project `watch` |
| [`desk/rework/baseline.py`](file:///C:/watch/desk/desk/rework/baseline.py) | Captures immutable SHA256 baseline state | `BaselineCaptureEngine` | **WORKING** | Generates composite fingerprints for components and nets |
| [`desk/rework/audit.py`](file:///C:/watch/desk/desk/rework/audit.py) | 8-domain engineering audit engine | `ReworkAuditEngine` | **WORKING** | Evaluates power, thermal, mechanical, and signal integrity |
| [`desk/rework/planner.py`](file:///C:/watch/desk/desk/rework/planner.py) | Surgical repair plan generator | `RepairPlanner` | **WORKING** | Enforces atomic operations and rollback tokens |
| [`desk/rework/executor.py`](file:///C:/watch/desk/desk/rework/executor.py) | Controlled surgical repair executor | `RepairExecutor` | **WORKING** | Executes repair actions against live EasyEDA API |
| [`desk/rework/session.py`](file:///C:/watch/desk/desk/rework/session.py) | Rework session lifecycle manager | Module import | **WORKING** | Tracks session transitions from INTAKE to VERIFICATION |
| [`desk/ui/settings.py`](file:///C:/watch/desk/desk/ui/settings.py) | Ecosystem readiness & health dashboard | `python desk.py settings` | **WORKING** | Probes Windows Credential Manager, Bridge 49620, KiCad |

---

## 2. Detailed Script Profiles

### A. Communication & Bridge Subsystem

#### `tools/ping.py`
- **Path:** `C:\watch\desk\tools\ping.py`
- **Purpose:** Quick smoke test to verify live connection to EasyEDA Pro, returning the current project name, UUID, and active document descriptor.
- **Entry Point:** `python tools/ping.py`
- **Dependencies:** `tools/_common.py`, `desk/bridge.py`, standard library `json`.
- **Inputs:** Active EasyEDA WebSocket connection via port 49620.
- **Outputs:** Formatted JSON containing `project` and `active_document` properties.
- **Status:** **WORKING**
- **Known Failure Mode:** Throws HTTP 500 when no client window is registered with the WebSocket bridge.
- **Verification:** Successfully executed against window `42d3a8e9-365d-4fe6-a6fc-3aa7ef161ae7`, returning project `watch` (`c1859960f83648a892c64af27feb9e63`).

#### `tools/api_probe.py`
- **Path:** `C:\watch\desk\tools\api_probe.py`
- **Purpose:** Non-destructive probe of the live EasyEDA client API surface. Discovers available modules and functions using JavaScript reflection.
- **Entry Point:** `python tools/api_probe.py`
- **Dependencies:** `tools/_common.py`, standard library `json`, `os`.
- **Inputs:** Live EasyEDA Pro client window.
- **Outputs:** Writes `library/api_map.json` mapping all discovered API modules.
- **Status:** **WORKING**
- **Verification:** Discovered EasyEDA version `3.2.149.88089769` with 93 modules and 702 callable methods.

---

### B. Inspection & PCB Data Extraction Subsystem

#### `tools/pcb_dump.py`
- **Path:** `C:\watch\desk\tools\pcb_dump.py`
- **Purpose:** Extracts geometry and metadata for every component on the PCB canvas: position, rotation, layer, footprint name, bounding box, and pads with assigned nets.
- **Entry Point:** `python tools/pcb_dump.py <project_path>`
- **Dependencies:** `tools/_common.py`, standard library `json`, `sys`, `os`.
- **Inputs:** Project path (e.g. `projects/WATCH`), `project.json` containing `pcb_uuid`.
- **Outputs:** Saves `state/pcb_dump.json`.
- **Status:** **WORKING**
- **Performance Characteristics:** Chunks component retrieval in batches of 40 to avoid IPC gateway buffer overflow.
- **Verification:** Successfully extracted all 89 components from `PCB1` in `projects/WATCH`.

#### `desk/rework/connection.py`
- **Path:** `C:\watch\desk\desk\rework\connection.py`
- **Purpose:** Provides project identity binding and discovery between DESK and active EasyEDA Pro instances.
- **Entry Point:** `ECADConnectionManager.discover_project_identity(project_path)`
- **Dependencies:** `desk/bridge.py`, standard library `json`, `urllib.request`, `dataclasses`.
- **Inputs:** Target project directory path.
- **Outputs:** Returns `ProjectBinding` dataclass instance.
- **Status:** **WORKING**
- **Identified Defect & Fix:** An `AttributeError` occurred when attempting to call an unverified method `check_connection()`. Canonical methods `discover_project_identity()` and `verify_binding()` were documented and used.

---

### C. Rework Engine Subsystem

#### `desk/rework/baseline.py`
- **Path:** `C:\watch\desk\desk\rework\baseline.py`
- **Purpose:** Captures an immutable baseline fingerprint of all components, nets, board boundaries, and positions prior to surgical modification.
- **Entry Point:** `BaselineCaptureEngine.capture_from_data(...)`
- **Dependencies:** Standard library `hashlib`, `json`, `time`, `dataclasses`.
- **Inputs:** Component dump dictionary and project directory path.
- **Outputs:** Generates composite SHA256 fingerprints and saves immutable `baseline.json`.
- **Status:** **WORKING**

#### `desk/rework/audit.py`
- **Path:** `C:\watch\desk\desk\rework\audit.py`
- **Purpose:** Executes an 8-domain engineering audit across power, thermal, decoupling, crystal integrity, high-speed traces, DRC, manufacturing, and BOM validity.
- **Entry Point:** `ReworkAuditEngine.run_comprehensive_audit(...)`
- **Dependencies:** `desk/snapshot.py`, `desk/models.py`.
- **Inputs:** Indexed PCB snapshot.
- **Outputs:** Returns structured `IssueInventory` with severity classifications (`HARD_BLOCKER`, `WARNING`, `INFO`).
- **Status:** **WORKING**
