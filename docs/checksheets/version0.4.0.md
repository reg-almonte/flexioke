---
status: pending-approval
approved_by:
approved_at:
---

# Version 0.4.0: Video Backgrounds, Stage Geometry Controls & Side A/B Uploads — Check Sheet

## Related
- Functional spec: `docs/specs/version0.4.0.md`
- ADR: `docs/design/ADR-0012-video-backgrounds-stage-geometry-and-side-ab.md`
- Epic: `docs/tickets/EPIC-0011-video-backgrounds-stage-geometry-and-side-ab.md`
- Stories: `docs/tickets/STORY-0034-video-background-engine-and-stage-sync.md`, `docs/tickets/STORY-0035-fullscreen-stage-geometry-customization.md`, `docs/tickets/STORY-0036-side-ab-dual-track-ingestion-and-playback.md`
- Tasks: `docs/tickets/TASK-0071-video-manager-service-and-streaming-endpoints.md`, `docs/tickets/TASK-0072-karaoke-stage-video-renderer-and-timecode-sync.md`, `docs/tickets/TASK-0073-fullscreen-geometry-css-variables-and-stage-settings.md`, `docs/tickets/TASK-0074-side-ab-ingestion-endpoints-and-metadata.md`, `docs/tickets/TASK-0075-side-ab-dual-stream-webaudio-and-vocal-toggles.md`

## Verification Items

### 1. Video Backend Service, Storage Auto-Discovery & Streaming Endpoints (STORY-0034 / TASK-0071)
- [x] Auto-discovery scans `./data/videos/` indexing `.mp4`, `.webm`, `.mov`, and `.mkv` files with thread safety — verified by: `tests/test_video_manager.py::test_video_manager_discovery_and_indexing`
- [x] `GET /api/videos` returns complete list of discovered video objects with filename, size, and streaming URL — verified by: `tests/test_video_api.py::test_get_videos_list`
- [x] `POST /api/videos/upload` handles multipart file uploads, validates video MIME/extensions, and saves to video store — verified by: `tests/test_video_api.py::test_upload_video`
- [x] Invalid video formats are rejected with 400 Bad Request — verified by: `tests/test_video_api.py::test_upload_invalid_video_format`
- [x] `GET /api/videos/{filename}` supports HTTP 206 Partial Content range requests and full streams — verified by: `tests/test_video_api.py::test_stream_video_full_and_range`
- [x] Song metadata stores and patches `video_id` and `video_offset_seconds` defaulting to `bg001.mp4` and `0.0` — verified by: `tests/test_video_api.py::test_job_metadata_video_assignment_and_offset`
- [x] Queue items preserve and live-propagate `video_id` and `video_offset_seconds` metadata during playback — verified by: `tests/test_queue_service.py::test_queue_video_metadata_propagation`
- [ ] User uploads custom background video via Song Details modal and verifies immediate availability — verified by: manual test in browser

### 2. Karaoke Stage Video Renderer & Timecode Synchronization (STORY-0034 / TASK-0072)
- [x] `<video id="karaoke-bg-video">` rendered behind lyrics stage with muted, looping, and translucent backdrop styling (`opacity-40`, `z-0`) — verified by: `tests/test_karaoke_video_stage.py::test_video_elements_in_html` & `tests/test_karaoke_video_stage.py::test_video_stage_styles_in_css`
- [x] Video playback state synchronizes with audio transport (plays on play, pauses on pause, seeks on seek) — verified by: `tests/test_karaoke_video_stage.py::test_video_timecode_synchronization_in_node`
- [x] Offset calculation formula `(audioTime + videoOffset) % videoDuration` ensures seamless looping and exact start offset — verified by: `tests/test_karaoke_video_stage.py::test_video_timecode_synchronization_in_node`
- [x] Video element unloads and resets cleanly when song ends or stage is cleared — verified by: `tests/test_karaoke_video_stage.py::test_video_timecode_synchronization_in_node`
- [x] Song Details modal allows selecting video and specifying video offset in seconds — verified by: `tests/test_karaoke_video_stage.py::test_lyrics_modal_video_controls_in_library_queue_js`
- [ ] User plays song with video offset, seeks audio playhead, and verifies background video remains synchronized without stutter — verified by: manual test in browser

