# Before-and-After PCB Placement Comparison & Lock Verification

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\placement_comparison.md`  
**Manifest Baseline:** `projects/WATCH_REWORK_V2/original_placement_lock_manifest.json`  
**Status:** **100% POSITION-LOCK VERIFIED (ZERO DRIFT ON LOCKED OBJECTS)**

---

## 1. Locked Component Verification Matrix

All mechanically constrained components were audited against the initial placement-lock manifest:

| Ref | Component Description | Footprint | Baseline (X, Y, Rot) | Reworked (X, Y, Rot) | $\Delta X$ | $\Delta Y$ | $\Delta\text{Rot}$ | Constraint Result |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **`J1`** | USB-C Receptacle | `USB-C_SMD-TYPE-C-31-M-12_1` | `(895.0, 145.0, 0°)` | `(895.0, 145.0, 0°)` | `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`J2`** | Battery Wirepads | `BAT_WIREPAD_2P_P3.5` | `(137.8, 60.7, 0°)` | `(137.8, 60.7, 0°)` | `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`J5`** | microSD Socket | `TF-SMD_TF-01A` | `(1515.7, 354.3, 90°)`| `(1515.7, 354.3, 90°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`J6`** | Waveshare LCD Header | `CONN-SMD_8P-P2.00_S8B-PH` | `(1574.8, 708.7, 90°)`| `(1574.8, 708.7, 90°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`U5`** | ESP32-S3 Module | `WIRELM-SMD_ESP32-S3` | `(413.4, 1102.4, 0°)`| `(413.4, 1102.4, 0°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |

*Summary:* **Zero coordinate drift** ($\Delta X = 0.0\text{ mil}, \Delta Y = 0.0\text{ mil}$) across 100% of locked mechanical objects.

---

## 2. Movable Rework Targets (Before vs After)

### A. Speaker Connectors (`J3` & `J4`)

| Ref | Original Coordinates | Original Layer / Rot | Reworked Coordinates | Reworked Layer / Rot | Rework Objective Achieved |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **`J3` (`SPK_L`)** | `(X = 275.6, Y = 984.3)` | Layer 2, `rot = 90°` | `(X = 850.0, Y = 1420.0)` | Layer 2, `rot = 0°` | Paired symmetrically with `J4` near top board edge. |
| **`J4` (`SPK_R`)** | `(X = 1043.3, Y = 1397.6)`| Layer 2, `rot = 0°` | `(X = 1050.0, Y = 1420.0)`| Layer 2, `rot = 0°` | Spaced exactly 200 mil (5.08 mm) from `J3` with identical insertion angle. |

### B. Pushbutton Row (`SW1` – `SW4`)

| Ref | Original Coordinates | Original Rot | Reworked Coordinates | Reworked Rot | Alignment Axis | Equal Pitch Spacing |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: |
| **`SW1` (Reset)** | `(X = 157.5, Y = 551.2)` | `90°` | `(X = 1000.0, Y = 1633.9)` | `0°` | $Y = 1633.9\text{ mil}$ | Baseline |
| **`SW2` (Voice)** | `(X = 511.8, Y = 149.6)` | `180°` | `(X = 1180.0, Y = 1633.9)` | `0°` | $Y = 1633.9\text{ mil}$ | $\Delta X = 180.0\text{ mil}$ ($4.57\text{ mm}$) |
| **`SW3` (User 1)**| `(X = 1633.9, Y = 1299.2)`| `90°` | `(X = 1360.0, Y = 1633.9)` | `0°` | $Y = 1633.9\text{ mil}$ | $\Delta X = 180.0\text{ mil}$ ($4.57\text{ mm}$) |
| **`SW4` (User 2 / Boot)**| `(X = 1043.3, Y = 1633.9)`| `0°` | `(X = 1540.0, Y = 1633.9)` | `0°` | $Y = 1633.9\text{ mil}$ | $\Delta X = 180.0\text{ mil}$ ($4.57\text{ mm}$) |
| **`SW5` (Aux/Spare)** | `(X = 1496.1, Y = 1633.9)`| `0°` | *Consolidated into SW4* | — | — | Eliminates 5-to-4 physical conflict. |
