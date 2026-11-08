# Client Engineering Approval & Sign-Off Items

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\client_approval_items.md`  
**Status:** **AWAITING CLIENT FORMAL SIGN-OFF**

---

## Items Presented for Formal Client Approval

### Item 1: Four-Switch Functional Multiplexing Architecture
- **Context:** The original document specified 5 button functions (`Reset`, `Boot`, `Voice Interaction`, `User 1`, `User 2`). The physical enclosure accommodates exactly 4 aligned switches along the top edge.
- **Proposed Architecture:**
  - **Switch 1:** Dedicated Hardware Reset (`MCU_EN`)
  - **Switch 2:** Dedicated Push-to-Talk Voice Interaction (`BTN_VOICE`, GPIO38)
  - **Switch 3:** Dedicated User Action 1 (`BTN_USER1`, GPIO39)
  - **Switch 4:** Multiplexed ROM Bootloader & User Action 2 (`MCU_BOOT` / `IO0`):
    - *At Reset / Power-Up:* Holding Switch 4 enters ROM bootloader mode for firmware downloads.
    - *During Normal Operation:* Short press on Switch 4 acts as `User Action 2` in firmware.
- **Client Action Required:** Confirm approval of this multiplexing approach or specify if an alternative button combination is preferred.

---

### Item 2: Speaker Connector Layout & Orientation (`J3` & `J4`)
- **Context:** Connectors `J3` (`SPK_L`) and `J4` (`SPK_R`) were moved from opposing corners into an adjacent, symmetrical pair on Layer 2 (Bottom) along the top edge:
  - `J3` at `(850.0 mil, 1420.0 mil, rot = 0°)`
  - `J4` at `(1050.0 mil, 1420.0 mil, rot = 0°)`
  - Spacing: `200.0 mil` (`5.08 mm`) center-to-center.
- **Client Action Required:** Confirm physical clearance with the internal speaker transducer housing and acoustic baffles.

---

### Item 3: Battery Pad `J2.1` Setback Adjustment
- **Context:** DRC flagged `J2.1` pad setback at `0.04 mm` from the PCB contour (< `0.3 mm` minimum fabrication standard for PCB edge routing).
- **Proposed Action:** Move solder pad pair `J2` inward by `0.26 mm` (`10.2 mil`) to achieve compliant `0.30 mm` edge clearance without impacting battery wire soldering.
- **Client Action Required:** Confirm approval of the 10.2 mil inward setback adjustment.

---

### Item 4: Boost 5V Accessory Power Architecture
- **Context:** `U4` (TPS61023) 5V boost converter generates `VBUS_BOOST`, currently isolated from USB-C `VBUS` to prevent destructive reverse-current when an external USB charger is connected.
- **Recommendation:** Maintain reverse-current isolation unless USB On-The-Go (OTG) 5V accessory power is explicitly requested, in which case a reverse-blocking P-channel power switch IC must be added.
- **Client Action Required:** Confirm if USB 5V OTG sourcing is required for external accessories, or if USB-C is strictly a charging sink.
