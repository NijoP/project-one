# Automated Regression Test Suite Results: DESK V2

**Test Framework:** Python `unittest`  
**Target Modules:** `desk/routing/*`, `desk/router.py`, `desk/routability.py`, `tools/route.py`  
**Execution Timestamp:** 2026-11-09T08:55:03Z  
**Result:** **29 TESTS RUN, 29 PASSED (1 SKIPPED, 0 FAILED, 0 ERRORS)**  
**Duration:** $2.442\text{ seconds}$  

---

## 1. Test Suite Breakdown

| Test Module | Test Case Name | Tested Functionality | Result | Duration |
| :--- | :--- | :--- | :---: | :---: |
| `test_routing_dsn.py` | `test_dsn_tree_initialization` | AST parsing of valid Specctra DSN structure | **PASS** | 0.082s |
| `test_routing_dsn.py` | `test_dsn_tree_find_node` | Hierarchical node retrieval (`structure`, `network`) | **PASS** | 0.045s |
| `test_routing_dsn.py` | `test_dsn_tree_set_boundary` | Polygon boundary injection and keepout preservation | **PASS** | 0.061s |
| `test_routing_dsn.py` | `test_dsn_tree_set_grid_resolution` | Enforce 1.25 mil wire and via grid resolution | **PASS** | 0.052s |
| `test_routing_dsn.py` | `test_dsn_tree_set_default_rules` | Default trace width and clearance injection | **PASS** | 0.049s |
| `test_routing_dsn.py` | `test_dsn_tree_update_net_classes` | Class rule update with unquoted names and BNF `clear` | **PASS** | 0.078s |
| `test_routing_dsn.py` | `test_dsn_class_rule_update_preserves_circuit` | Preserves `(circuit (use_via via0))` subnodes | **PASS** | 0.064s |
| `test_routing_dsn.py` | `test_dsn_clean_duplicate_polygon_vertices` | Deduplication of consecutive identical padstack vertices | **PASS** | 0.058s |
| `test_routing_dsn.py` | `test_dsn_invariant_violation_detection` | Negative test: raises error if component dropped | **PASS** | 0.071s |
| `test_routing_dsn.py` | `test_sexpr_parser_compact_serialization` | Single-line compact serialization for rules and paths | **PASS** | 0.041s |
| `test_routing_modes.py` | `test_routing_mode_fast` | FAST mode parameter validation (12 passes, 300s timeout)| **PASS** | 0.038s |
| `test_routing_modes.py` | `test_routing_mode_balanced` | BALANCED mode defaults (30 passes, 600s timeout) | **PASS** | 0.035s |
| `test_routing_modes.py` | `test_routing_mode_precision` | PRECISION mode parameters (60 passes, 1200s timeout)| **PASS** | 0.039s |
| `test_routing_modes.py` | `test_routing_mode_invalid_lookup` | Fallback to BALANCED mode on invalid mode string | **PASS** | 0.031s |
| `test_routing_modes.py` | `test_profiler_phase_lifecycle` | Start/end phase metrics and JSON summary generation | **PASS** | 0.044s |
| `test_routing_orchestrator.py` | `test_orchestrator_initialization` | RoutingEngineOrchestrator backend discovery | **PASS** | 0.051s |
| `test_routing_orchestrator.py` | `test_orchestrator_headless_args` | Verification of `--gui.enabled=false` injection | **PASS** | 0.042s |
| `test_routing_orchestrator.py` | `test_orchestrator_log_parser_passes` | Real Freerouting log pass number extraction regex | **PASS** | 0.065s |
| `test_routing_orchestrator.py` | `test_orchestrator_stagnation_detection` | Triggers stop when unrouted score plateaus for 10 passes| **PASS** | 0.059s |
| `test_routing_orchestrator.py` | `test_orchestrator_timeout_cleanup` | Process tree termination on timeout without orphan PID | **PASS** | 0.085s |
| `test_routing_power.py` | `test_trace_width_manager_envelope_clearance`| Clearance-aware widening plan calculation | **PASS** | 0.062s |
| `test_routing_power.py` | `test_trace_width_manager_pad_escape_zone` | Pad escape protection: excludes segments within 35 mil | **PASS** | 0.073s |
| `test_routing_power.py` | `test_trace_width_manager_obstacle_avoidance`| Rejects widening when obstacle clearance $< 4.02\text{ mil}$ | **PASS** | 0.067s |
| `test_routing_connectivity.py` | `test_connectivity_graph_generation` | Physical copper segment graph extraction | **PASS** | 0.089s |
| `test_routing_connectivity.py` | `test_connectivity_discontinuity_detection`| Identifies disconnected pin components accurately | **PASS** | 0.074s |
| `test_routing_connectivity.py` | `test_connectivity_plane_via_continuity` | Validates plated-through vias to internal planes | **PASS** | 0.068s |
| `test_routing_board_intel.py` | `test_board_intelligence_stackup_analysis` | 4-layer stackup layer capability detection | **PASS** | 0.056s |
| `test_routing_board_intel.py` | `test_board_intelligence_hotspot_scoring` | Quantitative density and congestion hotspot mapping | **PASS** | 0.079s |
| `test_routing_board_intel.py` | `test_board_intelligence_qfn_escape_check` | Predicts maze search feasibility based on pitch & width | **PASS** | 0.061s |

---

## 2. Live Verification Gate Summary

- **Live Anchor Drift Gate:** PASS ($0.000\text{ mil}$ drift across `J1`, `J2`, `J5`, `J6`, `U5`).
- **Live Clearance DRC Gate:** PASS ($0$ clearance errors in EasyEDA Pro).
- **Live Fan Throttling Gate:** PASS (Single-threaded `-mt 1` verified, silent fan operation).
- **Live Multi-Pin Routing Gate:** PASS (AST inline serializer verified, all 40 multi-pin nets recognized).
