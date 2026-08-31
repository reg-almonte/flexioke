/**
 * Flexioke — Core SPA Ingestion & View Switcher
 */
document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation Views ---
    const navTabStudio = document.getElementById('nav-tab-studio');
    const navTabKaraoke = document.getElementById('nav-tab-karaoke');
    const viewStemStudio = document.getElementById('view-stem-studio');
    const viewKaraoke = document.getElementById('view-karaoke');
    const headerModeBadge = document.getElementById('header-mode-badge');

    const topNavSensor = document.getElementById('top-nav-sensor');
    const appHeader = document.getElementById('app-header');
    let headerHideTimeout = null;

    const revealHeader = () => {
        if (headerHideTimeout) clearTimeout(headerHideTimeout);
        if (appHeader) {
            appHeader.classList.add('header-revealed');
            if (document.body.classList.contains('karaoke-active')) {
                appHeader.style.marginTop = '0px';
            }
        }
    };

    const scheduleHideHeader = () => {
        if (headerHideTimeout) clearTimeout(headerHideTimeout);
        headerHideTimeout = setTimeout(() => {
            if (appHeader && !appHeader.matches(':hover')) {
                appHeader.classList.remove('header-revealed');
                if (document.body.classList.contains('karaoke-active')) {
                    const h = appHeader.offsetHeight || 66;
                    appHeader.style.marginTop = `-${h}px`;
                }
            }
        }, 1200);
    };

    if (topNavSensor && appHeader) {
        topNavSensor.addEventListener('mouseenter', revealHeader);
        appHeader.addEventListener('mouseenter', revealHeader);
        appHeader.addEventListener('mouseleave', scheduleHideHeader);

        document.addEventListener('mousemove', (e) => {
            if (document.body.classList.contains('karaoke-active')) {
                if (e.clientY <= 25) {
                    revealHeader();
                } else if (e.clientY > 85 && !appHeader.matches(':hover')) {
                    scheduleHideHeader();
                }
            }
        });

        window.addEventListener('resize', () => {
            if (document.body.classList.contains('karaoke-active') && !appHeader.classList.contains('header-revealed')) {
                const h = appHeader.offsetHeight || 66;
                appHeader.style.marginTop = `-${h}px`;
            }
        });
    }

    if (navTabStudio && navTabKaraoke) {
        navTabStudio.addEventListener('click', () => {
            document.body.classList.remove('karaoke-active');
            if (appHeader) {
                appHeader.classList.remove('header-revealed');
                appHeader.style.marginTop = '';
            }
            navTabStudio.className = "px-4 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition flex items-center gap-1.5";
            navTabKaraoke.className = "px-4 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5";
            if (headerModeBadge) headerModeBadge.textContent = "Stem Studio";
            if (viewStemStudio) viewStemStudio.classList.remove('hidden');
            if (viewKaraoke) viewKaraoke.classList.add('hidden');
        });

        navTabKaraoke.addEventListener('click', () => {
            document.body.classList.add('karaoke-active');
            navTabKaraoke.className = "px-4 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition flex items-center gap-1.5";
            navTabStudio.className = "px-4 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5";
            if (headerModeBadge) headerModeBadge.textContent = "Karaoke Mode";
            if (viewKaraoke) viewKaraoke.classList.remove('hidden');
            if (viewStemStudio) viewStemStudio.classList.add('hidden');
            // Auto hide on switching to karaoke
            scheduleHideHeader();
        });
    }

    // --- Elements ---
    const tabUploadBtn = document.getElementById('tab-upload-btn');
    const tabUrlBtn = document.getElementById('tab-url-btn') || document.getElementById('tab-youtube-btn');
    const tabUploadContent = document.getElementById('tab-upload-content');
    const tabUrlContent = document.getElementById('tab-url-content') || document.getElementById('tab-youtube-content');

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectedFileBadge = document.getElementById('selected-file-badge');
    const selectedFileName = document.getElementById('selected-file-name');
    const selectedFileSize = document.getElementById('selected-file-size');
    const clearFileBtn = document.getElementById('clear-file-btn');
    const submitUploadBtn = document.getElementById('submit-upload-btn');

    const audioUrlInput = document.getElementById('audio-url-input') || document.getElementById('youtube-url-input');
    const submitAudioUrlBtn = document.getElementById('submit-audio-url-btn') || document.getElementById('submit-youtube-btn');

    const processingCard = document.getElementById('processing-card');
    const activeJobTitle = document.getElementById('active-job-title');
    const cancelActiveJobBtn = document.getElementById('cancel-active-job-btn');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressStageText = document.getElementById('progress-stage-text');
    const stepIngest = document.getElementById('step-ingest');
    const stepStage1 = document.getElementById('step-stage1');
    const stepStage2 = document.getElementById('step-stage2');

    const queuedJobsSection = document.getElementById('queued-jobs-section');
    const queuedJobsCount = document.getElementById('queued-jobs-count');
    const queuedJobsList = document.getElementById('queued-jobs-list');

    const errorCard = document.getElementById('error-card');
    const errorMessageText = document.getElementById('error-message-text');
    const dismissErrorBtn = document.getElementById('dismiss-error-btn');

    let currentSelectedFiles = [];
    let activePollingInterval = null;
    let currentActiveJobId = null;
    const trackedJobIds = new Set();

    // --- Tab Switching ---
    if (tabUploadBtn && tabUrlBtn && tabUploadContent && tabUrlContent) {
        tabUploadBtn.addEventListener('click', () => {
            tabUploadBtn.className = "flex-1 py-2 rounded-lg bg-brand-600 text-white font-semibold transition shadow-sm flex items-center justify-center gap-1.5";
            tabUrlBtn.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-1.5";
            tabUploadContent.classList.remove('hidden');
            tabUrlContent.classList.add('hidden');
        });

        tabUrlBtn.addEventListener('click', () => {
            tabUrlBtn.className = "flex-1 py-2 rounded-lg bg-brand-600 text-white font-semibold transition shadow-sm flex items-center justify-center gap-1.5";
            tabUploadBtn.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-1.5";
            tabUrlContent.classList.remove('hidden');
            tabUploadContent.classList.add('hidden');
        });
    }

    // --- Drag & Drop / Multi-File Selection ---
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('border-brand-500', 'bg-brand-500/10');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('border-brand-500', 'bg-brand-500/10');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-brand-500', 'bg-brand-500/10');
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files);
        }
    });

    function handleFileSelection(files) {
        currentSelectedFiles = Array.from(files);
        if (currentSelectedFiles.length === 0) return;

        if (currentSelectedFiles.length === 1) {
            const file = currentSelectedFiles[0];
            selectedFileName.textContent = file.name;
            selectedFileSize.textContent = `(${(file.size / (1024 * 1024)).toFixed(1)} MB)`;
        } else {
            const totalBytes = currentSelectedFiles.reduce((acc, f) => acc + f.size, 0);
            selectedFileName.textContent = `${currentSelectedFiles.length} audio files selected`;
            selectedFileSize.textContent = `(${(totalBytes / (1024 * 1024)).toFixed(1)} MB total)`;
        }
        selectedFileBadge.classList.remove('hidden');
        dropZone.classList.add('hidden');
        hideError();
    }

    clearFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentSelectedFiles = [];
        fileInput.value = '';
        selectedFileBadge.classList.add('hidden');
        dropZone.classList.remove('hidden');
    });

    // --- Multi-File Batch Upload Submission ---
    submitUploadBtn.addEventListener('click', async () => {
        if (!currentSelectedFiles || currentSelectedFiles.length === 0) {
            showError("Please select one or more audio files first.");
            return;
        }

        submitUploadBtn.disabled = true;
        hideError();

        const filesToUpload = [...currentSelectedFiles];
        // Reset upload form immediately
        clearFileBtn.click();

        try {
            for (const file of filesToUpload) {
                const formData = new FormData();
                formData.append('file', file);

                const response = await fetch('/api/jobs/upload', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || `Upload failed for ${file.name}`);
                }

                trackedJobIds.add(data.job_id);
            }

            startQueueTracking();
        } catch (err) {
            showError(err.message);
        } finally {
            submitUploadBtn.disabled = false;
        }
    });

    // --- Direct Audio URL Submission ---
    if (submitAudioUrlBtn && audioUrlInput) {
        submitAudioUrlBtn.addEventListener('click', async () => {
            const url = audioUrlInput.value.trim();
            if (!url) {
                showError("Please enter a direct audio URL.");
                return;
            }

            submitAudioUrlBtn.disabled = true;
            hideError();

            try {
                const response = await fetch('/api/jobs/download-url', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url })
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || "Audio URL download submission failed");
                }

                audioUrlInput.value = '';
                trackedJobIds.add(data.job_id);
                startQueueTracking();
            } catch (err) {
                showError(err.message);
            } finally {
                submitAudioUrlBtn.disabled = false;
            }
        });
    }

    // --- Active Job Cancellation ---
    if (cancelActiveJobBtn) {
        cancelActiveJobBtn.addEventListener('click', async () => {
            if (!currentActiveJobId) return;
            try {
                await fetch(`/api/jobs/${currentActiveJobId}/cancel`, { method: 'POST' });
                pollSeparationQueue();
            } catch (err) {
                console.error("Failed to cancel active job:", err);
            }
        });
    }

    // --- Separation Queue Manager & Polling ---
    function startQueueTracking() {
        if (activePollingInterval) {
            clearInterval(activePollingInterval);
        }
        processingCard.classList.remove('hidden');
        pollSeparationQueue();
        activePollingInterval = setInterval(pollSeparationQueue, 1500);
    }

    async function pollSeparationQueue() {
        try {
            const resp = await fetch('/api/jobs');
            if (!resp.ok) return;
            const data = await resp.json();
            const allJobs = data.jobs || [];

            // Active or queued jobs
            const activeJobs = allJobs.filter(j => 
                ['downloading', 'separating_stage_1', 'separating_stage_2'].includes(j.status)
            );
            const queuedJobs = allJobs.filter(j => j.status === 'queued')
                                      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

            const totalInFlight = activeJobs.length + queuedJobs.length;

            if (totalInFlight === 0) {
                // If everything completed, clean up
                if (activePollingInterval) {
                    clearInterval(activePollingInterval);
                    activePollingInterval = null;
                }
                setTimeout(() => {
                    processingCard.classList.add('hidden');
                }, 2000);
                window.dispatchEvent(new CustomEvent('flexioke:library-updated'));
                return;
            }

            processingCard.classList.remove('hidden');

            // Pick currently running job (or first queued job if none active yet)
            const currentRunningJob = activeJobs[0] || queuedJobs[0];
            currentActiveJobId = currentRunningJob.job_id;

            if (activeJobTitle) {
                const titleStr = currentRunningJob.artist 
                    ? `${currentRunningJob.title} — ${currentRunningJob.artist}` 
                    : currentRunningJob.title;
                activeJobTitle.textContent = titleStr;
            }

            updateProgressUI(currentRunningJob.progress, currentRunningJob.current_stage, currentRunningJob.status);

            // Render remaining queued jobs (excluding the one displayed as active)
            const remainingQueued = queuedJobs.filter(j => j.job_id !== currentRunningJob.job_id);

            if (remainingQueued.length > 0) {
                queuedJobsSection.classList.remove('hidden');
                queuedJobsCount.textContent = `${remainingQueued.length} queued`;
                queuedJobsList.innerHTML = remainingQueued.map((j, idx) => `
                    <div class="flex items-center justify-between p-2 bg-slate-900/80 rounded-lg border border-slate-800 text-xs">
                        <div class="flex items-center gap-2 truncate">
                            <span class="text-[10px] px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-300 font-semibold">#${idx + 1}</span>
                            <div class="truncate">
                                <p class="font-medium text-slate-200 truncate">${j.title}</p>
                                <p class="text-[10px] text-slate-400 truncate">${j.artist || 'Unknown Artist'}</p>
                            </div>
                        </div>
                        <button class="cancel-queued-btn text-slate-400 hover:text-rose-400 p-1 text-xs transition" data-job-id="${j.job_id}" title="Cancel separation">✕</button>
                    </div>
                `).join('');

                // Bind cancellation buttons
                queuedJobsList.querySelectorAll('.cancel-queued-btn').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        e.stopPropagation();
                        const jId = btn.getAttribute('data-job-id');
                        try {
                            await fetch(`/api/jobs/${jId}/cancel`, { method: 'POST' });
                            pollSeparationQueue();
                        } catch (err) {
                            console.error("Failed to cancel queued job:", err);
                        }
                    });
                });
            } else {
                queuedJobsSection.classList.add('hidden');
            }

            // Check if any tracked job just completed
            allJobs.forEach(j => {
                if (trackedJobIds.has(j.job_id) && j.status === 'completed') {
                    trackedJobIds.delete(j.job_id);
                    window.dispatchEvent(new CustomEvent('flexioke:job-completed', { detail: j }));
                }
            });
        } catch (err) {
            console.error("Queue polling error:", err);
        }
    }

    function updateProgressUI(progress, stageText, status) {
        progressBarFill.style.width = `${progress}%`;
        progressPercent.textContent = `${progress}%`;
        progressStageText.textContent = stageText || "Processing...";

        // Step indicators
        const activeClass = "p-1 rounded bg-brand-500/20 text-brand-400 font-semibold border border-brand-500/30";
        const inactiveClass = "p-1 rounded bg-slate-800/60 text-slate-400";

        stepIngest.className = (status === 'queued' || status === 'downloading' || progress < 25) ? activeClass : inactiveClass;
        stepStage1.className = (status === 'separating_stage_1' || (progress >= 25 && progress < 65)) ? activeClass : inactiveClass;
        stepStage2.className = (status === 'separating_stage_2' || progress >= 65) ? activeClass : inactiveClass;
    }

    function showError(msg) {
        errorMessageText.textContent = msg;
        errorCard.classList.remove('hidden');
    }

    function hideError() {
        errorCard.classList.add('hidden');
    }

    dismissErrorBtn.addEventListener('click', hideError);

    // Initial check for in-flight jobs on load
    pollSeparationQueue();
});
