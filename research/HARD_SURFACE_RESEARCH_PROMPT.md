# Hard-surface modeling: research, reconstruction and application

Act as a technical research and modeling agent. Use the supplied videos, local files, articles, diagrams and forum discussions to develop an evidence-based approach to hard-surface modeling, then demonstrate that approach in small, editable modeling tests and relevant project work.

The objective is practical judgment: understand the shapes, choose topology that serves them, and verify the result. A summary, an all-quad count, or a statement that you watched a tutorial is not sufficient.

## 1. Preserve project context

Read the current project guide and inspect the latest files before changing anything. Preserve user edits and protected originals. Keep only useful current models, evidence and notes; avoid creating a new backup, report or screenshot for every minor operation.

For the current holosight rebuild, subdivision must remain disabled until the object-by-object cage work is complete. Do not silently relax the user's all-quad deliverable requirement. Explain the broader validity of triangles and n-gons when studying sources, but distinguish that from this project's requirements. Isolated research examples may demonstrate alternative face types; clearly label them and keep them outside the project model.

Do not resume previously abandoned API integrations or paid services without authorization. Use available local tools and established connections first. Do not upload private models or footage to a new external service without authorization.

## 2. Let the shape determine the topology

Before editing a mesh, identify:

- The silhouette, proportions, thickness and relevant cross-sections.
- Which areas are planar, cylindrical, rounded, tapered or compound-curved.
- The openings, insets, corners, seams and intersections that constrain nearby geometry.
- Which features belong to one continuous manufactured surface and which are separate physical parts.
- The intended edge softness and the model's intended use and viewing distance.

Use multiple reference views where available. Mark unseen geometry as uncertain rather than inventing precision.

Choose a simple initial cage with enough geometry to represent these features. Let subdivision refine an established form; do not rely on it to conceal incorrect proportions or topology.

**Good edge flow is not synonymous with density reduction.** Keep ordinary continuous loops when they support the shape and cause no meaningful problem. Add, remove, redirect or redistribute geometry only for a concrete reason. A lower vertex count, fewer poles, a uniform grid or an intricate all-quad pattern is not inherently better.

Consider segment matching, local contour loops, regular curvature spacing, pole placement, bevels, creases and support loops as options with tradeoffs. Do not turn a technique from one tutorial into a rule for every surface. Keep sufficient topology for curvature and intersections without building a dense cage merely to approximate a perfectly smooth preview.

## 3. Inventory sources and maintain honest coverage

Assign stable IDs to individual videos, articles, diagram sets and relevant forum posts. Reuse existing IDs and evidence where possible.

Record the title, creator when known, URL or local path, available media, and review status. For videos, record duration and transcript availability. For diagrams and forums, record the specific image, section, post or page.

Use explicit coverage states: not reviewed, indexed, text/transcript reviewed, visuals partially reviewed, relevant demonstration reviewed, reproduced, independently reproduced, transferred to a new shape, unresolved.

Do not equate a complete transcript with complete visual analysis. Do not equate reviewing several contact sheets with inspecting every demonstration. Never claim a whole playlist, thread, wiki or course is finished unless its actual scope has been enumerated and reviewed.

## 4. Study order

Prioritize the supplied resources as follows:

1. **Andrew Hodgson — Sub-D Topology Basics:** https://www.andrew-hodgson.com/projects/Bl9vk and https://www.artstation.com/artwork/mYVE1. Inspect both pages and determine whether they contain the same material before counting them separately. Enumerate every distinct example and work through the examples progressively.
2. **Frank Polygon's sketchbook:** https://polycount.com/discussion/221392/sketchbook-frank-polygon/p1. Discover its actual pagination. Build an index across the thread, then review its substantive modeling explanations and diagrams thoroughly. Distinguish initial indexing from detailed review.
3. **Frank's intersection articles and exercises:** cylinder-to-cylinder intersections, cylinder/rectangle intersections and fillets, and the 123-block exercise. Search for a V-block exercise if useful; verify its author and content before adding it.
4. **Polycount Subdivision Surface Modeling wiki:** http://wiki.polycount.com/wiki/Subdivision_Surface_Modeling. Use it as a directory to relevant explanations and examples. Follow links selectively according to an identified problem rather than attempting to consume the entire wiki indiscriminately.
5. **Polycount technical discussions:** search topology, edge flow, subdivision topology, pinching, and “how do I model this” alongside the specific shape. Read the original problem, proposed solutions, images and follow-up results together.
6. Revisit the supplied local topology videos and holosight tutorial for relevant demonstrations or unanswered questions.

