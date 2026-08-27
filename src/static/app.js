/**
 * Flexioke — Core SPA Ingestion & View Switcher
 */
document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation Views ---
    const navTabStudio = document.getElementById('nav-tab-studio');
    const navTabKaraoke = document.getElementById('nav-tab-karaoke');
    const viewStemStudio = document.getElementById('view-stem-studio');
    const viewKaraoke = document.getElementById('view-karaoke');
    const karaokeSwitchToStudioBtn = document.getElementById('karaoke-switch-to-studio-btn');

    if (navTabStudio && navTabKaraoke) {
        navTabStudio.addEventListener('click', () => {
            navTabStudio.className = "px-4 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition flex items-center gap-1.5";
            navTabKaraoke.className = "px-4 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5";
            if (viewStemStudio) viewStemStudio.classList.remove('hidden');
            if (viewKaraoke) viewKaraoke.classList.add('hidden');
        });

        navTabKaraoke.addEventListener('click', () => {
            navTabKaraoke.className = "px-4 py-1.5 rounded-lg bg-brand-600 text-white shadow-sm transition flex items-center gap-1.5";
            navTabStudio.className = "px-4 py-1.5 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center gap-1.5";
            if (viewKaraoke) viewKaraoke.classList.remove('hidden');
            if (viewStemStudio) viewStemStudio.classList.add('hidden');
        });
    }

    if (karaokeSwitchToStudioBtn && navTabStudio) {
        karaokeSwitchToStudioBtn.addEventListener('click', () => {
            navTabStudio.click();
        });
    }

    // --- Elements ---
    const tabUploadBtn = document.getElementById('tab-upload-btn');
    const tabYoutubeBtn = document.getElementById('tab-youtube-btn');
    const tabUploadContent = document.getElementById('tab-upload-content');
    const tabYoutubeContent = document.getElementById('tab-youtube-content');

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const selectedFileBadge = document.getElementById('selected-file-badge');
    const selectedFileName = document.getElementById('selected-file-name');
    const selectedFileSize = document.getElementById('selected-file-size');
    const clearFileBtn = document.getElementById('clear-file-btn');
    const submitUploadBtn = document.getElementById('submit-upload-btn');

    const youtubeUrlInput = document.getElementById('youtube-url-input');
    const submitYoutubeBtn = document.getElementById('submit-youtube-btn');

    const processingCard = document.getElementById('processing-card');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressStageText = document.getElementById('progress-stage-text');
    const stepIngest = document.getElementById('step-ingest');
    const stepStage1 = document.getElementById('step-stage1');
    const stepStage2 = document.getElementById('step-stage2');

    const errorCard = document.getElementById('error-card');
    const errorMessageText = document.getElementById('error-message-text');
    const dismissErrorBtn = document.getElementById('dismiss-error-btn');

    let currentSelectedFile = null;
    let activePollingInterval = null;

    // --- Tab Switching ---
    tabUploadBtn.addEventListener('click', () => {
        tabUploadBtn.className = "flex-1 py-2 rounded-lg bg-brand-600 text-white font-semibold transition shadow-sm flex items-center justify-center gap-1.5";
        tabYoutubeBtn.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-1.5";
        tabUploadContent.classList.remove('hidden');
        tabYoutubeContent.classList.add('hidden');
    });

    tabYoutubeBtn.addEventListener('click', () => {
        tabYoutubeBtn.className = "flex-1 py-2 rounded-lg bg-brand-600 text-white font-semibold transition shadow-sm flex items-center justify-center gap-1.5";
        tabUploadBtn.className = "flex-1 py-2 rounded-lg text-slate-400 hover:text-slate-200 transition flex items-center justify-center gap-1.5";
        tabYoutubeContent.classList.remove('hidden');
        tabUploadContent.classList.add('hidden');
    });

    // --- Drag & Drop / File Selection ---
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
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    function handleFileSelection(file) {
        currentSelectedFile = file;
        selectedFileName.textContent = file.name;
        selectedFileSize.textContent = `(${(file.size / (1024 * 1024)).toFixed(1)} MB)`;
        selectedFileBadge.classList.remove('hidden');
        dropZone.classList.add('hidden');
        hideError();
    }

    clearFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentSelectedFile = null;
        fileInput.value = '';
        selectedFileBadge.classList.add('hidden');
        dropZone.classList.remove('hidden');
    });

    // --- File Upload Submission ---
    submitUploadBtn.addEventListener('click', async () => {
        if (!currentSelectedFile) {
            showError("Please select an audio file first.");
            return;
        }

        const formData = new FormData();
        formData.append('file', currentSelectedFile);

        submitUploadBtn.disabled = true;
        hideError();

        try {
            const response = await fetch('/api/jobs/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || "Upload failed");
            }

            // Start tracking job
            startJobTracking(data.job_id);
            // Reset upload form
            clearFileBtn.click();
        } catch (err) {
            showError(err.message);
        } finally {
            submitUploadBtn.disabled = false;
        }
    });

    // --- YouTube Submission ---
    submitYoutubeBtn.addEventListener('click', async () => {
        const url = youtubeUrlInput.value.trim();
        if (!url) {
            showError("Please enter a YouTube video URL.");
            return;
        }

        submitYoutubeBtn.disabled = true;
        hideError();

        try {
            const response = await fetch('/api/jobs/youtube', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || "YouTube extraction submission failed");
            }

            youtubeUrlInput.value = '';
            startJobTracking(data.job_id);
        } catch (err) {
            showError(err.message);
        } finally {
            submitYoutubeBtn.disabled = false;
        }
    });

    // --- Job Status Polling Manager ---
    function startJobTracking(jobId) {
        if (activePollingInterval) {
            clearInterval(activePollingInterval);
        }

        processingCard.classList.remove('hidden');
        updateProgressUI(5, "Initializing separation job...", "queued");

        activePollingInterval = setInterval(async () => {
            try {
                const resp = await fetch(`/api/jobs/${jobId}`);
                if (!resp.ok) {
                    throw new Error(`Failed to check job status (${resp.status})`);
                }
                const job = await resp.json();

                updateProgressUI(job.progress, job.current_stage, job.status);

                if (job.status === 'completed') {
                    clearInterval(activePollingInterval);
                    setTimeout(() => {
                        processingCard.classList.add('hidden');
                    }, 2500);

                    // Notify application of completed job
                    window.dispatchEvent(new CustomEvent('flexioke:job-completed', { detail: job }));
                } else if (job.status === 'failed') {
                    clearInterval(activePollingInterval);
                    processingCard.classList.add('hidden');
                    showError(job.error || "Separation pipeline failed.");
                }
            } catch (err) {
                console.error("Polling error:", err);
            }
        }, 1500);
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
});
