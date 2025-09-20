// Premium Signup Page Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const form = document.getElementById('signupForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const signupBtn = document.getElementById('signupBtn');
    const passwordToggle = document.getElementById('passwordToggle');
    const passwordStrength = document.getElementById('passwordStrength');
    const strengthFill = passwordStrength.querySelector('.strength-fill');
    const strengthText = passwordStrength.querySelector('.strength-text');
    
    // Form validation states
    const validation = {
        username: false,
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
        
        // Add subtle ripple effect without affecting position
        addPasswordToggleRipple(this);
    });
    
    // Real-time validation
    usernameInput.addEventListener('input', function() {
        validateUsername(this.value);
    });
    
    emailInput.addEventListener('input', function() {
        validateEmail(this.value);
    });
    
    passwordInput.addEventListener('input', function() {
        validatePassword(this.value);
        updatePasswordStrength(this.value);
    });
    
    // Show password strength on focus
    passwordInput.addEventListener('focus', function() {
        passwordStrength.classList.add('visible');
    });
    
    // Form submission with animation
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate all fields
        const isValid = validation.username && validation.email && validation.password;
        
        if (isValid) {
            handleFormSubmission();
        } else {
            // Shake the form for invalid submission
            shakeForm();
        }
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
        
        // Add mouse tracking to card (disabled for better UX)
        // const card = document.getElementById('signupCard');
        // card.addEventListener('mousemove', handleCardTilt);
        // card.addEventListener('mouseleave', resetCardTilt);
    }
    
    function handleCardTilt(e) {
        const card = e.currentTarget;
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        // Reduced rotation values for subtle effect
        const rotateX = (y - centerY) / centerY * -2; // Reduced from -10
        const rotateY = (x - centerX) / centerX * 2;  // Reduced from 10
        
        // Very subtle tilt and no scale change
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    }
    
    function resetCardTilt(e) {
        const card = e.currentTarget;
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
    }
    
    function validateUsername(value) {
        const feedback = document.getElementById('usernameFeedback');
        
        if (value.length === 0) {
            showFeedback(feedback, '', '');
            validation.username = false;
            return;
        }
        
        if (value.length < 3) {
            showFeedback(feedback, 'Username must be at least 3 characters long', 'error');
            validation.username = false;
        } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
            showFeedback(feedback, 'Username can only contain letters, numbers, and underscores', 'error');
            validation.username = false;
        } else {
            showFeedback(feedback, 'Username looks good!', 'success');
            validation.username = true;
        }
        
        updateFormState();
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
            showFeedback(feedback, 'Email format is correct!', 'success');
            validation.email = true;
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
        
        const requirements = [];
        if (value.length < 8) requirements.push('at least 8 characters');
        if (!/[A-Z]/.test(value)) requirements.push('one uppercase letter');
        if (!/[a-z]/.test(value)) requirements.push('one lowercase letter');
        if (!/\d/.test(value)) requirements.push('one number');
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(value)) requirements.push('one special character');
        
        if (requirements.length > 0) {
            showFeedback(feedback, `Password needs: ${requirements.join(', ')}`, 'error');
            validation.password = false;
        } else {
            showFeedback(feedback, 'Strong password!', 'success');
            validation.password = true;
        }
        
        updateFormState();
    }
    
    function updatePasswordStrength(password) {
        let strength = 0;
        let strengthLabel = 'Very Weak';
        
        // Calculate strength
        if (password.length >= 8) strength += 20;
        if (/[A-Z]/.test(password)) strength += 20;
        if (/[a-z]/.test(password)) strength += 20;
        if (/\d/.test(password)) strength += 20;
        if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 20;
        
        // Update strength label
        if (strength === 0) strengthLabel = 'Very Weak';
        else if (strength <= 40) strengthLabel = 'Weak';
        else if (strength <= 60) strengthLabel = 'Fair';
        else if (strength <= 80) strengthLabel = 'Good';
        else strengthLabel = 'Strong';
        
        // Update UI
        strengthFill.style.width = `${strength}%`;
        strengthText.textContent = `Password strength: ${strengthLabel}`;
        
        // Update color based on strength
        if (strength <= 40) {
            strengthFill.style.background = '#f43f5e';
        } else if (strength <= 80) {
            strengthFill.style.background = '#f59e0b';
        } else {
            strengthFill.style.background = '#10b981';
        }
    }
    
    function showFeedback(element, message, type) {
        element.textContent = message;
        element.className = `form-feedback ${type} ${message ? 'visible' : ''}`;
    }
    
    function updateFormState() {
        const allValid = validation.username && validation.email && validation.password;
        
        if (allValid) {
            signupBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
            signupBtn.style.boxShadow = '0 8px 25px rgba(16, 185, 129, 0.3)';
        } else {
            signupBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            signupBtn.style.boxShadow = '0 8px 25px rgba(102, 126, 234, 0.3)';
        }
    }
    
    function addPasswordToggleRipple(element) {
        const ripple = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(102, 126, 234, 0.3);
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
        const card = document.getElementById('signupCard');
        card.style.animation = 'none';
        card.offsetHeight; // Trigger reflow
        card.style.animation = 'shake 0.5s ease-in-out';
        
        setTimeout(() => {
            card.style.animation = '';
        }, 500);
    }
    
    function handleFormSubmission() {
        // Show loading state
        signupBtn.classList.add('loading');
        signupBtn.disabled = true;
        
        // Create FormData object
        const formData = new FormData(form);
        
        // Simulate API call (replace with actual form submission)
        fetch(form.action || window.location.pathname, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // Show success state
                signupBtn.classList.remove('loading');
                signupBtn.classList.add('success');
                
                // Show success modal after a delay
                setTimeout(() => {
                    showSuccessModal();
                }, 1000);
            } else {
                throw new Error('Signup failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Reset button state
            signupBtn.classList.remove('loading');
            signupBtn.disabled = false;
            
            // Show error feedback
            shakeForm();
        });
    }
    
    function showSuccessModal() {
        const modal = document.getElementById('successModal');
        modal.classList.add('visible');
        
        // Redirect after 2 seconds
        setTimeout(() => {
            window.location.href = '/login';
        }, 2000);
    }
    
    // Add shake animation CSS
    const shakeCSS = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
            20%, 40%, 60%, 80% { transform: translateX(10px); }
        }
    `;
    
    const style = document.createElement('style');
    style.textContent = shakeCSS;
    document.head.appendChild(style);
    
    // Enhanced floating shapes interaction
    const shapes = document.querySelectorAll('.shape');
    
    document.addEventListener('mousemove', function(e) {
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 0.01;
            const x = (mouseX - 0.5) * speed * 50;
            const y = (mouseY - 0.5) * speed * 50;
            
            shape.style.transform += ` translate(${x}px, ${y}px)`;
        });
    });
    
    // Add focus animations to inputs (without moving wrapper)
    document.querySelectorAll('.form-input').forEach(input => {
        input.addEventListener('focus', function() {
            // Only animate the input itself, not the wrapper
            this.style.transform = 'translateY(-1px)';
            this.style.transition = 'transform 0.2s ease, box-shadow 0.3s ease, border-color 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Particle effect on successful validation
    function createParticles(element) {
        const particles = 5;
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
    
    // Add particle animation CSS
    const particleCSS = `
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
    `;
    
    const particleStyle = document.createElement('style');
    particleStyle.textContent = particleCSS;
    document.head.appendChild(particleStyle);
    
    // Trigger particles on successful validation
    const originalShowFeedback = showFeedback;
    showFeedback = function(element, message, type) {
        originalShowFeedback(element, message, type);
        if (type === 'success' && message) {
            createParticles(element);
        }
    };
});