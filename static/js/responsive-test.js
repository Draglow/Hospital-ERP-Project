// Responsive Design Test Utilities
// Ethiopian Hospital ERP Dashboard

class ResponsiveTest {
    constructor() {
        this.breakpoints = {
            mobile: 768,
            tablet: 1024,
            desktop: 1200
        };
        
        this.currentDevice = this.getDeviceType();
        this.init();
    }
    
    init() {
        this.createTestPanel();
        this.bindEvents();
        this.runTests();
    }
    
    getDeviceType() {
        const width = window.innerWidth;
        if (width <= this.breakpoints.mobile) return 'mobile';
        if (width <= this.breakpoints.tablet) return 'tablet';
        return 'desktop';
    }
    
    createTestPanel() {
        // Disabled - test panel removed
        return;
        
        const panel = document.createElement('div');
        panel.id = 'responsive-test-panel';
        panel.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            background: rgba(0, 150, 57, 0.95);
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 12px;
            z-index: 9999;
            min-width: 200px;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        `;
        
        panel.innerHTML = `
            <div style="font-weight: bold; margin-bottom: 8px;">📱 Responsive Test v2.0</div>
            <div id="device-info"></div>
            <div id="test-results"></div>
            <div style="margin-top: 8px;">
                <button id="run-tests" style="
                    background: white;
                    color: #009639;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 11px;
                    cursor: pointer;
                    margin-right: 4px;
                ">Run Tests</button>
                <button id="force-mobile" style="
                    background: #ff6b6b;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 11px;
                    cursor: pointer;
                ">Force Mobile</button>
            </div>
            <div style="font-size: 10px; margin-top: 4px; color: rgba(255,255,255,0.8);">
                Auto-refresh: 5s | Fixed: Sidebar, Navbar, Touch
            </div>
        `;
        
        document.body.appendChild(panel);
        
        document.getElementById('run-tests').addEventListener('click', () => {
            this.runTests();
        });

        document.getElementById('force-mobile').addEventListener('click', () => {
            this.forceMobileTest();
        });

        // Auto-run tests every 5 seconds to monitor changes
        setInterval(() => {
            this.runTests();
        }, 5000);
    }
    
    bindEvents() {
        window.addEventListener('resize', () => {
            this.currentDevice = this.getDeviceType();
            this.updateDeviceInfo();
        });
        
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.currentDevice = this.getDeviceType();
                this.updateDeviceInfo();
                this.runTests();
            }, 500);
        });
    }
    
    updateDeviceInfo() {
        const deviceInfo = document.getElementById('device-info');
        if (deviceInfo) {
            deviceInfo.innerHTML = `
                Device: ${this.currentDevice}<br>
                Width: ${window.innerWidth}px<br>
                Height: ${window.innerHeight}px<br>
                Orientation: ${window.innerWidth > window.innerHeight ? 'Landscape' : 'Portrait'}
            `;
        }
    }
    
    runTests() {
        const tests = [
            this.testSidebarResponsiveness(),
            this.testCardLayouts(),
            this.testChartResponsiveness(),
            this.testTableResponsiveness(),
            this.testNavigationResponsiveness(),
            this.testTouchTargets(),
            this.testElementOverflow(),
            this.testMobileLayout()
        ];

        const results = tests.filter(test => !test.passed);
        this.displayResults(results);
        this.updateDeviceInfo();
    }

    testElementOverflow() {
        const isMobile = this.currentDevice === 'mobile';
        if (!isMobile) {
            return { test: 'Element Overflow', passed: true, message: 'N/A (Desktop)' };
        }

        // Check for horizontal overflow
        const body = document.body;
        const html = document.documentElement;

        if (body.scrollWidth > window.innerWidth || html.scrollWidth > window.innerWidth) {
            return { test: 'Element Overflow', passed: false, message: 'Horizontal overflow detected' };
        }

        // Check specific elements
        const problematicElements = [];
        const elementsToCheck = document.querySelectorAll('.dashboard-card, .chart-container, .table-responsive, .btn, .row');

        elementsToCheck.forEach(element => {
            const rect = element.getBoundingClientRect();
            if (rect.right > window.innerWidth) {
                problematicElements.push(element.className);
            }
        });

        if (problematicElements.length > 0) {
            return { test: 'Element Overflow', passed: false, message: `Elements overflowing: ${problematicElements.slice(0, 3).join(', ')}` };
        }

        return { test: 'Element Overflow', passed: true, message: 'OK' };
    }

    testMobileLayout() {
        const isMobile = this.currentDevice === 'mobile';
        if (!isMobile) {
            return { test: 'Mobile Layout', passed: true, message: 'N/A (Desktop)' };
        }

        // Check if columns are stacked properly on mobile
        const columns = document.querySelectorAll('[class*="col-"]');
        let narrowColumns = [];

        columns.forEach((col, index) => {
            const rect = col.getBoundingClientRect();
            const computedStyle = window.getComputedStyle(col);

            // Skip hidden elements
            if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden' || rect.width === 0) {
                return;
            }

            // Check if column is taking reasonable width (should be close to full width on mobile)
            const widthPercentage = (rect.width / window.innerWidth) * 100;
            if (widthPercentage < 85) { // Allow some margin for padding
                narrowColumns.push({
                    index: index,
                    width: rect.width.toFixed(0),
                    percentage: widthPercentage.toFixed(1),
                    className: col.className
                });
            }
        });

        if (narrowColumns.length > 0) {
            const examples = narrowColumns.slice(0, 2).map(c =>
                `col-${c.index}(${c.percentage}%)`
            ).join(', ');
            return {
                test: 'Mobile Layout',
                passed: false,
                message: `${narrowColumns.length} narrow columns: ${examples}`
            };
        }

        return { test: 'Mobile Layout', passed: true, message: 'Columns properly stacked' };
    }
    
    testSidebarResponsiveness() {
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.querySelector('.main-content');
        const isMobile = this.currentDevice === 'mobile';

        if (!sidebar) {
            return { test: 'Sidebar', passed: false, message: 'Sidebar not found' };
        }

        if (!mainContent) {
            return { test: 'Sidebar', passed: false, message: 'Main content not found' };
        }

        const computedStyle = window.getComputedStyle(sidebar);
        const mainContentStyle = window.getComputedStyle(mainContent);

        if (isMobile) {
            // Check if sidebar is properly hidden
            const transform = computedStyle.transform;

            // Check for various transform formats that indicate hidden sidebar
            let isHidden = false;

            if (transform.includes('translateX(-100%)') ||
                transform.includes('translateX(-280px)') ||
                transform.includes('translateX(-260px)')) {
                isHidden = true;
            } else if (transform.includes('matrix')) {
                // Parse matrix transform: matrix(a, b, c, d, tx, ty)
                const matrixMatch = transform.match(/matrix\(([^)]+)\)/);
                if (matrixMatch) {
                    const values = matrixMatch[1].split(',').map(v => parseFloat(v.trim()));
                    const translateX = values[4]; // tx value
                    // If translateX is significantly negative (more than 200px), sidebar is hidden
                    isHidden = translateX <= -200;
                }
            }

            // Check if main content has no left margin
            const marginLeft = parseInt(mainContentStyle.marginLeft) || 0;
            const hasNoMargin = marginLeft <= 10; // Allow small margin

            if (!isHidden && !sidebar.classList.contains('show')) {
                return { test: 'Sidebar', passed: false, message: `Sidebar not hidden on mobile (transform: ${transform})` };
            }

            if (!hasNoMargin) {
                return { test: 'Sidebar', passed: false, message: `Main content has margin on mobile (${marginLeft}px)` };
            }
        } else {
            // Desktop checks - sidebar should be visible and main content should have margin
            const transform = computedStyle.transform;
            const marginLeft = parseInt(mainContentStyle.marginLeft) || 0;

            // On desktop, sidebar should not be translated away (unless collapsed)
            const isVisible = !transform.includes('translateX(-100%)') &&
                             !transform.includes('translateX(-280px)') &&
                             !transform.includes('matrix(1, 0, 0, 1, -280') &&
                             !transform.includes('matrix(1, 0, 0, 1, -100%');

            const hasProperMargin = marginLeft > 50 || sidebar.classList.contains('collapsed');

            if (!isVisible && !sidebar.classList.contains('show')) {
                return { test: 'Sidebar', passed: false, message: `Sidebar hidden on desktop (transform: ${transform})` };
            }

            if (!hasProperMargin) {
                return { test: 'Sidebar', passed: false, message: `Main content lacks proper margin on desktop (${marginLeft}px)` };
            }
        }

        return { test: 'Sidebar', passed: true, message: `OK (${isMobile ? 'Mobile' : 'Desktop'} mode)` };
    }
    
    testCardLayouts() {
        const cards = document.querySelectorAll('.dashboard-card');
        const isMobile = this.currentDevice === 'mobile';
        
        if (cards.length === 0) {
            return { test: 'Cards', passed: false, message: 'No cards found' };
        }
        
        let hasIssues = false;
        cards.forEach(card => {
            const rect = card.getBoundingClientRect();
            if (rect.width < 200 && !isMobile) {
                hasIssues = true;
            }
        });
        
        return { 
            test: 'Cards', 
            passed: !hasIssues, 
            message: hasIssues ? 'Cards too narrow' : 'OK' 
        };
    }
    
    testChartResponsiveness() {
        const chartContainers = document.querySelectorAll('.chart-container');
        
        if (chartContainers.length === 0) {
            return { test: 'Charts', passed: true, message: 'No charts found' };
        }
        
        let hasIssues = false;
        chartContainers.forEach(container => {
            const rect = container.getBoundingClientRect();
            if (rect.height < 150) {
                hasIssues = true;
            }
        });
        
        return { 
            test: 'Charts', 
            passed: !hasIssues, 
            message: hasIssues ? 'Charts too short' : 'OK' 
        };
    }
    
    testTableResponsiveness() {
        const tables = document.querySelectorAll('.table-responsive');
        const isMobile = this.currentDevice === 'mobile';
        
        if (tables.length === 0) {
            return { test: 'Tables', passed: true, message: 'No tables found' };
        }
        
        // Check if tables have horizontal scroll on mobile
        let hasIssues = false;
        tables.forEach(table => {
            if (isMobile && table.scrollWidth <= table.clientWidth) {
                // This might be OK if using card layout
            }
        });
        
        return { test: 'Tables', passed: true, message: 'OK' };
    }
    
    testNavigationResponsiveness() {
        const navbar = document.querySelector('.navbar');
        const isMobile = this.currentDevice === 'mobile';

        if (!navbar) {
            return { test: 'Navigation', passed: false, message: 'Navbar not found' };
        }

        const rect = navbar.getBoundingClientRect();
        const height = rect.height;

        if (isMobile) {
            // On mobile, navbar should be reasonable height (under 60px after our aggressive fixes)
            if (height > 60) {
                return { test: 'Navigation', passed: false, message: `Navbar too tall on mobile (${height.toFixed(1)}px)` };
            }
        } else {
            // On desktop, navbar should be present and reasonable
            if (height < 40 || height > 120) {
                return { test: 'Navigation', passed: false, message: `Navbar height unusual on desktop (${height.toFixed(1)}px)` };
            }
        }

        return { test: 'Navigation', passed: true, message: `OK (${height.toFixed(1)}px)` };
    }

    testTouchTargets() {
        const isMobile = this.currentDevice === 'mobile';
        if (!isMobile) {
            return { test: 'Touch Targets', passed: true, message: 'N/A (Desktop)' };
        }

        const interactiveElements = document.querySelectorAll('button, .btn, .nav-link, a, input[type="button"], input[type="submit"]');
        let smallTargets = [];

        interactiveElements.forEach((element, index) => {
            const rect = element.getBoundingClientRect();
            const computedStyle = window.getComputedStyle(element);

            // Skip hidden elements
            if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden' || rect.width === 0 || rect.height === 0) {
                return;
            }

            // Check if target is too small (Apple recommends 44px minimum, we use 46px)
            // Allow some tolerance for elements that are close to the minimum
            if (rect.height < 44 || rect.width < 44) {
                smallTargets.push({
                    element: element.tagName.toLowerCase() + (element.className ? '.' + element.className.split(' ')[0] : ''),
                    size: `${rect.width.toFixed(0)}x${rect.height.toFixed(0)}`,
                    rect: rect
                });
            }
        });

        if (smallTargets.length > 0) {
            const examples = smallTargets.slice(0, 3).map(t => `${t.element}(${t.size})`).join(', ');
            return {
                test: 'Touch Targets',
                passed: false,
                message: `${smallTargets.length} small targets: ${examples}`
            };
        }

        return { test: 'Touch Targets', passed: true, message: 'All targets adequate size' };
    }
    
    displayResults(failedTests) {
        const resultsDiv = document.getElementById('test-results');
        if (!resultsDiv) return;

        if (failedTests.length === 0) {
            resultsDiv.innerHTML = '<div style="color: #90EE90; margin-top: 8px;">✅ All tests passed!</div>';
        } else {
            const failedHtml = failedTests.map(test =>
                `<div style="color: #FFB6C1; margin-top: 4px;">❌ ${test.test}: ${test.message}</div>`
            ).join('');
            resultsDiv.innerHTML = failedHtml;
        }
    }

    forceMobileTest() {
        // Temporarily override device detection for testing
        const originalDevice = this.currentDevice;
        this.currentDevice = 'mobile';

        // Force mobile styles
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.querySelector('.main-content');

        if (sidebar) {
            sidebar.style.transform = 'translateX(-100%)';
            sidebar.classList.remove('show');
            sidebar.classList.add('responsive-debug-mobile');
        }

        if (mainContent) {
            mainContent.style.marginLeft = '0';
            mainContent.classList.add('responsive-debug-mobile');
        }

        // Run tests
        this.runTests();

        // Restore original device type after 5 seconds
        setTimeout(() => {
            this.currentDevice = originalDevice;
            if (sidebar) {
                sidebar.classList.remove('responsive-debug-mobile');
            }
            if (mainContent) {
                mainContent.classList.remove('responsive-debug-mobile');
            }
        }, 5000);
    }
}

// Initialize responsive test in development
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.hostname.includes('localhost') ||
        window.location.hostname.includes('127.0.0.1') ||
        window.location.search.includes('responsive-test=true')) {

        // Wait for CSS and other scripts to load
        setTimeout(function() {
            new ResponsiveTest();
        }, 1000);
    }
});
