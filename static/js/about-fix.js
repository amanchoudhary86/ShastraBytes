// Complete About Page JavaScript Fix
document.addEventListener('DOMContentLoaded', function() {
    console.log('About page complete fix loaded!');
    
    // 1. Counter Animations
    function animateCounters() {
        const statItems = document.querySelectorAll('.stat-item');
        console.log('Found stat items:', statItems.length);
        
        statItems.forEach((item, index) => {
            const targetCount = parseInt(item.dataset.count) || 0;
            const statNumber = item.querySelector('.stat-number');
            const statLabel = item.querySelector('.stat-label');
            
            if (statNumber && targetCount > 0) {
                console.log('Animating counter for:', targetCount);
                
                let suffix = '+';
                if (statLabel && statLabel.textContent.includes('Success Rate')) {
                    suffix = '%';
                } else if (statLabel && statLabel.textContent.includes('Support Available')) {
                    suffix = '/7';
                }
                
                let current = 0;
                const increment = targetCount / 60; // 60 steps for smooth animation
                
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= targetCount) {
                        current = targetCount;
                        clearInterval(timer);
                    }
                    statNumber.textContent = Math.floor(current) + suffix;
                }, 30); // 30ms interval
            }
        });
    }
    
    // 2. Enhanced floating shapes interaction
    function initFloatingShapes() {
        const heroSection = document.querySelector('.hero-section');
        const shapes = document.querySelectorAll('.floating-shapes .shape');
        
        if (heroSection && shapes.length > 0) {
            heroSection.addEventListener('mousemove', function(e) {
                const rect = heroSection.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                
                shapes.forEach((shape, index) => {
                    const factor = (index + 1) * 0.03; // Subtle movement
                    const translateX = (x - 0.5) * 20 * factor;
                    const translateY = (y - 0.5) * 20 * factor;
                    
                    shape.style.transform = `translate(${translateX}px, ${translateY}px)`;
                });
            });
            
            // Reset on mouse leave
            heroSection.addEventListener('mouseleave', function() {
                shapes.forEach(shape => {
                    shape.style.transform = 'translate(0, 0)';
                });
            });
        }
    }
    
    // 3. Scroll animations using Intersection Observer
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Animate feature cards
        document.querySelectorAll('.feature-card').forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = `all 0.6s ease ${index * 0.1}s`;
            observer.observe(card);
        });

        // Animate team members
        document.querySelectorAll('.team-member').forEach((member, index) => {
            member.style.opacity = '0';
            member.style.transform = 'translateY(30px)';
            member.style.transition = `all 0.6s ease ${index * 0.15}s`;
            observer.observe(member);
        });
    }
    
    // 4. Button interactions
    function initButtonEffects() {
        document.querySelectorAll('.btn-premium').forEach(button => {
            button.addEventListener('click', function(e) {
                // Create ripple effect
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${x}px;
                    top: ${y}px;
                    background: rgba(255, 255, 255, 0.6);
                    border-radius: 50%;
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // 5. Chart animations for story section
    function initChartAnimations() {
        const chartBars = document.querySelectorAll('.chart-bar');
        chartBars.forEach((bar, index) => {
            const height = bar.style.height;
            bar.style.setProperty('--height', height);
            bar.style.height = '0';
            
            setTimeout(() => {
                bar.style.transition = 'height 1s ease';
                bar.style.height = height;
            }, 1000 + index * 200);
        });
    }
    
    // Initialize all features
    setTimeout(() => {
        animateCounters();
        initFloatingShapes();
        initScrollAnimations();
        initButtonEffects();
        initChartAnimations();
    }, 500);
    
    // Add CSS for animations
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .feature-card:hover {
            animation: pulse-glow 2s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); }
            50% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2); }
        }
    `;
    document.head.appendChild(style);
    
    console.log('All About page animations initialized successfully!');
});