# Four-Switch Alignment & Functional Multiplexing Report

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\four_switch_placement_report.md`  
**Physical Components:** `SW1`, `SW2`, `SW3`, `SW4`  
**Switch Model:** `TS-1187A-B-A-B` (SMD Tactile Pushbutton, 5.1 × 5.1 mm, 1.5mm Actuator)

---

## 1. Five-to-Four Functional Discrepancy Resolution

### The Conflict
- The original client requirements document specified **5 button functions**:
  1. `Reset` (Hardware MCU enable/restart)
  2. `Boot` (ROM bootloader strap)
  3. `Voice Interaction` (Primary push-to-talk key)
  4. `User Action 1` (Config / Volume Up)
  5. `User Action 2` (App Sync / Volume Down)
- The physical industrial design and enclosure aperture allocate space for **exactly 4 tactile switches in one aligned row**.

### The Engineering Solution (ROM-Strapping Multiplexing)
In the ESP32-S3 microcontroller, `GPIO0` is an external strapping pin sampled **only during the rising edge of reset (`MCU_EN`)**:
- At power-on or when `MCU_EN` is released:
  - If `GPIO0` is `LOW` $\rightarrow$ ROM Bootloader (firmware flashing mode).
  - If `GPIO0` is `HIGH` $\rightarrow$ Normal SPI Flash execution.
- After reset completes, `GPIO0` is fully released by the ROM and acts as a standard general-purpose digital input/output pin!

By mapping Switch 4 to `GPIO0`:
- **Flashing / Recovery Mode:** Hold Switch 4 while tapping Switch 1 (`Reset`) $\rightarrow$ enters Bootloader mode.
- **Normal Runtime Operation:** Tapping Switch 4 is read by firmware as `User Action 2`.

---

## 2. Four-Switch Functional Mapping Matrix

| Physical Position | Designator | Primary Runtime Function | Secondary / Boot Function | Electrical Net | ESP32-S3 Pin |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **Switch 1 (Leftmost)** | `SW1` | **System Reset** | Power-on Hard Restart | `MCU_EN` | Pin 3 (`EN`) |
| **Switch 2** | `SW2` | **Voice Interaction** | Push-to-Talk Audio Capture | `BTN_VOICE` | Pin 31 (`IO38`) |
| **Switch 3** | `SW3` | **User Action 1** | Short Press: Next / Long: Menu | `BTN_USER1` | Pin 32 (`IO39`) |
| **Switch 4 (Rightmost)**| `SW4` | **User Action 2** | **ROM Bootloader Mode (at Reset)** | `MCU_BOOT` / `IO0` | Pin 27 (`IO0`) |

*Result:* **Zero loss of functionality.** All 5 operations are supported across exactly 4 physical tactile switches.

---

## 3. Physical Placement Geometry

### Selected Board Edge: Top Edge Corner (Layer 1, Top)
The top edge provides direct, unobstructed accessibility through the upper rim of the wearable casing, maintaining clear clearance from the bottom USB-C port (`J1`) and right-side display header (`J6`).

### Alignment Specifications
- **Common Alignment Axis:** $Y = 1633.9\text{ mil}$
- **Orientation:** $0^\circ$ (All 4 actuators point outward along $+Y$ direction)
- **Equal Pitch Spacing:** $\Delta X = 180.0\text{ mil}$ ($4.572\text{ mm}$ center-to-center)

| Switch Ref | X Coordinate (mil) | Y Coordinate (mil) | Rotation | Center-to-Center Pitch |
| :---: | :---: | :---: | :---: | :---: |
| **`SW1`** | `1000.0` | `1633.9` | `0°` | Baseline |
| **`SW2`** | `1180.0` | `1633.9` | `0°` | `+180.0 mil` (`4.57 mm`) |
| **`SW3`** | `1360.0` | `1633.9` | `0°` | `+180.0 mil` (`4.57 mm`) |
| **`SW4`** | `1540.0` | `1633.9` | `0°` | `+180.0 mil` (`4.57 mm`) |

### Clearance Verification
- **Clearance to `J1` (USB-C):** $>1400\text{ mil}$ separation (opposite edge).
- **Clearance to `J5` (microSD):** $>1200\text{ mil}$ separation.
- **Clearance to `J6` (Display):** $>900\text{ mil}$ separation.
- **Clearance to `MIC2`:** $>150\text{ mil}$ clearance from acoustic sound port.
