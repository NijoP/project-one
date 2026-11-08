# Waveshare 1.47" LCD Interface Engineering Documentation

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\waveshare_lcd_interface.md`  
**Manufacturer Reference:** Waveshare 1.47inch LCD Module (Rounded Corners, 172 × 320, ST7789V3)  
**Official Wiki:** `https://www.waveshare.com/wiki/1.47inch_LCD_Module`  
**Connector Designator:** `J6`

---

## 1. Superseded Specification Correction

| Parameter | Original Incorrect Specification | Corrected Waveshare Module Specification |
| :--- | :--- | :--- |
| **Display Technology** | DWO Flexible AMOLED | IPS LCD with Rounded Corners |
| **Driver Controller** | Raydium RM67162 | Sitronix ST7789V3 |
| **Resolution** | Undefined circular/oval | 172 × 320 pixels (RGB) |
| **Electrical Interface** | 33-pin FPC (QSPI) | 8-pin PH2.0 Connector (4-wire SPI) |
| **Power Rails** | Complex multi-rail AMOLED bias | Single 3.3V supply (internal boost on module) |
| **Physical Dimensions** | Unknown custom glass | 22.0 × 38.5 mm (Active area: 17.39 × 32.35 mm) |

---

## 2. Connector J6 Pinout & Signal Map

The on-board connector `J6` is populated with an authentic **8-pin PH2.0 surface-mount horizontal header** ([`CONN-SMD_8P-P2.00_S8B-PH-SM4-TB-LF-SN`](file:///C:/watch/desk/projects/WATCH/state/pcb_dump.json)):

| Pin # | Wire Color (Waveshare Cable) | Signal Name | Net Name | ESP32-S3 Pin | Voltage Level | Description |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | Red | `VCC` | `3V3` | Pin 2 | 3.3V | Main module power supply |
| **2** | Black | `GND` | `GND` | Pin 1 | 0V | Ground reference |
| **3** | Blue | `DIN` | `LCD_SDA` | Pin 11 (`IO18`) | 3.3V Logic | 4-wire SPI MOSI data line |
| **4** | Yellow | `CLK` | `LCD_SCL` | Pin 10 (`IO17`) | 3.3V Logic | SPI Serial Clock line (up to 40MHz) |
| **5** | Orange | `CS` | `LCD_CS` | Pin 23 (`IO21`) | 3.3V Logic | Active-low SPI Chip Select |
| **6** | Green | `DC` | `LCD_DC` | Pin 28 (`IO35`) | 3.3V Logic | Data / Command register control |
| **7** | White | `RST` | `LCD_RST` | Pin 29 (`IO36`) | 3.3V Logic | Active-low hardware display reset |
| **8** | Purple | `BL` | `LCD_BL` | Pin 30 (`IO37`) | 3.3V / PWM | LED backlight brightness control |
| **9** | Shell Tab | `SHIELD` | `GND` | — | 0V | Mechanical retention pad (Ground) |
| **10**| Shell Tab | `SHIELD` | `GND` | — | 0V | Mechanical retention pad (Ground) |

---

## 3. PCB Position Lock & Orientation

- **Coordinates:** `(X = 1574.8 mil, Y = 708.7 mil)`
- **Rotation:** `90°`
- **Layer:** Layer 1 (Top Layer)
- **Mechanical Constraint:** Strictly locked in place. The header is located at the right edge of the PCB, allowing the pre-terminated PH2.0 cable to mate cleanly without mechanical obstruction or bending stress.
- **Decoupling:** Decoupled by 100nF MLCC capacitor `C29` immediately adjacent to Pin 1 (`3V3`).
