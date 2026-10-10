# CRNT DESIGNERS study selection

## Current exercise status - 9 October 2026

This table is the current status; chronological observations below are historical.

| Exercise | Current result | Status |
|---|---|---|
| Bracket | [Files and notes](bracket/README.md) | Study pass closed |
| Mechanical mount | Retired at user request | Deleted; do not restore |
| Multi-hole panel | [Files and notes](panel/README.md) | Reviewed, including shape correction |
| Pipe fitting | [Files and notes](pipe/README.md) | Study pass closed; documented triangles |
| Recessed cover | [Files and notes](cover/README.md) | Study pass closed |
| Slotted panel | [Files and notes](slotted-panel/README.md) | First reproduction reviewed |
| Mechanical joint | [Files and notes](mechanical-joint/README.md) | Axle circularity corrected and rechecked |
| Cylindrical design | [Files and notes](cylindrical-design/README.md) | Assembly built; final reference refinement pending |
| Complex mechanical part | Source frames retained | Critical shading comparison pending |
| Gear | Source frames retained | Reproduction pending |

[Transferable lessons](LEARNINGS.md). Each exercise keeps one current `.blend`, its `build.py` entry point, supporting `source/` scripts, `review/` images and validation reports. Shared tutorial frames stay under `frames/<video-id>/`, metadata under `videos/`, and all tutorial MP4s stay together in `../../vids/`.


