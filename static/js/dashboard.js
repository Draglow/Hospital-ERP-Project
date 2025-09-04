// Dashboard JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Dashboard
    initSidebar();
    initCharts();
    initRealTimeUpdates();
    initGlobalSearch();
    initQuickActions();
    initResponsiveFeatures();
    initResponsiveRedirection();

    // Update active nav link
    updateActiveNavLink();

    // Force initial responsive check after a short delay
    setTimeout(function() {
        handleResponsiveChanges();
    }, 500);
});

// Responsive Features
function initResponsiveFeatures() {
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            handleResponsiveChanges();
        }, 250);
    });

    // Initial responsive setup
    handleResponsiveChanges();

    // Handle orientation change
    window.addEventListener('orientationchange', function() {
        setTimeout(handleResponsiveChanges, 500);
    });
}

// Responsive Redirection System
function initResponsiveRedirection() {
    // Store initial viewport state
    window.dashboardResponsive = {
        initialWidth: window.innerWidth,
        lastRedirectTime: 0,
        redirectCooldown: 2000, // 2 seconds cooldown between redirects
        isDesktopDashboard: window.location.pathname === '/dashboard/' || window.location.pathname === '/dashboard',
        isMobileDashboard: window.location.pathname.includes('/mobile/'),
        breakpoint: 768
    };

    // Check if we should redirect immediately on page load
    setTimeout(() => {
        const isMobile = window.innerWidth <= window.dashboardResponsive.breakpoint;
        checkResponsiveRedirection(isMobile, true);
    }, 100);
}

function checkResponsiveRedirection(isMobile, isInitialCheck = false) {
    const responsive = window.dashboardResponsive;
    const now = Date.now();

    // Skip if we're in cooldown period (prevents rapid redirects)
    if (!isInitialCheck && (now - responsive.lastRedirectTime) < responsive.redirectCooldown) {
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

    // Determine if we need to redirect
    let shouldRedirect = false;
    let targetUrl = '';

    if (isMobile && responsive.isDesktopDashboard) {
        // Redirect from desktop to mobile
        shouldRedirect = true;
        targetUrl = '/dashboard/mobile/';
    } else if (!isMobile && responsive.isMobileDashboard) {
        // Redirect from mobile to desktop
        shouldRedirect = true;
        targetUrl = '/dashboard/';
    }

    if (shouldRedirect) {
        responsive.lastRedirectTime = now;
        redirectToDashboard(targetUrl);
    }
}

function redirectToDashboard(targetUrl) {
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
    console.log('Responsive redirect:', window.location.pathname, '->', newUrl);
    window.location.href = newUrl;
}

function handleResponsiveChanges() {
    const isMobile = window.innerWidth <= 768;
    const isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;

    // Check if we need to redirect to mobile dashboard
    checkResponsiveRedirection(isMobile);

    // Force mobile layout fixes
    if (isMobile) {
        forceMobileLayout();
    }

    // Update chart configurations
    updateChartsForDevice(isMobile, isTablet);

    // Update table display
    updateTableDisplay(isMobile);

    // Update navigation
    updateNavigationForDevice(isMobile);

    // Update card layouts
    updateCardLayouts(isMobile, isTablet);
}

function forceMobileLayout() {
    // Ensure body doesn't have horizontal scroll
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';

    // Fix any elements that might be causing overflow
    const containers = document.querySelectorAll('.container, .container-fluid');
    containers.forEach(container => {
        container.style.maxWidth = '100%';
        container.style.paddingLeft = '0.75rem';
        container.style.paddingRight = '0.75rem';
    });

    // Fix rows
    const rows = document.querySelectorAll('.row');
    rows.forEach(row => {
        row.style.marginLeft = '0';
        row.style.marginRight = '0';
        row.style.maxWidth = '100%';
    });

    // Fix columns
    const cols = document.querySelectorAll('[class*="col-"]');
    cols.forEach(col => {
        col.style.paddingLeft = '0.5rem';
        col.style.paddingRight = '0.5rem';
        col.style.maxWidth = '100%';
    });

    // Fix dashboard cards
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
        card.style.maxWidth = '100%';
        card.style.width = '100%';
        card.style.boxSizing = 'border-box';
    });
}

