# Blender work in this workspace

Use `tools/integrations/README.md` for the installed Blender workflow, startup and limitations.
BlendRelay is the primary MCP connection. Prefer scene/object inspection, selected mesh edits,
mesh validation and focused captures. Webita's connector is an installed, disabled fallback.
Do not launch the extensions' nested AI agents or upstream autonomous iteration controllers.

Follow the user's tutorial sequentially and compare against their supplied reference assets.
Preserve `M4A1/` as source/reference; the active modeled result is in `projects/m4a1-tutorial/`.
Match base silhouette, thickness, seating, depths and connected parts before adding subdivision.
Favor clear mostly-quad flow; use enough density for shape without gratuitous loops or forced terminations.
Use live Mirror where appropriate. A 16-sided circular base is preferred when sufficient.
One object containing disconnected islands is not proof of one continuous mesh.

Keep build source synchronized with accepted live changes before claiming completion.
Check both base meshes and evaluated modifiers. Open mirror/solidify boundaries in the base
mesh are not automatically defects. Quad counts and image metrics do not certify fidelity.
Inspect shaded and wireframe images plus side/front/rear views as appropriate; show the user
one model view and one topology view rather than duplicate images. Fix visible errors before
moving on. Never report an entire video watched or understood from sparse screenshots.
Keep one current output blend; do not make redundant variants or delete reference videos/assets.
Respect shell sandbox boundaries when using Blender code execution: no bypassing file permissions.
Preserve the user's saved startup scene/workspaces/settings in delivered blend files.
Do not save factory defaults or screenshot lighting over their working environment.
The current build edits the working scene without resetting settings. Review renders run
separately through `source/review_current.py` and never save their temporary overrides.
