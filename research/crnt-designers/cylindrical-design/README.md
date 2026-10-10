# Cylindrical design — active exercise

Source: CRNT Designers https://www.youtube.com/watch?v=x9rApivNiGE

9 October 2026: initial single-panel checkpoint saved in CylindricalDesign.blend. Build entry point: build.py. Disposable review: source/review_current.py. Images: review/. Geometry checks: validation.json.

Reviewed the three chronological sample sheets and full-resolution 00:39 topology view. Coverage is sampled visual analysis, not uninterrupted playback. Current reconstruction covers the initial curved panel and corner details, approximately 00:03–02:15 at the feature level.

The base surface lies on a parent cylinder. Four eight-sector blind details connect to its quad grid; the back and perimeter give the panel thickness. Both base and Subdivision 2 checks find all quads, zero nonmanifold edges and zero zero-area faces. Base: 450 vertices / 448 faces. Shaded, top/profile and wire views inspected. An inconsistent circular boundary ordering was caught in the wireframe and corrected before repeating the panel.

Remaining: match the corner chamfer and detail seating more closely against intermediate frames; compare evaluated curvature with the parent; repeat around/along the cylinder; model the connecting bands, larger details and end rims. This is not a finished exercise.

Lessons: preserve the curved parent during local detail construction; verify cyclic correspondence when bridging rings; inspect one module before multiplying an error through an array. Model validity does not prove the tutorial shape is matched.


## Assembly continuation
Eight linked panels now occupy two rows at 90-degree spacing. Added the open parent tube, eight vertical strips, four middle-band sections and both end rims. Circular and rounded-rectangular recesses are connected to the strip surfaces. Source order: build.py, source/assemble.py, source/bands.py. One current blend is retained; review overrides remain separate.

Reviewed full-resolution tutorial frames 02:39, 03:51, 04:15 and 05:08 as well as the earlier sampled sequence. Inspected assembled shaded, front, rear, top and wire views. Corrected the middle slot from an oval toward a rounded rectangle. Assembly validation before that coordinate-only slot correction found all 23 base/evaluated meshes closed and all-quad with no zero-area faces.

This is a reviewed assembly checkpoint, not an exact final match. The tutorial's corner chamfers, larger detail rim profiles, slot proportions and panel/band width balance still need a closer reference pass. Do not treat the geometry checks as approval of those dimensions. Next: focus on those visible differences before moving to the complex-part exercise.

Transfer: repeat linked geometry so corrections propagate; keep physical seams rather than merging separate panels; establish the band's curvature before carving its connected details. Inspect the assembled view because isolated panels do not reveal gap/proportion errors.

## User-requested corner correction
Rebuilt each corner as an explicit diagonal with endpoint support through thickness using edge creases (0.9). Linked geometry propagates the correction to all eight panels. Base and evaluated panel remain closed and all-quad with no zero-area faces. Re-rendered and inspected front and wire views. Source synchronized in build.py; assembly source retains linked geometry. Other previously documented fidelity limitations remain.