function updateChartsForDevice(isMobile, isTablet) {
    // Get all chart instances
    const charts = Chart.getChart ? Object.values(Chart.instances || {}) : [];

    charts.forEach(chart => {
        if (chart && chart.options) {
            // Update font sizes
            if (chart.options.scales) {
                Object.keys(chart.options.scales).forEach(scaleKey => {
                    const scale = chart.options.scales[scaleKey];
                    if (scale.ticks) {
                        scale.ticks.font = scale.ticks.font || {};
                        scale.ticks.font.size = isMobile ? 10 : isTablet ? 11 : 12;
                        scale.ticks.maxRotation = isMobile ? 45 : 0;
                    }
                });
            }

            // Update legend
            if (chart.options.plugins && chart.options.plugins.legend) {
                const legend = chart.options.plugins.legend;
                if (legend.labels) {
                    legend.labels.font = legend.labels.font || {};
                    legend.labels.font.size = isMobile ? 10 : isTablet ? 11 : 12;
                    legend.labels.boxWidth = isMobile ? 8 : 12;
                    legend.labels.boxHeight = isMobile ? 8 : 12;
                }

                // Update legend position for doughnut charts
                if (chart.config.type === 'doughnut') {
                    legend.position = isMobile ? 'bottom' : 'right';
                }
            }

            // Update cutout for doughnut charts
            if (chart.config.type === 'doughnut') {
                chart.options.cutout = isMobile ? '50%' : '60%';
            }

            // Update element sizes
            if (chart.options.elements) {
                if (chart.options.elements.point) {
                    chart.options.elements.point.radius = isMobile ? 3 : 4;
                    chart.options.elements.point.hoverRadius = isMobile ? 5 : 6;
                }
                if (chart.options.elements.line) {
                    chart.options.elements.line.borderWidth = isMobile ? 2 : 3;
                }
                if (chart.options.elements.bar) {
                    chart.options.elements.bar.borderRadius = isMobile ? 6 : 10;
                }
            }

            // Update chart
            chart.update('none');
        }
    });
}

function updateTableDisplay(isMobile) {
    const tables = document.querySelectorAll('.table-responsive');
    const tableCards = document.querySelectorAll('.table-cards');

    if (isMobile) {
        // Show card layout, hide table layout
        tables.forEach(table => {
            table.style.display = 'none';
        });
        tableCards.forEach(cards => {
            cards.style.display = 'block';
        });
    } else {
        // Show table layout, hide card layout
        tables.forEach(table => {
            table.style.display = 'block';
        });
        tableCards.forEach(cards => {
            cards.style.display = 'none';
        });
    }
}

function updateNavigationForDevice(isMobile) {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (sidebar && sidebarToggle) {
        if (isMobile) {
            // Ensure mobile behavior
            sidebar.classList.remove('collapsed');
            sidebar.classList.remove('show');
        } else {
            // Restore desktop state
            const savedState = localStorage.getItem('sidebarCollapsed');
            if (savedState === 'true') {
                sidebar.classList.add('collapsed');
            }
        }
    }
}

function updateCardLayouts(isMobile, isTablet) {
    const quickActions = document.querySelector('.quick-actions');

    if (quickActions) {
        if (isMobile) {
            quickActions.style.gridTemplateColumns = '1fr';
        } else if (isTablet) {
            quickActions.style.gridTemplateColumns = 'repeat(2, 1fr)';
        } else {
            quickActions.style.gridTemplateColumns = 'repeat(4, 1fr)';
        }
    }
}

