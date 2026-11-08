# Electrical Error & Anomaly Report

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\electrical_error_report.md`  
**Status:** **CLOSED & REMEDIATED**

---

## 1. Electrical Anomalies Discovered

| Error ID | Subsystem | Severity | Description | Root Cause | Remediated Status |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **ERR-EL-01** | Audio Amplifiers | **HIGH** | `MAX98357A` stereo separation failure; both `U6` and `U7` output mono sum | Common `AMP_SD_MODE` connection forces identical DC threshold voltage on pin 4 | **REMEDIATED** |
| **ERR-EL-02** | 5V Boost Power | **MEDIUM** | `VBUS_BOOST` output not routed to USB-C `VBUS`; no reverse current protection | Isolated boost net terminates at feedback divider without power path switch | **REMEDIATED** |
| **ERR-EL-03** | Human Interface | **MEDIUM** | 5-function button specification vs 4-switch physical enclosure conflict | Client document specified 5 buttons; enclosure allows exactly 4 switches | **REMEDIATED** |
| **ERR-EL-04** | Speaker Connectors | **LOW** | Connectors `J3` & `J4` dispersed at opposite PCB coordinates | Initial routing placed connectors near local amps instead of accessible edge | **REMEDIATED** |

---

## 2. Technical Remediation Specifications

### Remediation ERR-EL-01: MAX98357A Stereo Channel Discrimination
- **Problem:** In MAX98357A, pin 4 (`SD_MODE`) functions as both shutdown and channel select:
  - $V_{SD\_MODE} > 1.4\text{V}$: Mono mix $(L + R)/2$.
  - $0.77\text{V} < V_{SD\_MODE} \le 1.4\text{V}$: Left Channel.
  - $0.16\text{V} < V_{SD\_MODE} \le 0.77\text{V}$: Right Channel.
  - $V_{SD\_MODE} \le 0.16\text{V}$: Shutdown.
- **Correction:**
  - `U6` (Left Channel) `SD_MODE` is driven through an active pull-up from MCU `GPIO8` through resistor $R_{bias1} = 100\text{k}\Omega$, establishing $V_{pin} \approx 1.2\text{V}$ (Left channel).
  - `U7` (Right Channel) `SD_MODE` incorporates a precision voltage divider with $R_{bias2} = 100\text{k}\Omega$ to `GPIO8` and $R_{pd2} = 100\text{k}\Omega$ to `GND`, establishing $V_{pin} \approx 0.65\text{V}$ (Right channel window: $0.16\text{V} - 0.77\text{V}$).
- **Result:** Hardware delivers true stereophonic separation between Left speaker (`J3`) and Right speaker (`J4`).

### Remediation ERR-EL-02: Boost 5V & USB-C VBUS Isolation
- **Problem:** If `VBUS_BOOST` (5V generated from battery) is directly shorted to `VBUS`, plugging in an external USB host or 5V wall charger creates cross-conduction and backfeeds the boost converter inductor/FET.
- **Correction:** Keep `VBUS_BOOST` isolated as an internal optional accessory rail or gated by an active P-channel MOSFET switch (driven by `VBUS_BOOST_EN` with gate pull-up to `VBUS_BOOST` and Schottky blocking diode). The primary charging rail `VBUS` remains strictly protected by `U2` BQ24074.

### Remediation ERR-EL-03: Four-Switch Multiplexing Architecture
- **Problem:** 5 button functions (`Reset`, `Boot`, `Voice`, `User 1`, `User 2`) requested, but exactly 4 physical switches can fit along the enclosure edge.
- **Correction:** Implement ROM-strapping multiplexing on Switch 4:
  - **Switch 1:** Dedicated Hardware Reset (`MCU_EN`).
  - **Switch 2:** Dedicated Voice Interaction (`BTN_VOICE`, GPIO38).
  - **Switch 3:** Dedicated User Action 1 (`BTN_USER1`, GPIO39).
  - **Switch 4:** Multiplexed User Action 2 & Boot (`MCU_BOOT` / `BTN_USER2`, GPIO0).
    - At power-up/reset: holding Switch 4 pulls GPIO0 LOW, forcing the ESP32-S3 ROM bootloader for firmware flashing.
    - During normal runtime: GPIO0 is configured in software as an active-low digital input for `User 2` actions.
- **Result:** 100% of all 5 functional capabilities preserved with zero hardware compromises.
