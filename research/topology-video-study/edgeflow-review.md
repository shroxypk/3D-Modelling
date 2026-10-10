# Edge flow revisit — 3 October 2026

**Current model state after the requested fresh start:** the housing has been generated afresh with regular barrel/side strips and a contour-directed window, without the previously overapplied diamond reductions. The 200-vertex / 200-quad cage is closed, has no detected concave/degenerate faces or self/hood intersections, and all other mesh geometry/transforms are unchanged. Rear, side and oblique views were inspected. Subdivision is disabled. This is an intermediate shape cage, with transition shaping, lens seating and edge softness unfinished. The 282-vertex reduction pass discussed below is historical and superseded.

**Latest user correction:** the reduction technique was overapplied. Continuous regular topology can be the better choice when it causes no shading or edge-flow problems. The housing's reduced count is not proof of an improvement; extra poles and redirection carry their own costs. Do not propagate the pattern to other parts by default. Compare alternatives based on shape, shading and editability, and leave sound geometry alone.

The current holosight housing is rejected. An all-quad count and clean manifold audit do not establish good flow, density, shape or shading. No holosight geometry was modified during this study, and its subdivision modifiers remain disabled.

## Actual source coverage

- **Understanding Topology and Edge Flow in 3D Modeling — On Mars 3D:** all nine contact sheets inspected (51 frames at 30-second intervals, 00:45–25:45); 06:15 enlarged to trace the diamond reduction. The full automatic local transcript was read through its end at 26:15. This is sampled visual analysis plus full narration coverage, not continuous playback or reproduction of every operation.
- **Topology Study / How to Get a Flawless Edge Flow — Thomas Colin 3D:** all seven contact sheets inspected (37 frames, 00:45–18:45). Enlarged 05:15, 07:15, 13:15 and 17:15 to compare connections and spacing around a hole and outside notch. No complete transcript or full reconstruction of his multi-hole plate is claimed.

## What the demonstrations change in the work

1. Identify the feature contours before filling the surrounding surface. Thomas preserves the circular openings and routes nearby quads around them, then connects those bands to the planar field. Filling everything with a global grid first leaves unnecessary edges and awkward transitions.
2. A change of density is a deliberate local patch. The On Mars diamond turns two strips back locally using a three-edge/five-edge pole pair. It is not a license to collapse many lines into a single fan.
3. Placement matters as much as connectivity. Thomas slides vertices and reroutes connections near the hole/notch; the eventual border support is separate from that broad field. Keep reductions on planar regions with space around them, away from the housing's curved shoulder and narrow fillet.
4. Curvature needs regular spacing. In the On Mars cylinder example, end supports are followed by three intermediate axial cuts to improve the subdivision distribution (about 15:58–16:16). Sparseness does not mean removing every intermediate loop: keep loops that control actual form or its subdivision behavior. A battery barrel needs circumferential shape segments; its neighboring flat wall does not automatically need the same rows everywhere.
5. Support bands follow the intended edge and softness after the form is established. Avoid stacking equally tight rings around the window simply to make the result look finished.
6. The narration explicitly permits a triangle on a suitable flat hard-surface region (around 17:05–17:31). The user's all-quad target is a project requirement, not a universal rule taught by the video. Meet it with planned patches rather than arbitrary extra cuts. The final recommendation is to practice retopology over an established shape so that connectivity can be solved without simultaneously guessing the form.

## Practical checks completed

`edgeflow-on-mars/routing-study.blend` is a normalized reconstruction of the local diamond motif visible around 06:15, not a copy of the entire tutorial asset. It reduces four strips to two. It contains 29 vertices / 19 quads, no concave faces, and exactly one internal three-edge and one internal five-edge pole. Its minimum quad corner angle is about 53 degrees. The saved preview was inspected. No subdivision was used. This validates the connectivity of this planar patch only; it does not validate the holosight or its shading.

The installed EdgeFlow geometric implementation was also tested on an isolated cylinder patch with an incorrectly inset middle loop. It reduced maximum selected radial error from 0.06 to about 0.000592 units, left unselected vertices unchanged, and preserved all vertex/edge/face counts. This demonstrates curvature interpolation, not topology repair. EdgeFlowDraw is installed too; its interactive drawing behavior was not tested.

