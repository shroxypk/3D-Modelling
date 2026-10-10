# Mechanical joint study

Source: CRNT Designers https://www.youtube.com/watch?v=XOSZvoEypTA

9 October 2026: first reproduction and visual review completed. Current output: MechanicalJoint.blend. Synchronized construction: build.py. Temporary rendering: source/review_current.py (never saves its display overrides).

Coverage: chronological 12-second sample sheets and full-resolution frames at 00:39, 02:03, 04:51, 05:39 and 05:52 were reviewed. This is sampled visual analysis, not a claim that every operation or audio segment was watched.

Sequence followed at the feature level: retained curved cylinder wall; connected cylindrical shaft; supported root and terminal cap; narrow reinforcing ridge; separate stepped axle; second arm rotated about the axle. The mesh construction deliberately uses quad patches rather than repeating the tutorial's Boolean cleanup exactly.

Validation:
- Each arm and its curved housing are one connected component. The axle is a third separate component/object, as required by the assembly.
- Each arm: 738 base vertices, 736 quad faces. Axle: 930 base vertices, 928 quad faces.
- Base and evaluated subdivision meshes have zero nonquads, zero nonmanifold edges and zero zero-area faces.
- World-space evaluated surface intersection checks initially exposed 24 overlapping triangle pairs at the rotated arm/axle. Reducing axle radial size by 2.5 percent removed these; all three object pairs now report zero. This is a visual assembly check, not mechanical tolerance certification.
- Inspected perspective, front, rear, top, base and wireframe views. Corrected second-arm tilt to match the downward direction shown in the source.

Transferable lessons:
1. Determine which parts form a continuous surface before choosing object boundaries. Joining disconnected shells is insufficient.
2. A circular shaft can flow into a curved rectangular shell through matched boundary sectors; use enough subdivisions across the shell's curvature as well as around the shaft.
3. Reinforcing details should grow out of the existing surface. Their supporting loops need to follow the changing section through the transition.
4. Subdivision changes seating clearance. Check the assembled evaluated surfaces, especially after rotating one part.
5. Quad end grids avoid central triangle fans; their spacing still requires visual inspection.

Limitations: normalized, visually estimated dimensions. Ridge taper, edge radii and axle profile remain an approximation rather than an exact tutorial match. Extra shaft sectors continue beyond the local ridge and could be optimized for a production low-poly asset. No claim of exact topology replication or fabrication suitability.


## Circularity correction after user review
The axle originally inherited uneven angular spacing from the arm ridge. Its vertices were on circles, but Catmull-Clark smoothing introduced uneven radial shrinkage. The axle now has independent uniform 32-sector rings and matching quad end grids. At subdivision level 2, 720 radial samples at each of three axial sections measured about 0.0304% radial spread, consistent with the small facets of the evaluated polygon surface rather than the previous uneven outline. All three evaluated object pairs still report zero surface intersections. This supersedes the earlier axle acceptance.