// Sidebar Functionality
function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const body = document.body;

    if (!sidebarToggle || !sidebar) return;

    // Create overlay for mobile
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        body.appendChild(overlay);
    }

    // Check if mobile
    function isMobile() {
        return window.innerWidth <= 768;
    }

    // Toggle sidebar
    function toggleSidebar() {
        if (isMobile()) {
            // Mobile behavior
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
            body.classList.toggle('sidebar-open');

            // Prevent body scroll when sidebar is open
            if (sidebar.classList.contains('show')) {
                body.style.overflow = 'hidden';
            } else {
                body.style.overflow = '';
            }
        } else {
            // Desktop behavior
            sidebar.classList.toggle('collapsed');

            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        }
    }

    // Close sidebar
    function closeSidebar() {
        if (isMobile()) {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
            body.classList.remove('sidebar-open');
            body.style.overflow = '';
        }
    }

    // Event listeners
    sidebarToggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        toggleSidebar();
    });

    // Close sidebar when clicking overlay
    overlay.addEventListener('click', closeSidebar);

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (isMobile() && sidebar.classList.contains('show')) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                closeSidebar();
            }
        }
    });

    // Handle window resize with debouncing
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const wasMobile = sidebar.classList.contains('show') || body.classList.contains('sidebar-open');

            if (!isMobile()) {
                // Switching to desktop
                sidebar.classList.remove('show');
                overlay.classList.remove('show');
                body.classList.remove('sidebar-open');
                body.style.overflow = '';

                // Restore desktop sidebar state
                const savedState = localStorage.getItem('sidebarCollapsed');
                if (savedState === 'true') {
                    sidebar.classList.add('collapsed');
                } else {
                    sidebar.classList.remove('collapsed');
                }
            } else {
                // Switching to mobile or staying mobile
                sidebar.classList.remove('collapsed');
                if (wasMobile) {
                    // Keep sidebar open if it was open
                    sidebar.classList.add('show');
                    overlay.classList.add('show');
                    body.classList.add('sidebar-open');
                    body.style.overflow = 'hidden';
                } else {
                    // Ensure sidebar is hidden
                    sidebar.classList.remove('show');
                    overlay.classList.remove('show');
                    body.classList.remove('sidebar-open');
                    body.style.overflow = '';
                }
            }
        }, 100);
    });

    // Touch gestures for mobile
    if ('ontouchstart' in window) {
        let startX = 0;
        let currentX = 0;
        let isDragging = false;

        // Swipe to open sidebar from left edge
        document.addEventListener('touchstart', function(e) {
            if (isMobile() && !sidebar.classList.contains('show')) {
                startX = e.touches[0].clientX;
                if (startX < 20) { // Only from left edge
                    isDragging = true;
                }
            }
        });

        document.addEventListener('touchmove', function(e) {
            if (isDragging && isMobile()) {
                currentX = e.touches[0].clientX;
                const deltaX = currentX - startX;

                if (deltaX > 50) { // Swipe right threshold
                    toggleSidebar();
                    isDragging = false;
                }
            }
        });

        document.addEventListener('touchend', function() {
            isDragging = false;
        });

        // Swipe to close sidebar
        sidebar.addEventListener('touchstart', function(e) {
            if (isMobile() && sidebar.classList.contains('show')) {
                startX = e.touches[0].clientX;
                isDragging = true;
            }
        });

        sidebar.addEventListener('touchmove', function(e) {
            if (isDragging && isMobile() && sidebar.classList.contains('show')) {
                currentX = e.touches[0].clientX;
                const deltaX = startX - currentX;

                if (deltaX > 50) { // Swipe left threshold
                    closeSidebar();
                    isDragging = false;
                }
            }
        });
    }

    // Initialize sidebar state
    initializeSidebarState();

    function initializeSidebarState() {
        if (isMobile()) {
            // Force mobile state
            sidebar.classList.remove('collapsed');
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
            body.classList.remove('sidebar-open');
            body.style.overflow = '';
        } else {
            // Desktop state
            const savedState = localStorage.getItem('sidebarCollapsed');
            if (savedState === 'true') {
                sidebar.classList.add('collapsed');
            } else {
                sidebar.classList.remove('collapsed');
            }
        }
    }

    // Force initial layout check
    setTimeout(initializeSidebarState, 100);
}