## Housing application and remaining work

- Establish the window, roof/shoulder and battery cross-section before support loops.
- Keep regular strips on the barrel, and contour-following bands around the window.
- Route excess barrel rows into the planar side with localized reductions. Do not put their poles on the barrel-to-window shoulder. Check the available space before copying the diamond pattern; it is one possible transition, not a universal solution.
- Remove the current global depth interpolation as the default topology strategy. Plan each surface region and its boundary counts explicitly.
- Check front, rear, side and oblique cage views before adding sharpness control. Preserve part boundaries and the original file.
- The housing has now been replaced with an initial shape cage using local side reductions (see continuation below). Its support spacing and shading remain unverified. Do not mark it accepted because a numeric audit passes.

## Additional local-video review — 4 October 2026

Two topology-related recordings added to `Downloads/vids` were visually sampled across their full timelines after TubeAlfred returned an `insufficient_credits` response. Frame intervals and source names are retained in `sample-index.json`; the contact sheets are the review artifact. No transcript was available for either recording, so narration is not claimed as reviewed.

- **Blender beginners: Topology and Edge Flow (E05):** inspected 54 frames at 60-second intervals from 01:00 through 54:00. The full visual arc includes low-resolution shape and subdivision tests; topology traced over orthographic references; localized layout around an opening/curved feature; and a helmet-like form with a brow opening built from quad strips. The takeaway is to establish the large silhouette first, use a reference to plan the primary flow, and make local patches serve a visible form change rather than extending cuts across every flat area. The prior corner-panel and flared-stem reconstructions remain separate targeted studies; this sampled pass is not an exact reproduction of the whole video.
- **Edge Flow And Topology:** inspected 38 frames at 30-second intervals from 00:30 through 19:00. The author draws guide lines over a side-view car reference, then builds body panels from planes and positioned edge rows, checking the side/front references and adding a local loop with slide where the shape needs definition. The useful lesson is reference-led silhouette and panel planning, with a small number of meaningful longitudinal and crosswise rows. This is a car blockout lesson, not a focused demonstration of pole routing or Subdivision edge cases.

These additions bring the local non-holosight inventory to ten videos: six have their retained full local transcripts read with sampled visual sheets reviewed; the On Mars and Thomas Colin videos have full narration/visual-sample coverage as qualified above; E05 and Edge Flow And Topology have full-timeline visual samples but no available transcript. Sampling is not continuous playback, and a technical summary or small reconstruction does not prove complete mastery.

## Targeted web research and housing application

Read Frank Polygon's [cylinder/rectangle intersections and fillets](https://frankpolygon.artstation.com/blog/o7Pg/sub-d-modeling-cylinder-and-rectangle-intersections-fillets), plus the shape-first and curve-flow sections of his [Polycount sketchbook, page 3](https://polycount.com/discussion/221392/sketchbook-frank-polygon/p3). Visually inspected the diagrams `j21tzt9ypk8g.jpg` (raised rectangular feature on a rounded corner) and `9vot94vgddmi.jpg` (angled box joining a cylinder) in the browser. This was focused article/diagram research, not additional video playback or a review of the whole forum.

The useful guidance is to align intersecting shapes' segment spacing, retain the larger curve's geometry as support where appropriate, and solve the principal loop paths before sharpening. Extra edges should have a purpose; shape accuracy and smoothness cannot be inferred from quad counts.

Applied a local-density strategy to the main casting: eight battery arc segments, two spans on the front lower wall, and an eight-to-four-to-two reduction on each planar side. The window uses a single contour and a connected tunnel. Removed the old tightly stacked sharpening rings from this part. This is an adaptation to the existing holosight dimensions, not a reproduction of Frank's example.

Result: 282 vertices / 282 quad faces, one connected closed component; no concave faces, zero-area faces, self-intersections or hood intersections detected. Geometry and transforms of all 15 other mesh objects were unchanged. Subdivision remains off. Inspected side and oblique cage views. This is still an intermediate shape cage: refine the window-to-battery transition, edge softness and lens seating before the eventual shading assessment. The former 512-vertex cage was rejected; this replacement has not received user acceptance.
