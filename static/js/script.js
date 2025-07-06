// DOM elements
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');

// Menu toggle functionality
menuToggle.addEventListener('click', function() {
    // Toggle active state on menu button
    menuToggle.classList.toggle('active');
    
    // Toggle active state on navigation menu
    navMenu.classList.toggle('active');
    
    // Add loading animation class temporarily
    navMenu.classList.add('loading');
    setTimeout(() => {
        navMenu.classList.remove('loading');
    }, 400);
    
    // Update aria-expanded for accessibility
    const isExpanded = navMenu.classList.contains('active');
    menuToggle.setAttribute('aria-expanded', isExpanded);
});

// Close menu when clicking on a navigation link
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        // Close the menu
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        
        // Smooth scroll to section if it's an anchor link
        if (this.getAttribute('href').startsWith('#')) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const isClickInsideMenu = navMenu.contains(event.target);
    const isClickOnToggle = menuToggle.contains(event.target);
    
    if (!isClickInsideMenu && !isClickOnToggle && navMenu.classList.contains('active')) {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
    }
});

// Handle keyboard navigation
menuToggle.addEventListener('keydown', function(event) {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        menuToggle.click();
    }
});

// Handle ESC key to close menu
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && navMenu.classList.contains('active')) {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.focus();
    }
});

// Initialize accessibility attributes
menuToggle.setAttribute('aria-expanded', 'false');

// Add hover effects for nav items
navLinks.forEach(link => {
    link.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(5px)';
    });
    
    link.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
    });
});

// Animate content sections on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
        }
    });
}, observerOptions);

// Observe all content sections
document.querySelectorAll('.content-section').forEach(section => {
    observer.observe(section);
});

// Add CSS for fade in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .content-section {
        opacity: 0;
    }
`;
document.head.appendChild(style);

// Initialize menu state
console.log('SentimentalSocial V2 - Menu functionality initialized');