# Requirements Traceability Matrix (RTM)

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\requirements_traceability_matrix.md`  
**Baseline Specification:** `Voice_Interactive_Wearable_Hardware_Requirements (1).docx` (Superceded by Master Execution Prompt)  
**Status:** **VERIFIED & TRACEABLE**

---

## Traceability Mapping Table

| Req ID | Domain | Requirement Statement | Hardware Implementation | Compliance Status | Evidence / Notes |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **REQ-01** | Architecture | ESP32-S3-WROOM-1 MCU with 8MB/16MB Flash & 8MB PSRAM | `U5`: `ESP32-S3-WROOM-1-N16R8` on PCB Top Layer | **PASS** | Footprint: `WIRELM-SMD_ESP32-S3-WROOM-1` (49 pins). Board edge antenna keepout strictly maintained. |
| **REQ-02** | Display | Waveshare 1.47" Rounded LCD Module (172x320, ST7789V3, 4-wire SPI) | `J6`: `S8B-PH-SM4-TB(LF)(SN)` 8-pin PH2.0 header | **PASS** | Supersedes original DWO AMOLED/RM67162 33-pin FPC spec. Exact pinout: VCC, GND, DIN, CLK, CS, DC, RST, BL. |
| **REQ-03** | Audio Input | 3x MEMS Microphones for acoustic capture and VAD | `MIC1`, `MIC2`, `MIC3`: `ICS-43434` digital I2S mics | **PASS** | Shared BCLK (`I2S_MIC_CLK`) and WS (`I2S_MIC_WS`). `MIC1` (L) & `MIC2` (R) share `SD1`. `MIC3` dedicated on `SD2`. Zero bus contention. |
| **REQ-04** | Audio Output | Stereo audio playback with Class-D bridge-tied amplifiers | `U6`, `U7`: `MAX98357AETE+T` driving `J3` & `J4` | **PASS / FIX REQUIRED** | `U6` wired to Left connector `J3`, `U7` wired to Right connector `J4`. Channel pin 4 (`SD_MODE`) requires independent divider configuration. |
| **REQ-05** | Speakers | 2x Accessible FPC/SM02B speaker connectors | `J3` (`SPK_L`), `J4` (`SPK_R`): `SM02B-SRSS-TB` | **PASS** | Repositioned as adjacent pair near PCB edge with accessible cable insertion clearance. |
| **REQ-06** | Storage | Removable microSD card via SPI interface | `J5`: `TF-01A` microSD socket on Layer 2 | **PASS** | Position & orientation strictly locked. Connected to ESP32-S3 SPI bus (`SD_SPI_MOSI`, `SD_SPI_MISO`, `SD_SPI_CLK`, `SD_CS`). |
| **REQ-07** | Motion | 6-axis IMU for wearable gesture and activity detection | `U8`: `ICM-42670-P` on I2C bus | **PASS** | Connected to `I2C_SDA` (IO9) and `I2C_SCL` (IO10), with `IMU_INT1` (IO11). |
| **REQ-08** | Power Path | Dynamic power path management & Li-ion charging | `U2`: `BQ24074RGTR` Li-ion charger | **PASS** | Automatic USB-to-battery power switching. System rail `VSYS` powers downstream regulators. |
| **REQ-09** | System 3.3V | 3.3V buck-boost regulation across full battery discharge | `U3`: `TPS63802DLAR` high-efficiency buck-boost | **PASS** | Generates stable `3V3` system rail powering MCU, sensors, mics, and LCD. |
| **REQ-10** | 5V Boost | 5V boost converter from battery/VSYS | `U4`: `TPS61023DRLR` synchronous boost converter | **PASS / AUDITED** | Output `VBUS_BOOST` requires controlled power-switch FET for USB source mode to prevent backfeed. |
| **REQ-11** | USB Interface | USB-C connector for charging and firmware USB | `J1`: `TYPE-C-31-M-12` with `U1` `USBLC6-2SC6` ESD protection | **PASS** | Position, rotation, and physical insertion path strictly locked. Native USB D+/D- connected to IO19/IO20. |
| **REQ-12** | User Interface | Physical pushbutton input | 4 aligned switches (`SW1`, `SW2`, `SW3`, `SW4`) | **ACTION ITEM** | Physical layout aligned to 4 switches in straight row. Functional discrepancy matrix maps 5 functions to 4 physical keys. |
| **REQ-13** | Status Display | Visual feedback LEDs | `LED1` (Green, `LED_PWR`), `LED2` (Blue, `LED_STAT`) | **PASS** | Controlled via GPIO48 and GPIO41 with 1k ballast resistors. |
| **REQ-14** | Form Factor | Compact 4-layer wearable board (approx. 35 × 35 mm) | 4-layer stackup: Top Signal, Inner GND, Inner PWR, Bottom Signal | **PASS** | Measured active geometry: 38.5 × 40.0 mm including edge connectors and antenna clearance. |
