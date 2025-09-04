// Ethiopian Hospital ERP - Enhanced Homepage JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all homepage enhancements
    initSmoothScrolling();
    initDynamicNavbar();
    initParallaxScrolling();
    initAdvanced3DEffects();
    initFloatingAnimations();
    initEnhancedCounters();
    initHeroImageEffects();
    initAboutSectionEffects();
    initDemoSectionEffects();
    initDoctorOptimizations();
    initMobileDoctorsCarousel();
    initModernContactForm();
    initDemoInteractions();
    initWhyChooseSection();
    initModernFooter();
    initContactFormEnhancements();
    initPerformanceOptimizations();
    initAccessibilityFeatures();
});

// Enhanced Smooth Scrolling with Easing
function initSmoothScrolling() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const navbarHeight = 70; // Account for fixed navbar
                const targetPosition = targetElement.offsetTop - navbarHeight;

                // Enhanced smooth scrolling with easing
                smoothScrollTo(targetPosition, 800);
            }
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const navbarHeight = 70;
                    const targetPosition = target.offsetTop - navbarHeight;

                    smoothScrollTo(targetPosition, 800);
                }
            }
        });
    });
}

// Custom smooth scroll function with easing
function smoothScrollTo(targetPosition, duration) {
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = easeInOutQuad(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }

    function easeInOutQuad(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
}

// Fixed Dynamic Navbar Functionality
function initDynamicNavbar() {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    let ticking = false;

    // Ensure navbar is always visible and sticky
    navbar.style.position = 'fixed';
    navbar.style.top = '0';
    navbar.style.left = '0';
    navbar.style.right = '0';
    navbar.style.width = '100%';
    navbar.style.zIndex = '1050';

    function updateNavbar() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Add scrolled class when scrolling down
        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Keep navbar always visible (remove hide/show functionality)
        navbar.style.transform = 'translateY(0)';

        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }

    window.addEventListener('scroll', requestTick, { passive: true });

    // Add smooth transition
    navbar.style.transition = 'background-color 0.3s ease, backdrop-filter 0.3s ease';

    // Initial call to set proper state
    updateNavbar();
}

// Optimized Parallax Scrolling for Better Performance
function initParallaxScrolling() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    if (parallaxElements.length === 0) return;

    let ticking = false;
    let lastScrollTop = 0;

    // Throttle parallax updates for better performance
    function updateParallax() {
        const scrollTop = window.pageYOffset;

        // Only update if scroll position changed significantly
        if (Math.abs(scrollTop - lastScrollTop) < 2) {
            ticking = false;
            return;
        }

        parallaxElements.forEach(element => {
            const speed = parseFloat(element.dataset.parallax) || 0.3; // Reduced default speed
            const yPos = -(scrollTop * speed);
            element.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });

        lastScrollTop = scrollTop;
        ticking = false;
    }

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }

    // Use passive scroll listener for better performance
    window.addEventListener('scroll', requestTick, { passive: true });
}

// Advanced 3D Effects
function initAdvanced3DEffects() {
    // Exclude doctor cards from heavy 3D effects for performance
    const cards3D = document.querySelectorAll('.card-3d:not(.doctor-card)');

    cards3D.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 15;
            const rotateY = (centerX - x) / 15;

            const inner = this.querySelector('.card-3d-inner');
            if (inner) {
                inner.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
            }
        });

        card.addEventListener('mouseleave', function() {
            const inner = this.querySelector('.card-3d-inner');
            if (inner) {
                inner.style.transform = 'rotateX(0deg) rotateY(0deg) translateZ(0px)';
            }
        });
    });

    // Enhanced icon 3D effects
    const icons3D = document.querySelectorAll('.icon-3d');
    icons3D.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'translateZ(10px) rotateY(15deg) scale(1.1)';
        });

        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'translateZ(0px) rotateY(0deg) scale(1)';
        });
    });

    // Enhanced image 3D effects
    const images3D = document.querySelectorAll('.img-3d');
    images3D.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'translateZ(10px) rotateY(5deg) rotateX(2deg) scale(1.05)';
        });

        img.addEventListener('mouseleave', function() {
            this.style.transform = 'translateZ(0px) rotateY(0deg) rotateX(0deg) scale(1)';
        });
    });
}

