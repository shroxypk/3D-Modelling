# CRNT multi-hole panel

Source: `../../../vids/CRNT - 03 - Hard Surface Panel [Xbp8s_I_1gc].mp4`.
Current deliverable: `Panel.blend`; synchronized build: `build.py`.

## Construction and checks
The front has five staggered 16-sided recesses and a lower rounded rectangular recess. Floors, rims and the sheet form one continuous mesh. Mirror preserves symmetry; subdivision is enabled only after reviewing the base silhouette and features. Review renders run separately and never save their temporary scene overrides.

The source was reviewed through timestamped overview sheets and targeted full-resolution frames, not uninterrupted viewing. Radius and spacing use visible transform values; thickness, recess profiles and rectangular corner proportions are estimates. The result reproduces the demonstrated feature arrangement and direct edge-routing approach; it is not a claim of identical vertex positions or every mouse operation.

Sequence evidence:
- 00:03–00:24: bent sheet, thickness, longitudinal divisions.
- 00:27–01:03: 16-sided cylinders; side view confirms shallow blind cuts. The earlier through-hole checkpoint was incorrect and is replaced.
- 01:06–01:39: downward extension and lower rectangular feature.
- 01:51–02:39: direct quad connections between neighboring circles and columns into the rectangular area.
- 02:51–03:39: inset rims, inward step and floor lip; support edges.
- 03:51–05:30: subdivision checks, rectangular inset, circular floor fill, flange supports.

## Transferable lessons
1. A front view cannot establish whether a hole is blind. Inspect the cutter end against both sheet surfaces in a side view, and confirm the later floor construction.
2. Track proportion changes throughout the sequence: the panel is extended downward after the initial circular layout.
3. Adjacent circles can share short, direct quad strips. Route remaining edges into planar rows and the next feature rather than spiraling around each hole.
4. Floors must be connected to their walls. A separate insert or coincident cap is not equivalent.
5. Support width controls sharpness. Add support around the outline and through sheet thickness so subdivision does not taper the edges.
6. A manifold all-quad result is only a structural check. Compare silhouette, layout, depth, shading and the base cage separately.

Validation is in `validation.json`. The half-mesh's open boundaries lie on the Mirror plane; the evaluated Mirror and subdivision meshes must be closed and connected. View images in `review/`.

## Rectangle correction after user review
The prior study-pass assessment missed the stretched/chamfered rectangular corners. Replaced the scaled-grid corner clamp with four explicit quarter-circle segments per corner and straight tangent edges, a connected transfinite quad floor, revised 2.48 by 0.91 outer proportions, radius 0.12, and depth 0.025 (normalized estimates). Re-rendered and inspected shaded and base-topology views. Do not repeat the old completion claim as evidence of reference fidelity.
Transfer: topology validity cannot excuse an incorrect primitive outline; establish tangent lines and circular corner arcs explicitly before propagating a grid through a rounded rectangle.
