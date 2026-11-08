# Contributing to Project One

This document governs the engineering standards, synchronization protocols, and commit workflows for the `project-one` repository.

---

## 1. Core Principles

1. **Empirical Truth:** Never fabricate execution results or commit placeholder files. All logs, reports, and timing metrics must originate from verified tool execution or live EasyEDA Pro API queries.
2. **Append-Only History:** Never rewrite, rebase, or force-push historical execution logs or failure records.
3. **Strict Separation of Concerns:**
   - `C:\watch\desk` is the DESK execution engine and CLI toolchain.
   - `C:\watch\project-one` is the project-specific hardware design data, validation records, and telemetry lake.
4. **Credential Security:** Never commit secrets, tokens, passwords, or personal credentials.

---

## 2. Commit Message Convention

Use structured, semantic commit prefixes:

- `project:` General project structure, configuration, or documentation updates.
- `requirements:` Modifications to requirements traceability or specification documents.
- `schematic:` Schematic primitive changes, electrical fixes, or symbol updates.
- `pcb:` Placement modifications, routing adjustments, or mechanical clearance updates.
- `validation:` ERC, DRC, or hard quality gate test reports.
- `debug:` Root-cause investigations, failure logs, and error resolution records.
- `performance:` Latency measurements, bottleneck investigations, and optimizations.

---

## 3. Machine-Readable Data Standards

All structured data must comply with the corresponding schema in `schemas/`:
- Failure entries $\rightarrow$ `schemas/error_record.schema.json`
- Task logs $\rightarrow$ `schemas/task_record.schema.json`
- Performance metrics $\rightarrow$ `schemas/performance_record.schema.json`
- Validation records $\rightarrow$ `schemas/validation_record.schema.json`
