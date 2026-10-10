# Current modeling state — 2026-10-07

Working output: M4A1.blend. Build source: source/build.py. Preserve the supplied M4A1/ folder and tutorial videos as read-only references. Keep only one current output blend. User scene/workspace settings are retained; review_current.py renders in a separate process without saving overrides.

## Priority correction: handguard, opening 10–13 minutes

User identified the selected handguard parts as inaccurate. Returned to extracted tutorial frames in chronological order, with closer checks around the side-strip cuts and body closure (including 06:05, 07:15, 08:05, 08:55, 09:15, 09:25, 09:45, 09:55, 10:00 and 10:05). This is frame-based visual review, not a claim that the full video was continuously watched. Read-only cross-section inspection of finished-reference Cube.001/002/003 corroborated construction already visible in the tutorial.

Corrected the previous mistaken thin-sheet construction:
- handguard_base.py builds filled upper/lower extrusions, with flat closing faces at the middle cut and closed ends. Live width Mirror, no Solidify or Subdivision.
- side_strip.py builds one width-spanning perforated component, with connected ribs and six through-openings. Removed the old inner backing sheets that produced two shallow disconnected plates. Live Mirror and selective rib-edge Bevel.
- tutorial_rails.py gives the upper rail tapered base/tooth shoulders instead of rectangular sides. Existing tooth layout retained.

Checked shaded and wireframe assembly plus orthographic side/front/rear views. All three corrected editable base meshes are quads. Base boundaries on mirrored parts lie only on the symmetry plane; no base edges have more than two incident faces. Evaluated corrected meshes have no boundary/nonmanifold edges or zero-area faces. The side-strip bevel creates non-quad corner faces; it is not claimed all-quad after evaluation. Full-width side strip is one connected component; the main body deliberately has two closed components (upper and lower), as shown at this stage. Validation counts do not certify exact visual fidelity.

Current model.png and topology.png show the corrected handguard; review/handguard-side.png, handguard-front.png and handguard-rear.png are supporting checks. Source and saved geometry synchronized. Live BlendRelay disconnected during the final read-only audit; no Blender window process remained. Final validation/metadata save completed headlessly in the working file without review overrides. Reconnect/reopen working file for further live edits.

## Tutorial stage, not finished-reference feature checklist

The user explicitly reminded us that the supplied finished blend contains features not reached yet. Use the current tutorial timestamp to decide which features belong now. Use the finished blend only to cross-check demonstrated proportions/construction; do not treat later vents, cuts or other details as current omissions. The rail already exists from the approximately 12:40–15:40 stage. Return to the stock sequence after this focused correction.

## Stock restart requested by the user

The user rejected the stock topology and explicitly requested a full stock restart. Deleted the previous collar, stock frame and lower ribbed trim from the working blend. Replaced stock_restart.py entirely; removed the rejected stock.py and stock_lower_trim.py implementations and obsolete stock audit scripts. No old stock mesh is retained as a hidden alternate.

Restarted from the tutorial's cylinder step and reviewed chronological frames around 16:00-18:40. Current accepted construction stops around 18:10: 16-sided front cylinder, cylinder-derived upper crown, side extrusion, thin lower lip, slanted rear extension with its demonstrated division, and successive rear perimeter extrusions. This is extracted-frame review, not continuous-video coverage.

Stock crown/frame has 22 base quads, 44 evaluated quads with live width Mirror, one connected component and no zero-area or appreciably warped faces. It is intentionally an OPEN surface at this tutorial stage, with 50 evaluated boundary edges; it is not a completed manifold stock. The collar has two planar n-gon caps, matching a primitive construction. Do not restore the deleted slot/web/trim implementation or old automated quad-transition layout. Continue the tutorial's underside/front return and perimeter operations sequentially.

Current source and M4A1.blend are synchronized. User working settings retained. Review camera/lighting changes remain separate and unsaved. The goal remains incomplete; the handguard and other previously existing parts are preserved.

## Restart continuation through approximately 23:30

Added the inward lip extrusion and front/rear return quads, then connected the inside perimeter across the mirrored width. Added three-segment corner rows through the rear band and inner bridge, following the demonstrated corner rounding around 21:40-22:50. Continued the transverse crown cut and front lower extrusion shown around 23:00-23:30. No rejected rear-hole, slot, web or trim mesh was restored, and no automatic quad-transition routine is used in this restart.

Current stock is 64 base quads / 128 evaluated quads, one connected component, no zero-area faces and maximum face warp about 2.4e-8. It remains an unfinished open surface: 64 evaluated boundary edges, not a manifold finished stock. Shaded, side wireframe, front and underside review images inspected. Current source, saved blend and previews synchronized; startup settings preserved. Next: follow the rear junction extrusion and inset operations around 24-26 minutes, examining intermediate frames before building the opening.

## Rear-junction preparation in progress

Reviewed closer five-to-ten-second source frames around 24:10-26:40. Added the rear inner bevel strip and began the connected rear-wall extrusion for the junction using mesh extrusion operations. Removed extrusion center-plane faces and leftover wire edges. Current extrusion is still a rectangular intermediate block: its upper attachment, corner shaping and inset do NOT yet match the demonstrated completed junction. Finish these before adding the circular opening or progressing to lower slots. Do not report this intermediate shape as reference-accurate or completed through 24:40.

Current stock: 91 base faces, 86 quads; 182 evaluated faces, 172 quads. One component, zero zero-area faces, max face warp 8.6e-7. The 70 evaluated nonmanifold edges are unfinished boundary edges; base has no edges with more than two faces. Five base non-quads are bevel termination faces, with explicit splits for warped faces. Shaded, wire and underside views inspected. Current code and saved blend synchronized. The upper junction gap visible in the review remains the next required correction, not an accepted final condition.
