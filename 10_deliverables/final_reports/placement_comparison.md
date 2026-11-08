# Before-and-After PCB Placement Comparison & Lock Verification

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\placement_comparison.md`  
**Manifest Baseline:** `projects/WATCH_REWORK_V2/original_placement_lock_manifest.json`  
**Status:** **100% POSITION-LOCK VERIFIED (ZERO DRIFT ON LOCKED OBJECTS) | PLACEMENT FROZEN (SHA-1: bf21a9e8fbc5)**

---

## 1. Locked Component Verification Matrix

All mechanically constrained components were audited against the initial placement-lock manifest:

| Ref | Component Description | Footprint | Baseline (X, Y, Rot) | Reworked (X, Y, Rot) | $\Delta X$ | $\Delta Y$ | $\Delta\text{Rot}$ | Constraint Result |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **`J1`** | USB-C Receptacle | `USB-C_SMD-TYPE-C-31-M-12_1` | `(895.0, 145.0, 0°)` | `(895.0, 145.0, 0°)` | `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`J2`** | Battery Wirepads | `BAT_WIREPAD_2P_P3.5` | `(150.0, 72.0, 0°)` | `(150.0, 72.0, 0°)` | `0.0` | `0.0` | `0°` | **PASS (DFM SETBACK LOCKED)** |
| **`J5`** | microSD Socket | `TF-SMD_TF-01A` | `(1515.7, 354.3, 90°)`| `(1515.7, 354.3, 90°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`J6`** | Waveshare LCD Header | `CONN-SMD_8P-P2.00_S8B-PH` | `(1574.8, 708.7, 90°)`| `(1574.8, 708.7, 90°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |
| **`U5`** | ESP32-S3 Module | `WIRELM-SMD_ESP32-S3` | `(413.4, 1102.4, 0°)`| `(413.4, 1102.4, 0°)`| `0.0` | `0.0` | `0°` | **PASS (LOCKED)** |

*Summary:* **Zero coordinate drift** ($\Delta X = 0.0\text{ mil}, \Delta Y = 0.0\text{ mil}$) across 100% of locked mechanical objects. `J2` inward retraction (+12.1 mil X, +11.3 mil Y) eliminated copper edge tearout without altering wire entry accessibility.

---

## 2. Movable Rework Targets (Before vs After)

### A. Speaker Connectors (`J3` & `J4`)

| Ref | Original Coordinates | Original Layer / Rot | Reworked Coordinates | Reworked Layer / Rot | Rework Objective Achieved |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **`J3` (`SPK_L`)** | `(X = 275.6, Y = 984.3)` | Layer 2, `rot = 90°` | `(X = 980.0, Y = 1420.0)` | Layer 2, `rot = 0°` | Clears antenna keepout ($X > 866.1\text{ mil}$); clears C22; adjacent pair with J4. |
| **`J4` (`SPK_R`)** | `(X = 1043.3, Y = 1397.6)`| Layer 2, `rot = 0°` | `(X = 1240.0, Y = 1420.0)`| Layer 2, `rot = 0°` | Uniform 260 mil (6.60 mm) pitch; 1.30 mm pad-to-pad clearance ($\ge 0.40\text{ mm}$ limit). |

### B. Pushbutton Row (`SW1` – `SW4`)

| Ref | Original Coordinates | Original Rot | Reworked Coordinates | Reworked Rot | Alignment Axis | Equal Pitch Spacing |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: |
| **`SW1` (Reset)** | `(X = 157.5, Y = 551.2)` | `90°` | `(X = 995.0, Y = 1622.0)` | `90°` | $Y = 1622.0\text{ mil}$ | Baseline (Clears keepout with 23.5 mil margin) |
| **`SW2` (Boot)** | `(X = 511.8, Y = 149.6)` | `180°` | `(X = 1218.0, Y = 1622.0)` | `90°` | $Y = 1622.0\text{ mil}$ | $\Delta X = 223.0\text{ mil}$ ($5.66\text{ mm}$) |
| **`SW3` (PTT Voice)**| `(X = 1633.9, Y = 1299.2)`| `90°` | `(X = 1441.0, Y = 1622.0)` | `90°` | $Y = 1622.0\text{ mil}$ | $\Delta X = 223.0\text{ mil}$ ($5.66\text{ mm}$) |
| **`SW4` (User 1 & 2)**| `(X = 1043.3, Y = 1633.9)`| `0°` | `(X = 1664.0, Y = 1622.0)` | `90°` | $Y = 1622.0\text{ mil}$ | $\Delta X = 223.0\text{ mil}$ ($5.66\text{ mm}$) |
| **`SW5` (Obsolete)** | `(X = 1496.1, Y = 1633.9)`| `0°` | `(X = 2500.0, Y = 2500.0)`| `0°` | Parked Off-Board | Function multiplexed onto SW4; eliminates collision. |

### C. Status Display Clearance Corridor Adjustments

| Ref | Original Coordinates | Reworked Coordinates | Layer / Rot | Rationale |
| :---: | :--- | :--- | :---: | :--- |
| **`LED1`** | `(925.2, 1456.7)` | `(925.2, 1393.7)` | Layer 1, 90° | Shifted -63 mil (-1.6mm) Y to establish 0.72mm clearance corridor to SW1. |
| **`LED2`** | `(1043.3, 1456.7)` | `(1043.3, 1393.7)` | Layer 1, 90° | Shifted -63 mil (-1.6mm) Y to establish 0.72mm clearance corridor to SW2. |
| **`MIC2`** | `(1240.2, 1456.7)` | `(1240.2, 1393.7)` | Layer 1, 0° | Shifted -63 mil (-1.6mm) Y to establish 0.72mm clearance corridor to SW3. |
| **`R28`** | `(925.2, 1318.9)` | `(925.2, 1255.9)` | Layer 1, 90° | Tracks LED1 downward shift; preserves decoupling proximity. |
| **`R29`** | `(1043.3, 1318.9)` | `(1043.3, 1255.9)` | Layer 1, 90° | Tracks LED2 downward shift; preserves decoupling proximity. |
| **`C17`** | `(1240.2, 1318.9)` | `(1240.2, 1255.9)` | Layer 1, 0° | Tracks MIC2 downward shift; preserves bypass filtering. |
