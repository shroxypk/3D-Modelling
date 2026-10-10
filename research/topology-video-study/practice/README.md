# Circular-detail test

Source: local `Hard Surface Detailing Made Easy _ Blender Tutorial.mp4`, 00:33–04:22. Complete retained transcript reread and all three overview sheets inspected in this renewed pass. The source compares a four-corner extrusion against a circularized eight-point region.

This exercise is a controlled adaptation, not a claim of pixel-exact reconstruction. The added 16-point case tests the user's preferred circular base. All cases use the same nominal radius 0.6, height 0.65 and two-segment support profile. Cap routing is explicitly generated as a quad grid. No disconnected cylinder is placed on top of the sheet.

Open [Practice.blend](Practice.blend). The three objects are ordered left to right: 4, 8, 16 boundary vertices. The source mesh is preserved under a live level-3 Subdivision modifier. Outer sheet boundaries are intentionally open. User startup workspaces/settings were loaded; temporary render cameras/lighting are not saved.

## Inspected result

Both [shaded](model.png) and [base cage](topology.png) images were inspected. All three are connected surfaces with no degenerate faces, internal nonmanifold edges or non-quad faces. The four-point example loses substantially more size and retains a less circular section. The eight-point case is close to circular but still shrinks. The sixteen-point version retains more of the specified radius.

| Boundary points | Base faces | Mean evaluated radius | Midwall radial range / mean |
|---|---:|---:|---:|
| 4 | 25 | 0.39285 | 3.169% |
| 8 | 52 | 0.54066 | 0.228% |
| 16 | 112 | 0.58464 | 0.036% |

Measurements use 720 horizontal rays at mid-height after level-3 subdivision. Full values and topology checks are in `validation.json`. They evaluate this cross-section only, not every rim/root highlight. The flat outer sheet's subdivision shape also changes with boundary density; this is not a controlled comparison of identical evaluated sheet silhouettes.

## Practical conclusion

Circularity and dimensional retention are separate checks. A nearly circular smoothed result can still be too small to seat correctly. More segments reduced both errors in this example, but this does not justify dense topology everywhere. For an intended fit, compare the evaluated radius and support profile against the target; do not infer accuracy from a clean quad count or smooth viewport. The four-point specimen is intentionally retained as a failure comparison, not an accepted part.

Unfinished: curved-parent transfer, local support-spacing variants, stronger reflection views, and independent manual reproduction without the source diagrams. No complete-video mastery is claimed.