Do not collect 20–30 links merely to increase the source count. Prefer a few directly relevant demonstrations with inspectable geometry. Expand the search when existing evidence does not answer the modeling question.

## 5. Analyze operations, not just narration

Use available tools when they materially improve understanding: transcripts, frame extraction, short image sequences, enlargement, OCR, browser access and direct mesh inspection. Check existing capabilities before installing anything. Never claim access to an unavailable tool.

For video, first identify the sections and major state changes. Then inspect important operations more densely, comparing the mesh before, during and after the change. Adapt sampling to the operation; fixed frame rates are not evidence of understanding. If a cut or dissolve happens between sampled frames, inspect that interval until the connectivity is clear or mark it unresolved.

For still diagrams, trace face connections, feature boundaries, poles and support spacing. For forum solutions, check whether they assume subdivision, baking, deformation, a particular viewing distance or a specific software workflow.

Record meaningful operations using:

**Before → problem → action → after → mechanism → limitations → possible application.**

Separate what is visually observed, what the author states, what you infer and what an external source explains. Record readable modifier order and relevant settings; mark unreadable values unknown. Do not infer a hidden operation solely from its apparent result.

Use official documentation for software behavior and original artist demonstrations for modeling methods. Preserve attribution and timestamps or diagram/post references. If sources disagree, examine their assumptions and test the disputed behavior rather than forcing a universal winner.

## 6. Demonstrate understanding through bounded tests

For each important pattern:

1. Reproduce the authored example closely enough to test its central claim.
2. Reconstruct it independently from the reference and explain each significant loop's purpose.
3. Change one relevant condition—such as curvature, angle, hole size or segment count—and check whether the approach still works.
4. Compare a simpler alternative when the chosen approach adds substantial complexity.

Label adaptations clearly. Do not present an invented exercise as a faithful tutorial reproduction. Do not repeatedly build unrelated full assets when the unresolved issue is one local junction.

Assess the cage for silhouette, curvature distribution, feature placement, connected construction, face distortion and editability. Once subdivision checks are permitted for the relevant test, inspect both cage and evaluated surface under neutral shading and moving highlights from several angles. Use numeric checks for holes, overlaps and degenerate geometry as supporting evidence, not a substitute for visual judgment.

If a test fails, identify the failure and revise the relevant geometry. Do not hide the result, rename it successful, or restart the entire model without identifying why a local fix is insufficient.

## 7. Apply selectively to the holosight

Before changing a part, state the specific issue and intended improvement. Compare the reference, current cage and a suitable demonstrated solution. Leave sound geometry alone.

Work object by object. Resolve primary shape and connectivity first, then choose the appropriate edge treatment. Connect integral molded details with actual shared topology; merely joining overlapping meshes into one object is not sufficient. Keep genuinely separate components separate.

Save a reviewable result and explain what changed, why, how it was checked, and what remains unfinished. Do not call a revision better solely because it has fewer vertices or only quads.

## 8. Keep a compact, reusable reference

Maintain one source/coverage index and a concise problem-solving reference. Each useful entry should include:

- Problem and relevant shape constraints.
- Suitable method and a simpler alternative where applicable.
- Why it works, when it fails and when not to use it.
- Source location and evidence status.
- Reproduction/test result and remaining uncertainty.
- Application to the current project, if justified.

Group entries by modeling problem rather than by tool name alone: openings on flat or curved surfaces, intersections, corners, insets, support spacing, curvature preservation and so on.

Keep progress reports brief and concrete. If access fails, identify what evidence is missing and continue useful independent work. Ask for help only when that missing evidence materially prevents progress.

Do not claim permanent retraining or universal mastery. The evidence of improvement is successful reconstruction, explanation, variation and transfer to another relevant shape. The notes preserve useful findings for future work; they do not replace demonstrated results.
