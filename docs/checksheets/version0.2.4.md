---
status: pending-approval
approved_by:
approved_at:
---

# Manual QA Check Sheet: Version 0.2.4 (EPIC-0006)

**Target Feature:** Stem Studio Upgrade & Separation Job Queue  
**Related Specs & ADRs:**
- Requirement: `docs/requirements/version0.2.4.md`
- Functional Spec: `docs/specs/version0.2.4.md`
- ADR: `docs/design/ADR-0007-stem-studio-upgrade-and-job-queue.md`
- Epic: `docs/tickets/EPIC-0006-stem-studio-upgrade-and-job-queue.md`

**Local Server URL:** `http://localhost:8000`

---

## 📋 Story-by-Story Manual Verification Checklist

### 🎵 STORY-0017: Direct Audio URL Ingestion & Smart Title/Artist Parsing
- [ ] **1. Direct Audio URL Tab:** Navigate to **Stem Studio** $\to$ Click the **"Audio URL"** tab.
- [ ] **2. Valid Direct MP3 Download:** Paste a public direct audio link (e.g. raw `.mp3` / `.wav` URL) $\to$ Click **"Download & Process"**. Verify the audio streams down with real-time percentage progress and enters the separation queue.
- [ ] **3. URL Error Handling:** Enter a non-audio URL or 404 URL $\to$ Verify user-friendly error feedback without UI crash.
- [ ] **4. Smart Title/Artist Parsing:** Ingest a file/URL named `Artist - Song Title.mp3` or `01. Artist - Song.mp3`. Verify Title and Artist are cleanly parsed and auto-populated.

---

### 🗂️ STORY-0018: Multi-File Batch Ingestion & Asynchronous Separation FIFO Queue
- [ ] **5. Multi-File Selection & Drag-and-Drop:** Select 2–3 audio files at once in the file upload dialog (or drag & drop onto the upload dropzone). Verify all files are accepted and queued.
- [ ] **6. Sequential FIFO Separation:** Observe the separation worker processing the first job while subsequent files wait with live `#1 in queue`, `#2 in queue` position badges.
- [ ] **7. Separation Queue Cancellation:** Click **"Cancel"** (`✕`) on a queued job $\to$ Verify it cancels immediately, removes from queue, and the next song advances smoothly.

---

### 🪗 STORY-0019: Stem Studio Collapsible Accordions & Persistent Notes Scratchpad
- [ ] **8. Collapsible Sidebar Accordions:** Click the header on each sidebar section (**"Add New Song"**, **"Song Library"**, **"Separation Queue"**). Verify smooth slide animation and chevron rotation.
- [ ] **9. Accordion State Persistence:** Collapse one or two accordion cards $\to$ Refresh the browser page (`Cmd+R` / `F5`). Verify the collapsed states persist.
- [ ] **10. Studio Notes Modal:** Click the **"📝 Notes"** button in the top navigation header.
- [ ] **11. Scratchpad Auto-Save:** Type notes/lyrics $\to$ Verify the green **"Saved"** indicator appears and notes persist across page reloads.
- [ ] **12. Clickable Links in Notes:** Paste a URL (e.g. `https://google.com`) $\to$ Verify it automatically renders as a safe clickable link in the preview.

---

### 🔍 STORY-0020: Expanded Studio Song Catalog Modal & Default Recent Sort
- [ ] **13. Studio Catalog Modal Trigger:** In Stem Studio's **"Song Library"** accordion header, click the expand icon (**`⛶`**). Verify the full-screen modal opens.
- [ ] **14. Stem Studio Sort Order:** In Stem Studio, verify library tracks default to **Recently Added** (newest separated songs appear at top).
- [ ] **15. Karaoke Mode Sort Order:** Switch to **Karaoke Mode** $\to$ Verify library tracks default to **Title (A-Z)** alphabetical sort.
- [ ] **16. Catalog Modal Search & Filtering:** In the catalog modal, type search queries, switch sort orders, and click **"✕"** to clear search instantly.
- [ ] **17. Catalog Modal "📝 Edit" Action:** Click **"📝 Edit"** on any song in the catalog modal $\to$ Verify the catalog modal dismisses and opens the Song Details & LRC Lyrics modal seamlessly.

---

### 📦 STORY-0021: Combined Stem Zip Export, Track Deletion & Post-Processing Archiving
- [ ] **18. Combined Stem `.zip` Export:** Load a completed song into the Multitrack Player $\to$ Click **"📦 Export Stems (.zip)"** in the player header. Verify that `{title}_stems.zip` downloads containing `instrumental.mp3`, `lead_vocals.mp3`, `backing_vocals.mp3`, and `lyrics.lrc` (if present).
- [ ] **19. Permanent Track Deletion:** In the Edit Details / Lyrics modal, click **"🗑 Delete Track"**. Verify the confirmation prompt appears.
- [ ] **20. Cascade Storage & Queue Cleanup:** Confirm deletion $\to$ Verify the track disappears from Song Library, clears from Playback Queue, unloads from Multitrack Player, and deletes from `./data/jobs/{job_id}/`.
- [ ] **21. Post-Separation Raw Audio Archiving:** Check `./data/archive/` $\to$ Verify the original uploaded/downloaded audio file was automatically moved out of the active `./data/jobs/{job_id}/` folder into `./data/archive/{job_id}_{filename}`.
