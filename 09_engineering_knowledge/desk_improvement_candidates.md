# DESK Engine Improvement Candidates

Based on the empirical failures and performance measurements recorded during Project One rework:

1. **EasyEDA Pro Split-Screen Tab Activation (`BN-001`, `INC-008`):**
   - *Observation:* `eda.dmt_EditorControl.openDocument(uuid)` fails to switch focus when a document is already open in an inactive split-screen tab, causing 600ms guard timeouts.
   - *Improvement:* Update `desk/bridge.py` `guard()` to use `eda.dmt_EditorControl.activateDocument(tabId)` when the target sheet is detected in the split tree.

2. **Vectorised Schematic Component Querying (`INC-009`):**
   - *Observation:* `pcb_PrimitiveComponent` uses `getAllPrimitiveId()`, while `sch_PrimitiveComponent` uses `getAll()`.
   - *Improvement:* Normalize adapter interfaces in `desk/eda/` to abstract away IPC method naming differences between PCB and Schematic primitives.

3. **Automated Directory Guarding (`INC-010`):**
   - *Observation:* Tools crash with `FileNotFoundError` if destination state directories are uninitialized.
   - *Improvement:* Standardize `os.makedirs(os.path.dirname(filepath), exist_ok=True)` in all DESK file generation utilities.

4. **Dynamic Window ID Resolution (`INC-007`):**
   - *Observation:* Cached window IDs in `project.json` become stale when EasyEDA is restarted.
   - *Improvement:* Integrate `ECADConnectionManager.discover_project_identity()` directly into `desk.py` startup so window IDs are refreshed dynamically.

5. **Headless Autorouter Execution (`BN-004`, `INC-015`):**
   - *Observation:* Freerouting v2.1.0 defaults to GUI mode and displays a modal `WindowUserSettings` dialog upon finishing the autoroute pass, freezing headless background runs indefinitely.
   - *Improvement:* Mandate `--gui.enabled=false` on all Freerouting CLI calls and enforce `"gui": {"enabled": false}` in generated configuration files.

6. **Decoupled Power Trunk Widening (`BN-005`):**
   - *Observation:* Enforcing high-current trace widths ($35\text{ mil}$ `VBAT`, $25\text{ mil}$ `GND`) at the global DSN net class level causes Freerouting's `MazeSearchAlgo` to fail when connecting to $0.5\text{ mm}$ pitch QFN pads (e.g. `BQ24074.BAT`) where pad clearance is only $9.8\text{ mil}$.
   - *Improvement:* Generate DSN files with escape-friendly widths ($\le 10\text{ mil}$) and execute a post-import vectorised JavaScript pass in EasyEDA Pro canvas to widen the high-current trunk lines (`length > 20 mil`) to their target IPC-2152 heavy copper widths ($35\text{ mil}$ `VBAT`, $30\text{ mil}`VSYS`).

7. **A* Routing Grid Safeguard (`BN-006`):**
   - *Observation:* Coarsening or fine-graining the DSN grid to $0.25\text{ mil}$ causes a $16\times$ search space explosion, hitting `TIME_LIMIT_TO_PREVENT_ENDLESS_LOOP` on long cross-board traces.
   - *Improvement:* Standardize on $1.25\text{ mil}$ grid for boards $>30\text{ mm}$ with $4.02\text{ mil}$ fine-pitch clearances.

8. **IPC Bridge Error Body Introspection (`BN-008`):**
   - *Observation:* Bridge server returns HTTP 500 when EasyEDA JavaScript throws an exception. `desk/bridge.py` caught this as a generic network failure and obscured the actual error.
   - *Improvement:* Read and decode the HTTP 500 response payload (`e.read().decode()`) to extract and surface the underlying JavaScript error message.

*(For full architectural and disassembly details, see [routing_bottleneck_and_optimization_report.md](routing_bottleneck_and_optimization_report.md))*
