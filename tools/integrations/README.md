# Installed Blender workflow

Configured and tested 2026-10-07 with Blender 5.2.1 on Windows.

## Active components

- **BlendRelay 0.7.3** is the primary Codex MCP, named `blendrelay`. Provides scene/object
  inspection, selected mesh edits, geometry checks, focused views, materials/modifiers and
  Python operations. Installed in Blender's user extensions. The local runtime uses
  loopback authentication and `relay-data/`; never publish its connection credentials.
- **Webita blender-codex-mcp 1.5.5** is installed and tested, but its Codex `blender` entry is
  disabled to avoid duplicate active toolsets. Telemetry is disabled in both Codex environment
  and Blender preferences. Optional online services are off. Its bridge uses localhost:9876.
- **Codex-and-Blender** supplies the actual `deterministic_review` implementation used by
  `review_project.py` to check shaded, topology and side images. Durable build source and
  visual review are adopted; the demo scene and nested agent controller are not run.
- **blender_mcp_verifier / Blender Vision Critic** supplies its offline
  `check_scene_part_integrity` check. Tested against the current five-part checkpoint.
  Gemini image generation, VLM scoring and SigLIP downloads are NOT enabled. Name checks do
  not establish welded geometry or reference accuracy; those require direct mesh/visual checks.

## Use

Restart/reload Codex to expose the newly configured native MCP tools in future sessions.
The servers have already been tested through a real MCP client in this session.
Open Blender with `open-model.ps1` (optional `-BlendFile` path). It starts BlendRelay without
launching another AI agent or saving the scene. Codex starts the runtime on demand; allow
several seconds for Blender's reconnect timer. For an already-open unsaved scene, connect
the existing session instead of opening/replacing it. The custom runtime directory is
`C:/Users/Dell/Downloads/3D/tools/integrations/relay-data`.

Use `runtime/Scripts/python.exe review_project.py` for the project image checks.
`test_relay.py` runs real scene inspection, base-mesh checks, a focused stock capture and
offline inventory verification. `relay-test.json` records results. `test_live.py` verifies
the fallback connector, with results in `live-test.json`. Local socket tests need sandbox
network permission. Do not rerun tests blindly when an existing user scene differs.

Base-mesh tests found no zero-area faces, zero-length edges or nonfinite coordinates in
the current five meshes. Handguard/stock base boundaries are present with live modifiers;
this is not a final evaluated-surface approval. Shape fidelity remains pending. The focused
stock image exposes a diagonal shading transition needing investigation before progression.

## Compatibility fixes

- Webita's dependency allows incompatible MCP 2.x. Installed MCP 1.30.0; `requirements.lock`
  captures the resolved environment. Keep `mcp<2` when updating this connector.
- BlendRelay returns a list as session `structuredContent`, which the MCP 1.x client rejects.
  `relay_server.py` wraps that response and schema in a `sessions` object. Upstream code is
  unchanged. Codex uses this adapter. Other tools remain unchanged.

## Source revisions

- webita/blender-codex-mcp: `7b959c51fc4c166dc8b7ff4e85f989fa726f655c`
- danielsobrado/Codex-and-Blender: `e2d41423437e7ed9142ab2991a8b68d15ea85515`
- ayyar/blender_mcp_verifier: `e81c5826e3fec70032e5c55b9ad862b2abc9e2db`
- shefq/blendrelay-mcp: `1edc0097f549221e44aece67efc7a8b789fb4360`

These tools improve feedback and control, not modeling judgment or video understanding.
Reference comparison and topology inspection remain required at every accepted checkpoint.
