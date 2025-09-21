// Enhanced Roadmap JavaScript Functionality

class RoadmapManager {
    constructor() {
        this.currentRoadmap = null;
        this.observer = null;
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.setupEventListeners();
        this.setupProgressTracking();
    }

    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                    
                    // Add staggered animation for child elements
                    const children = entry.target.querySelectorAll('.topic-card');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.style.opacity = '1';
                            child.style.transform = 'translateY(0)';
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);
    }

    setupEventListeners() {
        // Topic card interactions
        document.addEventListener('click', (e) => {
            if (e.target.closest('.topic-card')) {
                this.handleTopicClick(e.target.closest('.topic-card'));
            }
        });

        // Progress tracking
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('topic-checkbox')) {
                this.updateProgress();
            }
        });

        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', this.handleSmoothScroll);
        });
    }

    setupProgressTracking() {
        // Initialize progress bar
        this.updateProgressBar();
        
        // Update progress on scroll
        window.addEventListener('scroll', this.throttle(() => {
            this.updateProgressBar();
        }, 100));
    }

    handleTopicClick(topicCard) {
        const topicId = topicCard.getAttribute('data-topic-id');
        const details = topicCard.querySelector('.topic-details');
        
        if (details) {
            this.toggleTopicDetails(topicId, details);
        }
        
        // Add visual feedback
        topicCard.style.transform = 'scale(0.98)';
        setTimeout(() => {
            topicCard.style.transform = '';
        }, 150);
    }

    toggleTopicDetails(topicId, details) {
        if (details.style.display === 'none' || details.style.display === '') {
            details.style.display = 'block';
            details.style.opacity = '0';
            details.style.transform = 'translateY(-10px)';
            
            // Animate in
            requestAnimationFrame(() => {
                details.style.transition = 'all 0.3s ease';
                details.style.opacity = '1';
                details.style.transform = 'translateY(0)';
            });
        } else {
            // Animate out
            details.style.transition = 'all 0.3s ease';
            details.style.opacity = '0';
            details.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                details.style.display = 'none';
            }, 300);
        }
    }

    updateProgress() {
        const completedTopics = document.querySelectorAll('.topic-checkbox:checked').length;
        const totalTopics = document.querySelectorAll('.topic-checkbox').length;
        const progress = totalTopics > 0 ? (completedTopics / totalTopics) * 100 : 0;
        
        this.updateProgressBar(progress);
        
        // Update phase completion
        this.updatePhaseCompletion();
        
        // Show completion celebration if 100%
        if (progress === 100) {
            this.showCompletionCelebration();
        }
    }

    updateProgressBar(progress = null) {
        const progressBar = document.getElementById('progressBar');
        if (!progressBar) return;
        
        if (progress === null) {
            // Calculate based on visible progress
            const completedTopics = document.querySelectorAll('.topic-status.completed').length;
            const totalTopics = document.querySelectorAll('.topic-status').length;
            progress = totalTopics > 0 ? (completedTopics / totalTopics) * 100 : 0;
        }
        
        progressBar.style.width = progress + '%';
        
        // Add glow effect for high progress
        if (progress > 80) {
            progressBar.style.boxShadow = '0 0 20px rgba(0, 212, 255, 0.8)';
        } else {
            progressBar.style.boxShadow = '0 0 10px rgba(0, 212, 255, 0.5)';
        }
    }

    updatePhaseCompletion() {
        const phases = document.querySelectorAll('.roadmap-phase');
        
        phases.forEach(phase => {
            const topics = phase.querySelectorAll('.topic-card');
            const completedTopics = phase.querySelectorAll('.topic-status.completed');
            const phaseProgress = topics.length > 0 ? (completedTopics.length / topics.length) * 100 : 0;
            
            // Update phase visual state
            if (phaseProgress === 100) {
                phase.classList.add('phase-completed');
            } else if (phaseProgress > 0) {
                phase.classList.add('phase-in-progress');
            }
        });
    }

    showCompletionCelebration() {
        // Create celebration element
        const celebration = document.createElement('div');
        celebration.className = 'roadmap-complete';
        celebration.innerHTML = `
            <h2>🎉 Congratulations!</h2>
            <p>You've completed your learning roadmap!</p>
            <div class="celebration-animation">
                <div class="confetti"></div>
                <div class="confetti"></div>
                <div class="confetti"></div>
                <div class="confetti"></div>
                <div class="confetti"></div>
            </div>
        `;
        
        // Add to page
        const container = document.querySelector('.roadmap-container');
        container.appendChild(celebration);
        
        // Remove after 5 seconds
        setTimeout(() => {
            celebration.remove();
        }, 5000);
    }

    handleSmoothScroll(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    // Utility function for throttling
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Public methods for external use
    generateRoadmap(roadmapData) {
        this.currentRoadmap = roadmapData;
        this.displayRoadmap(roadmapData);
    }

    displayRoadmap(roadmap) {
        // This would be called from the main roadmap page
        // Implementation depends on the specific roadmap structure
        console.log('Displaying roadmap:', roadmap);
    }

    saveProgress() {
        // Save progress to backend
        const progressData = this.getProgressData();
        
        fetch('/update-roadmap-progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(progressData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Progress saved successfully!', 'success');
            } else {
                this.showNotification('Error saving progress: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.showNotification('Error saving progress', 'error');
        });
    }

    getProgressData() {
        const completedTopics = Array.from(document.querySelectorAll('.topic-checkbox:checked'))
            .map(checkbox => checkbox.getAttribute('data-topic-id'));
        
        return {
            completed_topics: completedTopics,
            progress_percentage: this.calculateProgressPercentage()
        };
    }

    calculateProgressPercentage() {
        const completedTopics = document.querySelectorAll('.topic-checkbox:checked').length;
        const totalTopics = document.querySelectorAll('.topic-checkbox').length;
        return totalTopics > 0 ? Math.round((completedTopics / totalTopics) * 100) : 0;
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '600',
            zIndex: '10000',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });
        
        // Set background color based on type
        const colors = {
            success: '#6bcf7f',
            error: '#ff6b6b',
            info: '#00d4ff',
            warning: '#ffd93d'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
        });
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
}

// Initialize roadmap manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.roadmapManager = new RoadmapManager();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RoadmapManager;
}
