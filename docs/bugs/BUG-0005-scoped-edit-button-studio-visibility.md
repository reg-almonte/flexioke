---
status: in-progress
filed_at: 2026-08-31
---

# Bug Report: Edit Details / Lyrics Button Missing in Stem Studio Song Library

## Related
- Functional Spec: `docs/specs/version0.2.3.md` (§5 Context-Scoped Song Library Card Controls)
- Requirements: `docs/requirements/version0.2.3.md` (§6 Context-Inappropriate Editing)
- Story: `docs/tickets/STORY-0016-fixed-sidebar-and-song-catalog-modal.md`
- Task: `docs/tickets/TASK-0038-scoped-edit-button-visibility.md`

## Summary
In Version 0.2.3, the "Edit Details / Lyrics" button (`✏` / `📝`, `.edit-lyrics-btn`, `.lyrics-btn`) was intentionally removed from Karaoke Mode (Page 2 sidebar and Catalog Modal) to prevent accidental editing during live performances. However, it was also inadvertently omitted from the Stem Studio Song Library (Page 1), where metadata and lyric editing is supposed to be accessible. *(Fix applied, pending verification)*

## Root Cause Analysis
In `src/static/library_queue.js`, `SongLibraryManager.render()` checked contextual studio scope using:
```javascript
const isStudio = container.closest('#view-studio') !== null || container.id === 'studio-library-list';
```
In `src/static/index.html`:
1. The DOM container for Stem Studio is `#view-stem-studio` (not `#view-studio`).
2. The library list container element in Stem Studio lacked the ID `studio-library-list`.
Because `container.closest('#view-studio')` evaluated to `null`, `isStudio` was permanently `false`, causing the edit button to be omitted across both views.

## Applied Fix
1. In `src/static/library_queue.js`:
   - Updated the selector to `container.closest('#view-stem-studio') !== null || container.id === 'studio-library-list'`.
   - Included both `.lyrics-btn` and `.edit-lyrics-btn` classes on the rendered button for semantic consistency.
2. In `src/static/index.html`:
   - Added explicit IDs `id="studio-library-list"` and `id="karaoke-library-list"` to the respective library containers.
3. In `tests/test_library_queue_frontend.py`:
   - Enhanced `test_scoped_edit_lyrics_button_visibility` to strictly verify `#view-stem-studio`, `#studio-library-list`, and `.edit-lyrics-btn` existence and absence of the typo `#view-studio`.
