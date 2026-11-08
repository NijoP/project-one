# Speaker FPC Connector Pinout & Placement Engineering Report

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\speaker_fpc_report.md`  
**Target Connectors:** `J3` (`SPK_L`), `J4` (`SPK_R`)  
**Footprint:** `CONN-SMD_2P-P1.00_SM02B-SRSS-TB-LF-SN` (1.00mm Pitch Shrouded Header)

---

## 1. Electrical & Mechanical Compatibility

Both connectors are driven by dedicated Texas Instruments / Analog Devices `MAX98357AETE+T` Class-D bridge-tied load (BTL) mono audio power amplifiers.

| Parameter | Specification | Verification Result |
| :--- | :--- | :--- |
| **Drive Topology** | Bridge-Tied Load (BTL) Filterless Class-D | `SPK+` and `SPK-` are both active differential outputs (neither is grounded). |
| **Output Power** | Up to 3.2W into 4Ω at 5V, or ~1.5W into 8Ω at 3.7V | Fully within wearable acoustic transducer limits. |
| **Pin Pitch** | 1.00 mm (JST SH series compatible) | Standard miniature wearable speaker lead pitch. |
| **Current Rating** | 1.0 A AC/DC per pin | Ample headroom for 300-500mA peak audio currents. |
| **Shield Tabs** | Dual side retention tabs soldered to Ground | High mechanical resistance against cable pull forces. |

---

## 2. Connector Pinout & Channel Mapping

### Left Speaker Connector (`J3` - `SPK_L`)
- **Driving IC:** `U6` (`MAX98357A`)
- **Schematic Label:** `SPK_L`
- **Pin 1:** `SPK_L_P` (Positive BTL output from U6 Pin 9)
- **Pin 2:** `SPK_L_N` (Negative BTL output from U6 Pin 10)
- **Pins 3, 4:** `GND` (Mechanical retention solder tabs)

### Right Speaker Connector (`J4` - `SPK_R`)
- **Driving IC:** `U7` (`MAX98357A`)
- **Schematic Label:** `SPK_R`
- **Pin 1:** `SPK_R_P` (Positive BTL output from U7 Pin 9)
- **Pin 2:** `SPK_R_N` (Negative BTL output from U7 Pin 10)
- **Pins 3, 4:** `GND` (Mechanical retention solder tabs)

---

## 3. Physical Placement & Arrangement Optimization

### Pre-Rework Baseline Issue
- In the initial layout, `J3` was placed on Bottom Layer at `(X = 275.6 mil, Y = 984.3 mil, rot = 90°)`, while `J4` was placed at `(X = 1043.3 mil, Y = 1397.6 mil, rot = 0°)`.
- **Flaw:** The connectors were over `850 mil` apart on disparate axes with conflicting insertion angles, creating asymmetric cable harness routing inside the enclosure.

### Corrected Adjacent Pair Arrangement
- **Selected Board Edge:** Top Edge accessible zone on Layer 2 (Bottom Layer).
- **Coordinates & Orientations:**
  - **`J3` (`SPK_L`):** `X = 850.0 mil, Y = 1420.0 mil`, Rotation: `0°`
  - **`J4` (`SPK_R`):** `X = 1050.0 mil, Y = 1420.0 mil`, Rotation: `0°`
- **Inter-Connector Pitch:** Exactly `200.0 mil` (`5.08 mm`) center-to-center.
- **Benefits:**
  1. **Consistent Insertion Direction:** Both FPC/leads insert from the same edge along the Y-axis.
  2. **Equal Cable Travel:** Symmetric harness length for left and right earpieces/speakers.
  3. **Zero Collision:** Maintained >100 mil clearance from `MIC2` acoustic port and edge switches.
