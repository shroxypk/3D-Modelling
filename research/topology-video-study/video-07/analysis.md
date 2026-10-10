# Blender beginners: Topology and Edge Flow (E05)

Source file: `C:\Users\Dell\Downloads\vids\Blender beginners_ Topology and Edge Flow (E05).mp4`  
Public source: https://www.youtube.com/watch?v=Webfe2XvapY  
Creator: CG Krab. Duration: 54:02.40.  
Source chapter: **Corner topo example**, 24:00–26:08. The chapter list was verified from the local MP4 metadata and public YouTube chapter listing.

## Visual sample

The full timeline now has a visual sample of 54 frames at one-minute intervals, 01:00–54:00, arranged in `sheet-01.jpg` through `sheet-09.jpg`. Timestamps and sampling interval are in `sample-index.json`. The broader visual pass shows primitive/subdivision tests, layout traced over reference images, a curved panel with localized topology and a helmet-like form with an opening. `corner-topology-overview.jpg` and `next-chapter-overview.jpg` remain enlarged targeted samples for the two practice studies below. TubeAlfred could not provide a transcript because the account returned HTTP 402 (insufficient credits), so narration is unreviewed. This is timeline-spanning visual sampling, not continuous playback or full operation-by-operation analysis.

## Reproduction and judgment

`modeling/studies/study_e05_corner_panel.py` builds the visible form as one connected plate with a rounded-rectangle pocket. The 16-point loops follow the opening and cavity wall; a small number of local rows support the lip and outside edge. The floor and back use 5x5 quad patches. No extra loops cross the broad planar panel.

The base cage has 194 vertices, 384 edges, and 192 quads, with no loose vertices, boundary edges, nonmanifold edges, or zero-area faces. Level-2 Catmull–Clark evaluates to 3,074 vertices, 6,144 edges, and 3,072 quads, with the same closed/manifold/area checks. The smooth view preserves the shallow rounded recess, and the control cage exposes the local transition rows. This tests the chapter's visible result; the operation sequence and exact dimensions are not legible enough in the selected frames to claim an exact tutorial reproduction.

Review pair: `research/topology-study/e05-corner-panel-model.png` and `research/topology-study/e05-corner-panel-topology.png`.

## Second source-derived practice: cylindrical stem into a flared foot

The next sample uses four frames at 31:55, 32:30, 33:00, and 33:40, retained in `next-chapter-overview.jpg`. They show a tall cylindrical stem and a broad rounded foot/flange being developed, with a smooth result and the supporting cage. These images establish the demonstrated shape and the use of subdivision; they do not expose every edit or prove an exact operation sequence.

The Blender study in `../topology-study/e05-flared-cylinder.blend` reconstructs the rotational profile with 24 radial segments. It keeps long stem spacing open and adds rows around the flange rim and both profile transitions. The two planar ends use quad grids that match the circular boundary. The control cage has 434 vertices and 432 quads; level-2 Catmull–Clark yields 6,914 vertices and 6,912 quads. Both meshes are closed and have no loose vertices or zero-area faces. The render review uses one smooth model view and one actual low-density cage view, not wires from the subdivided result.

This demonstrates profile-loop placement and selective support density for a rotational form. It does not establish that the same cap layout or spacing is suitable for a curved Boolean intersection or the holosight.
