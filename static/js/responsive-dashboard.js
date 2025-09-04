/**
 * Responsive Dashboard Detection System
 * Ethiopian Hospital ERP
 * 
 * Automatically switches between desktop and mobile dashboard versions
 * based on viewport size with support for manual overrides.
 */

class ResponsiveDashboard {
    constructor() {
        this.config = {
            mobileBreakpoint: 768,
            redirectCooldown: 2000, // 2 seconds
            debounceDelay: 250,
            orientationChangeDelay: 500,
            devToolsCheckInterval: 500 // Check for dev tools changes every 500ms
        };

        this.state = {
            initialWidth: window.innerWidth,
            lastRedirectTime: 0,
            isDesktopDashboard: this.isDesktopDashboard(),
            isMobileDashboard: this.isMobileDashboard(),
            resizeTimer: null,
            orientationTimer: null,
            devToolsTimer: null,
            lastOuterWidth: window.outerWidth,
            lastOuterHeight: window.outerHeight,
            lastInnerWidth: window.innerWidth,
            lastInnerHeight: window.innerHeight,
            devToolsWasOpen: this.isDevToolsOpen()
        };

        this.init();
    }

    init() {
        console.log('Initializing Responsive Dashboard Detection...');

        // Bind event listeners
        this.bindEvents();

        // Start developer tools monitoring
        this.startDevToolsMonitoring();

        // Initial check after a short delay to ensure DOM is ready
        setTimeout(() => {
            this.checkResponsiveRedirection(true);
        }, 100);

        console.log('Responsive Dashboard Detection initialized');
    }

