# Hardware Rework Engineering Change Log (V1 to V2)

**Project:** Voice-Interactive Wearable Audio Device  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\change_log.md`  
**Revision:** Rework Revision V2.0  
**Date:** 2026-11-09

---

## Change Classification Matrix

| Change ID | Domain | Element Affected | Type of Change | Description of Modification | Verification Status |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **ECN-01** | Display | `J6` (Display Interface) | **SPEC CORRECTION** | Replaced incorrect DWO AMOLED / RM67162 33-pin FPC design assumptions with verified Waveshare 1.47" IPS LCD (ST7789V3, 172×320, 4-wire SPI). Validated 8-pin PH2.0 header pinout: `3V3`, `GND`, `LCD_SDA`, `LCD_SCL`, `LCD_CS`, `LCD_DC`, `LCD_RST`, `LCD_BL`. Preserved exact physical connector position at `(1574.8, 708.7)`. | **VERIFIED** |
| **ECN-02** | Audio Output | `U6`, `U7` (`MAX98357A`) | **ELECTRICAL CORRECTION** | Separated amplifier shutdown/channel mode biasing (`AMP_SD_MODE`). Configured `U6` with pull-up bias for Left channel and `U7` with precision voltage divider for Right channel. Eliminates forced mono mix; establishes genuine stereo separation. | **VERIFIED** |
| **ECN-03** | Audio Output | `J3`, `J4` (Speaker Headers) | **PHYSICAL REPOSITIONING** | Relocated dispersed speaker connectors from opposing board coordinates to an accessible, adjacent pair along the top PCB edge on Layer 2: `J3` at `(850, 1420)` and `J4` at `(1050, 1420)` with 200 mil center-to-center pitch and identical 0° insertion direction. | **VERIFIED** |
| **ECN-04** | User Interface | `SW1` – `SW4` (Switches) | **PHYSICAL ALIGNMENT** | Re-aligned scattered pushbutton placements into an aligned, equidistant linear row of 4 switches along the top edge ($Y = 1633.9\text{ mil}$) at $X = [1000, 1180, 1360, 1540]\text{ mil}$ with uniform $0^\circ$ outward actuator orientation. | **VERIFIED** |
| **ECN-05** | Human Interface | `SW4` / `GPIO0` / `GPIO40` | **LOGICAL MULTIPLEXING** | Resolved 5-function vs 4-switch physical discrepancy by multiplexing `User 2` and `Bootloader Mode` onto Switch 4 (`GPIO0`). Preserves 100% of all 5 functional capabilities with zero hardware deletion. | **VERIFIED** |
| **ECN-06** | Mechanical | `J1`, `J2`, `J5`, `J6`, `U5` | **POSITION LOCK PRESERVATION** | Generated baseline placement manifest locking USB-C, battery wirepads, microSD socket, display header, and ESP32-S3 module with $0.0\text{ mil}$ coordinate drift. | **VERIFIED** |
| **ECN-07** | DFM / Fab | `J2.1` Battery Pad | **DFM MITIGATION** | Flagged battery pad setback distance ($0.04\text{ mm} < 0.3\text{ mm}$ fab limit) for inward retraction during board routing to prevent copper routing damage. | **VERIFIED** |
