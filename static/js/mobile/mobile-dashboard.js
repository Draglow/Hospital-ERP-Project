// Mobile Dashboard JavaScript - Ethiopian Hospital ERP

class MobileDashboard {
    constructor() {
        this.isInitialized = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.touchEndX = 0;
        this.touchEndY = 0;
        this.swipeThreshold = 50;
        this.isSwipeEnabled = true;
        
        // Mobile-specific settings
        this.isMobile = window.innerWidth <= 768;
        this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }
    
    init() {
        if (this.isInitialized) return;

        console.log('Initializing Mobile Dashboard...');

        // Initialize responsive redirection first
        this.initResponsiveRedirection();

        // Initialize core mobile features
        this.initMobileSidebar();
        this.initMobileSearch();
        this.initMobileNotifications();
        this.initMobileNotificationPanel();
        this.initMobileProfile();
        this.initTouchGestures();
        this.initMobileCharts();
        this.initMobileTime();
        this.initMobileResponsive();
        this.initMobilePerformance();
        this.initMobileAccessibility();
        this.initMobileBottomNavigation();
        this.initMobileCRUDTesting();

        // Mark as initialized
        this.isInitialized = true;

        console.log('Mobile Dashboard initialized successfully');

        // Show welcome notification only once per session
        this.showWelcomeMessage();
    }
    
