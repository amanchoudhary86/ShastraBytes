// About Page Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    console.log('About page JavaScript loaded successfully!');
    console.log('Found stat-items:', document.querySelectorAll('.stat-item').length);
    
    // Initialize all animations and interactions
    initScrollAnimations();
    initCounters();
    initFloatingShapes();
    initTimelineAnimations();
    initParallaxEffects();
    initInteractiveElements();

    // Scroll-triggered animations
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.feature-card').forEach((card, index) => {
            card.classList.add('fade-in-up');
            card.style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
        });

        document.querySelectorAll('.timeline-item').forEach((item, index) => {
            if (index % 2 === 0) {
                item.classList.add('fade-in-left');
            } else {
                item.classList.add('fade-in-right');
            }
            observer.observe(item);
        });

        document.querySelectorAll('.team-member').forEach((member, index) => {
            member.classList.add('fade-in-up');
            member.style.animationDelay = `${index * 0.2}s`;
            observer.observe(member);
        });
    }

    // Animated counters for statistics
    function initCounters() {
        const observerOptions = {
            threshold: 0.3
        };

        const counterObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    const statItem = entry.target.closest('.stat-item');
                    if (statItem) {
                        const targetCount = parseInt(statItem.dataset.count) || 0;
                        const statNumber = statItem.querySelector('.stat-number');
                        const statLabel = statItem.querySelector('.stat-label');
                        
                        let suffix = '+';
                        if (statLabel && statLabel.textContent.includes('Success Rate')) {
                            suffix = '%';
                        } else if (statLabel && statLabel.textContent.includes('Support Available')) {
                            suffix = '/7';
                        }
                        
                        if (statNumber) {
                            animateCounter(statNumber, targetCount, suffix, 2000);
                            entry.target.dataset.animated = 'true';
                        }
                    }
                }
            });
        }, observerOptions);

        // Observe all stat items
        document.querySelectorAll('.stat-item').forEach(statItem => {
            counterObserver.observe(statItem);
        });
    }

    function animateCounter(element, target, suffix, duration) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start) + suffix;
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target + suffix;
            }
        }
        
        updateCounter();
    }

    // Interactive floating shapes
    function initFloatingShapes() {
        const hero = document.querySelector('.hero-section');
        if (!hero) return;

        const existingShapes = document.querySelectorAll('.floating-shapes .shape');
        
        // If shapes already exist, enhance them with mouse interaction
        if (existingShapes.length > 0) {
            // Mouse interaction with existing shapes
            hero.addEventListener('mousemove', function(e) {
                const rect = hero.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                
                existingShapes.forEach((shape, index) => {
                    const factor = (index + 1) * 0.05;
                    const translateX = (x - 0.5) * 30 * factor;
                    const translateY = (y - 0.5) * 30 * factor;
                    
                    shape.style.transform = `translate(${translateX}px, ${translateY}px)`;
                });
            });
            return;
        }

        // Fallback: Create floating shapes if none exist
        const shapesContainer = document.createElement('div');
        shapesContainer.className = 'floating-shapes';
        hero.appendChild(shapesContainer);

        // Create multiple floating shapes
        for (let i = 0; i < 6; i++) {
            const shape = document.createElement('div');
            shape.className = 'floating-shape';
            shape.style.left = Math.random() * 100 + '%';
            shape.style.top = Math.random() * 100 + '%';
            shape.style.animationDelay = Math.random() * 6 + 's';
            shape.style.animationDuration = (6 + Math.random() * 4) + 's';
            shapesContainer.appendChild(shape);
        }

        // Mouse interaction with created shapes
        hero.addEventListener('mousemove', function(e) {
            const rect = hero.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            
            document.querySelectorAll('.floating-shape').forEach((shape, index) => {
                const factor = (index + 1) * 0.1;
                const translateX = (x - 0.5) * 50 * factor;
                const translateY = (y - 0.5) * 50 * factor;
                
                shape.style.transform = `translate(${translateX}px, ${translateY}px)`;
            });
        });
    }

    // Timeline animations
    function initTimelineAnimations() {
        const timelineItems = document.querySelectorAll('.timeline-item');
        
        const timelineObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    
                    // Add stagger effect
                    const content = entry.target.querySelector('.timeline-content');
                    if (content) {
                        content.style.animation = 'slideInUp 0.6s ease forwards';
                    }
                }
            });
        }, { threshold: 0.3 });

        timelineItems.forEach(item => {
            timelineObserver.observe(item);
        });
    }

    // Parallax effects
    function initParallaxEffects() {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const parallaxElements = document.querySelectorAll('.parallax');
            
            parallaxElements.forEach(element => {
                const rate = scrolled * -0.5;
                element.style.transform = `translateY(${rate}px)`;
            });
        });
    }

    // Interactive elements
    function initInteractiveElements() {
        // Feature cards hover effects
        const featureCards = document.querySelectorAll('.feature-card');
        featureCards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-20px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Team member interactions
        const teamMembers = document.querySelectorAll('.team-member');
        teamMembers.forEach(member => {
            member.addEventListener('mouseenter', function() {
                const avatar = this.querySelector('.team-avatar');
                if (avatar) {
                    avatar.style.transform = 'scale(1.1) rotate(360deg)';
                }
            });
            
            member.addEventListener('mouseleave', function() {
                const avatar = this.querySelector('.team-avatar');
                if (avatar) {
                    avatar.style.transform = 'scale(1) rotate(0deg)';
                }
            });
        });

        // Button ripple effect
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                `;
                ripple.className = 'ripple';
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Typing animation for code visualization
    function initTypingAnimation() {
        const codeLines = document.querySelectorAll('.code-line');
        codeLines.forEach((line, index) => {
            line.style.width = '0';
            line.style.animation = `none`;
            
            setTimeout(() => {
                line.style.animation = `typeWriter 0.5s ease forwards, pulse 2s ease-in-out infinite 0.5s`;
            }, index * 200);
        });
    }

    // Initialize code animation when story section is visible
    const storySection = document.querySelector('.story-section');
    if (storySection) {
        const storyObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    initTypingAnimation();
                    storyObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        storyObserver.observe(storySection);
    }

    // Add custom CSS animations
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes typeWriter {
            to {
                width: 100%;
            }
        }
        
        .animate {
            opacity: 1 !important;
            transform: translateY(0) translateX(0) !important;
        }
    `;
    document.head.appendChild(style);

    // Performance optimization: Throttle scroll events
    let ticking = false;
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    // Throttled scroll handler for better performance
    const handleScroll = throttle(function() {
        // Add any scroll-based animations here
    }, 16); // ~60fps

    window.addEventListener('scroll', handleScroll);

    // Preload critical animations
    document.body.style.setProperty('--animation-duration', '0.6s');
    document.body.style.setProperty('--stagger-delay', '0.1s');

    console.log('About page interactive features initialized successfully!');
});

// Utility functions
function createParticleEffect(element, particleCount = 10) {
    const particles = [];
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #667eea;
            border-radius: 50%;
            pointer-events: none;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            animation: particle-float 2s ease-out forwards;
            animation-delay: ${i * 0.1}s;
        `;
        element.appendChild(particle);
        particles.push(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 2000);
    }
}

// Export functions for potential external use
window.AboutPageEffects = {
    createParticleEffect,
    initFloatingShapes,
    initCounters
};