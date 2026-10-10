# Transferable modeling lessons

These are recorded observations from the exercises, with their limits; they do not imply permanent model retraining or complete tutorial coverage.

| Principle | Evidence / example | Check to repeat on another model |
|---|---|---|
| Match shape before optimizing topology | [Panel correction](panel/README.md) | Compare front outline, corner tangencies and depth against the same tutorial stage |
| Model actual connectivity | [Bracket](bracket/README.md), [joint](mechanical-joint/README.md) | Count connected components and inspect the shared root; one object may contain separate islands |
| Inspect inner walls as well as outer surfaces | [Pipe](pipe/README.md) | Section the bore and inspect branch interiors |
| Blind recesses need floors and controlled depth | [Cover](cover/README.md), [slotted panel](slotted-panel/README.md) | Compare rim height, floor and silhouette from oblique views |
| Circular flow can continue into straight strips | [Slotted panel](slotted-panel/README.md) | Trace the continuous border; avoid unnecessary poles on the rounded transition |
| Uniform circular vertices are not enough if angular spacing is uneven | [Joint circularity correction](mechanical-joint/README.md) | Give rotationally symmetric pieces their own uniform sectors; inspect and measure evaluated roundness |
| Subdivision changes seating | [Joint](mechanical-joint/README.md) | Check evaluated assembly intersections after rotation and smoothing |
| All quads does not mean accurate or well shaded | Every exercise above | Inspect shaded and base wire views; record remaining differences honestly |
| Use density where the shape needs it | [Joint](mechanical-joint/README.md) | Curved shell resolution and ridge supports serve different purposes; do not reuse their spacing on an unrelated axle |

For each next exercise: record source coverage, construction order, the visible failure caught, the correction, validation limits and one practical transfer. The cylindrical-panel study will test preserving parent curvature while adding local details and repeating separate panels.