Requested 8 October 2026. [Channel](https://www.youtube.com/@CRNTDESIGNERS/videos).
The newest 36 entries were retrieved in channel order and all 36 thumbnails inspected. Eight distinct exercises were selected and downloaded locally at up to 1080p, with metadata. These are a curated initial set, not a ranking of the entire channel.

## Selected tutorials, newest first

| Latest-list position | Video / local ID | Length | Reason to retain |
|---|---|---|---|
| 1 | [Complex mechanical part](https://www.youtube.com/watch?v=tHwIDGy4dcM) | 4:10 | Two differently oriented bosses meeting a rounded housing; inspect the crown junction critically |
| 2 | [Mechanical bracket](https://www.youtube.com/watch?v=Fy7iJNiJhlo) | 5:11 | Continuous upright/base connection, fillets, symmetry and mounting holes |
| 3 | [Clean mechanical mount](https://www.youtube.com/watch?v=uExiZMG1Ptk) | 6:00 | Aperture, sloping floor, base profile and connected housing; closely relevant to earlier shape/flow failures |
| 9 | [Hard-surface panel with clean topology](https://www.youtube.com/watch?v=Xbp8s_I_1gc) | 5:33 | Multiple adjacent circular details and rectangular recess, planned together |
| 26 | [Complex pipe fitting](https://www.youtube.com/watch?v=MDnNrsJeHbQ) | 4:32 | Cylinder intersection with inner wall and flared base; compare with Frank Polygon's segment matching |
| 33 | [Cylindrical design](https://www.youtube.com/watch?v=x9rApivNiGE) | 5:11 | Derive curved panels from a parent cylinder, thickness, repetition and inset detail |
| 34 | [Hard surface modeling with clean topology — recessed cover](https://www.youtube.com/watch?v=BnP1U8Y10QA) | 4:26 | Stepped rim and seated corner recesses; useful for panel/button seating mistakes |
| 35 | [Gear modeling](https://www.youtube.com/watch?v=vG__QhK7dvM) | 5:41 | Repeated radial topology and spoke/rim junctions; lower priority than housing/holes |

Videos: `../../vids/CRNT - NN - Title [ID].mp4` (numbered in study order). Metadata: `videos/<ID>.info.json`. Selection inventory: `latest-36.json`; thumbnails: `catalog/`.
Not downloaded: the other 28 entries. This avoids many similar junction/plate examples while retaining a distinct radial-repetition lesson. Trim-sheet, textured sci-fi assembly and twisted nail examples have lower relevance to the current modeling problems.

## Actual first-pass coverage

All eight have been visually inspected in timeline contact sheets at 12-second intervals starting at 00:03, plus a near-end frame. Counts: complex part 22; bracket 27; mount 31; panel 29; fitting 24; cylindrical design 27; cover 23; gear 30. Total 213 sampled frames. The exact seconds are stored in each `frames/<ID>/coverage.json`.

This is a selection/sequence analysis, NOT continuous playback, complete operation tracing, audio review, or successful reproduction. No English subtitles were available through the downloader. Fast edits, exact vertex selections and hidden-side connectivity require closer inspection. An absence of captions does not establish an absence of narration.

## Observations and tests to perform

### Bracket — first reproduction priority
00:03–00:51: scale the base, derive the arch from a cylinder, extend its lower sides, and combine with the base using a Boolean union. 01:03–01:27: remove redundant regions and mirror the upright. 01:39–02:15: introduce the shared hole and connect its border to the surrounding geometry. 02:27–03:27: shape the root fillet, clean side flow and support the perimeter. 03:39–04:39: repeat symmetrically and construct the mounting hole from the base. 04:51–05:09: subdivision and shaded/cage inspection.

Test: prove connected components and welded seams after union/cleanup; keep hole concentricity and root thickness consistent. The visible sequence makes clear that merely overlapping an arch on a plate is not the intended end state. Dense review needed around 00:45–01:20 and 01:51–02:51.

### Mechanical mount
00:03–00:39: establish the block profile, incline and taper. 00:51–01:27: build the upper border and Boolean aperture. 01:39–02:51: merge cleanup and side support around the floor transition. 03:03–04:39: reconcile front/rear border loops and bottom/side edges. 04:51–05:39: add surface resolution and the circular recess. Final 05:51–05:57 shows the resulting form.

Test: compare front, side and underside BEFORE SubD; inspect thickness through the aperture and floor bend. Do not copy the final wire density onto an inaccurate blockout. Exact cleanup sequence remains pending.

### Multi-hole panel
00:03–01:39: shape the bent sheet and lay out five circular features plus the rectangular feature before local cleanup. 01:51–02:51: connect the intervening planar regions and establish circular borders. 03:03–03:51: create circular depth and support. 04:03–05:15: establish rectangular detail, reconcile the rear surface and bent perimeter. 05:27–05:30: base/evaluated views.

Test: use a small three-hole transfer with different spacing. Avoid copying the old failed spiral/fan rings. Adjacent features determine the connecting strips. Verify coplanarity and nonintersecting loops; the final wire image alone does not certify shading.

### Pipe fitting
00:03–00:27: cylinder with widened filleted base. 00:39–01:03: introduce transverse branch and union. 01:15–02:03: reconcile branch intersection with parent strips and add local support. 02:15–03:15: open the tube and route interior faces, working on a half. 03:27–03:39: smoothing and symmetry. 03:51–04:29: create flange holes and support their boundaries.

Test: inspect outer AND inner intersection; matching outer loops alone can leave internal obstructions. Compare parent-cylinder curvature near the branch under a broad highlight. This is an art-modeling topology study, not engineering verification.

### Recessed cover
00:03–01:03: establish stepped profile with extrusions and bevels. 01:15–02:15: cut a corner recess and repair/support its boundary. 02:27–03:03: inset/extrude a seated concentric bottom feature. 03:15–03:51: symmetry, planar face filling and border support. 04:03–04:24: underside/final surface inspection.

Test: distinguish a recess's continuous floor/sidewall from a separate fastener. Copy the depth sequence, not a floating circle. Some cap regions are not demonstrated as all-quads; adapt only after confirming the source's intended shape and connection.

### Cylindrical design
00:03–00:27: cut a panel from the curved parent. 00:39–01:51: form corner details and panel border while retaining that curvature. 02:03–03:27: move origin and repeat panels around the cylinder and along its length. 03:39–04:27: add middle-band details. 04:39–05:08: end rim and interior treatment.

Test: compare extracted panel against parent radius before/after smoothing and thickness. Check gaps between distinct panels rather than welding every physical seam. Small circular caps visibly use a fan in some samples; this is not a template for all-quad project caps.

### Complex mechanical part
00:03–01:03: arch profile, crossing cylinders and base. 01:15–02:15: large bore/rim and front-face connection. 02:27–02:51: smaller boss connection cleanup. 03:03–03:39: smooth preview, small bore and border treatment. 03:51–04:08: base support and finished views.

Concern: at 03:03 and the upper view at 04:03, a dent-like highlight appears near the small boss/crown transition. It needs close inspection and a reproduction test, not automatic acceptance because the thumbnail looks clean. Keep as a critical comparison after the simpler bracket/fitting.

### Gear
00:03–00:27: generated toothed ring and filled center. 00:39–01:39: spoke layout and openings. 01:51–03:15: cleanup and rounded spoke junctions. 03:27–03:39: central hub and bore. 03:51–05:15: work on a sector, route teeth/rim and restore symmetry. 05:27–05:39: subdivision result.

Test: validate the sector seam and repeated spacing. The generated gear operation is a starting primitive, not evidence of engineered tooth accuracy. Do not transfer the very dense rim into unrelated circular caps.

## Closer bracket junction review - 8 October

Inspected all 51 targeted frames at two-second intervals across 00:44-01:20 and 01:50-02:52. This is closer visual evidence, not continuous playback or a finished reproduction.

- 00:50-00:56: Boolean union is applied, then the redundant operand deleted. Subsequent edit-mode work acts on the combined upright/base surface.
- 00:58-01:18: cuts and dissolves simplify the intersection and establish useful base divisions. Do not preserve Boolean slivers as support geometry.
- 01:54-02:02: selected faces are removed, vertices merged by distance, and the upper annular region filled with radial connections. Large planar regions remain temporarily; intermediate topology is not the final cage.
- 02:04-02:08: bevel the shared upright/base root to establish the fillet before routing lower hole connections.
- 02:10-02:30: construct connections down from the circular boundary into the fillet/base. These are deliberate edits, not one automatic fill.
- 02:32-02:40: inspect the side profile and dissolve redundant connections. At 02:42-02:52, a thickness-direction cut and symmetry operations restore the other root side.

Transfer principle: establish a continuous root and its radius first, then route the hole boundary into that surface. Preserve useful continuous strips. A single object or clean front view does not prove welded seams, correct inner walls or sound underside topology.

Follow-up: all 57 additional frames at three-second intervals across 01:20-01:50 and 02:53-05:08 inspected. The upright bore is cut with one cylinder spanning both uprights (01:32-01:50). The perimeter is beveled after root cleanup (03:05-03:17), then hole-rim and underside support are added (03:26-03:38). The mounting region is extended and divided (03:50-04:17), inset and circularized from the existing sheet (04:20-04:26), opened and bridged through its thickness (04:29-04:32), then shaped and supported as a countersink (04:35-04:41). Subdivision is inspected near 04:53-05:08.

This corrects the broad first-pass timing above: the shared bore starts earlier than 01:39, and mounting-hole construction is specifically around 04:20 onward. Exact hidden selections between samples remain uncertain. All of these are sampled visual observations, not a claim of continuous playback or audio review.

Practical transfer: [hole-to-root surface study](practice/README.md), followed by the [solid bracket base checkpoint](bracket/README.md). The latter includes joined uprights/base and through countersinks, with corrected root-side patches. Neither is an exact keystroke reproduction. Reference measurements, subdivision support and final shading remain pending.

## Study order
Bracket → mount → multi-hole panel → pipe fitting → recessed cover → cylindrical panel → complex part defect comparison → gear.
Follow each with a small reconstruction, then a controlled variation and shaded/base/evaluated checks. Current status: selected/downloaded and first-pass analysis; these new tutorials have not yet been reproduced.

Current override: mount retired and all dedicated files plus its video deleted at user direction. Panel (Xbp8s_I_1gc) is active. Historical selection/coverage above does not describe the current retained inventory.

Latest status: panel study pass complete with reviewed base and evaluated mesh; pipe fitting MDnNrsJeHbQ now active. See panel/README.md for corrected blind-recess and downward-extension observations.

## Latest status - 2026-10-08

Pipe fitting study pass is closed; source and result are synchronized in `pipe/`. It includes the flared base, two connected mirrored branches, internal bore junctions and four blind flange recesses. Mostly quads, with 20 base triangles retained; see pipe/README.md for honest coverage and dimensional limitations. Next: recessed cover (BnP1U8Y10QA).
