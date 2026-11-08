# Complete ESP32-S3 GPIO Allocation & Strapping Table

**Project:** Voice-Interactive Wearable Audio Device (Rework V2)  
**Document Ref:** `C:\watch\desk\projects\WATCH_REWORK_V2\gpio_allocation_table.md`  
**Controller:** `ESP32-S3-WROOM-1-N16R8` (`U5`)

---

## 1. Master GPIO Map

| Pin | GPIO / Signal | Function | Bus / Domain | Direction | Boot Strapping / Pull State |
| :---: | :---: | :--- | :--- | :---: | :--- |
| **1** | `GND` | Ground reference | Power | PWR | Ground plane return |
| **2** | `3V3` | Primary 3.3V power | Power | PWR | Main supply input from U3 |
| **3** | `MCU_EN` | Hardware chip enable / reset | Control | IN | 10k pull-up to 3V3, 1µF delay cap; Switch 1 pull-down |
| **4** | `IO4` | `I2S_MIC_WS` | Audio In | OUT | Frame synchronization (Word Select) for MIC1-3 |
| **5** | `IO5` | `I2S_SPK_BCLK` | Audio Out | OUT | Bit clock for MAX98357A stereo amplifiers (U6, U7) |
| **6** | `IO6` | `I2S_SPK_WS` | Audio Out | OUT | Word select (L/R clock) for audio output |
| **7** | `IO7` | `I2S_SPK_DOUT` | Audio Out | OUT | Serial audio data out to U6 & U7 |
| **8** | `IO15` | `SD_CS` | Storage | OUT | Chip select for microSD socket (J5) |
| **9** | `IO16` | `SD_DET` | Storage | IN | Card presence detection switch (Active LOW) |
| **10** | `IO17` | `LCD_SCL` | Display | OUT | SPI Serial Clock for Waveshare 1.47" ST7789V3 (J6) |
| **11** | `IO18` | `LCD_SDA` | Display | OUT | SPI MOSI Data Out for Waveshare display (J6) |
| **12** | `IO8` | `AMP_SD_MODE` | Audio Out | OUT | Amplifier shutdown and stereo channel bias control |
| **13** | `IO19` | `USB_DM` | USB | I/O | Native USB Full-Speed D- differential signal |
| **14** | `IO20` | `USB_DP` | USB | I/O | Native USB Full-Speed D+ differential signal |
| **15** | `IO3` | `I2S_MIC_CLK` | Audio In | OUT | Bit clock for ICS-43434 microphones (MIC1-3) |
| **16** | `IO46` | `CHG_STAT` | Power | IN | Charger status flag (Open-drain, 10k pull-up to 3V3) |
| **17** | `IO9` | `I2C_SDA` | Sensor | I/O | I2C Serial Data for ICM-42670-P IMU (U8) |
| **18** | `IO10` | `I2C_SCL` | Sensor | OUT | I2C Serial Clock for ICM-42670-P IMU (U8) |
| **19** | `IO11` | `IMU_INT1` | Sensor | IN | IMU motion interrupt (Wake on motion / Free fall) |
| **20** | `IO12` | `SD_SPI_MOSI` | Storage | OUT | SPI Data Out to microSD card (J5) |
| **21** | `IO13` | `SD_SPI_MISO` | Storage | IN | SPI Data In from microSD card (J5) |
| **22** | `IO14` | `SD_SPI_CLK` | Storage | OUT | SPI Clock for microSD card (J5) |
| **23** | `IO21` | `LCD_CS` | Display | OUT | Active-low Chip Select for Waveshare display (J6) |
| **24** | `IO47` | `CHG_EN` | Power | OUT | Active-low charge enable for BQ24074 (U2) |
| **25** | `IO48` | `LED_PWR` | UI | OUT | Green Power/Charging Status Indicator LED |
| **26** | `IO45` | `VBUS_SENSE` | Power | IN | USB 5V VBUS voltage divider sense input |
| **27** | `IO0` | `MCU_BOOT` / `BTN_USER2`| UI / Boot | I/O | **Multiplexed:** Boot strapping at reset; User 2 button |
| **28** | `IO35` | `LCD_DC` | Display | OUT | Data/Command select for ST7789V3 LCD (J6) |
| **29** | `IO36` | `LCD_RST` | Display | OUT | Active-low hardware reset for Waveshare display (J6) |
| **30** | `IO37` | `LCD_BL` | Display | OUT | PWM backlight brightness control for Waveshare display |
| **31** | `IO38` | `BTN_VOICE` | UI | IN | Primary Voice Interaction Pushbutton (Switch 2) |
| **32** | `IO39` | `BTN_USER1` | UI | IN | User Action 1 Pushbutton (Switch 3) |
| **33** | `IO40` | `BTN_USER2` (Aux) | UI | IN | Secondary input / Aux trigger |
| **34** | `IO41` | `LED_STAT` | UI | OUT | Blue User / Network Activity Status Indicator LED |
| **35** | `IO42` | `VBUS_BOOST_EN`| Power | OUT | Enable for TPS61023 5V boost converter (U4) |
| **38** | `IO43` | `I2S_MIC_SD2` | Audio In | IN | Dedicated I2S data line for third microphone (MIC3) |
| **39** | `IO44` | `I2S_MIC_SD1` | Audio In | IN | Stereo multiplexed I2S data line for MIC1 & MIC2 |
| **40** | `GND` | Ground reference | Power | PWR | Ground return |
| **41** | `EP` | Thermal Ground | Power | PWR | Exposed thermal pad soldered to Layer 2 ground plane |

---

## 2. Boot Strapping Analysis & Verification

1. **`GPIO0` (`MCU_BOOT`):**
   - Must be HIGH during chip power-up / reset release to execute firmware from SPI Flash.
   - Pulled HIGH to 3.3V via 10kΩ resistor `R21`.
   - Connected to Switch 4: pressing Switch 4 grounds GPIO0, allowing manual ROM bootloader entry when resetting.
2. **`GPIO46` (`CHG_STAT`):**
   - Boot strap pin sampled on reset.
   - Pulled HIGH via 10kΩ pull-up `R4` to 3.3V, ensuring normal boot state.
3. **`GPIO45` (`VBUS_SENSE`):**
   - Strapping pin for SPI Flash VDD; must remain LOW at reset (pulled down by voltage divider `R30`/`R31`).
