# Modeling and topology principles to carry into new studies

## Tested additions - 8 October 2026

- Circularity and dimensional retention are separate. In the [controlled circular-detail exercise](topology-video-study/practice/README.md), nominal radius 0.6 became about 0.54066 with eight boundary points and 0.58464 with sixteen after subdivision. Both looked rounder than the four-point case, but neither retained the specified radius. Measure evaluated fit. These measurements apply to the tested midwall and support profile, not every shape.
- The [CRNT bracket junction review](crnt-designers/README.md) shows union cleanup before root beveling, then deliberate routing from the hole through the root into the base. Avoid overlapping separately rounded objects when the intended part is continuous. Boolean output is an intermediate construction step.

## Working principles

- Manifoldness does not detect every folded face. The [solid bracket checkpoint](crnt-designers/bracket/README.md) passed connectivity checks while a concave side patch overlapped itself. A concave polygon's arithmetic centroid may lie outside its interior; inspect the patch and bevel result, and do not equate valid edge incidence with a valid surface.

- Purposeful root density: the [connected root study](crnt-designers/practice/README.md) compares one straight segment against four quarter-circle segments at equal nominal radius. The four-segment version better retains the intended curved profile after subdivision. Judge the radius and highlights, not the quad count. This sheet study does not validate a full solid bracket.

- Match the tutorial's intended shape, proportions, construction order, and connected-part relationships first. Use judgment to interpret the demonstration; a single selected coordinate or one frame is evidence, not a substitute for understanding the whole sequence.
- Establish the base form and fit from the reference before adding Subdivision Surface. Keep the shape readable and edges intentionally sharp or soft according to the object.
- Prefer a clean all-quad surface with purposeful edge flow. Let loops follow real silhouette changes, openings, bends, and functional transitions. A moderate, useful density is fine; avoid both needless reduction and random dense loops.
- For circular forms, use a 16-vertex circle when it matches the scale and silhouette. Extrude an existing loop to create a shoulder instead of adding a disconnected redundant ring.
- Keep symmetry or other useful modifiers live while they help. Apply thickness and bevel only after the base fit is established; avoid destructive steps that make later shape corrections harder.
- Make surfaces that are supposed to be one continuous piece share a mesh and topology. Keep separate components separate when the tutorial or real assembly calls for them.
- Check the model in shaded form and with its cage visible. Inspect important joins, openings, and curves from more than one view; fix pinching, shading artifacts, intersections, and inaccurate seating before proceeding.
- Build in the tutorial's chronological order. Review each section before modeling the next; use references to check shape, not to invent steps that the video has not reached.
