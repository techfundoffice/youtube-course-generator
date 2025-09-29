// YouTube Course Generator - Frontend JavaScript
// Handles form submission, real-time processing feedback, and UI interactions

document.addEventListener('DOMContentLoaded', function() {
    const courseForm = document.getElementById('courseForm');
    const generateBtn = document.getElementById('generateBtn');
    const processingStatus = document.getElementById('processingStatus');
    const progressBar = document.getElementById('progressBar');
    const statusText = document.getElementById('statusText');
    const youtubeUrlInput = document.getElementById('youtube_url');
    
    // Layer status elements
    const metadataLayer = document.getElementById('metadataLayer');
    const transcriptLayer = document.getElementById('transcriptLayer');
    const aiLayer = document.getElementById('aiLayer');
    
    let processingInterval;
    let startTime;
    
    // YouTube URL validation patterns
    const youtubePatterns = [
        /^https?:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]+/,
        /^https?:\/\/(www\.)?youtu\.be\/[\w-]+/,
        /^https?:\/\/(www\.)?youtube\.com\/embed\/[\w-]+/,
        /^https?:\/\/(www\.)?youtube\.com\/v\/[\w-]+/,
        /^https?:\/\/m\.youtube\.com\/watch\?v=[\w-]+/,
        /^https?:\/\/(www\.)?youtube\.com\/shorts\/[\w-]+/,
        /^https?:\/\/m\.youtube\.com\/shorts\/[\w-]+/
    ];
    
    // Real-time URL validation
    youtubeUrlInput.addEventListener('input', function() {
        const url = this.value.trim();
        const isValid = validateYouTubeUrl(url);
        
        if (url && !isValid) {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
        } else if (url && isValid) {
            this.classList.add('is-valid');
            this.classList.remove('is-invalid');
        } else {
            this.classList.remove('is-valid', 'is-invalid');
        }
    });
    
    // Form submission handler
    courseForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const youtubeUrl = youtubeUrlInput.value.trim();
        
        if (!youtubeUrl) {
            showError('Please enter a YouTube URL');
            return;
        }
        
        if (!validateYouTubeUrl(youtubeUrl)) {
            showError('Please enter a valid YouTube URL');
            return;
        }
        
        startProcessing(youtubeUrl);
    });
    
    function validateYouTubeUrl(url) {
        if (!url) return false;
        return youtubePatterns.some(pattern => pattern.test(url));
    }
    
    function startProcessing(youtubeUrl) {
        // Disable form and show processing status
        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        // Processing status always visible - no need to show/hide
        startTime = Date.now();
        
        // Reset all layers
        resetLayerStatus();
        
        // Start progress simulation
        simulateProgress();
        
        // Generate session ID for tracking BEFORE form submission
        const sessionId = Math.random().toString(36).substr(2, 8);
        window.currentSessionId = sessionId;
        console.log('Generated session ID:', sessionId);
        
        // Start fetching logs immediately during processing
        setTimeout(() => {
            console.log('Starting real-time log fetching for session:', sessionId);
            startLogFetching(sessionId);
            
            // Also test the logs API directly
            fetch(`/api/logs/${sessionId}`)
                .then(response => response.json())
                .then(data => {
                    console.log('Direct logs API test:', data);
                })
                .catch(error => {
                    console.error('Direct logs API test failed:', error);
                });
        }, 2000);
        
        // Submit form data
        submitForm(youtubeUrl, sessionId);
    }
    
    function submitForm(youtubeUrl, sessionId) {
        const formData = new FormData();
        formData.append('youtube_url', youtubeUrl);
        formData.append('session_id', sessionId);
        
        fetch('/generate', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        })
        .then(html => {
            // Success - replace page content or redirect
            document.open();
            document.write(html);
            document.close();
            
            // Start fetching real processing logs after DOM is ready
            setTimeout(() => {
                if (window.currentSessionId) {
                    console.log('Starting log fetching for session:', window.currentSessionId);
                    startLogFetching(window.currentSessionId);
                } else {
                    console.log('No session ID available for log fetching');
                }
            }, 1000);
        })
        .catch(error => {
            console.error('Processing error:', error);
            showError(`Processing failed: ${error.message}`);
            resetForm();
        });
    }
    
    function startLogFetching(sessionId) {
        if (!sessionId) return;
        
        // Start fetching logs immediately and then every 2 seconds
        fetchProcessingLogs(sessionId);
        
        const logInterval = setInterval(() => {
            fetchProcessingLogs(sessionId);
        }, 2000);
        
        // Stop fetching after 5 minutes
        setTimeout(() => {
            clearInterval(logInterval);
            console.log('Stopped log fetching after 5 minutes');
        }, 300000);
        
        // Store interval globally so we can clear it if needed
        window.currentLogInterval = logInterval;
    }
    
    function fetchProcessingLogs(sessionId) {
        if (!sessionId) return;
        
        console.log('Fetching logs for session:', sessionId);
        fetch(`/api/logs/${sessionId}`)
            .then(response => response.json())
            .then(data => {
                console.log('Logs response:', data);
                if (data.success && data.logs && data.logs.length > 0) {
                    console.log('Displaying', data.logs.length, 'logs');
                    displayProcessingLogs(data.logs);
                } else {
                    console.log('No logs yet, showing loading message');
                    // Show loading message if no logs yet
                    const logsContainer = document.getElementById('processingLogs');
                    if (logsContainer && (!data.logs || data.logs.length === 0)) {
                        logsContainer.innerHTML = `
                            <div class="text-muted text-center p-3">
                                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                Waiting for processing logs...
                            </div>
                        `;
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching processing logs:', error);
                const logsContainer = document.getElementById('processingLogs');
                if (logsContainer) {
                    logsContainer.innerHTML = `
                        <div class="text-danger text-center p-3">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            Error loading logs: ${error.message}
                        </div>
                    `;
                }
            });
    }
    
    function displayProcessingLogs(logs) {
        const logsContainer = document.getElementById('processingLogs');
        console.log('Logs container found:', !!logsContainer);
        if (!logsContainer) {
            console.error('processingLogs container not found');
            return;
        }
        
        const logsHtml = logs.map(log => {
            const statusClass = log.level === 'ERROR' ? 'text-danger' : 
                              log.level === 'WARNING' ? 'text-warning' : 
                              log.status === 'SUCCESS' ? 'text-success' : 
                              log.status === 'FAILED' ? 'text-danger' :
                              log.status === 'ACTIVATED' ? 'text-warning' : 'text-info';
            
            const timestamp = new Date(log.timestamp).toLocaleTimeString();
            const step = log.step || log.step_name || 'Unknown';
            const details = log.details || log.message || '';
            
            return `
                <div class="log-entry mb-1 p-2 border-start border-2 ${statusClass}" style="border-color: currentColor !important;">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong class="small">${step}</strong>
                            <span class="badge ${statusClass.includes('danger') ? 'bg-danger' : 
                                               statusClass.includes('warning') ? 'bg-warning' : 
                                               statusClass.includes('success') ? 'bg-success' : 'bg-secondary'} ms-2 small">
                                ${log.status}
                            </span>
                        </div>
                        <small class="text-muted">${timestamp}</small>
                    </div>
                    <div class="mt-1 small text-light">${details}</div>
                </div>
            `;
        }).join('');
        
        logsContainer.innerHTML = logsHtml;
        
        // Auto-scroll to bottom
        logsContainer.scrollTop = logsContainer.scrollHeight;
        console.log('Logs displayed successfully');
    }
    
    function simulateProgress() {
        let progress = 0;
        let currentPhase = 0;
        
        const phases = [
            {
                name: 'Extracting video metadata...',
                duration: 15000, // 15 seconds
                progress: 25,
                layer: 'metadata'
            },
            {
                name: 'Extracting transcript...',
                duration: 20000, // 20 seconds
                progress: 50,
                layer: 'transcript'
            },
            {
                name: 'Generating course with AI...',
                duration: 45000, // 45 seconds
                progress: 90,
                layer: 'ai'
            },
            {
                name: 'Finalizing course structure...',
                duration: 10000, // 10 seconds
                progress: 100,
                layer: null
            }
        ];
        
        function updatePhase() {
            if (currentPhase >= phases.length) {
                clearInterval(processingInterval);
                return;
            }
            
            const phase = phases[currentPhase];
            statusText.textContent = phase.name;
            
            if (phase.layer) {
                updateLayerStatus(phase.layer, 'processing');
            }
            
            // Animate progress to target
            animateProgress(progress, phase.progress, phase.duration);
            
            // Set timeout for next phase
            setTimeout(() => {
                if (phase.layer) {
                    // Simulate some failures for realistic behavior
                    const shouldFail = Math.random() < 0.3; // 30% chance of initial failure
                    if (shouldFail && phase.layer !== 'ai') { // AI layer should always eventually succeed
                        updateLayerStatus(phase.layer, 'failed');
                        // Show retry attempt
                        setTimeout(() => {
                            updateLayerStatus(phase.layer, 'processing');
                            setTimeout(() => {
                                updateLayerStatus(phase.layer, 'success');
                            }, 3000);
                        }, 2000);
                    } else {
                        updateLayerStatus(phase.layer, 'success');
                    }
                }
                
                progress = phase.progress;
                currentPhase++;
                updatePhase();
            }, phase.duration);
        }
        
        updatePhase();
    }
    
    function animateProgress(start, end, duration) {
        const startTime = Date.now();
        const difference = end - start;
        
        function updateProgress() {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const currentValue = start + (difference * progress);
            
            progressBar.style.width = currentValue + '%';
            progressBar.setAttribute('aria-valuenow', currentValue);
            
            if (progress < 1) {
                requestAnimationFrame(updateProgress);
            }
        }
        
        updateProgress();
    }
    
    function updateLayerStatus(layer, status) {
        const layerElement = document.getElementById(layer + 'Layer');
        if (!layerElement) return;
        
        const icon = layerElement.querySelector('i');
        
        // Remove all status classes
        layerElement.classList.remove('success', 'processing', 'failed');
        icon.classList.remove('fa-circle', 'fa-check-circle', 'fa-times-circle', 'fa-spinner', 'fa-spin');
        
        // Add new status
        layerElement.classList.add(status);
        
        switch (status) {
            case 'success':
                icon.classList.add('fa-check-circle');
                break;
            case 'processing':
                icon.classList.add('fa-spinner', 'fa-spin');
                break;
            case 'failed':
                icon.classList.add('fa-times-circle');
                break;
            default:
                icon.classList.add('fa-circle');
        }
    }
    
    function resetLayerStatus() {
        ['metadata', 'transcript', 'ai'].forEach(layer => {
            updateLayerStatus(layer, 'pending');
        });
    }
    
    function resetForm() {
        generateBtn.disabled = false;
        generateBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate 7-Day Course';
        // Processing status always visible - no need to hide
        progressBar.style.width = '0%';
        resetLayerStatus();
        
        if (processingInterval) {
            clearInterval(processingInterval);
        }
    }
    
    function showError(message) {
        // Remove any existing alerts
        const existingAlert = document.querySelector('.alert-danger');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        // Create new alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.setAttribute('role', 'alert');
        alert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert before the main content
        const main = document.querySelector('main');
        main.insertBefore(alert, main.firstChild);
        
        // Auto-dismiss after 10 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 10000);
    }
    
    // URL parameter handling for pre-filling
    const urlParams = new URLSearchParams(window.location.search);
    const prefilledUrl = urlParams.get('url');
    if (prefilledUrl && validateYouTubeUrl(prefilledUrl)) {
        youtubeUrlInput.value = prefilledUrl;
        youtubeUrlInput.dispatchEvent(new Event('input'));
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (!generateBtn.disabled) {
                courseForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to cancel processing (if implemented)
        if (e.key === 'Escape') {
            // Could implement cancellation here
            console.log('Processing cancellation not implemented');
        }
    });
    
    // Auto-focus URL input on page load
    youtubeUrlInput.focus();
    
    // Paste handling for URLs
    document.addEventListener('paste', function(e) {
        if (document.activeElement !== youtubeUrlInput) {
            const clipboardData = e.clipboardData || window.clipboardData;
            const pastedData = clipboardData.getData('text');
            
            if (validateYouTubeUrl(pastedData)) {
                youtubeUrlInput.value = pastedData;
                youtubeUrlInput.focus();
                youtubeUrlInput.dispatchEvent(new Event('input'));
                e.preventDefault();
            }
        }
    });
    
    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', function() {
            const loadTime = performance.now();
            console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        });
    }
    
    // Service worker registration for offline functionality (future enhancement)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            // Service worker could be implemented for offline course viewing
            console.log('Service worker support detected');
        });
    }
    
    // Error reporting
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
        // Could implement error reporting service here
    });
    
    // Unhandled promise rejection handling
    window.addEventListener('unhandledrejection', function(e) {
        console.error('Unhandled promise rejection:', e.reason);
        // Could implement error reporting service here
    });
});

// Utility functions for export
window.YouTubeCourseGenerator = {
    validateUrl: function(url) {
        const patterns = [
            /^https?:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]+/,
            /^https?:\/\/(www\.)?youtu\.be\/[\w-]+/,
            /^https?:\/\/(www\.)?youtube\.com\/embed\/[\w-]+/,
            /^https?:\/\/(www\.)?youtube\.com\/v\/[\w-]+/,
            /^https?:\/\/m\.youtube\.com\/watch\?v=[\w-]+/,
            /^https?:\/\/(www\.)?youtube\.com\/shorts\/[\w-]+/,
            /^https?:\/\/m\.youtube\.com\/shorts\/[\w-]+/
        ];
        return patterns.some(pattern => pattern.test(url));
    },
    
    extractVideoId: function(url) {
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/,
            /youtube\.com\/watch\?.*v=([^&\n?#]+)/,
            /youtube\.com\/shorts\/([^&\n?#]+)/
        ];
        
        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) {
                return match[1];
            }
        }
        return null;
    }
};