// Optimized Floating Animations with Performance Improvements
function initFloatingAnimations() {
    const floatingElements = document.querySelectorAll('.float-gentle, .float-medium, .float-strong');

    floatingElements.forEach((element) => {
        const delay = Math.random() * 3; // Random delay up to 3 seconds for better distribution
        element.style.animationDelay = `${delay}s`;

        // Add will-change property for better performance
        element.style.willChange = 'transform';

        // Remove will-change after animation starts to free up resources
        setTimeout(() => {
            element.style.willChange = 'auto';
        }, (delay + 1) * 1000);
    });
}

// Enhanced Counter Animation
function initEnhancedCounters() {
    const counters = document.querySelectorAll('.counter-3d');
    
    const animateCounter = (counter) => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2500;
        let current = 0;
        
        const easeOutQuart = (t) => 1 - (--t) * t * t * t;
        
        const startTime = performance.now();
        
        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easedProgress = easeOutQuart(progress);
            
            current = target * easedProgress;
            counter.textContent = Math.floor(current).toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
                // Add completion effect
                counter.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    counter.style.transform = 'scale(1)';
                }, 200);
            }
        };
        
        requestAnimationFrame(updateCounter);
    };
    
    // Intersection Observer for counter animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                entry.target.classList.add('animated');
                animateCounter(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => observer.observe(counter));
}





// Enhanced Contact Form
function initContactFormEnhancements() {
    const form = document.querySelector('#contact-form');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea');
    
    inputs.forEach(input => {
        // Enhanced floating labels
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            this.style.transform = 'translateZ(5px)';
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
            this.style.transform = 'translateZ(0px)';
        });
        
        // Real-time validation with visual feedback
        input.addEventListener('input', function() {
            clearTimeout(this.validationTimeout);
            this.validationTimeout = setTimeout(() => {
                validateFieldEnhanced(this);
            }, 500);
        });
    });
    
    // Enhanced form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Animate submit button
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
        submitBtn.disabled = true;
        submitBtn.style.transform = 'scale(0.95)';
        
        // Simulate form submission
        setTimeout(() => {
            submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
            submitBtn.style.background = 'var(--primary-green)';
            
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                submitBtn.style.transform = 'scale(1)';
                submitBtn.style.background = '';
                form.reset();
            }, 2000);
        }, 1500);
    });
}

// Enhanced Field Validation
function validateFieldEnhanced(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    
    // Clear previous validation
    field.classList.remove('is-valid', 'is-invalid');
    
    if (required && !value) {
        showFieldErrorEnhanced(field, 'This field is required');
        return false;
    }
    
    if (type === 'email' && value && !isValidEmail(value)) {
        showFieldErrorEnhanced(field, 'Please enter a valid email address');
        return false;
    }
    
    if (field.hasAttribute('data-phone') && value && !isValidEthiopianPhone(value)) {
        showFieldErrorEnhanced(field, 'Please enter a valid Ethiopian phone number');
        return false;
    }
    
    showFieldSuccessEnhanced(field);
    return true;
}

function showFieldErrorEnhanced(field, message) {
    field.classList.add('is-invalid');
    field.style.borderColor = 'var(--primary-red)';
    field.style.boxShadow = '0 0 10px rgba(218, 2, 14, 0.3)';
    
    let feedback = field.parentElement.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentElement.appendChild(feedback);
    }
    feedback.textContent = message;
}

function showFieldSuccessEnhanced(field) {
    field.classList.add('is-valid');
    field.style.borderColor = 'var(--primary-green)';
    field.style.boxShadow = '0 0 10px rgba(0, 150, 57, 0.3)';
    
    const feedback = field.parentElement.querySelector('.invalid-feedback');
    if (feedback) feedback.remove();
}

// Enhanced Performance Optimizations
function initPerformanceOptimizations() {
    // Lazy load images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Optimize animations for mobile and low-end devices
    if (window.innerWidth <= 768 || navigator.hardwareConcurrency <= 4) {
        document.body.classList.add('mobile-optimized');

        // Disable parallax on mobile
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        parallaxElements.forEach(el => {
            el.removeAttribute('data-parallax');
            el.style.transform = 'none';
        });
    }

    // Optimize will-change usage
    const animatedElements = document.querySelectorAll('.float-gentle, .float-medium, .float-strong');
    animatedElements.forEach(element => {
        // Remove will-change after animation completes one cycle
        const animationDuration = parseFloat(getComputedStyle(element).animationDuration) * 1000;
        setTimeout(() => {
            element.style.willChange = 'auto';
        }, animationDuration);
    });

    // Throttle resize events
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            if (window.innerWidth <= 768) {
                document.body.classList.add('mobile-optimized');
            } else {
                document.body.classList.remove('mobile-optimized');
            }
        }, 250);
    });
}

