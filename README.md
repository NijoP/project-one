# Project One: Voice-Interactive Wearable Hardware Knowledge Base

**Display Title:** Project One  
**Repository Slug:** `project-one`  
**GitHub Remote:** [https://github.com/NijoP/project-one](https://github.com/NijoP/project-one)  
**Classification:** Confidential Engineering Knowledge Base & Data Lake  
**Target Hardware:** Compact Voice-Interactive Wearable Audio Device  
**Core Controller:** Espressif ESP32-S3-WROOM-1 (4-Layer PCB Stackup)

---

## 1. Mission & Engineering Objective

`Project One` is the permanent engineering data repository and technical knowledge base for the Voice-Interactive Wearable hardware rework executed with DESK (Design Engineering System Kit).

Rather than serving solely as a static file dump, this repository preserves the **complete, structured execution history**:
- Formal engineering requirements traceability
- Native EasyEDA design files, component dumps, and coordinate geometry
- Empirical failure logs with complete stack traces, root-cause analyses, and verified mitigations
- Performance telemetry, latency benchmarks, and bottleneck profiling
- Structured JSON and JSONL datasets for machine learning, automated regression tests, and future DESK engine optimizations

---

## 2. Directory Architecture

```
project-one/
│
├── README.md                          # Repository mission, overview, and navigation
├── PROJECT_STATUS.md                  # Master live execution status & phase completion matrix
├── CHANGELOG.md                       # Chronological engineering changes (V1 -> V2)
├── CONTRIBUTING.md                    # Engineering contribution and sync guidelines
├── .gitignore                         # Repository exclusion rules
│
├── 01_project_overview/               # Executive briefs, system scope, architecture & timeline
├── 02_requirements/                   # Original client DOCX, extracted text, and traceability matrix
├── 03_hardware_design/                # EasyEDA sources, PCB coordinates, schematics, BOM & GPIO maps
├── 04_datasheets/                     # IC component specifications, parametric data & index
├── 05_validation/                     # 8 hard quality gates, ERC/DRC results, physics reports
├── 06_execution_logs/                 # Continuous progress logs, failure logs, and Python script audits
├── 07_engineering_decisions/          # Client approval items, trade studies, and design decisions
├── 08_automation_and_tools/           # Project-specific scripts, JSON schemas, sync automation
├── 09_engineering_knowledge/          # Reusable lessons learned, recurring failure patterns & DESK improvements
├── 10_deliverables/                   # Production packages, BOMs, mechanical placement reports
└── schemas/                           # JSON Schema specifications for automated telemetry ingestion
```

---

## 3. Hardware Architecture Summary

- **Controller:** ESP32-S3-WROOM-1-N16R8 (Dual-core Xtensa LX7, 8MB PSRAM, 16MB Flash).
- **Acoustic Subsystem:** 3x `ICS-43434` digital I2S microphones (`MIC1` Left, `MIC2` Right, `MIC3` Dedicated channel) + 2x `MAX98357A` Class-D bridge-tied mono amplifiers driving `J3`/`J4` stereo speaker headers.
- **Display Interface:** Waveshare 1.47" Rounded IPS LCD (ST7789V3, 172×320, 4-wire SPI) via 8-pin PH2.0 header `J6`.
- **Power Architecture:** Dynamic power-path management via `BQ24074RGTR` (`U2`), high-efficiency 3.3V buck-boost `TPS63802DLAR` (`U3`), and secondary 5V boost `TPS61023DRLR` (`U4`).
- **Physical Controls:** 4 equidistant aligned tactile switches (`SW1`–`SW4`) on top board edge with ROM-bootloader multiplexing.
- **Physical Lock Status:** 100% position lock preserved on USB-C (`J1`), battery wirepads (`J2`), microSD (`J5`), LCD header (`J6`), and ESP32-S3 (`U5`).

---

## 4. Provenance & Synchronization

All data points maintain strict provenance linking back to:
- **DESK Execution Working Directory:** `C:\watch\desk`
- **Active EasyEDA Window ID:** `42d3a8e9-365d-4fe6-a6fc-3aa7ef161ae7`
- **EasyEDA Project UUID:** `c1859960f83648a892c64af27feb9e63` (`watch`)
- **Telemetry Server:** `http://127.0.0.1:49630` (DESK Local Mission Control)
