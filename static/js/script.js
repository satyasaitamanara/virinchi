// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // Create animated background elements
    createAnimatedBackground();
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Real-time validation
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearError(this);
            
            // Password strength indicator
            if (this.name === 'password') {
                updatePasswordStrength(this.value);
            }
            
            // Confirm password validation
            if (this.name === 'confirm_password') {
                const password = document.querySelector('input[name="password"]').value;
                if (this.value !== password) {
                    showError(this, 'Passwords do not match');
                } else {
                    clearError(this);
                }
            }
        });
    });
});

// Create animated background
function createAnimatedBackground() {
    const animatedBg = document.createElement('div');
    animatedBg.className = 'animated-bg';
    
    for (let i = 0; i < 8; i++) {
        const circle = document.createElement('div');
        circle.className = 'circle';
        
        // Random size and position
        const size = Math.random() * 100 + 50;
        circle.style.width = `${size}px`;
        circle.style.height = `${size}px`;
        circle.style.top = `${Math.random() * 100}%`;
        circle.style.left = `${Math.random() * 100}%`;
        
        // Random animation delay
        circle.style.animationDelay = `${Math.random() * 10}s`;
        
        animatedBg.appendChild(circle);
    }
    
    document.body.appendChild(animatedBg);
}

// Form validation functions
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('.form-input');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Clear previous error
    clearError(field);
    
    // Validation rules
    if (field.hasAttribute('required') && value === '') {
        errorMessage = 'This field is required';
        isValid = false;
    } else if (fieldName === 'email' && value !== '' && !isValidEmail(value)) {
        errorMessage = 'Please enter a valid email address';
        isValid = false;
    } else if (fieldName === 'password' && value.length < 6) {
        errorMessage = 'Password must be at least 6 characters';
        isValid = false;
    } else if (fieldName === 'confirm_password') {
        const password = document.querySelector('input[name="password"]').value;
        if (value !== password) {
            errorMessage = 'Passwords do not match';
            isValid = false;
        }
    }
    
    // Show error message
    if (!isValid) {
        showError(field, errorMessage);
    }
    
    return isValid;
}

function showError(field, message) {
    const formGroup = field.closest('.form-group');
    let errorElement = formGroup.querySelector('.form-error');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        formGroup.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    field.style.borderColor = '#f72585';
}

function clearError(field) {
    const formGroup = field.closest('.form-group');
    const errorElement = formGroup.querySelector('.form-error');
    
    if (errorElement) {
        errorElement.style.display = 'none';
    }
    
    field.style.borderColor = '#e9ecef';
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Password strength indicator
function updatePasswordStrength(password) {
    const strengthMeter = document.querySelector('.strength-meter');
    if (!strengthMeter) return;
    
    const strength = checkPasswordStrength(password);
    let width = 0;
    let color = '';
    
    switch(strength) {
        case 0:
            width = 0;
            color = '#dc3545';
            break;
        case 1:
            width = 25;
            color = '#dc3545';
            break;
        case 2:
            width = 50;
            color = '#ffc107';
            break;
        case 3:
            width = 75;
            color = '#17a2b8';
            break;
        case 4:
        case 5:
            width = 100;
            color = '#28a745';
            break;
    }
    
    strengthMeter.style.width = `${width}%`;
    strengthMeter.style.background = color;
}

function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[!@#$%^&*(),.?":{}|<>]+/)) strength++;
    
    return strength;
}

// Add floating label effect
document.addEventListener('DOMContentLoaded', function() {
    const formInputs = document.querySelectorAll('.form-input');
    
    formInputs.forEach(input => {
        // Add focus effect
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (this.value === '') {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Check if input has value on page load
        if (input.value !== '') {
            input.parentElement.classList.add('focused');
        }
    });
});

// Add error handling for file downloads
document.addEventListener('DOMContentLoaded', function() {
    // Check for flash messages and display them
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transition = 'opacity 0.5s ease';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
    
    // Add confirmation for delete actions
    const deleteButtons = document.querySelectorAll('a[href*="delete_content"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this content?')) {
                e.preventDefault();
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
        const modal = document.getElementById('pdf-modal');
        const pdfViewer = document.getElementById('pdf-viewer');
        const closeBtn = document.querySelector('.close');
        const viewButtons = document.querySelectorAll('.view-pdf-btn');
        
        // Open modal when View button is clicked
        viewButtons.forEach(button => {
            button.addEventListener('click', function() {
                const filename = this.getAttribute('data-filename');
                const pdfUrl = "{{ url_for('download_file', filename='') }}" + filename;
                
                // Set PDF source and show modal
                pdfViewer.src = pdfUrl;
                modal.style.display = 'block';
                
                // Prevent body scrolling when modal is open
                document.body.style.overflow = 'hidden';
            });
        });
        
        // Close modal when X is clicked
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            pdfViewer.src = '';
            document.body.style.overflow = 'auto';
        });
        
        // Close modal when clicking outside the content
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
                pdfViewer.src = '';
                document.body.style.overflow = 'auto';
            }
        });
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape' && modal.style.display === 'block') {
                modal.style.display = 'none';
                pdfViewer.src = '';
                document.body.style.overflow = 'auto';
            }
        });
    });