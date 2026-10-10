# CRNT complex pipe fitting study

Current result: Pipe.blend. Build source: build.py plus source/branch.py and source/finish.py.
Video: ../../../vids/CRNT - 04 - Complex Pipe Fitting [MDnNrsJeHbQ].mp4.

## Reviewed construction sequence

- 00:03-00:24: 32-sided main tube, extruded flange, broad concave transition and main bore.
- 00:27-00:51: 16-sided side cylinder, positioned at X -1.0359, Z 1.2, radius .606. The operand's inner end is shaped before union.
- 01:03-01:39: union and removal of short intersection edges, preserving the branch's longitudinal strips.
- 01:51-02:03: narrow root supports and neck divisions.
- 02:15-02:27: cut the side bore through to the main bore, reconnect the lip.
- 02:39-03:15: inspect the inside and resolve intersection fragments, then support its edge.
- 03:27-03:39: subdivision review and symmetry to create the opposing branch.
- 03:51-04:15: four small flange recesses with floors, edge supports.
- 04:27: compare the smooth result and its silhouette.

Coverage is based on overview contact sheets and targeted full-resolution frames, not uninterrupted playback. No claim that every action or entire video was watched. The bore radius .48 and small-recess dimensions are visual estimates, not values read from the tutorial. The result is not an exact copy of the tutorial mesh.

## What this exercise tested

1. A cylinder intersection requires work on both surfaces. A plausible exterior union can still obstruct the internal passage. Review a section and trace the openings.
2. Prepare the Boolean operand to suit the host shape. A planar or badly triangulated cap can intrude into the main bore; the build moves its end into the wall and uses planar chord strips.
3. Keep original circular end rings while merging short intersection fragments into the junction. A distance threshold alone is not sufficient: protect the branch corners and inspect the resulting contour.
4. Add narrow support bands only at lips and junctions. Preserve the broad flange transition rather than covering it with arbitrary tight loops.
5. Local flange details can come from a 2x2 quad patch, an eight-sided inset and an extruded wall. Here the floors are four quads, not a triangle fan.
6. Floors are visible in the tutorial recesses. Do not assume every circular detail is a through-hole.
7. Mirror produces the opposing branch and a continuous center seam. Keeping the modifier live leaves the construction editable.
8. Mostly-quad counts do not demonstrate fidelity. Inspect the base, subdivision result, side profile, bore and section separately.

## Review and remaining limitations

- Full base: 1,414 vertices, 1,428 faces, 20 triangles; other faces are quads.
- One connected component; no nonmanifold edges or zero-area faces after Mirror.
- Open base boundaries all lie on the Mirror plane.
- Subdivision level 2: one connected manifold component, no zero-area faces.
- Ray checks confirm an unobstructed main vertical passage and unobstructed straight passage through both side branches.
- All four recessed floors remain above the flange bottom (evaluated center heights about .134).
- Shaded, topology, side, bore and disposable section views inspected. No major visible breakage in these views; this does not certify perfect curvature under every lighting setup.
- Base retains the 20 junction triangles. Do not describe it as all-quads. Recess and bore proportions are estimates and can be refined if a closer dimensional reference is available.

Review images are in review/. The review script uses temporary display/camera settings and never saves its scene. Pipe.blend keeps the working environment and live Mirror/Subdivision modifiers; no redundant blend variants were created.

Study pass closed so the next exercise can proceed: recessed cover (BnP1U8Y10QA).