### 3. Fullscreen Stage Geometry Customization & Persistence (STORY-0035 / TASK-0073)
- [x] `#karaoke-settings-modal` provides interactive range sliders for Width (`60%`–`100%`), Height (`30vh`–`80vh`), and Vertical Offset (`-20%`–`+20%`) — verified by: `tests/test_stage_geometry.py::test_stage_geometry_elements_in_html`
- [x] Dynamic CSS custom properties (`--karaoke-fullscreen-stage-width`, `--karaoke-fullscreen-stage-max-height`, `--karaoke-fullscreen-stage-v-offset`) update in real-time — verified by: `tests/test_stage_geometry.py::test_stage_geometry_css_variables_in_styles_css`
- [x] Geometry styling applies strictly to Fullscreen mode; Windowed stage card layout remains untouched — verified by: `tests/test_stage_geometry.py::test_stage_geometry_css_variables_in_styles_css`
- [x] Geometry settings persist in `localStorage` (`flexioke_stage_config`) and reset to defaults on demand — verified by: `tests/test_stage_geometry.py::test_stage_geometry_simulation_in_node`
- [ ] User enters fullscreen, adjusts stage width/height/vertical offset sliders in settings modal, and confirms responsive real-time scaling — verified by: manual test in browser

### 4. Direct Side A / Side B Dual-Track Ingestion & Stem Mapping (STORY-0036 / TASK-0074)
- [x] `SourceType` enum extended with `SIDE_AB = "side_ab"` — verified by: `tests/test_side_ab_api.py::test_source_type_side_ab_enum`
- [x] `POST /api/jobs/upload-side-ab` ingests Side B (Instrumental) + optional Side A (Vocal), generating instant completed jobs with progress 100% — verified by: `tests/test_side_ab_api.py::test_upload_side_b_only` & `tests/test_side_ab_api.py::test_upload_side_a_and_side_b`
- [x] `POST /api/jobs/{job_id}/attach-side-a` attaches vocal track to existing Side B song and updates stem mapping — verified by: `tests/test_side_ab_api.py::test_attach_side_a_to_existing_job`
- [x] Invalid audio file formats in Side A/B upload are rejected with 400 Bad Request — verified by: `tests/test_side_ab_api.py::test_upload_side_ab_invalid_files`
- [x] Stem Studio UI provides dedicated tab and dropzones for Side A/B dual-track upload — verified by: `tests/test_side_ab_api.py::test_side_ab_ui_elements_in_html`
- [x] Playback queue preserves `source_type: "side_ab"` and stems across queue operations and active playback dispatch — verified by: `tests/test_queue_service.py::test_queue_side_ab_source_type`
- [ ] User uploads Side B track in Stem Studio and attaches Side A later via Song Details modal — verified by: manual test in browser

### 5. Dual-Stream WebAudio Hot-Swapping & Dynamic Vocal Toggles (STORY-0036 / TASK-0075)
- [x] Player engine preloads and timecode-locks both Side A and Side B audio streams — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] Default / Vocal ON plays Side A (Full mix) at master volume with Side B muted (0 gain) — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] Toggling Lead Vocal to OFF mutes Side A (0 gain) and unpauses/unmutes Side B (Instrumental) at master volume with zero drift — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] Mutex muting in Stem Studio produces total silence when both stems are muted — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] Single-sided tracks gracefully lock Lead Vocal button (`Lead: OFF (Side B Only)` or `Lead: ON (Side A Only)`) — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] Backing Vocal toggle is locked and disabled with `Backing: N/A (Side A/B)` for all Side A/B tracks — verified by: `tests/test_side_ab_frontend.py::test_side_ab_webaudio_and_toggle_simulation`
- [x] `Side A/B` badges rendered across Song Library, Playlists, and Song Catalog modal — verified by: `tests/test_side_ab_frontend.py::test_side_ab_badges_in_library_and_playlists`
- [ ] User plays Side A/B track in Karaoke mode, toggles vocal on/off, and verifies instantaneous, click-free vocal hot-swapping — verified by: manual test in browser

## Completeness Review (auto-generated)
- **Review Date:** 2026-09-13
- **Review Status:** Complete
- **Findings:** No gaps found.
- **Summary:**
  - 34 of 34 expected items verified across Functional Spec (`docs/specs/version0.4.0.md`), ADR-0012 (`docs/design/ADR-0012-video-backgrounds-stage-geometry-and-side-ab.md`), Epic 0011, and Stories 0034–0036.
  - Zero missing coverage gaps identified.
  - Zero orphaned entries detected.
  - All automated test bindings and manual milestone gates are accurately mapped.