    // ===== MOBILE SIDEBAR =====
    initMobileSidebar() {
        const sidebarToggle = document.getElementById('mobileSidebarToggle');
        const sidebar = document.getElementById('mobileSidebar');
        const overlay = document.getElementById('mobileSidebarOverlay');
        
        if (!sidebarToggle || !sidebar || !overlay) return;
        
        // Toggle sidebar
        sidebarToggle.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMobileSidebar();
        });
        
        // Close sidebar when clicking overlay
        overlay.addEventListener('click', () => {
            this.closeMobileSidebar();
        });
        
        // Close sidebar when clicking nav links
        const navLinks = sidebar.querySelectorAll('.mobile-nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (!link.classList.contains('mobile-nav-expandable')) {
                    this.closeMobileSidebar();
                }
            });
        });
        
        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar.classList.contains('active')) {
                this.closeMobileSidebar();
            }
        });
    }
    
    toggleMobileSidebar() {
        const sidebar = document.getElementById('mobileSidebar');
        const overlay = document.getElementById('mobileSidebarOverlay');
        const toggle = document.getElementById('mobileSidebarToggle');
        
        if (sidebar.classList.contains('active')) {
            this.closeMobileSidebar();
        } else {
            this.openMobileSidebar();
        }
    }
    
    openMobileSidebar() {
        const sidebar = document.getElementById('mobileSidebar');
        const overlay = document.getElementById('mobileSidebarOverlay');
        const toggle = document.getElementById('mobileSidebarToggle');
        
        sidebar.classList.add('active');
        overlay.classList.add('active');
        toggle.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        // Focus management for accessibility
        const firstFocusable = sidebar.querySelector('.mobile-nav-link');
        if (firstFocusable) {
            firstFocusable.focus();
        }
    }
    
    closeMobileSidebar() {
        const sidebar = document.getElementById('mobileSidebar');
        const overlay = document.getElementById('mobileSidebarOverlay');
        const toggle = document.getElementById('mobileSidebarToggle');
        
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        toggle.classList.remove('active');
        document.body.style.overflow = '';
        
        // Return focus to toggle button
        toggle.focus();
    }
    
    // ===== MOBILE SEARCH =====
    initMobileSearch() {
        const searchToggle = document.getElementById('mobileSearchToggle');
        const searchBar = document.getElementById('mobileSearchBar');
        const searchClose = document.getElementById('mobileSearchClose');
        const searchInput = document.getElementById('mobileGlobalSearch');
        
        if (!searchToggle || !searchBar || !searchClose || !searchInput) return;
        
        // Toggle search bar
        searchToggle.addEventListener('click', () => {
            this.toggleMobileSearch();
        });
        
        // Close search bar
        searchClose.addEventListener('click', () => {
            this.closeMobileSearch();
        });
        
        // Handle search input
        searchInput.addEventListener('input', (e) => {
            this.handleMobileSearch(e.target.value);
        });
        
        // Handle enter key
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.performMobileSearch(e.target.value);
            } else if (e.key === 'Escape') {
                this.closeMobileSearch();
            }
        });

        // Hide results when clicking outside
        document.addEventListener('click', (e) => {
            const searchBar = document.getElementById('mobileSearchBar');
            if (searchBar && !searchBar.contains(e.target)) {
                this.hideMobileSearchResults();
            }
        });
    }
    
    toggleMobileSearch() {
        const searchBar = document.getElementById('mobileSearchBar');
        const searchInput = document.getElementById('mobileGlobalSearch');
        
        if (searchBar.classList.contains('active')) {
            this.closeMobileSearch();
        } else {
            searchBar.classList.add('active');
            setTimeout(() => {
                searchInput.focus();
            }, 300);
        }
    }
    
    closeMobileSearch() {
        const searchBar = document.getElementById('mobileSearchBar');
        const searchInput = document.getElementById('mobileGlobalSearch');

        searchBar.classList.remove('active');
        searchInput.value = '';
        searchInput.blur();
        this.hideMobileSearchResults();
    }
    
    handleMobileSearch(query) {
        // Debounced search functionality
        clearTimeout(this.searchTimeout);
        this.searchTimeout = setTimeout(() => {
            if (query.length >= 2) {
                this.performMobileSearch(query);
            } else {
                this.hideMobileSearchResults();
            }
        }, 300);
    }

    performMobileSearch(query) {
        console.log('Performing mobile search:', query);

        // Show loading state
        this.showMobileSearchLoading();

        // Make AJAX request to global search endpoint
        fetch(`/dashboard/search/global/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                this.displayMobileSearchResults(data.results);
            })
            .catch(error => {
                console.error('Search error:', error);
                this.showMobileSearchError();
            });
    }

    showMobileSearchLoading() {
        const searchBar = document.getElementById('mobileSearchBar');
        let resultsContainer = document.getElementById('mobileSearchResults');

        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'mobileSearchResults';
            resultsContainer.className = 'mobile-search-results';
            searchBar.appendChild(resultsContainer);
        }

        resultsContainer.innerHTML = `
            <div class="mobile-search-loading">
                <i class="fas fa-spinner fa-spin me-2"></i>
                Searching...
            </div>
        `;
        resultsContainer.style.display = 'block';
    }

    displayMobileSearchResults(results) {
        const searchBar = document.getElementById('mobileSearchBar');
        let resultsContainer = document.getElementById('mobileSearchResults');

        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'mobileSearchResults';
            resultsContainer.className = 'mobile-search-results';
            searchBar.appendChild(resultsContainer);
        }

        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="mobile-search-no-results">
                    <i class="fas fa-search me-2 text-muted"></i>
                    No results found
                </div>
            `;
        } else {
            resultsContainer.innerHTML = results.map(result => `
                <div class="mobile-search-result-item" data-url="${result.url}">
                    <div class="mobile-search-result-content">
                        <div class="mobile-search-result-icon">
                            <i class="fas fa-${result.icon}"></i>
                        </div>
                        <div class="mobile-search-result-text">
                            <div class="mobile-search-result-title">${result.title}</div>
                            <div class="mobile-search-result-subtitle">${result.subtitle}</div>
                        </div>
                        <div class="mobile-search-result-type">
                            ${result.type}
                        </div>
                    </div>
                </div>
            `).join('');

            // Add click handlers
            resultsContainer.querySelectorAll('.mobile-search-result-item').forEach(item => {
                item.addEventListener('click', () => {
                    const url = item.dataset.url;
                    if (url) {
                        // Add mobile parameter to URL
                        const separator = url.includes('?') ? '&' : '?';
                        window.location.href = `${url}${separator}mobile=1`;
                    }
                });
            });
        }

        resultsContainer.style.display = 'block';
    }

    showMobileSearchError() {
        const searchBar = document.getElementById('mobileSearchBar');
        let resultsContainer = document.getElementById('mobileSearchResults');

        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'mobileSearchResults';
            resultsContainer.className = 'mobile-search-results';
            searchBar.appendChild(resultsContainer);
        }

        resultsContainer.innerHTML = `
            <div class="mobile-search-error">
                <i class="fas fa-exclamation-triangle me-2 text-warning"></i>
                Search error. Please try again.
            </div>
        `;
        resultsContainer.style.display = 'block';
    }

    hideMobileSearchResults() {
        const resultsContainer = document.getElementById('mobileSearchResults');
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
    }
    
    // ===== MOBILE NOTIFICATIONS =====
    initMobileNotifications() {
        // This method is kept for backward compatibility but functionality moved to initMobileNotificationPanel
        console.log('Mobile notifications initialized');
    }

    // ===== MOBILE NOTIFICATION PANEL =====
    initMobileNotificationPanel() {
        console.log('Initializing mobile notification panel...');

        const notificationToggle = document.getElementById('mobileNotificationToggle');
        const notificationPanel = document.getElementById('mobileNotificationsPanel');
        const notificationOverlay = document.getElementById('mobileNotificationsOverlay');
        const notificationClose = document.getElementById('mobileNotificationsClose');
        const markAllReadBtn = document.getElementById('mobileMarkAllReadBtn');
        const viewAllBtn = document.getElementById('mobileViewAllNotificationsBtn');

        console.log('Notification elements found:', {
            toggle: !!notificationToggle,
            panel: !!notificationPanel,
            overlay: !!notificationOverlay,
            close: !!notificationClose
        });

        if (!notificationToggle) {
            console.error('Mobile notification toggle button not found!');
            return;
        }

        if (!notificationPanel) {
            console.error('Mobile notification panel not found!');
            return;
        }

        if (!notificationOverlay) {
            console.error('Mobile notification overlay not found!');
            return;
        }

        // Toggle notification panel
        notificationToggle.addEventListener('click', (e) => {
            console.log('Notification toggle clicked');
            e.preventDefault();
            e.stopPropagation();
            this.toggleMobileNotificationPanel();
        });

        // Close notification panel
        if (notificationClose) {
            notificationClose.addEventListener('click', (e) => {
                console.log('Notification close clicked');
                e.preventDefault();
                this.closeMobileNotificationPanel();
            });
        }

        // Close panel when clicking overlay
        notificationOverlay.addEventListener('click', (e) => {
            console.log('Notification overlay clicked');
            this.closeMobileNotificationPanel();
        });

        // Mark all as read
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', (e) => {
                console.log('Mark all read clicked');
                e.preventDefault();
                this.markAllNotificationsAsRead();
            });
        }

        // View all notifications
        if (viewAllBtn) {
            viewAllBtn.addEventListener('click', (e) => {
                console.log('View all notifications clicked');
                e.preventDefault();
                this.closeMobileNotificationPanel();
                window.location.href = '/notifications/?mobile=1';
            });
        }

        // Handle escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && notificationPanel.classList.contains('active')) {
                console.log('Escape key pressed, closing notification panel');
                this.closeMobileNotificationPanel();
            }
        });

        // Touch gestures for swipe-to-close
        this.initNotificationPanelGestures();

        console.log('Mobile notification panel initialized successfully');
    }

    toggleMobileNotificationPanel() {
        console.log('toggleMobileNotificationPanel called');

        const panel = document.getElementById('mobileNotificationsPanel');
        const overlay = document.getElementById('mobileNotificationsOverlay');

        console.log('Panel and overlay elements:', {
            panel: !!panel,
            overlay: !!overlay,
            panelActive: panel ? panel.classList.contains('active') : false
        });

        if (!panel || !overlay) {
            console.error('Panel or overlay not found!');
            return;
        }

        if (panel.classList.contains('active')) {
            console.log('Panel is active, closing...');
            this.closeMobileNotificationPanel();
        } else {
            console.log('Panel is not active, opening...');
            this.openMobileNotificationPanel();
        }
    }

    openMobileNotificationPanel() {
        console.log('openMobileNotificationPanel called');

        const panel = document.getElementById('mobileNotificationsPanel');
        const overlay = document.getElementById('mobileNotificationsOverlay');

        if (!panel || !overlay) {
            console.error('Cannot open panel - elements not found');
            return;
        }

        console.log('Opening notification panel...');

        // Close sidebar if open
        this.closeMobileSidebar();

        // Open notification panel
        panel.classList.add('active');
        overlay.classList.add('active');
        document.body.classList.add('mobile-panel-open');
        document.body.style.overflow = 'hidden';

        console.log('Panel classes added, loading notifications...');

        // Load notifications
        this.loadMobileNotifications();

        // Focus management for accessibility
        setTimeout(() => {
            const closeBtn = document.getElementById('mobileNotificationsClose');
            if (closeBtn) {
                closeBtn.focus();
                console.log('Focus set to close button');
            }
        }, 300);

        console.log('Notification panel opened successfully');
    }

    closeMobileNotificationPanel() {
        const panel = document.getElementById('mobileNotificationsPanel');
        const overlay = document.getElementById('mobileNotificationsOverlay');

        panel.classList.remove('active');
        overlay.classList.remove('active');
        document.body.classList.remove('mobile-panel-open');
        document.body.style.overflow = '';
    }

    loadMobileNotifications() {
        const loadingElement = document.getElementById('mobileNotificationsLoading');
        const listElement = document.getElementById('mobileNotificationsList');
        const emptyElement = document.getElementById('mobileNotificationsEmpty');
        const actionsElement = document.getElementById('mobileNotificationsActions');

        // Show loading state
        loadingElement.style.display = 'block';
        listElement.style.display = 'none';
        emptyElement.style.display = 'none';
        actionsElement.style.display = 'none';

        // Fetch notifications
        fetch('/notifications/dropdown/')
            .then(response => response.text())
            .then(html => {
                // Hide loading
                loadingElement.style.display = 'none';

                // Parse the response to extract notifications
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;

                const notifications = tempDiv.querySelectorAll('.notification-item');

                if (notifications.length > 0) {
                    // Show notifications list
                    this.renderMobileNotifications(notifications);
                    listElement.style.display = 'block';
                    actionsElement.style.display = 'block';
                } else {
                    // Show empty state
                    emptyElement.style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error loading notifications:', error);
                loadingElement.style.display = 'none';
                emptyElement.style.display = 'block';

                // Update empty state for error
                const emptyIcon = emptyElement.querySelector('i');
                const emptyTitle = emptyElement.querySelector('h6');
                const emptyText = emptyElement.querySelector('p');

                if (emptyIcon) emptyIcon.className = 'fas fa-exclamation-triangle text-warning mb-3';
                if (emptyTitle) emptyTitle.textContent = 'Error loading notifications';
                if (emptyText) emptyText.textContent = 'Please try again later.';
            });
    }

    renderMobileNotifications(notifications) {
        const listElement = document.getElementById('mobileNotificationsList');
        if (!listElement) return;

        let notificationsHtml = '';

        notifications.forEach((notification, index) => {
            if (index >= 10) return; // Limit to 10 notifications

            // Extract notification data from dropdown item
            const notificationId = notification.dataset.notificationId;
            const title = notification.querySelector('.notification-title')?.textContent?.trim() || 'Notification';
            const message = notification.querySelector('.notification-message')?.textContent?.trim() || '';
            const time = notification.querySelector('.notification-time')?.textContent?.trim() || '';
            const isUnread = notification.classList.contains('unread');

            // Determine notification type based on icon or content
            const iconElement = notification.querySelector('.notification-icon i');
            let type = 'system';
            if (iconElement) {
                if (iconElement.classList.contains('fa-user-plus')) type = 'patient';
                else if (iconElement.classList.contains('fa-calendar')) type = 'appointment';
                else if (iconElement.classList.contains('fa-pills')) type = 'pharmacy';
                else if (iconElement.classList.contains('fa-file-invoice')) type = 'billing';
            } else {
                type = this.getNotificationType(title);
            }

            notificationsHtml += `
                <div class="mobile-notification-item ${isUnread ? 'unread' : ''}" data-notification-id="${notificationId}">
                    <div class="mobile-notification-icon ${type}">
                        <i class="${this.getNotificationIcon(type)}"></i>
                    </div>
                    <div class="mobile-notification-content">
                        <div class="mobile-notification-title">${this.truncateText(title, 50)}</div>
                        <div class="mobile-notification-message">${this.truncateText(message || this.generateNotificationMessage(type), 60)}</div>
                        <div class="mobile-notification-time">${time || this.getTimeAgo(new Date())}</div>
                    </div>
                </div>
            `;
        });

        listElement.innerHTML = notificationsHtml;

        // Add click handlers
        listElement.querySelectorAll('.mobile-notification-item').forEach(item => {
            item.addEventListener('click', () => {
                this.handleNotificationClick(item);
            });
        });
    }

    getNotificationType(title) {
        if (title.toLowerCase().includes('appointment')) return 'appointment';
        if (title.toLowerCase().includes('patient')) return 'patient';
        if (title.toLowerCase().includes('invoice') || title.toLowerCase().includes('billing')) return 'billing';
        if (title.toLowerCase().includes('medicine') || title.toLowerCase().includes('pharmacy')) return 'pharmacy';
        return 'system';
    }

    getNotificationIcon(type) {
        const icons = {
            appointment: 'fas fa-calendar-alt',
            patient: 'fas fa-user-plus',
            billing: 'fas fa-file-invoice',
            pharmacy: 'fas fa-pills',
            system: 'fas fa-cog'
        };
        return icons[type] || 'fas fa-bell';
    }

    generateNotificationMessage(type) {
        const messages = {
            appointment: 'New appointment scheduled or updated',
            patient: 'New patient registered or updated',
            billing: 'Invoice created or payment received',
            pharmacy: 'Medicine stock or prescription update',
            system: 'System notification or update'
        };
        return messages[type] || 'New notification';
    }

    truncateText(text, maxLength) {
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }

    getTimeAgo(date) {
        const now = new Date();
        const diffInMinutes = Math.floor((now - date) / (1000 * 60));

        if (diffInMinutes < 1) return 'Just now';
        if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
        if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
        return `${Math.floor(diffInMinutes / 1440)}d ago`;
    }

    handleNotificationClick(item) {
        // Mark as read
        item.classList.remove('unread');

        // Add visual feedback
        item.style.transform = 'scale(0.98)';
        setTimeout(() => {
            item.style.transform = '';
        }, 150);

        // Handle notification action (could navigate to relevant page)
        console.log('Notification clicked:', item.dataset.notificationId);
    }

    markAllNotificationsAsRead() {
        const unreadItems = document.querySelectorAll('.mobile-notification-item.unread');
        unreadItems.forEach(item => {
            item.classList.remove('unread');
        });

        // Update badge
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.style.display = 'none';
        }

        // Show success message
        this.showMobileNotification('All notifications marked as read', 'success');

        // Make API call to mark as read
        fetch('/notifications/mark-all-read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCSRFToken(),
                'Content-Type': 'application/json',
            },
        }).catch(error => {
            console.error('Error marking notifications as read:', error);
        });
    }

    removeNotificationFromSidebar(notificationId, wasUnread) {
        console.log('Removing notification from sidebar:', notificationId);

        // Find and remove the notification item from the mobile sidebar
        const notificationItem = document.querySelector(`.mobile-notification-item[data-notification-id="${notificationId}"]`);
        if (notificationItem) {
            // Animate removal
            notificationItem.style.transition = 'all 0.3s ease';
            notificationItem.style.transform = 'translateX(100%)';
            notificationItem.style.opacity = '0';

            setTimeout(() => {
                notificationItem.remove();

                // Update notification count if it was unread
                if (wasUnread) {
                    this.updateNotificationBadge();
                }

                // Check if sidebar is now empty
                const remainingItems = document.querySelectorAll('.mobile-notification-item');
                if (remainingItems.length === 0) {
                    this.showEmptyNotificationState();
                }

                console.log('Notification removed from sidebar successfully');
            }, 300);
        }
    }

    updateNotificationBadge() {
        // Update the notification badge in the header
        const badge = document.querySelector('.notification-badge');
        const unreadItems = document.querySelectorAll('.mobile-notification-item.unread');

        if (badge) {
            if (unreadItems.length === 0) {
                badge.style.display = 'none';
            } else {
                badge.textContent = unreadItems.length;
                badge.style.display = 'block';
            }
        }

        // Also update any other notification counters
        const headerBadge = document.querySelector('#mobileNotificationToggle .badge');
        if (headerBadge) {
            if (unreadItems.length === 0) {
                headerBadge.style.display = 'none';
            } else {
                headerBadge.textContent = unreadItems.length;
                headerBadge.style.display = 'block';
            }
        }
    }

    showEmptyNotificationState() {
        const listElement = document.getElementById('mobileNotificationsList');
        const emptyElement = document.getElementById('mobileNotificationsEmpty');
        const actionsElement = document.getElementById('mobileNotificationsActions');

        if (listElement) {
            listElement.style.display = 'none';
        }

        if (emptyElement) {
            emptyElement.style.display = 'block';
        }

        if (actionsElement) {
            actionsElement.style.display = 'none';
        }
    }

    initNotificationPanelGestures() {
        const panel = document.getElementById('mobileNotificationsPanel');
        if (!panel) return;

        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        panel.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            isDragging = true;
        }, { passive: true });

        panel.addEventListener('touchmove', (e) => {
            if (!isDragging) return;

            currentX = e.touches[0].clientX;
            const diffX = currentX - startX;

            // Only allow swipe to the right (closing)
            if (diffX > 0) {
                const translateX = Math.min(diffX, panel.offsetWidth);
                panel.style.transform = `translateX(${translateX}px)`;
            }
        }, { passive: true });

        panel.addEventListener('touchend', () => {
            if (!isDragging) return;

            const diffX = currentX - startX;
            const threshold = panel.offsetWidth * 0.3;

            if (diffX > threshold) {
                this.closeMobileNotificationPanel();
            } else {
                panel.style.transform = '';
            }

            isDragging = false;
        }, { passive: true });
    }
    
    // ===== MOBILE PROFILE =====
    initMobileProfile() {
        const profileToggle = document.getElementById('mobileProfileToggle');
        const profilePanel = document.getElementById('mobileProfilePanel');
        const profileClose = document.getElementById('mobileProfileClose');
        
        if (!profileToggle || !profilePanel || !profileClose) return;
        
        // Toggle profile panel
        profileToggle.addEventListener('click', () => {
            this.toggleMobileProfile();
        });
        
        // Close profile panel
        profileClose.addEventListener('click', () => {
            this.closeMobileProfile();
        });
    }
    
    toggleMobileProfile() {
        const panel = document.getElementById('mobileProfilePanel');
        
        if (panel.classList.contains('active')) {
            this.closeMobileProfile();
        } else {
            this.openMobileProfile();
        }
    }
    
    openMobileProfile() {
        const panel = document.getElementById('mobileProfilePanel');
        
        // Close other panels first
        this.closeMobileNotificationPanel();
        
        panel.classList.add('active');
    }
    
    closeMobileProfile() {
        const panel = document.getElementById('mobileProfilePanel');
        panel.classList.remove('active');
    }
    
    // ===== TOUCH GESTURES =====
    initTouchGestures() {
        if (!('ontouchstart' in window)) return;
        
        // Swipe to open/close sidebar
        document.addEventListener('touchstart', (e) => {
            this.handleTouchStart(e);
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            this.handleTouchMove(e);
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            this.handleTouchEnd(e);
        }, { passive: true });
    }
    
    handleTouchStart(e) {
        if (!this.isSwipeEnabled) return;
        
        this.touchStartX = e.touches[0].clientX;
        this.touchStartY = e.touches[0].clientY;
    }
    
    handleTouchMove(e) {
        if (!this.isSwipeEnabled) return;
        
        this.touchEndX = e.touches[0].clientX;
        this.touchEndY = e.touches[0].clientY;
    }
    
    handleTouchEnd(e) {
        if (!this.isSwipeEnabled) return;
        
        const deltaX = this.touchEndX - this.touchStartX;
        const deltaY = this.touchEndY - this.touchStartY;
        const absDeltaX = Math.abs(deltaX);
        const absDeltaY = Math.abs(deltaY);
        
        // Only process horizontal swipes
        if (absDeltaX > absDeltaY && absDeltaX > this.swipeThreshold) {
            const sidebar = document.getElementById('mobileSidebar');
            
            // Swipe right from left edge to open sidebar
            if (deltaX > 0 && this.touchStartX < 50 && !sidebar.classList.contains('active')) {
                this.openMobileSidebar();
            }
            // Swipe left to close sidebar
            else if (deltaX < 0 && sidebar.classList.contains('active')) {
                this.closeMobileSidebar();
            }
        }
    }
    
    // ===== MOBILE CHARTS =====
    initMobileCharts() {
        // Mobile-optimized chart configurations will be handled in the dashboard index
        this.mobileChartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: this.isMobile ? 'bottom' : 'right',
                    labels: {
                        padding: this.isMobile ? 10 : 15,
                        usePointStyle: true,
                        font: {
                            size: this.isMobile ? 10 : 12
                        },
                        boxWidth: this.isMobile ? 8 : 12,
                        boxHeight: this.isMobile ? 8 : 12
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    titleColor: '#2c3e50',
                    bodyColor: '#2c3e50',
                    borderColor: '#009639',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6c757d',
                        font: {
                            size: this.isMobile ? 10 : 12
                        },
                        padding: 8
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#6c757d',
                        font: {
                            size: this.isMobile ? 10 : 12
                        },
                        maxRotation: this.isMobile ? 45 : 0,
                        padding: 8
                    }
                }
            },
            elements: {
                point: {
                    radius: this.isMobile ? 3 : 4,
                    hoverRadius: this.isMobile ? 5 : 6
                },
                line: {
                    borderWidth: this.isMobile ? 2 : 3
                },
                bar: {
                    borderRadius: this.isMobile ? 6 : 10,
                    borderSkipped: false
                }
            },
            layout: {
                padding: this.isMobile ? 5 : 10
            }
        };
    }
    
    // ===== MOBILE TIME =====
    initMobileTime() {
        this.updateMobileTime();
        setInterval(() => this.updateMobileTime(), 1000);
        
        this.updateEthiopianDate();
        setInterval(() => this.updateEthiopianDate(), 60000); // Update every minute
    }
    
    updateMobileTime() {
        const timeElement = document.getElementById('mobileCurrentTime');
        if (timeElement) {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', {
                timeZone: 'Africa/Addis_Ababa',
                hour12: true,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
            timeElement.textContent = timeString;
        }
    }
    
    updateEthiopianDate() {
        const dateElement = document.getElementById('mobileEthiopianDate');
        if (dateElement) {
            // Simplified Ethiopian date display
            const now = new Date();
            const options = { 
                month: 'short', 
                day: 'numeric',
                timeZone: 'Africa/Addis_Ababa'
            };
            dateElement.textContent = now.toLocaleDateString('en-US', options);
        }
    }
    
    // ===== MOBILE RESPONSIVE =====
    initMobileResponsive() {
        this.handleMobileResize();
        window.addEventListener('resize', () => this.handleMobileResize());
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.handleMobileResize(), 500);
        });
    }
    
    handleMobileResize() {
        const wasIsMobile = this.isMobile;
        const wasIsTablet = this.isTablet;

        this.isMobile = window.innerWidth <= 768;
        this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;

        // Check for responsive redirection
        this.checkResponsiveRedirection();

        // Close panels on resize to larger screen
        if (wasIsMobile && !this.isMobile) {
            this.closeMobileSidebar();
            this.closeMobileNotificationPanel();
            this.closeMobileProfile();
            this.closeMobileSearch();
        }

        // Update chart options if device type changed
        if (wasIsMobile !== this.isMobile || wasIsTablet !== this.isTablet) {
            this.initMobileCharts();
        }
    }

    // ===== RESPONSIVE REDIRECTION =====
    initResponsiveRedirection() {
        // Store responsive state
        this.responsiveState = {
            initialWidth: window.innerWidth,
            lastRedirectTime: 0,
            redirectCooldown: 2000, // 2 seconds cooldown
            breakpoint: 768,
            isMobileDashboard: window.location.pathname.includes('/mobile/'),
            isDesktopDashboard: window.location.pathname === '/dashboard/' || window.location.pathname === '/dashboard'
        };

        // Check if we should redirect immediately on page load
        setTimeout(() => {
            this.checkResponsiveRedirection(true);
        }, 100);
    }

    checkResponsiveRedirection(isInitialCheck = false) {
        const now = Date.now();
        const isMobile = window.innerWidth <= this.responsiveState.breakpoint;

        // Skip if we're in cooldown period
        if (!isInitialCheck && (now - this.responsiveState.lastRedirectTime) < this.responsiveState.redirectCooldown) {
            return;
        }

        // Check URL parameters for manual override
        const urlParams = new URLSearchParams(window.location.search);
        const forceDesktop = urlParams.get('desktop') === '1';
        const forceMobile = urlParams.get('mobile') === '1';

        // Skip redirection if user has manually overridden
        if (forceDesktop || forceMobile) {
            return;
        }

        // Redirect to desktop if viewport is large enough and we're on mobile dashboard
        if (!isMobile && this.responsiveState.isMobileDashboard) {
            this.responsiveState.lastRedirectTime = now;
            this.redirectToDashboard('/dashboard/');
        }
    }

    redirectToDashboard(targetUrl) {
        // Preserve existing query parameters (except mobile/desktop overrides)
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.delete('mobile');
        urlParams.delete('desktop');

        // Build the new URL with preserved parameters
        let newUrl = targetUrl;
        if (urlParams.toString()) {
            newUrl += '?' + urlParams.toString();
        }

        // Add a parameter to indicate this was an automatic redirect
        const separator = newUrl.includes('?') ? '&' : '?';
        newUrl += separator + 'auto_redirect=1';

        // Perform the redirect
        console.log('Mobile responsive redirect:', window.location.pathname, '->', newUrl);
        window.location.href = newUrl;
    }
    
    // ===== MOBILE PERFORMANCE =====
    initMobilePerformance() {
        // Lazy load images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
        
        // Optimize scroll performance
        let ticking = false;
        const handleScroll = () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    // Handle scroll-based animations here
                    ticking = false;
                });
                ticking = true;
            }
        };
        
        window.addEventListener('scroll', handleScroll, { passive: true });
    }
    
    // ===== MOBILE ACCESSIBILITY =====
    initMobileAccessibility() {
        // Focus management
        this.initFocusManagement();
        
        // Screen reader announcements
        this.initScreenReaderSupport();
        
        // Keyboard navigation
        this.initKeyboardNavigation();
    }
    
    initFocusManagement() {
        // Trap focus in modals/panels
        const trapFocus = (element) => {
            const focusableElements = element.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            const firstFocusable = focusableElements[0];
            const lastFocusable = focusableElements[focusableElements.length - 1];
            
            element.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusable) {
                            lastFocusable.focus();
                            e.preventDefault();
                        }
                    } else {
                        if (document.activeElement === lastFocusable) {
                            firstFocusable.focus();
                            e.preventDefault();
                        }
                    }
                }
            });
        };
        
        const sidebar = document.getElementById('mobileSidebar');
        const notificationPanel = document.getElementById('mobileNotificationsPanel');
        const profilePanel = document.getElementById('mobileProfilePanel');
        
        if (sidebar) trapFocus(sidebar);
        if (notificationPanel) trapFocus(notificationPanel);
        if (profilePanel) trapFocus(profilePanel);
    }
    
    initScreenReaderSupport() {
        // Create live region for announcements
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        liveRegion.id = 'mobile-live-region';
        document.body.appendChild(liveRegion);
    }
    
    initKeyboardNavigation() {
        // Enhanced keyboard navigation for mobile elements
        document.addEventListener('keydown', (e) => {
            // Handle escape key globally
            if (e.key === 'Escape') {
                this.closeMobileSidebar();
                this.closeMobileNotificationPanel();
                this.closeMobileProfile();
                this.closeMobileSearch();
            }
        });
    }
    
    // ===== WELCOME MESSAGE =====
    showWelcomeMessage() {
        // Check if welcome message was already shown in this session
        const welcomeShown = sessionStorage.getItem('mobileWelcomeShown');
        const lastWelcomeTime = localStorage.getItem('lastMobileWelcome');
        const now = Date.now();

        // Show welcome message only if:
        // 1. Not shown in current session, AND
        // 2. Not shown in the last 30 minutes (to prevent spam on page refreshes)
        if (!welcomeShown && (!lastWelcomeTime || (now - parseInt(lastWelcomeTime)) > 30 * 60 * 1000)) {
            setTimeout(() => {
                // Get user's name for personalization
                const userName = this.getUserName();
                const welcomeMessage = userName ?
                    `Welcome back, ${userName}! 👋` :
                    'Welcome to Ethiopian Hospital ERP! 🏥';

                this.showEnhancedWelcomeNotification(welcomeMessage);

                // Mark as shown for this session and store timestamp
                sessionStorage.setItem('mobileWelcomeShown', 'true');
                localStorage.setItem('lastMobileWelcome', now.toString());
            }, 1500); // Slightly longer delay for better UX
        }
    }

    getUserName() {
        // Try to get user name from various sources
        const userNameElement = document.querySelector('.mobile-page-header p');
        if (userNameElement) {
            const text = userNameElement.textContent;
            const match = text.match(/Welcome back,\s*(.+?)!/);
            if (match && match[1] && match[1].trim() !== 'undefined') {
                return match[1].trim();
            }
        }
        return null;
    }

    showEnhancedWelcomeNotification(message) {
        const notification = document.createElement('div');
        notification.className = 'mobile-welcome-notification';

        notification.innerHTML = `
            <div class="mobile-welcome-content">
                <div class="mobile-welcome-icon">
                    <i class="fas fa-heart text-ethiopia-red"></i>
                </div>
                <div class="mobile-welcome-text">
                    <div class="mobile-welcome-title">${message}</div>
                    <div class="mobile-welcome-subtitle">Ethiopian Hospital ERP Mobile</div>
                </div>
                <button type="button" class="mobile-welcome-close" aria-label="Close welcome message">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Add styles for the enhanced welcome notification
        if (!document.getElementById('mobile-welcome-styles')) {
            const styles = document.createElement('style');
            styles.id = 'mobile-welcome-styles';
            styles.textContent = `
                .mobile-welcome-notification {
                    position: fixed;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    z-index: 9999;
                    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                    color: white;
                    border-radius: 12px;
                    box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
                    animation: slideInFromTop 0.5s ease-out;
                    max-width: 90vw;
                    min-width: 280px;
                }

                .mobile-welcome-content {
                    display: flex;
                    align-items: center;
                    padding: 16px 20px;
                    gap: 12px;
                }

                .mobile-welcome-icon {
                    font-size: 24px;
                    animation: heartbeat 2s ease-in-out infinite;
                }

                .mobile-welcome-text {
                    flex: 1;
                }

                .mobile-welcome-title {
                    font-weight: 600;
                    font-size: 16px;
                    margin-bottom: 2px;
                }

                .mobile-welcome-subtitle {
                    font-size: 12px;
                    opacity: 0.9;
                }

                .mobile-welcome-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                    padding: 4px;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                }

                .mobile-welcome-close:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }

                @keyframes slideInFromTop {
                    from {
                        transform: translateX(-50%) translateY(-100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(-50%) translateY(0);
                        opacity: 1;
                    }
                }

                @keyframes heartbeat {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }

                @keyframes slideOutToTop {
                    from {
                        transform: translateX(-50%) translateY(0);
                        opacity: 1;
                    }
                    to {
                        transform: translateX(-50%) translateY(-100%);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(notification);

        // Auto-remove after 6 seconds
        const autoRemoveTimer = setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOutToTop 0.5s ease-in forwards';
                setTimeout(() => {
                    notification.remove();
                }, 500);
            }
        }, 6000);

        // Manual close button
        const closeBtn = notification.querySelector('.mobile-welcome-close');
        closeBtn.addEventListener('click', () => {
            clearTimeout(autoRemoveTimer);
            notification.style.animation = 'slideOutToTop 0.5s ease-in forwards';
            setTimeout(() => {
                notification.remove();
            }, 500);
        });
    }

    // ===== UTILITY METHODS =====
    showMobileNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `mobile-alert mobile-alert-${type}`;

        // Add icon based on type
        const icons = {
            'success': 'fas fa-check-circle',
            'warning': 'fas fa-exclamation-triangle',
            'danger': 'fas fa-times-circle',
            'info': 'fas fa-info-circle'
        };

        // Truncate message for consistency using utility function
        const truncatedMessage = this.truncateText(message, 18);

        notification.innerHTML = `
            <div class="mobile-alert-content">
                <i class="${icons[type] || icons.info} me-2"></i>
                ${truncatedMessage}
            </div>
            <button type="button" class="mobile-alert-close" aria-label="Close notification">
                <i class="fas fa-times"></i>
            </button>
        `;

        const container = document.querySelector('.mobile-content-container');
        if (container) {
            // Remove any existing notifications with the same message to prevent spam
            const existingNotifications = container.querySelectorAll('.mobile-alert');
            existingNotifications.forEach(existing => {
                const existingText = existing.querySelector('.mobile-alert-content').textContent.trim();
                const newText = message.trim();
                // Remove if exact match or if it's a similar welcome/success message
                if (existingText === newText ||
                    (existingText.includes('Welcome') && newText.includes('Welcome')) ||
                    (existingText.includes('loaded successfully') && newText.includes('loaded successfully'))) {
                    existing.remove();
                }
            });

            container.insertBefore(notification, container.firstChild);

            // Auto-remove after 5 seconds
            const autoRemoveTimer = setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOutToTop 0.3s ease-in forwards';
                    setTimeout(() => {
                        notification.remove();
                    }, 300);
                }
            }, 5000);

            // Handle close button
            const closeBtn = notification.querySelector('.mobile-alert-close');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => {
                    clearTimeout(autoRemoveTimer);
                    notification.style.animation = 'slideOutToTop 0.3s ease-in forwards';
                    setTimeout(() => {
                        notification.remove();
                    }, 300);
                });
            }

            // Add swipe to dismiss functionality
            let startY = 0;
            let currentY = 0;
            let isDragging = false;

            notification.addEventListener('touchstart', (e) => {
                startY = e.touches[0].clientY;
                isDragging = true;
                notification.style.transition = 'none';
            });

            notification.addEventListener('touchmove', (e) => {
                if (!isDragging) return;
                currentY = e.touches[0].clientY;
                const deltaY = currentY - startY;

                if (deltaY < 0) { // Swiping up
                    notification.style.transform = `translateY(${deltaY}px)`;
                    notification.style.opacity = Math.max(0.3, 1 + deltaY / 100);
                }
            });

            notification.addEventListener('touchend', () => {
                if (!isDragging) return;
                isDragging = false;

                const deltaY = currentY - startY;
                notification.style.transition = 'all 0.3s ease';

                if (deltaY < -50) { // Swiped up enough to dismiss
                    clearTimeout(autoRemoveTimer);
                    notification.style.transform = 'translateY(-100%)';
                    notification.style.opacity = '0';
                    setTimeout(() => {
                        notification.remove();
                    }, 300);
                } else {
                    // Snap back
                    notification.style.transform = 'translateY(0)';
                    notification.style.opacity = '1';
                }
            });
        }
    }
    
    announceToScreenReader(message) {
        const liveRegion = document.getElementById('mobile-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
        }
    }

    // Utility function for consistent text truncation
    truncateText(text, maxLength = 18) {
        if (!text || typeof text !== 'string') return '';
        return text.length > maxLength ? text.substring(0, maxLength - 3) + '...' : text;
    }
    
    // Export chart options for use in dashboard
    getMobileChartOptions() {
        return this.mobileChartOptions;
    }

    // ===== UTILITY METHODS =====
    getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            return csrfToken.value;
        }

        // Try to get from cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }

        return '';
    }

    // ===== MOBILE BOTTOM NAVIGATION ENHANCEMENTS =====
    initMobileBottomNavigation() {
        const bottomNav = document.getElementById('mobileBottomNav');
        const navItems = bottomNav?.querySelectorAll('.mobile-bottom-nav-item');

        if (!bottomNav || !navItems.length) return;

        // Add smooth transitions and enhanced interactions
        navItems.forEach((item, index) => {
            // Add ripple effect on touch
            item.addEventListener('touchstart', (e) => {
                this.createRippleEffect(item, e);
            });

            // Add click effect
            item.addEventListener('click', (e) => {
                this.createRippleEffect(item, e);
                this.animateNavItemClick(item);
            });

            // Add hover effects for desktop
            item.addEventListener('mouseenter', () => {
                this.animateNavItemHover(item, true);
            });

            item.addEventListener('mouseleave', () => {
                this.animateNavItemHover(item, false);
            });

            // Stagger animation on load
            setTimeout(() => {
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Initialize with staggered animation
        navItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            item.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        });

        console.log('Mobile bottom navigation enhanced');
    }

    // ===== MOBILE CRUD TESTING UTILITIES =====
    initMobileCRUDTesting() {
        // Initialize CRUD testing utilities for mobile
        this.crudTester = new MobileCRUDTester();
        console.log('Mobile CRUD testing utilities initialized');
    }

    createRippleEffect(element, event) {
        const ripple = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = (event.touches ? event.touches[0].clientX : event.clientX) - rect.left - size / 2;
        const y = (event.touches ? event.touches[0].clientY : event.clientY) - rect.top - size / 2;

        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(0, 150, 57, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
            z-index: 1;
        `;

        element.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    animateNavItemClick(item) {
        item.style.transform = 'translateY(-2px) scale(0.95)';
        setTimeout(() => {
            item.style.transform = item.classList.contains('active')
                ? 'translateY(-4px) scale(1.05)'
                : 'translateY(0) scale(1)';
        }, 150);
    }

    animateNavItemHover(item, isHover) {
        if (item.classList.contains('active')) return;

        if (isHover) {
            item.style.transform = 'translateY(-2px) scale(1.02)';
        } else {
            item.style.transform = 'translateY(0) scale(1)';
        }
    }
}

// Initialize mobile dashboard
const mobileDashboard = new MobileDashboard();

// Export for global use
window.MobileDashboard = MobileDashboard;
window.mobileDashboard = mobileDashboard;
