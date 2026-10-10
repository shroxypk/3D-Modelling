# Recessed cover exercise - active

Current file: Cover.blend. Study pass closed after center-border, underside and subdivision review.
Source order: build.py, source/recess.py, source/floor_symmetry.py, source/finish.py. Disposable review: source/review_current.py; it does not save scene overrides.

## Observations and coverage

Reviewed the existing three overview sheets, targeted opening frames at 9, 15, 21, 24, 27, 30, 33, 39, 42, 45, 47, 51, 54, 57, 60, 63, 69, 72 and 75 seconds. This is sampled visual review, not uninterrupted playback or a complete-video claim.

- Initial body is 2 x 2 x .8, followed by a .2-wide stepped top profile.
- At 00:24 the upper region is lowered .4, leaving a .2 base and .2 raised region.
- The tutor changes bevel values and undoes operations before accepting the shoulder. An intermediate modal value is not the final dimension.
- Around 01:12, the entire corner profile is rounded with four segments. The visible bevel width is .264.
- The corner recess comes next, cuts into this body, and later receives connected concentric floor detail. It is not a floating fastener.

## Current result and limitation

Stepped base, shoulder and rounded corners built; no Subdivision modifier yet. 160 vertices, 142 faces, 140 quads and two temporary planar cap ngons. No nonmanifold edges or zero-area faces. The top and underside are to receive the tutorial's later planar filling; do not call the current mesh all-quads.

The accepted shoulder coordinates were reconstructed from the later silhouette after the tutor's revisions. Those profile coordinates are estimates; the topology count matching the video does not prove exact dimensional equivalence.

Shaded perspective, top wireframe and side renders were checked. The first direct bevel attempt folded the shoulder despite matching vertex/face counts. The problem was caught in the render and replaced with a monotonic profile with no coincident rings before corner rounding. Current review images supersede the faulty attempt.

## Transferable lesson from this checkpoint

Track accepted edits, undo operations and changing modal settings, not just a visible numeric value. Chaining overlapping bevels can create coincident rings and folded surfaces even when the final mesh remains manifold and its counts match a reference. Inspect profile spacing, silhouette and shading before adding dependent details.

## October 8 continuation: connected recesses

Additional sampled frames: 78, 81, 87, 90, 93, 96, 99, 105, 111, 117, 123, 135, 147, 159, 162, 165, 168, 171, 183, 195, 207 and 255 seconds. This is targeted frame analysis, not a full playback claim.

The tutorial rotates the body 45 degrees before placing a 12-sided cutter at Y=1.0256. Converted to the unrotated working model, its center is X=Y=1.0256/sqrt(2). Radius is .103. The final cutter location .32691 and half-height .173 put the original blind floor at .15391. The rim follows the shoulder rather than staying horizontal.

Rebuilt the cleaned recess as a twelve-sector quad patch connected directly to the existing shoulder. Added the supported rim, .030931-deep floor step, and raised center based on the .0273 extrusion. Small support widths are estimated from the accepted close-up. The center uses a simple nine-quad patch instead of the tutorial's triangle fan. This is an intentional topology improvement, not an exact copy of every edge.

Live two-axis Mirror repeats the detailed quadrant. Current evaluated result: 918 vertices, 900 faces, one connected component, zero nonmanifold edges and zero zero-area faces. Eight temporary planar ngons remain across the mirrored top and underside. No subdivision yet. A failed initial cap-fill call was caught by the boundary check and replaced with the explicit quad patch before saving.

Model, close-up topology and side views were rendered. Dark bands in the flat-shaded shoulder and the right silhouette in the side render still need investigation during the base-surface review; manifold counts are not an approval of shading. Do not mark the exercise finished or move to the next exercise yet.

Next: investigate remaining base-surface appearance, follow 03:15 onward for central cap filling, border detail and underside support; then inspect subdivision and record the final lessons.

Transferable lesson: preserve the changing-height intersection of a cylinder with a slope, and distinguish a blind floor, a deeper circular step and a raised center. Validate the evaluated Mirror result as one connected surface; validate that a fill operation actually created faces.

## Finished study pass

Reviewed additional frames 213, 219, 222, 225, 228, 231, 237, 243, 246, 249 and 264. Added the narrow center-border groove using the visible .015 width and .0213 depth, supported the underside, and filled both planar caps with quad grids. Live Mirror plus Subdivision level 2 retained. Full base: 1,182 vertices / 1,180 all-quad faces; evaluated subdivision: 18,882 vertices / 18,880 faces. Both closed with no zero-area faces. A side ray scan also found no gap across the base width.

The final smoothed, top cage, underside and side views were inspected. The earlier dark faceted band does not persist in the smooth review. No obvious open seams or overlapping recess surfaces in these views. The all-quad center disks and planar grids deliberately differ from the tutorial's fan/temporary cap fills. The shoulder profile and some support spacing remain visual estimates, so this is a completed learning reproduction, not a claim of exact dimensional identity. No temporary review settings were saved over the user's working setup.

Reusable lessons: construct the continuous sloped opening before repeating it; retain the blind floor; support narrow concave and convex transitions separately; check the unsubdivided silhouette before smoothing; distinguish render artifacts/flat facets from actual gaps using additional views and geometric checks.
