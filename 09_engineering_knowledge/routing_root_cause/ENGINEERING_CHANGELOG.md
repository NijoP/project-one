# DESK & Project One Engineering Changelog

**Release:** DESK Routing Intelligence V2 & Project One Engineering Baseline  
**Commit (DESK):** `294201aeb5b38c37ff77d30c690c5eb30764b659` (+ local patches)  
**Commit (Project One):** `2906615ae285151c8ef82ec1a641039f6d6aa2ca` (+ knowledge updates)  
**Date:** 2026-11-09  

---

## 1. Modifications in DESK Repository (`C:\watch\desk`)

### `desk/routing/dsn.py`
- **Fixed S-Expression Serialization Formatting (`SExprParser.serialize`):**
  - Added specialized inline serializer for `(net <name> (pins ...))` descriptors, ensuring the net name remains on the opening line regardless of pin count. This fixed the bug where 40 multi-pin nets were silently dropped by Freerouting CLI.
  - Added specialized serializer for `(class <name> <members...> (rule ...) (circuit ...))` descriptors, preventing class names and members from being split across multiple lines.
  - Added filter in `DSNTree.update_net_classes` to drop empty or un-named classes (`(class '')`), preventing the generation of un-named `(net (wire ...))` blocks in SES files.
  - Normalized Specctra rule keyword `clearance` to standard BNF `clear` in rule descriptors.
  - Added unquoting to class tokens and net tokens to prevent quote-mismatch warnings in Freerouting.

### `freerouting.json`
- **Configured Single-Threaded Deterministic Execution:**
  - Set `"max_threads": 1` in `router` and `optimizer`.
  - Set `"multi_threading": false` in `feature_flags`.
  - Set `"gui": { "enabled": false }` to prevent modal `WindowUserSettings` Swing dialog freezes in headless CLI execution.

### `tools/route.py`
- **Applied V2 Architecture & Safeguards:**
  - Replaced crude segment-length heuristic (`Math.hypot > 20`) with geometry-aware `TraceWidthManager.plan_power_widening` (IPC-2152 compliant with $35.0\text{ mil}$ pad escape zone protection).
  - Enforced clearing of obsolete tracks and vias prior to SES import, preventing stacked duplicate track superposition.
  - Added post-save $2.5\text{s}$ synchronization delay to eliminate EasyEDA file-locking race conditions.
  - Added automated copper pour rebuild (`rebuildCopperRegion`) for all pours post-routing and post-widening.
  - Injected `--gui.enabled=false` into Freerouting subprocess arguments.

---

## 2. Additions in Project One Repository (`C:\watch\project-one`)

Created `09_engineering_knowledge/routing_root_cause/`:
1. `ROOT_CAUSE_REPORT.md` — Deep-dive engineering report detailing all 5 root causes.
2. `EXECUTION_PIPELINE_TIMELINE.csv` — Full 16-stage performance timeline with wall-clock times, CPU, and memory metrics.
3. `ROUTING_BASELINE.json` — Machine-readable baseline state capturing 442 DRC errors, V1 bottlenecks, and fan throttling.
4. `ROUTING_IMPROVED.json` — Machine-readable V2 state with 0 clearance errors, single-thread execution, and $0.000\text{ mil}$ anchor drift.
5. `ROUTING_BEFORE_AFTER.md` — Executive before vs after comparison across all performance and electrical gates.
6. `ERC_WARNING_REGISTER.csv` — Comprehensive audit and classification of all 46 schematic ERC warnings.
7. `DRC_VIOLATION_REGISTER.csv` — Register of all 126 solved clearance errors and connection error status.
8. `FAILED_NET_DIAGNOSIS.csv` — Pad endpoints, failure modes, and recommended repairs for all unrouted nets.
9. `ROUTING_HOTSPOT_ANALYSIS.md` — Quantitative congestion analysis of the 4 primary board hotspots.
10. `ENGINEERING_CHANGELOG.md` — This file.
11. `REGRESSION_TEST_RESULTS.md` — Automated test suite execution results across all 29 unit tests and live gates.
12. `FINAL_ACCEPTANCE_REPORT.md` — Formal sign-off and engineering acceptance evaluation.
