// Navigation functionality
        function showSection(sectionName) {
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });

            // Show target section
            document.getElementById(sectionName).classList.add('active');

            // Update nav link states
            document.querySelectorAll('.nav-links a').forEach(link => {
                if (link.getAttribute('data-section') === sectionName) {
                    link.classList.add('active-link');
                } else {
                    link.classList.remove('active-link');
                }
            });

            // Close mobile menu
            document.getElementById('navLinks').classList.remove('active');

            // Scroll to top
            window.scrollTo(0, 0);
        }

        function toggleMobileMenu() {
            const navLinks = document.getElementById('navLinks');
            navLinks.classList.toggle('active');
        }
        
        // FAQ functionality
        function toggleFaq(element) {
            const faqItem = element.parentElement;
            const isActive = faqItem.classList.contains('active');
            
            // Close all FAQ items
            document.querySelectorAll('.faq-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                faqItem.classList.add('active');
            }
        }
        
        // Scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        // Typing animation for hero subtitle
        function typeWriter(element, text, speed = 100) {
            let i = 0;
            element.innerHTML = '';
            
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }
        
        // Add particle effect to hero background
        function createParticles() {
            const hero = document.querySelector('.hero');
            if (!hero) return;
            
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.style.cssText = `
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: rgba(74, 144, 226, 0.3);
                    border-radius: 50%;
                    pointer-events: none;
                    animation: float ${Math.random() * 10 + 10}s infinite linear;
                    left: ${Math.random() * 100}%;
                    top: ${Math.random() * 100}%;
                    animation-delay: ${Math.random() * 10}s;
                `;
                hero.appendChild(particle);
            }
        }
        
        // Add floating animation keyframes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                0% {
                    transform: translateY(100vh) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                90% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(-100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        document.addEventListener('DOMContentLoaded', () => {
            const animateElements = document.querySelectorAll('.animate-on-scroll');
            animateElements.forEach(el => observer.observe(el));

            // Add navigation event listeners
            document.querySelectorAll('[data-section]').forEach(link => {
                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    const section = link.getAttribute('data-section');
                    if (section) {
                        showSection(section);
                    }
                });
            });

            // Add mobile toggle event listener
            const mobileToggle = document.getElementById('mobileToggle');
            if (mobileToggle) {
                mobileToggle.addEventListener('click', toggleMobileMenu);
            }

            // Add FAQ event listeners
            document.querySelectorAll('.faq-question').forEach(question => {
                question.addEventListener('click', () => toggleFaq(question));
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                const navLinks = document.getElementById('navLinks');
                const mobileToggle = document.querySelector('.mobile-toggle');
                
                if (navLinks && mobileToggle && !navLinks.contains(e.target) && !mobileToggle.contains(e.target)) {
                    navLinks.classList.remove('active');
                }
            });
            
            // Smooth scrolling for anchor links
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
        });

        // Initialize typing animation when page loads
        window.addEventListener('load', () => {
            const subtitle = document.querySelector('.hero .subtitle');
            if (subtitle) {
                const originalText = subtitle.textContent;
                setTimeout(() => {
                    typeWriter(subtitle, originalText, 80);
                }, 1000);
            }
        });
        
        // Add navbar background on scroll
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 50) {
                    navbar.style.background = 'rgba(26, 26, 26, 0.98)';
                } else {
                    navbar.style.background = 'rgba(26, 26, 26, 0.95)';
                }
            }
        });
        
        // Initialize particles after a delay
        setTimeout(createParticles, 2000);