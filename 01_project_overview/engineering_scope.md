# Engineering Scope — Rework V2.0

## Included Scope
1. Correction of display interface: Transition from speculative DWO AMOLED / RM67162 33-pin FPC to authentic Waveshare 1.47" IPS LCD module (ST7789V3, 8-pin PH2.0).
2. Physical position-lock preservation: Strict 0.0 mil coordinate and rotation lock for USB-C (J1), battery pads (J2), microSD (J5), display connector (J6), and ESP32-S3 (U5).
3. Speaker connector repositioning: Relocate dispersed J3 and J4 into an adjacent, symmetrical pair on Layer 2 near top PCB edge (200 mil pitch).
4. Four-switch linear arrangement: Align SW1-SW4 in a straight equidistant row along top edge (Y = 1633.9 mil, 180 mil pitch); multiplex 5 functions across 4 physical switches.
5. Electrical schematic audit: Correct MAX98357A stereo mode short; isolate 5V boost against USB reverse current; verify 3-mic I2S bus contention.
6. Design rule & manufacturing gate validation: Evaluate 8 hard quality gates; flag J2.1 battery pad setback for retraction.

## Excluded Scope
- Global redesign or re-placement of non-speaker connectors.
- Alteration of USB-C or microSD insertion directions.
- Relocation of ESP32-S3 module or violation of antenna keepout.
