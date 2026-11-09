# Routing Hotspot & Congestion Analysis: Project One PCB

**Project:** Voice-Interactive Wearable Hardware Rework (`WATCH`)  
**PCB Outline:** $45.0\text{ mm} \times 45.0\text{ mm}$ ($1,771.65\text{ mil} \times 1,771.65\text{ mil}$), Area: $20.25\text{ cm}^2$  
**Layer Stackup:** 4 Copper Layers (`TopLayer`, `Inner1/GND`, `Inner2/PWR`, `BottomLayer`)  
**Component Population:** 89 parts (22 Top, 67 Bottom)  
**Total Pins / Pads:** 366 pads  
**Pin Density:** $10.8\text{ pins/cm}^2$ (Bottom Layer), $7.3\text{ pins/cm}^2$ (Top Layer)  

---

## 1. Congestion Hotspot Overview

```
 ┌─────────────────────────────────────────────────────────────┐
 │ (0, 1771 mil)                                (1771, 1771)  │
 │   ┌───────────────────────┐   ┌─────────────────────────┐   │
 │   │ HOTSPOT 1: ESP32-S3   │   │ HOTSPOT 4: CONNECTORS   │   │
 │   │ U5 (48-QFN, 0.4mm)    │   │ J5 (microSD), J6 (LCD)  │   │
 │   │ Pin Density: 24/cm²   │   │ U8 (Audio Amp)          │   │
 │   └───────────────────────┘   └─────────────────────────┘   │
 │                                                             │
 │   ┌───────────────────────┐   ┌─────────────────────────┐   │
 │   │ HOTSPOT 2: PMIC U6    │   │ HOTSPOT 3: SENSORS      │   │
 │   │ BQ24074 (16-QFN, 0.5m)│   │ U7 (IMU), U2, U3 LDOs   │   │
 │   │ Power Hub (VBAT/VSYS) │   │ High-density passives   │   │
 │   └───────────────────────┘   └─────────────────────────┘   │
 │ (0, 0)                                       (1771, 0)     │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Hotspot Characterization

### Hotspot 1: ESP32-S3 (`U5`) South and East Escapes
- **Component:** `U5` (ESP32-S3-WROOM-1 / SoC footprint) at coordinates $X=413.39\text{ mil}, Y=1102.36\text{ mil}$, Layer 1.
- **Physical Characteristics:** 40 castellated/SMD perimeter pins plus large central ground thermal slug (Pin 41).
- **Escape Constraint:** The southern perimeter carries high-speed SPI bus lines (`SD_SPI_CLK`, `SD_SPI_MOSI`, `SD_SPI_MISO`, `SD_CS`), I2C bus (`I2C_SCL`, `I2C_SDA`), and I2S digital audio channels (`I2S_SPK_BCLK`, `I2S_SPK_WS`, `I2S_SPK_DOUT`).
- **Corridor Bottleneck:** The trace routing corridor between the ESP32 perimeter and adjacent decoupling capacitors (`C1`–`C4`, `C14`–`C16`) is only $1.2\text{ mm}$ ($47.2\text{ mil}$) wide.
- **Resolution:** Escape traces must use $5.0\text{ mil}$ ($0.127\text{ mm}$) width and $4.0\text{ mil}$ ($0.102\text{ mm}$) clearance. Dropping micro-vias ($18.0\text{ mil}$ pad / $10.0\text{ mil}$ drill) immediately behind perimeter pads allows digital audio signals to transition to Layer 2 (Bottom copper) without consuming Layer 1 surface channels.

### Hotspot 2: BQ24074 PMIC (`U6`) Power Distribution Hub
- **Component:** `U6` (TI BQ24074 16-pin QFN, $3.0\text{ mm} \times 3.0\text{ mm}$, $0.5\text{ mm}$ pitch) at $X=50.2\text{ mm}, Y=100.0\text{ mm}$.
- **Physical Characteristics:** Adjacent pad pitch $p = 0.50\text{ mm}$ ($19.68\text{ mil}$), pad width $w_{pad} = 0.25\text{ mm}$ ($9.84\text{ mil}$). Gap between adjacent pads: $g = 0.25\text{ mm}$ ($9.84\text{ mil}$).
- **Failure Mode in V1:** Forcing $35.0\text{ mil}$ (`VBAT`) and $30.0\text{ mil}$ (`VSYS`) into global Specctra DSN rules caused immediate maze search collapse:
  $$\text{Required Door Width} = w_{trace} + 2 \times \text{clearance} = 35.0 + 2 \times 4.02 = 43.04\text{ mil} \gg 9.84\text{ mil}$$
- **Resolution (V2 Two-Phase Power Widening):**
  1. In DSN: Clamp escape width at pad boundary to $6.0\text{ mil}$ with $4.0\text{ mil}$ clearance:
     $$\text{Escape Door Width} = 6.0 + 2 \times 4.0 = 14.0\text{ mil}$$
     By escaping perpendicularly from the pad tip, clearance envelope to adjacent pads is maintained ($4.92\text{ mil} > 4.00\text{ mil}$).
  2. Post-Import: Canvas vector widening expands open-board power trunks between `J2`, `C5`, and power switches to $30.0\text{ mil}$ and $35.0\text{ mil}$ outside the $35.0\text{ mil}$ fine-pitch keepout radius.

### Hotspot 3: LSM6DSOX IMU (`U7`) Sensor Cluster
- **Component:** `U7` (14-pin LGA, $2.5\text{ mm} \times 3.0\text{ mm}$, $0.5\text{ mm}$ pitch) at $X=89.57\text{ mil}, Y=124.02\text{ mil}$.
- **Issue:** 5 pins are assigned to `GND` (`U7_2`, `U7_3`, `U7_11`, `U7_15`, `U7_17`). In the baseline board, outer copper pour polygons could not penetrate the dense surrounding ring of 0402 passives, leaving all 5 pins isolated.
- **Resolution:** Group adjacent GND pads (e.g. pins 2 and 3) into a single surface copper bridge and drop a shared $20/10\text{ mil}$ via directly to Layer 15 (`GND_PLANE_INNER1`).

### Hotspot 4: microSD (`J5`) and LCD (`J6`) High-Speed Interfaces
- **Components:** `J5` (Push-push microSD) and `J6` (FPC 0.5mm connector for ST7789 display).
- **Issue:** Both connectors sit along the right perimeter ($X > 1500\text{ mil}$). In the baseline, orphan vias (`e377`, `e379`) were dropped within $0.068\text{ mm}$ of SMD pads `R21_1` and `J6_6`, triggering clearance DRC violations.
- **Resolution:** Removed both orphan vias. Corridors along the $X=1400$–$1550\text{ mil}$ boundary are now completely open for parallel differential-style routing of SPI clocks and control airwires.
