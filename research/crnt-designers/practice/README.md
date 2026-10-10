# Connected hole-to-root study

Source: CRNT DESIGNERS Mechanical Bracket, especially 02:04-03:38. This is an isolated surface adaptation of the routing principle, not the complete solid bracket or an exact procedural reproduction.

Open [RootStudy.blend](RootStudy.blend). Left: one straight root segment. Right: four segments on the same nominal radius-0.4 quarter-circle. Both use identical 24-point hole boundaries, annular connections, overall nominal dimensions and level-2 subdivision. Hole boundaries remain connected to the upright and six strips continue through the root to the base. Live Solidify supplies test-sheet thickness after subdivision; this differs from the tutorial's modeled solid volume. The initial base is intentionally an open surface.

## Inspected evidence

The [shaded view](model.png) and [base topology](topology.png) were visually inspected. The one-segment control retains a broad chamfer-like region and abrupt highlight transitions. Four root segments produce a more continuous curved transition. More segments here serve an actual radius, not arbitrary density. These images do not certify exact reference fidelity, all viewing angles or absence of every local shading issue.

Both base surfaces are one connected component, entirely quads, with no degenerate faces or internal nonmanifold edges. After subdivision and thickness, both have zero nonmanifold edges and zero degenerate faces. Details are in [validation.json](validation.json). These checks do not establish absence of self-intersections or correct dimensions.

The build also samples the subdivided midline against the intended quarter-circle before thickness. This is a vertex-sample measurement, not a continuous maximum-error bound. It distinguishes smoother appearance from actual radius retention.

For nominal radius 0.4, the maximum sampled absolute radius error was 0.11927 (29.8%, five midline samples) with one root segment and 0.01017 (2.54%, eleven samples) with four. Sampling density differs because the base meshes differ; neither number is a certified continuous-surface bound.

Saved workspaces/settings originate from the user's startup file. Review cameras and lighting run separately and are not saved into the working blend.

## Remaining work

Reconstruct the full solid bracket with its shared bore, root side patches, mounting-hole countersinks and symmetry. Match proportions against source views. This coupon does not replace those steps. Test the final solid from front, side, underside and under stronger reflections before accepting it.
