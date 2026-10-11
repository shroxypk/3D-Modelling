# Holosight case study — 11 October 2026

**Outcome: Needs revision.** The first local correction is verified; neither the full asset nor the current tutorial stage has final visual acceptance.

## Scope and progression

Finish this Holosight as the first documented end-to-end case study. Follow the supplied tutorial in sequence, matching form and intended connectivity before finishing. Establish reproducible construction and visual approval here before testing reusable inspection, validation and review operations on a second structurally different asset. No general asset generator is being built.

Game-ready delivery is a later gate: choose target engine/use, scale, UV/material requirements and performance budget when relevant, then verify the actual exported file in the target engine. This checkpoint is not export-ready and has no new polygon or UV targets imposed.

## Baseline and preservation

- Starting branch: `main`, clean working tree at `4e55656c10c9d9056e7b309c7e285d9e910ecab4`, matching the published GitHub checkpoint. That commit is the reversible before-state; no duplicate blend was created.
- Working file: `Holosight.blend`, last saved 9 October before this edit. No running Blender process or connected BlendRelay session was found at audit time. No unsaved live scene was replaced.
- Blender 5.2.1 LTS opened the saved file in separate background processes. Full constructors were read but not executed. No whole-project regeneration was used to inspect the model.
- [Baseline audit](review/case-study/baseline-audit.json) records the blend and source SHA-256 hashes, mesh fingerprints, base/evaluated measurements and modifiers.
- [Before surface](review/case-study/before-model.png) and [before topology](review/case-study/before-topology.png) preserve the cap comparison. Other before-state renders remain recoverable from the baseline Git commit.
- The saved file and sources matched their committed bytes. That establishes no subsequent disk changes, **not** exact source-rebuild equivalence. Historical synchronization claims remain unverified until a separate reconstruction comparison is performed.

## Ranked diagnosis

| Priority | Finding and evidence | Status / next treatment |
|---|---|---|
| 1 | Cap front contains narrow triangle fans where the oblique slot intersects the grid. Visible in the before wire image; `slot.py` triangulates Boolean n-gons. The sampled tutorial frame at 52:00 uses broad flat faces alongside the slot, rather than this grid. This is evidence of a construction difference, not proof that every triangle causes shading failure. | Partially improved by the local correction below. Remaining slot-end slivers need a focused routing decision against the tutorial. |
| 2 | Long thin strips cross the shoulder. The profile wire view and explicit housing rows confirm them. | Unresolved. First test their actual surface/finishing behavior; do not dissolve shape-defining rows on curved transitions just to reduce counts. |
| 3 | Hood and nose are visibly faceted. The scene audit finds flat-shaded faces and no housing finishing modifiers. | Finishing remains pending at this stage. Faceting is not by itself evidence of broken normals. Reflection and finished-edge checks have not been performed. |
| 4 | Underside no longer exhibits the previously described cross-width twist in the inspected shaded view. Glass spacing and exact overall reference proportions still require a matched-view check. | Provisional visual observation only; no global intersection or reference-fit certification. |

Only the existing tutorial frame at 52:00 was revisited in this pass. No claim of continuous viewing, a newly completed episode, or exact dimensional fidelity is made. The displayed tutorial bevel value may be a modal intermediate; it is not sufficient evidence to change the modeled bevel width blindly.

## Small correction performed

Removed **14 internal diagonals** between coplanar cap-face triangle pairs that form convex quads. Only the housing object `02 | Inner housing` changed. No vertex moved; no slot width, depth, angle, lip, tooth, rim, shoulder or silhouette was redesigned. Materials and smoothing flags must agree for eligible pairs.

`source/refine_cap.py` implements the local operation. `source/slot.py` calls it after its existing slot construction, so the source records the same incremental correction applied to the saved scene. This synchronizes this delta; it does not prove the entire constructor reproduces all existing geometry. The correction was tested without saving, reviewed, then applied to the original unchanged baseline file with a hash guard. The saved project was reopened successfully.

## Verification actually run

- Blender dry run: unchanged vertex positions, unchanged faces outside the cap-front plane, preserved surface area within the stated floating-point tolerance, no change to nonmanifold count, no collapsed faces introduced.
- Second application made zero edits: local operation is idempotent on this checkpoint. Full-build determinism remains untested.
- Fresh saved-file audit and existing validation both succeeded. Housing: **1,071 faces = 990 quads + 69 triangles + 12 n-gons**, one evaluated component, zero nonmanifold edges, zero loose geometry, zero faces below the existing 1e-10 area threshold. Before: 1,085 faces = 976 quads + 97 triangles + 12 n-gons.
- Hood, rail and both panes have exactly unchanged base-mesh fingerprints and modifier inventories. The housing's modifier inventory is also unchanged.
- Review captures regenerated in Blender: three-quarter model/topology, side, front, top model/topology, isolated housing/shoulder, cap and underside. Top captures were added to the existing review script.
- Before/after cap shaded renders are pixel-identical at the same camera/settings. The wireframe shows fewer diagonals. This establishes no regression in this view, not approval under every lighting condition.
- The saved blend hash was unchanged by the review process. Temporary camera, lighting and wire overlays were not saved over the working environment.

See [current audit](review/audit.json), [validation](validation.json), and [dry-run check](review/case-study/refinement-check.json). Raw face/edge minima are measurements, not universal failure thresholds. Intersection detection, duplicate-surface checks, reflective shading, materials, UVs and engine import remain outside the checks completed here.

## Acceptance gates

1. **Current cap/shoulder checkpoint:** matched tutorial views, remaining sliver diagnosis, no unintended silhouette or shading changes; record Pass, Pass with notes, Needs revision or Blocked. Current outcome remains Needs revision.
2. **Sequential tutorial completion:** finish each actual feature and its connectivity; keep source and saved edits synchronized. Do not treat the rail placeholder as a final mount.
3. **Repeatability:** reproduce the accepted model in an isolated process, compare object/mesh/modifier state and matched renders, then verify save/reopen. Preserve the working file throughout.
4. **Final asset review:** intended form, materials and finishing accepted against supplied references. Only then establish and verify the required game-engine delivery settings.
5. **Transfer test:** use a second structurally different asset to determine which review/validation operations deserve reuse. Asset-specific constructors remain separate.

**Single next action:** inspect the remaining slot-end junctions against the next consecutive tutorial frames, then choose a local layout that preserves the cap contour and gives a clean, editable slot boundary. Do not proceed to later features until this checkpoint has a documented visual decision.
