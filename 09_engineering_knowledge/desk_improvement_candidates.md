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
