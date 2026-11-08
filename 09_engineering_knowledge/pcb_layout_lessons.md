# Reusable PCB Layout Lessons Learned

## 1. DFM Board Edge Setback for Solder Pads
- Surface-mount wirepads (e.g. Battery J2) must maintain at least `0.30 mm` (`12 mil`) clearance from the board outline. Placing pads closer (e.g. 0.04 mm) exposes copper during V-scoring or CNC routing, risking short circuits to metal casings.

## 2. MLCC Proximity to Mechanical Connectors
- Avoid placing 0603/0805 MLCC capacitors within `1.0 mm` of pluggable connectors (e.g. microSD socket J5 or USB-C J1). Board flexure during insertion/removal generates shear stresses that crack ceramic dielectric layers.

## 3. High-Current Buck-Boost Inductor Placement
- Power inductor L1 must be placed directly adjacent to TPS63802 switch nodes, but separated from sensitive analog circuitry (e.g. microphone bias lines and MAX98357A inputs) by continuous Layer 2 copper ground shielding.
