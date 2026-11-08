# Reusable Hardware Design Lessons Learned

## 1. I2S Digital Microphone Array Routing & Clocking
- **Clock Tree Fanout:** Sharing `I2S_BCLK` and `I2S_WS` across three digital microphones requires short, impedance-matched traces. Ensure branch stubs are < 10mm to avoid high-frequency reflection ringing.
- **Stereo TDM Pairing:** ICS-43434 microphones allow dual-sharing of a single data pin (`SD1`) by pulling `L/R` (pin 2) to GND on Left mic and to 3V3 on Right mic. The third mic must use a dedicated serial data pin (`SD2`) to prevent bus collision.

## 2. MAX98357A Stereo Channel Discrimination
- **SD_MODE Biasing Pitfall:** Pin 4 (`SD_MODE`) on MAX98357A controls both shutdown and channel select. If tied to a common enable net without independent resistor dividers, both amplifiers collapse into mono mix `(L+R)/2`.
- **Verified Rule:** Left channel requires single pull-up ($R pprox 100	ext{k}\Omega$) establishing $>1.4	ext{V}$. Right channel requires precision voltage divider ($R_1 = 100	ext{k}\Omega$ to IO, $R_2 = 100	ext{k}\Omega$ to GND) establishing $pprox 0.65	ext{V}$.

## 3. Physical Position Locking in Surgical Rework
- **Mechanical Anchor Immutability:** USB-C connectors, SD card cages, and display headers interface directly with plastic enclosure tooling. Never globally auto-place components during a redesign. Capture an immutable JSON lock manifest before moving any objects.