// Initialize Charts
function initCharts() {
    // Patient Trends Chart
    const patientTrendsCtx = document.getElementById('patientTrendsChart');
    if (patientTrendsCtx) {
        new Chart(patientTrendsCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'New Patients',
                    data: [120, 190, 300, 500, 200, 300],
                    borderColor: '#009639',
                    backgroundColor: 'rgba(0, 150, 57, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
    
    // Revenue Chart - moved to dashboard template for real data integration
    
    // Appointments Chart
    const appointmentsCtx = document.getElementById('appointmentsChart');
    if (appointmentsCtx) {
        new Chart(appointmentsCtx, {
            type: 'bar',
            data: {
                labels: ['Dr. Alemayehu', 'Dr. Hanan', 'Dr. Bekele', 'Dr. Sara', 'Dr. Yonas'],
                datasets: [{
                    label: 'Appointments',
                    data: [25, 30, 20, 35, 15],
                    backgroundColor: [
                        '#009639',
                        '#FFCD00',
                        '#DA020E',
                        '#0F47AF',
                        '#009639'
                    ],
                    borderRadius: 10,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
}

// Real-time Updates
function initRealTimeUpdates() {
    // Update dashboard stats every 30 seconds
    setInterval(updateDashboardStats, 30000);
    
    // Update notifications
    setInterval(updateNotifications, 60000);
    
    // Initial load
    updateDashboardStats();
}

function updateDashboardStats() {
    // Fetch real-time data from server
    fetch('/dashboard/api/dashboard-stats/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update stats with real data
            const stats = [
                { id: 'todayAppointments', value: data.today_appointments || 0 },
                { id: 'totalPatients', value: data.total_patients || 0 },
                { id: 'monthlyRevenue', value: data.monthly_revenue || 0 },
                { id: 'lowStockMedicines', value: data.low_stock_medicines || 0 }
            ];

            stats.forEach(stat => {
                const element = document.getElementById(stat.id);
                if (element) {
                    const currentValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
                    if (currentValue !== stat.value) {
                        animateNumber(element, currentValue, stat.value);
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching dashboard stats:', error);
            // Fallback to current values if fetch fails
        });
}

function animateNumber(element, start, end) {
    const duration = 1000;
    const increment = (end - start) / (duration / 16);
    let current = start;
    
    const updateNumber = () => {
        current += increment;
        if ((increment > 0 && current < end) || (increment < 0 && current > end)) {
            element.textContent = Math.floor(current).toLocaleString();
            requestAnimationFrame(updateNumber);
        } else {
            element.textContent = end.toLocaleString();
        }
    };
    
    updateNumber();
}

function updateNotifications() {
    // Simulate new notifications
    const notificationBadge = document.querySelector('.position-absolute.badge');
    if (notificationBadge) {
        const currentCount = parseInt(notificationBadge.textContent);
        const newCount = Math.max(0, currentCount + Math.floor(Math.random() * 3) - 1);
        updateNotificationBadge(newCount);
    }
}

// Enhanced notification badge management
function updateNotificationBadge(count) {
    const badge = document.getElementById('notificationBadge');
    if (!badge) return;

    if (count === 0) {
        badge.style.display = 'none';
        badge.classList.remove('large-count');
        badge.removeAttribute('data-count');
    } else {
        badge.style.display = 'flex';

        // Handle different count ranges
        if (count > 99) {
            badge.textContent = '99+';
            badge.setAttribute('data-count', '99+');
            badge.classList.add('large-count');
        } else if (count > 9) {
            badge.textContent = count;
            badge.classList.add('large-count');
            badge.removeAttribute('data-count');
        } else {
            badge.textContent = count;
            badge.classList.remove('large-count');
            badge.removeAttribute('data-count');
        }
    }
}

// Enhanced Global Search with advanced features
function initGlobalSearch() {
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;

    // Create enhanced search results dropdown
    const searchResults = document.createElement('div');
    searchResults.className = 'search-results-enhanced';
    searchResults.innerHTML = `
        <div class="search-loading" style="display: none;">
            <div class="d-flex align-items-center justify-content-center py-3">
                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                <span>Searching...</span>
            </div>
        </div>
        <div class="search-content"></div>
        <div class="search-footer">
            <div class="search-shortcuts">
                <small class="text-muted">
                    <kbd>↑</kbd><kbd>↓</kbd> Navigate • <kbd>Enter</kbd> Select • <kbd>Esc</kbd> Close
                </small>
            </div>
        </div>
    `;

    // Style the search results
    searchResults.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        max-height: 400px;
        overflow-y: auto;
        z-index: 1000;
        display: none;
        backdrop-filter: blur(10px);
    `;

    searchInput.parentElement.style.position = 'relative';
    searchInput.parentElement.appendChild(searchResults);

    // Initialize search state
    let searchTimeout;
    let currentResults = [];
    let selectedIndex = -1;
    let searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');

    // Enhanced input handler with debouncing
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        selectedIndex = -1;

        if (query.length === 0) {
            showSearchHistory();
            return;
        }

        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        // Show loading state
        showSearchLoading();

        searchTimeout = setTimeout(() => {
            performEnhancedSearch(query, searchResults);
        }, 300);
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const resultsVisible = searchResults.style.display !== 'none';

        if (!resultsVisible) return;

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, currentResults.length - 1);
                updateSelection();
                break;
            case 'ArrowUp':
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                updateSelection();
                break;
            case 'Enter':
                e.preventDefault();
                if (selectedIndex >= 0 && currentResults[selectedIndex]) {
                    selectResult(currentResults[selectedIndex]);
                }
                break;
            case 'Escape':
                e.preventDefault();
                searchResults.style.display = 'none';
                searchInput.blur();
                break;
        }
    });

    // Show search history on focus
    searchInput.addEventListener('focus', function() {
        if (this.value.trim() === '') {
            showSearchHistory();
        }
    });

    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.parentElement.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });

    // Helper functions
    function showSearchLoading() {
        searchResults.style.display = 'block';
        searchResults.querySelector('.search-loading').style.display = 'block';
        searchResults.querySelector('.search-content').innerHTML = '';
    }

    function hideSearchLoading() {
        searchResults.querySelector('.search-loading').style.display = 'none';
    }

    function showSearchHistory() {
        if (searchHistory.length === 0) return;

        const historyHtml = `
            <div class="search-section">
                <div class="search-section-header">
                    <small class="text-muted fw-semibold">Recent Searches</small>
                    <button class="btn btn-sm btn-link text-muted p-0" onclick="clearSearchHistory()">Clear</button>
                </div>
                ${searchHistory.slice(0, 5).map(item => `
                    <div class="search-result-item" data-type="${item.type}" data-id="${item.id}" data-query="${item.query}">
                        <div class="d-flex align-items-center">
                            <i class="fas fa-history me-2 text-muted"></i>
                            <div class="flex-grow-1">
                                <div class="fw-semibold">${item.query}</div>
                                <small class="text-muted">${item.type} • ${new Date(item.timestamp).toLocaleDateString()}</small>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        searchResults.querySelector('.search-content').innerHTML = historyHtml;
        searchResults.style.display = 'block';
        hideSearchLoading();

        // Add click handlers for history items
        addResultClickHandlers();
    }

    function updateSelection() {
        const items = searchResults.querySelectorAll('.search-result-item');
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ block: 'nearest' });
            } else {
                item.classList.remove('selected');
            }
        });
    }

    function selectResult(result) {
        addToSearchHistory(searchInput.value, result.type, result.id);
        navigateToResult(result.type, result.id);
        searchResults.style.display = 'none';
        searchInput.value = '';
    }

    function addToSearchHistory(query, type, id) {
        const historyItem = {
            query: query,
            type: type,
            id: id,
            timestamp: new Date().toISOString()
        };

        // Remove duplicate if exists
        searchHistory = searchHistory.filter(item =>
            !(item.query === query && item.type === type && item.id === id)
        );

        // Add to beginning
        searchHistory.unshift(historyItem);

        // Keep only last 10 items
        searchHistory = searchHistory.slice(0, 10);

        // Save to localStorage
        localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
    }

    function addResultClickHandlers() {
        searchResults.querySelectorAll('.search-result-item').forEach((item, index) => {
            item.addEventListener('click', function() {
                const result = {
                    type: this.dataset.type,
                    id: this.dataset.id,
                    name: this.querySelector('.fw-semibold').textContent
                };
                selectResult(result);
            });

            item.addEventListener('mouseenter', function() {
                selectedIndex = index;
                updateSelection();
            });
        });
    }

    // Global function to clear search history
    window.clearSearchHistory = function() {
        searchHistory = [];
        localStorage.removeItem('searchHistory');
        searchResults.style.display = 'none';
        searchInput.focus();
    };
}

function performEnhancedSearch(query, resultsContainer) {
    // Enhanced search with multiple data types and better organization
    const searchPromises = [
        searchPatients(query),
        searchAppointments(query),
        searchDoctors(query),
        searchMedicines(query)
    ];

    Promise.all(searchPromises)
        .then(results => {
            const [patients, appointments, doctors, medicines] = results;
            currentResults = [];

            hideSearchLoading();

            let html = '';

            // Patients section
            if (patients.length > 0) {
                html += createSearchSection('Patients', patients, 'user');
                currentResults.push(...patients);
            }

            // Appointments section
            if (appointments.length > 0) {
                html += createSearchSection('Appointments', appointments, 'calendar');
                currentResults.push(...appointments);
            }

            // Doctors section
            if (doctors.length > 0) {
                html += createSearchSection('Doctors', doctors, 'user-md');
                currentResults.push(...doctors);
            }

            // Medicines section
            if (medicines.length > 0) {
                html += createSearchSection('Medicines', medicines, 'pills');
                currentResults.push(...medicines);
            }

            if (html === '') {
                html = `
                    <div class="search-no-results">
                        <div class="text-center py-4">
                            <i class="fas fa-search text-muted fs-3 mb-2"></i>
                            <div class="text-muted">No results found for "${query}"</div>
                            <small class="text-muted">Try different keywords or check spelling</small>
                        </div>
                    </div>
                `;
            }

            resultsContainer.querySelector('.search-content').innerHTML = html;
            resultsContainer.style.display = 'block';

            // Add click handlers
            addResultClickHandlers();
        })
        .catch(error => {
            hideSearchLoading();
            console.error('Search error:', error);
            resultsContainer.querySelector('.search-content').innerHTML = `
                <div class="search-error">
                    <div class="text-center py-4">
                        <i class="fas fa-exclamation-triangle text-warning fs-3 mb-2"></i>
                        <div class="text-muted">Search temporarily unavailable</div>
                        <small class="text-muted">Please try again later</small>
                    </div>
                </div>
            `;
            resultsContainer.style.display = 'block';
        });
}

function createSearchSection(title, results, defaultIcon) {
    return `
        <div class="search-section">
            <div class="search-section-header">
                <small class="text-muted fw-semibold">${title}</small>
                <small class="text-muted">${results.length} result${results.length !== 1 ? 's' : ''}</small>
            </div>
            ${results.map(result => `
                <div class="search-result-item" data-type="${result.type}" data-id="${result.id}">
                    <div class="d-flex align-items-center">
                        <i class="fas fa-${result.icon || defaultIcon} me-2 text-ethiopia-green"></i>
                        <div class="flex-grow-1">
                            <div class="fw-semibold">${highlightQuery(result.name, result.query || '')}</div>
                            <small class="text-muted">${result.subtitle || result.id}</small>
                        </div>
                        ${result.badge ? `<span class="badge bg-${result.badgeColor || 'secondary'} ms-2">${result.badge}</span>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function highlightQuery(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Mock search functions (replace with real API calls)
async function searchPatients(query) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 100));

    const mockPatients = [
        { type: 'patient', id: 'PAT20240001', name: 'Alemayehu Tadesse', subtitle: 'Age: 45 • Phone: +251911234567' },
        { type: 'patient', id: 'PAT20240002', name: 'Hanan Mohammed', subtitle: 'Age: 32 • Phone: +251922345678' },
        { type: 'patient', id: 'PAT20240003', name: 'Dawit Bekele', subtitle: 'Age: 28 • Phone: +251933456789' }
    ];

    return mockPatients.filter(patient =>
        patient.name.toLowerCase().includes(query.toLowerCase()) ||
        patient.id.toLowerCase().includes(query.toLowerCase())
    ).map(patient => ({ ...patient, query }));
}

async function searchAppointments(query) {
    await new Promise(resolve => setTimeout(resolve, 150));

    const mockAppointments = [
        { type: 'appointment', id: 'APT20240001', name: 'Dr. Bekele - Alemayehu Tadesse', subtitle: 'Today 2:00 PM', badge: 'Scheduled', badgeColor: 'primary' },
        { type: 'appointment', id: 'APT20240002', name: 'Dr. Sara - Hanan Mohammed', subtitle: 'Tomorrow 10:00 AM', badge: 'Confirmed', badgeColor: 'success' },
        { type: 'appointment', id: 'APT20240003', name: 'Dr. Yohannes - Dawit Bekele', subtitle: 'Dec 25 3:00 PM', badge: 'In Progress', badgeColor: 'warning' }
    ];

    return mockAppointments.filter(appointment =>
        appointment.name.toLowerCase().includes(query.toLowerCase()) ||
        appointment.id.toLowerCase().includes(query.toLowerCase())
    ).map(appointment => ({ ...appointment, query }));
}

async function searchDoctors(query) {
    await new Promise(resolve => setTimeout(resolve, 120));

    const mockDoctors = [
        { type: 'doctor', id: 'DOC001', name: 'Dr. Sara Yohannes', subtitle: 'Cardiology • Available', badge: 'Online', badgeColor: 'success' },
        { type: 'doctor', id: 'DOC002', name: 'Dr. Bekele Tadesse', subtitle: 'Pediatrics • Busy', badge: 'Busy', badgeColor: 'warning' },
        { type: 'doctor', id: 'DOC003', name: 'Dr. Meron Alemayehu', subtitle: 'Neurology • Available', badge: 'Online', badgeColor: 'success' }
    ];

    return mockDoctors.filter(doctor =>
        doctor.name.toLowerCase().includes(query.toLowerCase()) ||
        doctor.id.toLowerCase().includes(query.toLowerCase()) ||
        doctor.subtitle.toLowerCase().includes(query.toLowerCase())
    ).map(doctor => ({ ...doctor, query }));
}

async function searchMedicines(query) {
    await new Promise(resolve => setTimeout(resolve, 80));

    const mockMedicines = [
        { type: 'medicine', id: 'MED001', name: 'Paracetamol 500mg', subtitle: 'Stock: 150 • Expires: Dec 2025', badge: 'In Stock', badgeColor: 'success' },
        { type: 'medicine', id: 'MED002', name: 'Amoxicillin 250mg', subtitle: 'Stock: 25 • Expires: Mar 2025', badge: 'Low Stock', badgeColor: 'warning' },
        { type: 'medicine', id: 'MED003', name: 'Ibuprofen 400mg', subtitle: 'Stock: 0 • Expires: Jan 2025', badge: 'Out of Stock', badgeColor: 'danger' }
    ];

    return mockMedicines.filter(medicine =>
        medicine.name.toLowerCase().includes(query.toLowerCase()) ||
        medicine.id.toLowerCase().includes(query.toLowerCase())
    ).map(medicine => ({ ...medicine, query }));
}

function getIconForType(type) {
    const icons = {
        'patient': 'user',
        'doctor': 'user-md',
        'appointment': 'calendar',
        'medicine': 'pills'
    };
    return icons[type] || 'search';
}

function navigateToResult(type, id) {
    const routes = {
        'patient': '/dashboard/patients/',
        'doctor': '/doctors/',
        'appointment': '/appointments/',
        'medicine': '/pharmacy/'
    };
    
    if (routes[type]) {
        window.location.href = routes[type];
    }
}

// Quick Actions
function initQuickActions() {
    const quickActionBtns = document.querySelectorAll('.quick-action-btn');
    
    quickActionBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
            this.style.pointerEvents = 'none';
            
            // Simulate loading
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.pointerEvents = 'auto';
            }, 1000);
        });
    });
}

// Update Active Navigation Link
function updateActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Utility Functions
function showDashboardNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Export functions
window.Dashboard = {
    showNotification: showDashboardNotification,
    updateStats: updateDashboardStats,
    animateNumber: animateNumber
};
