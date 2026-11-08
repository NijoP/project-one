# Project Brief — Voice-Interactive Wearable Audio Device

## Overview
A compact, battery-powered wearable audio device providing interactive, voice-controlled personal audio playback.
Features offline voice activity detection, three-microphone speech capture, stereo Class-D audio playback, microSD storage, and a 1.47" rounded IPS display.

## Key Specifications
- **MCU:** ESP32-S3-WROOM-1-N16R8 (Dual-core 240MHz, 16MB Flash, 8MB PSRAM, Wi-Fi & BLE 5.0)
- **Audio Input:** 3x Knowles/TDK ICS-43434 digital I2S MEMS microphones
- **Audio Output:** 2x Maxim Integrated MAX98357A Class-D BTL mono audio amplifiers
- **Display:** Waveshare 1.47" Rounded IPS LCD (ST7789V3, 172x320, 4-wire SPI, PH2.0 8-pin connector)
- **Power:** Li-ion battery charging via BQ24074RGTR, 3.3V buck-boost via TPS63802DLAR, 5V boost via TPS61023DRLR
- **Storage:** Removable microSD TF socket (SPI mode)
- **Motion Sensor:** TDK InvenSense ICM-42670-P 6-axis IMU (I2C)
- **Physical Controls:** 4 aligned tactile switches along top enclosure rim
- **Dimensions:** 4-layer PCB, 38.5 x 40.0 mm active footprint