    bindEvents() {
        // Window resize with debouncing
        window.addEventListener('resize', () => {
            clearTimeout(this.state.resizeTimer);
            this.state.resizeTimer = setTimeout(() => {
                this.handleResize();
            }, this.config.debounceDelay);
        });

        // Orientation change
        window.addEventListener('orientationchange', () => {
            clearTimeout(this.state.orientationTimer);
            this.state.orientationTimer = setTimeout(() => {
                this.handleOrientationChange();
            }, this.config.orientationChangeDelay);
        });

        // Page visibility change (for when user switches tabs)
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                setTimeout(() => {
                    this.checkResponsiveRedirection();
                }, 100);
            }
        });

        // Window focus events (can indicate dev tools closure)
        window.addEventListener('focus', () => {
            setTimeout(() => {
                this.checkDevToolsState();
            }, 100);
        });
    }

    handleResize() {
        console.log('Viewport resized to:', window.innerWidth + 'x' + window.innerHeight);
        this.checkResponsiveRedirection();
    }

    handleOrientationChange() {
        console.log('Orientation changed, new viewport:', window.innerWidth + 'x' + window.innerHeight);
        this.checkResponsiveRedirection();
    }

    isDesktopDashboard() {
        const path = window.location.pathname;
        return path === '/dashboard/' || path === '/dashboard';
    }

    isMobileDashboard() {
        return window.location.pathname.includes('/mobile/');
    }

    isMobileViewport() {
        return window.innerWidth <= this.config.mobileBreakpoint;
    }

    hasManualOverride() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('desktop') === '1' || urlParams.get('mobile') === '1';
    }

    isInCooldown() {
        const now = Date.now();
        return (now - this.state.lastRedirectTime) < this.config.redirectCooldown;
    }

    isDevToolsOpen() {
        // Multiple methods to detect if developer tools are open
        const threshold = 160; // Threshold for detecting dev tools

        // Method 1: Check if outer dimensions are significantly larger than inner
        const widthDiff = window.outerWidth - window.innerWidth;
        const heightDiff = window.outerHeight - window.innerHeight;

        // Method 2: Check for common dev tools indicators
        const hasDevTools = widthDiff > threshold || heightDiff > threshold;

        // Method 3: Check for specific dev tools properties (Chrome/Firefox)
        const chromeDevTools = window.outerHeight - window.innerHeight > 200;
        const firefoxDevTools = window.Firebug && window.Firebug.chrome && window.Firebug.chrome.isInitialized;

        return hasDevTools || chromeDevTools || firefoxDevTools;
    }

    startDevToolsMonitoring() {
        // Start periodic monitoring of developer tools state
        this.state.devToolsTimer = setInterval(() => {
            this.checkDevToolsState();
        }, this.config.devToolsCheckInterval);

        console.log('Developer tools monitoring started');
    }

    stopDevToolsMonitoring() {
        if (this.state.devToolsTimer) {
            clearInterval(this.state.devToolsTimer);
            this.state.devToolsTimer = null;
            console.log('Developer tools monitoring stopped');
        }
    }

    checkDevToolsState() {
        const currentOuterWidth = window.outerWidth;
        const currentOuterHeight = window.outerHeight;
        const currentInnerWidth = window.innerWidth;
        const currentInnerHeight = window.innerHeight;
        const currentDevToolsOpen = this.isDevToolsOpen();

        // Check if outer dimensions changed (indicates dev tools open/close)
        const outerDimensionsChanged =
            currentOuterWidth !== this.state.lastOuterWidth ||
            currentOuterHeight !== this.state.lastOuterHeight;

        // Check if inner dimensions changed significantly
        const innerDimensionsChanged =
            Math.abs(currentInnerWidth - this.state.lastInnerWidth) > 50 ||
            Math.abs(currentInnerHeight - this.state.lastInnerHeight) > 50;

        // Detect developer tools closure
        const devToolsClosed = this.state.devToolsWasOpen && !currentDevToolsOpen;

        // Detect significant viewport change that might indicate dev tools closure
        const significantViewportChange = outerDimensionsChanged || innerDimensionsChanged;

        if (devToolsClosed || significantViewportChange) {
            console.log('Developer tools state change detected:', {
                devToolsClosed,
                significantViewportChange,
                outerDimensionsChanged,
                innerDimensionsChanged,
                previousViewport: `${this.state.lastInnerWidth}x${this.state.lastInnerHeight}`,
                currentViewport: `${currentInnerWidth}x${currentInnerHeight}`,
                previousOuter: `${this.state.lastOuterWidth}x${this.state.lastOuterHeight}`,
                currentOuter: `${currentOuterWidth}x${currentOuterHeight}`
            });

            // Update stored dimensions
            this.updateStoredDimensions();

            // Trigger immediate responsive check with special flag
            setTimeout(() => {
                this.checkResponsiveRedirection(false, true);
            }, 100);
        } else {
            // Update stored dimensions for next comparison
            this.updateStoredDimensions();
        }
    }

    updateStoredDimensions() {
        this.state.lastOuterWidth = window.outerWidth;
        this.state.lastOuterHeight = window.outerHeight;
        this.state.lastInnerWidth = window.innerWidth;
        this.state.lastInnerHeight = window.innerHeight;
        this.state.devToolsWasOpen = this.isDevToolsOpen();
    }

    checkResponsiveRedirection(isInitialCheck = false, isDevToolsTriggered = false) {
        // For dev tools triggered checks, we use a shorter cooldown or bypass it entirely
        const effectiveCooldown = isDevToolsTriggered ? 500 : this.config.redirectCooldown;

        // Skip if we're in cooldown period (prevents rapid redirects)
        if (!isInitialCheck && !isDevToolsTriggered && this.isInCooldown()) {
            console.log('Responsive redirect skipped: in cooldown period');
            return;
        }

        // For dev tools triggered checks, use shorter cooldown
        if (isDevToolsTriggered) {
            const now = Date.now();
            if ((now - this.state.lastRedirectTime) < effectiveCooldown) {
                console.log('Dev tools triggered redirect skipped: in short cooldown period');
                return;
            }
        }

        // Skip if user has manually overridden the dashboard type
        if (this.hasManualOverride()) {
            console.log('Responsive redirect skipped: manual override detected');
            return;
        }

        // Skip if this was an auto redirect to prevent loops (but allow dev tools triggered checks)
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('auto_redirect') === '1' && !isInitialCheck && !isDevToolsTriggered) {
            console.log('Responsive redirect skipped: auto redirect flag detected');
            return;
        }

        const isMobile = this.isMobileViewport();
        let shouldRedirect = false;
        let targetUrl = '';

        // Determine if we need to redirect
        if (isMobile && this.state.isDesktopDashboard) {
            // Redirect from desktop to mobile
            shouldRedirect = true;
            targetUrl = '/dashboard/mobile/';
            console.log(`Should redirect to mobile dashboard (triggered by: ${isDevToolsTriggered ? 'dev tools' : 'viewport change'})`);
        } else if (!isMobile && this.state.isMobileDashboard) {
            // Redirect from mobile to desktop
            shouldRedirect = true;
            targetUrl = '/dashboard/';
            console.log(`Should redirect to desktop dashboard (triggered by: ${isDevToolsTriggered ? 'dev tools' : 'viewport change'})`);
        }

        if (shouldRedirect) {
            this.performRedirect(targetUrl, isDevToolsTriggered);
        }
    }

    performRedirect(targetUrl, isDevToolsTriggered = false) {
        // Update last redirect time
        this.state.lastRedirectTime = Date.now();

        // Preserve existing query parameters (except mobile/desktop overrides)
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.delete('mobile');
        urlParams.delete('desktop');
        urlParams.delete('auto_redirect'); // Remove any existing auto_redirect flag

        // Build the new URL with preserved parameters
        let newUrl = targetUrl;
        if (urlParams.toString()) {
            newUrl += '?' + urlParams.toString();
        }

        // Add auto_redirect flag to prevent redirect loops
        const separator = newUrl.includes('?') ? '&' : '?';
        newUrl += separator + 'auto_redirect=1';

        // Add dev tools flag if this was triggered by dev tools closure
        if (isDevToolsTriggered) {
            newUrl += '&devtools_redirect=1';
        }

        // Log the redirect
        console.log('Responsive redirect:', {
            from: window.location.pathname,
            to: newUrl,
            viewport: window.innerWidth + 'x' + window.innerHeight,
            outerDimensions: window.outerWidth + 'x' + window.outerHeight,
            trigger: isDevToolsTriggered ? 'dev_tools_closure' : 'viewport_change',
            devToolsOpen: this.isDevToolsOpen()
        });

        // Perform the redirect
        window.location.href = newUrl;
    }

    // Public method to manually trigger a check
    triggerCheck() {
        this.checkResponsiveRedirection();
    }

    // Public method to get current state
    getState() {
        return {
            ...this.state,
            isMobileViewport: this.isMobileViewport(),
            hasManualOverride: this.hasManualOverride(),
            isDevToolsOpen: this.isDevToolsOpen(),
            currentViewport: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            currentOuterDimensions: {
                width: window.outerWidth,
                height: window.outerHeight
            },
            config: this.config,
            urlParams: Object.fromEntries(new URLSearchParams(window.location.search))
        };
    }

    // Public method to disable/enable responsive detection
    setEnabled(enabled) {
        this.enabled = enabled;
        console.log('Responsive detection', enabled ? 'enabled' : 'disabled');
    }

    // Public method to update configuration
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
        console.log('Responsive detection config updated:', this.config);
    }

    // Public method to force a specific dashboard type
    forceDashboardType(type) {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.delete('mobile');
        currentUrl.searchParams.delete('desktop');
        currentUrl.searchParams.delete('auto_redirect');
        currentUrl.searchParams.delete('devtools_redirect');

        if (type === 'mobile') {
            currentUrl.searchParams.set('mobile', '1');
        } else if (type === 'desktop') {
            currentUrl.searchParams.set('desktop', '1');
        }

        window.location.href = currentUrl.toString();
    }

    // Public method to manually trigger dev tools check
    triggerDevToolsCheck() {
        console.log('Manual dev tools check triggered');
        this.checkDevToolsState();
    }

    // Public method to get dev tools status
    getDevToolsStatus() {
        return {
            isOpen: this.isDevToolsOpen(),
            outerDimensions: {
                width: window.outerWidth,
                height: window.outerHeight
            },
            innerDimensions: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            dimensionDifference: {
                width: window.outerWidth - window.innerWidth,
                height: window.outerHeight - window.innerHeight
            }
        };
    }

    // Cleanup method
    destroy() {
        // Clear all timers
        if (this.state.resizeTimer) {
            clearTimeout(this.state.resizeTimer);
        }
        if (this.state.orientationTimer) {
            clearTimeout(this.state.orientationTimer);
        }
        this.stopDevToolsMonitoring();

        console.log('Responsive Dashboard Detection destroyed');
    }
}

// Initialize responsive dashboard detection when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if we're on a dashboard page
    const path = window.location.pathname;
    if (path.includes('/dashboard')) {
        window.responsiveDashboard = new ResponsiveDashboard();

        // Cleanup on page unload
        window.addEventListener('beforeunload', function() {
            if (window.responsiveDashboard) {
                window.responsiveDashboard.destroy();
            }
        });
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponsiveDashboard;
}
