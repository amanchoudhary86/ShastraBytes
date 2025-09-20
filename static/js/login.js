// Premium Login Page Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('loginBtn');
    const passwordToggle = document.getElementById('passwordToggle');
    
    // Form validation states
    const validation = {
        email: false,
        password: false
    };
    
    // Initialize animations
    initializeAnimations();
    
    // Password toggle functionality
    passwordToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
        
        // Add subtle ripple effect
        addPasswordToggleRipple(this);
    });
    
    // Real-time validation
    emailInput.addEventListener('input', function() {
        validateEmail(this.value);
    });
    
    passwordInput.addEventListener('input', function() {
        validatePassword(this.value);
    });
    
    // Form submission with animation
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all fields
        const isValid = validation.email && validation.password;
        
        if (isValid) {
            handleFormSubmission();
        } else {
            // Shake the form for invalid submission
            shakeForm();
            
            // Show validation errors if fields are empty
            if (!emailInput.value) {
                showFeedback(document.getElementById('emailFeedback'), 'Email is required', 'error');
            }
            if (!passwordInput.value) {
                showFeedback(document.getElementById('passwordFeedback'), 'Password is required', 'error');
            }
        }
    });
    
    // Demo buttons
    document.querySelectorAll('.demo-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            addRippleEffect(this);
            
            // Demo login logic
            if (this.classList.contains('student-demo')) {
                // Fill demo student credentials
                emailInput.value = 'student@demo.com';
                passwordInput.value = 'demo123';
                
                // Trigger validation
                validateEmail('student@demo.com');
                validatePassword('demo123');
                
                // Auto submit after a delay
                setTimeout(() => {
                    handleFormSubmission();
                }, 800);
            } else if (this.classList.contains('recruiter-demo')) {
                // Fill demo recruiter credentials
                emailInput.value = 'recruiter@demo.com';
                passwordInput.value = 'demo123';
                
                // Trigger validation
                validateEmail('recruiter@demo.com');
                validatePassword('demo123');
                
                // Auto submit after a delay
                setTimeout(() => {
                    handleFormSubmission();
                }, 800);
            }
        });
    });
    
    // Functions
    function initializeAnimations() {
        // Stagger form element animations
        const elements = document.querySelectorAll('.form-group');
        elements.forEach((el, index) => {
            el.style.animationDelay = `${0.1 * index}s`;
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.animation = `slideInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${0.1 * index}s forwards`;
        });
    }
    
    function validateEmail(value) {
        const feedback = document.getElementById('emailFeedback');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (value.length === 0) {
            showFeedback(feedback, '', '');
            validation.email = false;
            return;
        }
        
        if (!emailRegex.test(value)) {
            showFeedback(feedback, 'Please enter a valid email address', 'error');
            validation.email = false;
        } else {
            showFeedback(feedback, 'Email looks good!', 'success');
            validation.email = true;
            createParticles(emailInput);
        }
        
        updateFormState();
    }
    
    function validatePassword(value) {
        const feedback = document.getElementById('passwordFeedback');
        
        if (value.length === 0) {
            showFeedback(feedback, '', '');
            validation.password = false;
            return;
        }
        
        if (value.length < 6) {
            showFeedback(feedback, 'Password must be at least 6 characters', 'error');
            validation.password = false;
        } else {
            showFeedback(feedback, 'Password accepted!', 'success');
            validation.password = true;
            createParticles(passwordInput);
        }
        
        updateFormState();
    }
    
    function showFeedback(element, message, type) {
        element.textContent = message;
        element.className = `form-feedback ${type} ${message ? 'visible' : ''}`;
    }
    
    function updateFormState() {
        const allValid = validation.email && validation.password;
        
        if (allValid) {
            loginBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            loginBtn.style.boxShadow = '0 8px 25px rgba(16, 185, 129, 0.3)';
        } else {
            loginBtn.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
            loginBtn.style.boxShadow = '0 8px 25px rgba(79, 172, 254, 0.3)';
        }
    }
    
    function addPasswordToggleRipple(element) {
        const ripple = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(79, 172, 254, 0.3);
            transform: scale(0);
            animation: ripple 0.4s linear;
            width: ${size}px;
            height: ${size}px;
            left: 50%;
            top: 50%;
            margin-left: ${-size/2}px;
            margin-top: ${-size/2}px;
            pointer-events: none;
            z-index: 1;
        `;
        
        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 400);
    }
    
    function addRippleEffect(element) {
        const ripple = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            width: ${size}px;
            height: ${size}px;
            left: 50%;
            top: 50%;
            margin-left: ${-size/2}px;
            margin-top: ${-size/2}px;
            pointer-events: none;
            z-index: 1;
        `;
        
        element.style.position = 'relative';
        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }
    
    function shakeForm() {
        const card = document.getElementById('loginCard');
        card.style.animation = 'none';
        card.offsetHeight; // Trigger reflow
        card.style.animation = 'shake 0.5s ease-in-out';
        
        setTimeout(() => {
            card.style.animation = '';
        }, 500);
    }
    
    function handleFormSubmission() {
        // Show loading state
        loginBtn.classList.add('loading');
        loginBtn.disabled = true;
        
        // Create FormData object
        const formData = new FormData(form);
        
        // Simulate API call (replace with actual form submission)
        fetch(form.action || window.location.pathname, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok || response.redirected) {
                // Show success state
                loginBtn.classList.remove('loading');
                loginBtn.classList.add('success');
                
                // Show success modal after a delay
                setTimeout(() => {
                    showSuccessModal();
                }, 1000);
                
                // Redirect after another delay
                setTimeout(() => {
                    if (response.redirected) {
                        window.location.href = response.url;
                    } else {
                        window.location.href = '/dashboard';
                    }
                }, 2500);
            } else {
                throw new Error('Login failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Reset button state
            loginBtn.classList.remove('loading');
            loginBtn.disabled = false;
            
            // Show error feedback
            showFeedback(document.getElementById('emailFeedback'), 'Invalid email or password', 'error');
            shakeForm();
        });
    }
    
    function showSuccessModal() {
        const modal = document.getElementById('successModal');
        modal.classList.add('visible');
    }
    
    // Particle effect on successful validation
    function createParticles(element) {
        const particles = 3;
        for (let i = 0; i < particles; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: 4px;
                height: 4px;
                background: #10b981;
                border-radius: 50%;
                pointer-events: none;
                animation: particleFloat 1s ease-out forwards;
                z-index: 1000;
            `;
            
            const rect = element.getBoundingClientRect();
            particle.style.left = rect.right - 20 + Math.random() * 10 + 'px';
            particle.style.top = rect.top + rect.height/2 + Math.random() * 10 + 'px';
            
            document.body.appendChild(particle);
            setTimeout(() => particle.remove(), 1000);
        }
    }
    
    // Add required animations CSS
    const animationCSS = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
            20%, 40%, 60%, 80% { transform: translateX(10px); }
        }
        
        @keyframes particleFloat {
            0% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            100% {
                opacity: 0;
                transform: translateY(-30px) scale(0.5);
            }
        }
        
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    
    const style = document.createElement('style');
    style.textContent = animationCSS;
    document.head.appendChild(style);
    
    // Enhanced floating shapes interaction
    const shapes = document.querySelectorAll('.shape');
    
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 0.008;
            const x = (mouseX - 0.5) * speed * 40;
            const y = (mouseY - 0.5) * speed * 40;
            
            shape.style.transform += ` translate(${x}px, ${y}px)`;
        });
    });
    
    // Add focus animations to inputs (without moving wrapper)
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'translateY(-1px)';
            this.style.transition = 'transform 0.2s ease, box-shadow 0.3s ease, border-color 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Auto-fill demo on page load for testing (remove in production)
    // setTimeout(() => {
    //     document.querySelector('.student-demo').click();
    // }, 1000);
});