// Accessibility Features
function initAccessibilityFeatures() {
    // Keyboard navigation for cards (exclude doctor cards for performance)
    const interactiveCards = document.querySelectorAll('.card-3d:not(.doctor-card), .service-card-enhanced');
    
    interactiveCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        card.addEventListener('focus', function() {
            this.style.outline = '3px solid var(--primary-blue)';
            this.style.outlineOffset = '2px';
        });
        
        card.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
    
    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.body.classList.add('reduced-motion');
    }
}

// Enhanced Hero Image Effects
function initHeroImageEffects() {
    const heroImageWrapper = document.querySelector('.hero-image-wrapper');
    const heroLeadImage = document.querySelector('.hero-lead-image');
    const floatingIcons = document.querySelectorAll('.floating-icon');

    if (heroImageWrapper && heroLeadImage) {
        // Add parallax effect to hero image
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;

            if (scrolled < window.innerHeight) {
                heroLeadImage.style.transform = `translateY(${rate}px) translateZ(20px)`;
            }
        }, { passive: true });

        // Add mouse movement effect
        heroImageWrapper.addEventListener('mousemove', (e) => {
            const rect = heroImageWrapper.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            heroImageWrapper.style.transform = `translateZ(30px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });

        heroImageWrapper.addEventListener('mouseleave', () => {
            heroImageWrapper.style.transform = 'translateZ(0) rotateX(0) rotateY(0) scale(1)';
        });
    }

    // Animate floating icons on scroll
    if (floatingIcons.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = `float-gentle 3s ease-in-out infinite`;
                    entry.target.style.animationDelay = `${Math.random() * 2}s`;
                }
            });
        }, { threshold: 0.5 });

        floatingIcons.forEach(icon => observer.observe(icon));
    }
}

// Enhanced About Section Effects
function initAboutSectionEffects() {
    const aboutImage = document.querySelector('.about-main-image');
    const featureItems = document.querySelectorAll('.feature-item');

    if (aboutImage) {
        // Add tilt effect to about image
        aboutImage.addEventListener('mousemove', (e) => {
            const rect = aboutImage.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            aboutImage.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });

        aboutImage.addEventListener('mouseleave', () => {
            aboutImage.style.transform = 'rotateX(0) rotateY(0) scale(1)';
        });
    }

    // Animate feature items on scroll
    if (featureItems.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, { threshold: 0.3 });

        featureItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'all 0.6s ease';
            observer.observe(item);
        });
    }
}

// Enhanced Demo Section Effects
function initDemoSectionEffects() {
    const demoImage = document.querySelector('.demo-image');
    const pulseRings = document.querySelectorAll('.pulse-ring');

    if (demoImage) {
        // Add hover effect to demo image
        demoImage.addEventListener('mouseenter', () => {
            pulseRings.forEach(ring => {
                ring.style.animationPlayState = 'paused';
            });
        });

        demoImage.addEventListener('mouseleave', () => {
            pulseRings.forEach(ring => {
                ring.style.animationPlayState = 'running';
            });
        });

        // Add scroll-triggered animation
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 1s ease forwards';
                }
            });
        }, { threshold: 0.3 });

        observer.observe(demoImage);
    }
}

// Performance-Optimized Doctor Section
function initDoctorOptimizations() {
    const doctorCards = document.querySelectorAll('.doctor-card');

    if (doctorCards.length === 0) return;

    // Optimize will-change usage for doctor cards
    doctorCards.forEach(card => {
        // Only add will-change on hover to save memory
        card.addEventListener('mouseenter', () => {
            card.style.willChange = 'transform, box-shadow';
        }, { passive: true });

        card.addEventListener('mouseleave', () => {
            // Remove will-change after transition completes
            setTimeout(() => {
                card.style.willChange = 'auto';
            }, 400); // Match transition duration
        }, { passive: true });

        // Optimize for touch devices
        card.addEventListener('touchstart', () => {
            card.style.willChange = 'transform';
        }, { passive: true });

        card.addEventListener('touchend', () => {
            setTimeout(() => {
                card.style.willChange = 'auto';
            }, 200);
        }, { passive: true });
    });

    // Intersection Observer for doctor section performance
    const doctorObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Enable animations when in viewport
                entry.target.classList.add('doctor-visible');
            } else {
                // Disable animations when out of viewport to save resources
                entry.target.classList.remove('doctor-visible');
                // Reset will-change when out of view
                entry.target.style.willChange = 'auto';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px 0px'
    });

    doctorCards.forEach(card => {
        doctorObserver.observe(card);
    });

    // Disable complex animations on low-end devices
    if (navigator.hardwareConcurrency <= 4 || window.innerWidth <= 768) {
        doctorCards.forEach(card => {
            card.classList.add('doctor-simplified');
        });
    }

    // Throttle scroll events for doctor section
    let doctorScrollTicking = false;

    function optimizeDoctorScroll() {
        if (!doctorScrollTicking) {
            requestAnimationFrame(() => {
                const windowHeight = window.innerHeight;

                // Check if doctor section is in viewport
                const doctorSection = document.querySelector('.doctor-card').closest('section');
                if (doctorSection) {
                    const rect = doctorSection.getBoundingClientRect();
                    const isInViewport = rect.top < windowHeight && rect.bottom > 0;

                    if (!isInViewport) {
                        // Disable animations when section is not visible
                        doctorCards.forEach(card => {
                            card.style.willChange = 'auto';
                        });
                    }
                }

                doctorScrollTicking = false;
            });
            doctorScrollTicking = true;
        }
    }

    window.addEventListener('scroll', optimizeDoctorScroll, { passive: true });
}

// Mobile Doctors Carousel with Swipe Support
function initMobileDoctorsCarousel() {
    const carousel = document.querySelector('.doctors-mobile-carousel');
    const track = document.getElementById('doctorsTrack');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dots = document.querySelectorAll('.dot');

    if (!carousel || !track || slides.length === 0) return;

    let currentSlide = 0;
    let isTransitioning = false;

    // Touch/Swipe variables
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    let startTime = 0;

    const slideWidth = 100; // Percentage
    const minSwipeDistance = 50; // Minimum distance for swipe
    const maxSwipeTime = 300; // Maximum time for swipe gesture

    // Update carousel position
    function updateCarousel(animate = true) {
        if (isTransitioning) return;

        isTransitioning = true;

        if (animate) {
            track.style.transition = 'transform 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
        } else {
            track.style.transition = 'none';
        }

        track.style.transform = `translateX(-${currentSlide * slideWidth}%)`;

        // Update dots
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });

        // Update button states
        prevBtn.disabled = currentSlide === 0;
        nextBtn.disabled = currentSlide === slides.length - 1;

        setTimeout(() => {
            isTransitioning = false;
        }, 400);
    }

    // Go to specific slide
    function goToSlide(slideIndex, animate = true) {
        if (slideIndex < 0 || slideIndex >= slides.length || slideIndex === currentSlide) return;
        currentSlide = slideIndex;
        updateCarousel(animate);
    }

    // Next slide
    function nextSlide() {
        if (currentSlide < slides.length - 1) {
            goToSlide(currentSlide + 1);
        }
    }

    // Previous slide
    function prevSlide() {
        if (currentSlide > 0) {
            goToSlide(currentSlide - 1);
        }
    }

    // Touch start
    function handleTouchStart(e) {
        if (isTransitioning) return;

        isDragging = true;
        startX = e.touches ? e.touches[0].clientX : e.clientX;
        currentX = startX;
        startTime = Date.now();

        track.style.transition = 'none';
        carousel.style.cursor = 'grabbing';

        // Prevent text selection
        e.preventDefault();
    }

    // Touch move
    function handleTouchMove(e) {
        if (!isDragging) return;

        currentX = e.touches ? e.touches[0].clientX : e.clientX;
        const deltaX = currentX - startX;
        const movePercentage = (deltaX / carousel.offsetWidth) * 100;

        // Apply resistance at boundaries
        let resistance = 1;
        if ((currentSlide === 0 && deltaX > 0) ||
            (currentSlide === slides.length - 1 && deltaX < 0)) {
            resistance = 0.3;
        }

        const translateX = -currentSlide * slideWidth + (movePercentage * resistance);
        track.style.transform = `translateX(${translateX}%)`;

        e.preventDefault();
    }

    // Touch end
    function handleTouchEnd() {
        if (!isDragging) return;

        isDragging = false;
        carousel.style.cursor = 'grab';

        const deltaX = currentX - startX;
        const deltaTime = Date.now() - startTime;
        const velocity = Math.abs(deltaX) / deltaTime;

        // Determine if swipe was significant enough
        const isSignificantSwipe = Math.abs(deltaX) > minSwipeDistance ||
                                  (velocity > 0.5 && deltaTime < maxSwipeTime);

        if (isSignificantSwipe) {
            if (deltaX > 0 && currentSlide > 0) {
                // Swipe right - go to previous slide
                prevSlide();
            } else if (deltaX < 0 && currentSlide < slides.length - 1) {
                // Swipe left - go to next slide
                nextSlide();
            } else {
                // Snap back to current slide
                updateCarousel();
            }
        } else {
            // Snap back to current slide
            updateCarousel();
        }
    }

    // Event listeners for touch/mouse
    carousel.addEventListener('touchstart', handleTouchStart, { passive: false });
    carousel.addEventListener('touchmove', handleTouchMove, { passive: false });
    carousel.addEventListener('touchend', handleTouchEnd, { passive: true });

    // Mouse events for desktop testing
    carousel.addEventListener('mousedown', handleTouchStart);
    carousel.addEventListener('mousemove', handleTouchMove);
    carousel.addEventListener('mouseup', handleTouchEnd);
    carousel.addEventListener('mouseleave', handleTouchEnd);

    // Button event listeners
    prevBtn?.addEventListener('click', prevSlide);
    nextBtn?.addEventListener('click', nextSlide);

    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Keyboard navigation
    carousel.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            prevSlide();
            e.preventDefault();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            e.preventDefault();
        }
    });

    // Make carousel focusable for keyboard navigation
    carousel.setAttribute('tabindex', '0');
    carousel.style.cursor = 'grab';

    // Auto-hide swipe hint after first interaction
    let hasInteracted = false;
    function hideSwipeHint() {
        if (!hasInteracted) {
            hasInteracted = true;
            const swipeIndicators = document.querySelector('.mobile-swipe-indicators');
            if (swipeIndicators) {
                setTimeout(() => {
                    swipeIndicators.style.opacity = '0.7';
                    swipeIndicators.style.transform = 'scale(0.95)';
                }, 2000);
            }
        }
    }

    carousel.addEventListener('touchstart', hideSwipeHint, { once: true });
    carousel.addEventListener('mousedown', hideSwipeHint, { once: true });

    // Initialize
    updateCarousel(false);

    // Add visual feedback for touch
    carousel.style.touchAction = 'pan-y pinch-zoom';
}

// Modern Contact Form Functionality
function initModernContactForm() {
    const form = document.getElementById('modern-contact-form');
    const inputs = form?.querySelectorAll('.modern-form-input, .modern-form-select, .modern-form-textarea');
    const submitBtn = form?.querySelector('.modern-submit-btn');
    const fileInput = form?.querySelector('#contactAttachment');

    if (!form) return;

    // Real-time validation
    inputs?.forEach(input => {
        input.addEventListener('input', validateField);
        input.addEventListener('blur', validateField);
        input.addEventListener('focus', clearFieldError);
    });

    // File upload handling
    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }

    // Form submission
    form.addEventListener('submit', handleFormSubmit);

    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        const fieldType = field.type || field.tagName.toLowerCase();
        const feedback = field.parentElement.querySelector('.form-validation-feedback');

        let isValid = true;
        let message = '';

        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            message = 'This field is required';
        }

        // Email validation
        else if (fieldType === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                message = 'Please enter a valid email address';
            }
        }

        // Phone validation
        else if (fieldType === 'tel' && value) {
            const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
            if (!phoneRegex.test(value.replace(/[\s\-\(\)]/g, ''))) {
                isValid = false;
                message = 'Please enter a valid phone number';
            }
        }

        // Name validation
        else if ((field.id.includes('Name') || field.id.includes('name')) && value) {
            if (value.length < 2) {
                isValid = false;
                message = 'Name must be at least 2 characters';
            }
        }

        // Message validation
        else if (field.id === 'contactMessage' && value) {
            if (value.length < 10) {
                isValid = false;
                message = 'Message must be at least 10 characters';
            }
        }

        // Update field appearance and feedback
        updateFieldValidation(field, feedback, isValid, message);

        return isValid;
    }

    function clearFieldError(e) {
        const field = e.target;
        const feedback = field.parentElement.querySelector('.form-validation-feedback');

        field.classList.remove('invalid');
        if (feedback) {
            feedback.classList.remove('error');
            feedback.style.opacity = '0';
        }
    }

    function updateFieldValidation(field, feedback, isValid, message) {
        if (isValid && field.value.trim()) {
            field.classList.remove('invalid');
            field.classList.add('valid');
            if (feedback) {
                feedback.textContent = 'Looks good!';
                feedback.classList.remove('error');
                feedback.classList.add('success');
                feedback.style.opacity = '1';
            }
        } else if (!isValid) {
            field.classList.remove('valid');
            field.classList.add('invalid');
            if (feedback) {
                feedback.textContent = message;
                feedback.classList.remove('success');
                feedback.classList.add('error');
                feedback.style.opacity = '1';
            }
        } else {
            field.classList.remove('valid', 'invalid');
            if (feedback) {
                feedback.style.opacity = '0';
            }
        }
    }

    function handleFileUpload(e) {
        const file = e.target.files[0];
        const wrapper = e.target.closest('.file-upload-wrapper');
        const label = wrapper.querySelector('.file-upload-label');
        const progress = wrapper.querySelector('.file-upload-progress');

        if (file) {
            // Validate file size (10MB limit)
            if (file.size > 10 * 1024 * 1024) {
                alert('File size must be less than 10MB');
                e.target.value = '';
                return;
            }

            // Update label text
            label.querySelector('.file-upload-text').textContent = file.name;

            // Simulate upload progress
            progress.classList.add('active');
            const progressBar = progress.querySelector('.progress-bar');
            let width = 0;
            const interval = setInterval(() => {
                width += Math.random() * 30;
                if (width >= 100) {
                    width = 100;
                    clearInterval(interval);
                    setTimeout(() => {
                        progress.classList.remove('active');
                    }, 500);
                }
                progressBar.style.width = width + '%';
            }, 100);
        }
    }

    function handleFormSubmit(e) {
        e.preventDefault();

        // Validate all fields
        let isFormValid = true;
        inputs.forEach(input => {
            const fieldValid = validateField({ target: input });
            if (!fieldValid) isFormValid = false;
        });

        if (!isFormValid) {
            showFormMessage('error', 'Please correct the errors above');
            return;
        }

        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;

        // Simulate form submission
        setTimeout(() => {
            // Reset form
            form.reset();
            inputs.forEach(input => {
                input.classList.remove('valid', 'invalid');
                const feedback = input.parentElement.querySelector('.form-validation-feedback');
                if (feedback) feedback.style.opacity = '0';
            });

            // Reset file upload
            const fileLabel = form.querySelector('.file-upload-text');
            if (fileLabel) fileLabel.textContent = 'Attach Documents (Optional)';

            // Show success message
            showFormMessage('success', 'Message sent successfully! We\'ll get back to you soon.');

            // Reset button
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }, 2000);
    }

    function showFormMessage(type, message) {
        const successMsg = form.querySelector('.status-success');
        const errorMsg = form.querySelector('.status-error');

        // Hide all messages first
        successMsg.classList.remove('show');
        errorMsg.classList.remove('show');

        // Show appropriate message
        setTimeout(() => {
            if (type === 'success') {
                successMsg.querySelector('span').textContent = message;
                successMsg.classList.add('show');
            } else {
                errorMsg.querySelector('span').textContent = message;
                errorMsg.classList.add('show');
            }

            // Auto-hide after 5 seconds
            setTimeout(() => {
                successMsg.classList.remove('show');
                errorMsg.classList.remove('show');
            }, 5000);
        }, 100);
    }
}

// Demo Interactions Functionality
function initDemoInteractions() {
    const demoPlayBtn = document.querySelector('[data-demo-trigger]');
    const demoRequestBtn = document.querySelector('[data-demo-request]');
    const brochureBtn = document.querySelector('[data-brochure-download]');
    const progressBars = document.querySelectorAll('.feature-progress .progress-bar');
    const statCounters = document.querySelectorAll('[data-counter]');

    // Demo play button
    if (demoPlayBtn) {
        demoPlayBtn.addEventListener('click', handleDemoPlay);
    }

    // Demo request button
    if (demoRequestBtn) {
        demoRequestBtn.addEventListener('click', handleDemoRequest);
    }

    // Brochure download button
    if (brochureBtn) {
        brochureBtn.addEventListener('click', handleBrochureDownload);
    }

    // Animate progress bars when in view
    if (progressBars.length > 0) {
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBar = entry.target;
                    const progress = progressBar.getAttribute('data-progress') || 0;

                    setTimeout(() => {
                        progressBar.style.width = progress + '%';
                    }, Math.random() * 500);

                    progressObserver.unobserve(progressBar);
                }
            });
        }, { threshold: 0.3 });

        progressBars.forEach(bar => progressObserver.observe(bar));
    }

    // Animate counters when in view
    if (statCounters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statCounters.forEach(counter => counterObserver.observe(counter));
    }

    function handleDemoPlay() {
        // Simulate demo video modal or redirect
        const demoOverlay = document.querySelector('.demo-play-overlay');
        if (demoOverlay) {
            demoOverlay.style.background = 'rgba(0, 0, 0, 0.8)';
            demoOverlay.innerHTML = `
                <div style="color: white; text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">
                        <i class="fas fa-spinner fa-spin"></i>
                    </div>
                    <p>Loading demo video...</p>
                </div>
            `;

            // Simulate loading
            setTimeout(() => {
                alert('Demo video would open here. Integration with video platform needed.');
                location.reload(); // Reset the overlay
            }, 2000);
        }
    }

    function handleDemoRequest() {
        // Simulate demo scheduling
        demoRequestBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Scheduling...</span>';
        demoRequestBtn.disabled = true;

        setTimeout(() => {
            alert('Demo request submitted! Our team will contact you within 24 hours to schedule your personalized demo.');
            demoRequestBtn.innerHTML = '<i class="fas fa-video"></i> <span>Schedule Live Demo</span>';
            demoRequestBtn.disabled = false;
        }, 2000);
    }

    function handleBrochureDownload() {
        // Simulate brochure download
        brochureBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Preparing...</span>';
        brochureBtn.disabled = true;

        setTimeout(() => {
            // Create a fake download
            const link = document.createElement('a');
            link.href = 'data:text/plain;charset=utf-8,Ethiopian Hospital ERP System Brochure\n\nThank you for your interest in our healthcare management system!';
            link.download = 'Ethiopian-Hospital-ERP-Brochure.txt';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            brochureBtn.innerHTML = '<i class="fas fa-download"></i> <span>Download Brochure</span>';
            brochureBtn.disabled = false;
        }, 1500);
    }

    function animateCounter(element) {
        const target = parseFloat(element.getAttribute('data-counter'));
        const duration = 2000; // 2 seconds
        const step = target / (duration / 16); // 60fps
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }

            // Format the number
            let displayValue = current;
            if (target >= 100 && target < 1000) {
                displayValue = Math.floor(current);
            } else if (target >= 1000) {
                displayValue = Math.floor(current);
            } else {
                displayValue = current.toFixed(1);
            }

            element.textContent = displayValue + (target === 99.9 ? '' : target >= 1000 ? '+' : '');
        }, 16);
    }

    // Add hover effects to demo features
    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const progressBar = item.querySelector('.progress-bar');
            if (progressBar) {
                progressBar.style.transform = 'scaleX(1.05)';
                setTimeout(() => {
                    progressBar.style.transform = 'scaleX(1)';
                }, 200);
            }
        });
    });

    // Add click-to-copy functionality for contact info
    const contactCards = document.querySelectorAll('.contact-info-card');
    contactCards.forEach(card => {
        const link = card.querySelector('.contact-card-link');
        if (link && (link.href.startsWith('tel:') || link.href.startsWith('mailto:'))) {
            card.addEventListener('click', (e) => {
                if (e.target === card || e.target.closest('.contact-card-icon, h4, p')) {
                    const text = card.querySelector('p').textContent.trim();
                    navigator.clipboard?.writeText(text).then(() => {
                        // Show temporary feedback
                        const originalText = card.querySelector('h4').textContent;
                        card.querySelector('h4').textContent = 'Copied!';
                        setTimeout(() => {
                            card.querySelector('h4').textContent = originalText;
                        }, 1000);
                    }).catch(() => {
                        // Fallback for browsers without clipboard API
                        console.log('Clipboard not available');
                    });
                }
            });
        }
    });
}

// Utility Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidEthiopianPhone(phone) {
    const phoneRegex = /^(\+251|251|0)?[79]\d{8}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Why Choose Section Functionality
function initWhyChooseSection() {
    const progressCircles = document.querySelectorAll('.progress-circle');
    const trustCounters = document.querySelectorAll('.trust-number[data-counter]');

    // Animate progress circles when in view
    if (progressCircles.length > 0) {
        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const circle = entry.target;
                    const progress = circle.getAttribute('data-progress') || 0;

                    // Set CSS custom property for the progress
                    circle.style.setProperty('--progress', progress);

                    // Animate the progress text if it's a percentage
                    const progressText = circle.querySelector('.progress-text');
                    if (progressText && progress < 100) {
                        animateProgressText(progressText, progress);
                    }

                    progressObserver.unobserve(circle);
                }
            });
        }, { threshold: 0.3 });

        progressCircles.forEach(circle => progressObserver.observe(circle));
    }

    // Animate trust counters
    if (trustCounters.length > 0) {
        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        trustCounters.forEach(counter => counterObserver.observe(counter));
    }

    // Add hover effects to benefit items
    const benefitItems = document.querySelectorAll('.benefit-item');
    benefitItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const progressCircle = item.querySelector('.progress-circle');
            if (progressCircle) {
                progressCircle.style.transform = 'scale(1.1)';
            }
        });

        item.addEventListener('mouseleave', () => {
            const progressCircle = item.querySelector('.progress-circle');
            if (progressCircle) {
                progressCircle.style.transform = 'scale(1)';
            }
        });
    });

    function animateProgressText(element, targetValue) {
        let currentValue = 0;
        const increment = targetValue / 50; // 50 steps
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(timer);
            }
            element.textContent = Math.floor(currentValue) + '%';
        }, 30);
    }

    function animateCounter(element) {
        const target = parseFloat(element.getAttribute('data-counter'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }

            // Format the number based on its value
            let displayValue;
            if (target >= 1000000) {
                displayValue = (current / 1000000).toFixed(1) + 'M';
            } else if (target >= 1000) {
                displayValue = Math.floor(current) + '+';
            } else if (target === 99.9) {
                displayValue = current.toFixed(1) + '%';
            } else {
                displayValue = Math.floor(current);
            }

            element.textContent = displayValue;
        }, 16);
    }
}

// Modern Footer Functionality
function initModernFooter() {
    const newsletterForm = document.querySelector('.newsletter-form');
    const socialLinks = document.querySelectorAll('.social-link');
    const contactItems = document.querySelectorAll('.contact-item');

    // Newsletter form submission
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', handleNewsletterSubmit);
    }

    // Social link hover effects
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            link.style.transform = 'translateY(-3px) scale(1.05)';
        });

        link.addEventListener('mouseleave', () => {
            link.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Contact item click-to-copy functionality
    contactItems.forEach(item => {
        item.addEventListener('click', () => {
            const contactValue = item.querySelector('.contact-value');
            if (contactValue) {
                const text = contactValue.textContent.trim();

                // Try to copy to clipboard
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(() => {
                        showCopyFeedback(item);
                    }).catch(() => {
                        // Fallback for older browsers
                        fallbackCopyToClipboard(text);
                        showCopyFeedback(item);
                    });
                } else {
                    fallbackCopyToClipboard(text);
                    showCopyFeedback(item);
                }
            }
        });

        // Add cursor pointer to indicate clickability
        item.style.cursor = 'pointer';
        item.title = 'Click to copy';
    });

    function handleNewsletterSubmit(e) {
        e.preventDefault();

        const input = e.target.querySelector('.newsletter-input');
        const button = e.target.querySelector('.newsletter-btn');
        const email = input.value.trim();

        // Basic email validation
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showNewsletterMessage('Please enter a valid email address', 'error');
            return;
        }

        // Show loading state
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        button.disabled = true;

        // Simulate API call
        setTimeout(() => {
            input.value = '';
            button.innerHTML = '<i class="fas fa-check"></i>';
            showNewsletterMessage('Successfully subscribed to our newsletter!', 'success');

            // Reset button after 2 seconds
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-paper-plane"></i>';
                button.disabled = false;
            }, 2000);
        }, 1500);
    }

    function showCopyFeedback(item) {
        const originalBg = item.style.background;
        item.style.background = 'rgba(0, 150, 57, 0.2)';
        item.style.transform = 'scale(1.02)';

        // Show temporary feedback
        const feedback = document.createElement('div');
        feedback.textContent = 'Copied!';
        feedback.style.cssText = `
            position: absolute;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--primary-green);
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            z-index: 1000;
            animation: fadeInOut 2s ease;
        `;

        item.style.position = 'relative';
        item.appendChild(feedback);

        setTimeout(() => {
            item.style.background = originalBg;
            item.style.transform = 'scale(1)';
            if (feedback.parentNode) {
                feedback.parentNode.removeChild(feedback);
            }
        }, 2000);
    }

    function fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Fallback: Oops, unable to copy', err);
        }

        document.body.removeChild(textArea);
    }

    function showNewsletterMessage(message, type) {
        const messageEl = document.createElement('div');
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'var(--primary-green)' : 'var(--primary-red)'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
        `;

        document.body.appendChild(messageEl);

        setTimeout(() => {
            messageEl.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 3000);
    }
}

// Export for global use
window.HomepageEnhancements = {
    initParallaxScrolling,
    initAdvanced3DEffects,
    initFloatingAnimations,
    validateFieldEnhanced,
    initWhyChooseSection,
    initModernFooter
};
