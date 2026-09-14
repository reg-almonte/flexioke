---
status: pending-approval
approved_by:
approved_at:
implementation: pending
---

# TASK-0076: Migrate Test Files into Domain Subdirectories

## Parent Story
- `docs/tickets/STORY-0037-domain-tiered-test-suite-reorganization.md`

## What to build
Migrate flat test files from `tests/` into dedicated functional subdirectories:
- `tests/api/`: 12 API endpoint suites (`test_audio_url_api.py`, `test_frontend_routes.py`, `test_health.py`, `test_job_cancellation.py`, `test_library_api.py`, `test_lrclib_api.py`, `test_lyrics_api.py`, `test_playlist_api.py`, `test_side_ab_api.py`, `test_upload_api.py`, `test_video_api.py`, `test_youtube_api.py`).
- `tests/services/`: 12 backend manager & service suites (`test_audio_downloader.py`, `test_audio_validator.py`, `test_job_manager.py`, `test_lrclib_client.py`, `test_lyrics_store.py`, `test_pipeline_and_stems.py`, `test_playlist_manager.py`, `test_queue_service.py`, `test_stage1_separator.py`, `test_stage2_separator.py`, `test_track_export_and_cleanup.py`, `test_video_manager.py`).
- `tests/frontend/`: 16 DOM & WebAudio simulation suites (`test_favorites_frontend.py`, `test_karaoke_cinema_fullscreen.py`, `test_karaoke_controls_and_interruption.py`, `test_karaoke_fullscreen.py`, `test_karaoke_navigation.py`, `test_karaoke_playlists_frontend.py`, `test_karaoke_stage.py`, `test_karaoke_video_stage.py`, `test_library_queue_frontend.py`, `test_lyrics_modal_frontend.py`, `test_lyrics_modal_navigation.py`, `test_player_module.py`, `test_side_ab_frontend.py`, `test_stage_geometry.py`, `test_studio_playlists_frontend.py`, `test_svg_icons.py`).
- `tests/integration/`: 2 cross-cutting regression milestone suites (`test_v026_features.py`, `test_v040_features.py`).

## Acceptance Criteria
- [ ] All 42 test files are moved to their respective domain directories with `__init__.py` markers if appropriate.
- [ ] Zero test files remain in the root of `tests/`.

## Blocked by
- None (can start immediately).
