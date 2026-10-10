# Bracket exercise: completed learning pass

Source: https://www.youtube.com/watch?v=Fy7iJNiJhlo . Current output: [Bracket.blend](Bracket.blend).

Completed as a topology learning exercise, not a dimension-certified replica. The solid has two aligned upright bores, welded symmetry, connected root fillets and two through countersinks. The source sequence was visually sampled and traced; full continuous playback and narration are not claimed. The reconstruction uses planned patches rather than duplicating every Boolean keystroke.

Top-view comparison at 04:56 prompted corrections to base length, upright thickness and hole placement. The normalized base length/width ratio is now 4.36. The working modifiers are Mirror, Bevel and level-2 Subdivision. Startup workspaces are preserved; review overrides are never saved into the model.

## Verified

Inspected shaded, cage, top, side, underside and metallic reflection views. The reflection check shows continuous broad highlights across the arch and root without the former side wedges. This does not establish flawless shading from every angle.

The editable half has 380 faces: 364 quads and 16 triangles confined to planar root-side patches. Those triangles replaced forced concave quads that pinched under subdivision. After Mirror the solid is one connected component, with no boundaries, internal nonmanifold edges or degenerate faces. The fully evaluated mesh passes the same integrity checks. See validation.json.

360 radial rays per sampled cross-section give upright mean radius 0.52393 against nominal 0.53, and mounting-hole mean radius 0.33602 against nominal 0.34: about 1.2% shrinkage. Both upright centerlines and mounting-hole centerlines remain unobstructed. See fit-check.json. These are sampled sections, not engineering tolerances or complete collision verification.

## Lessons and limits

Manifoldness and quad counts did not catch the original folded concave patches; visual review did. Preserve actual curved profiles, measure evaluated fit, and allow limited planar triangles when forced quads damage the result. The approximate dimensions and remaining shrinkage are recorded rather than spending further passes polishing this exercise. Move on to the mechanical mount.
