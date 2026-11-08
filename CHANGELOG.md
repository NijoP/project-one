# Changelog — Project One

All notable changes to the Voice-Interactive Wearable hardware design, execution telemetry, and knowledge base are documented in this file.

---

## [2.0.0] - 2026-11-09

### Added
- Created dedicated GitHub knowledge base repository `project-one` under authenticated account `NijoP`.
- Initialized comprehensive directory architecture (`01_project_overview` through `10_deliverables` and `schemas`).
- Integrated continuous failure tracking (`06_execution_logs/failures/`) and performance progress telemetry (`06_execution_logs/progress/`).
- Added formal JSON schemas for machine-readable error, task, performance, and validation records in `schemas/`.
- Generated Production Bill of Materials (`03_hardware_design/bom/bom.csv` and `bom.md`) covering all 89 components across 19 line items.
- Generated ESP32-S3 master GPIO allocation and boot strapping matrix (`03_hardware_design/gpio_mapping/gpio_map.md`).

### Changed
- **Display Interface:** Replaced incorrect DWO AMOLED / RM67162 33-pin FPC design assumptions with verified Waveshare 1.47" IPS LCD module (ST7789V3, 172×320, 4-wire SPI via 8-pin PH2.0 header `J6`).
- **Audio Amplifiers:** Corrected `MAX98357A` stereo channel mode short. Configured `U6` with pull-up bias for Left channel and `U7` with precision divider for Right channel on `AMP_SD_MODE`.
- **Speaker Connectors:** Repositioned `J3` (`SPK_L`) and `J4` (`SPK_R`) from dispersed opposite corners into an adjacent, symmetrical pair on Layer 2 along the top board edge (`200 mil` pitch).
- **Physical Switches:** Re-aligned scattered pushbutton placements into an aligned, equidistant linear row of 4 switches (`SW1`–`SW4`) along the top edge ($Y = 1633.9\text{ mil}$).
- **Button Architecture:** Resolved the 5-function vs 4-switch enclosure conflict by multiplexing `User 2` and `Bootloader Mode` onto Switch 4 (`GPIO0`).

### Preserved (Locked)
- Preserved exact coordinates and rotations for USB-C (`J1`), Battery Wirepads (`J2`), microSD Socket (`J5`), Display Header (`J6`), and ESP32-S3 MCU (`U5`) with 0.0 mil drift.
