# Responsive Dashboard Detection System

## Overview

The Ethiopian Hospital ERP now includes an advanced responsive detection system that automatically switches between desktop and mobile dashboard versions based on viewport size. This system provides a seamless user experience across all devices and screen sizes.

## Features

### ✅ Automatic Detection
- **Viewport Monitoring**: Continuously monitors browser viewport size
- **Real-time Switching**: Automatically redirects between dashboard versions when viewport crosses the 768px breakpoint
- **Device Simulation Support**: Works with browser developer tools device simulation
- **Developer Tools Detection**: Automatically detects when dev tools are closed and triggers immediate viewport check
- **Manual Override**: Supports `?mobile=1` and `?desktop=1` URL parameters to override automatic detection

### ✅ Smart Redirection
- **Cooldown Period**: 2-second cooldown between redirects to prevent rapid switching (500ms for dev tools triggered)
- **Loop Prevention**: Auto-redirect flags prevent infinite redirect loops
- **Parameter Preservation**: Maintains existing query parameters when redirecting
- **Orientation Change Support**: Handles device orientation changes
- **Developer Tools Closure Detection**: Immediate redirect check when dev tools are closed

### ✅ Enhanced User Experience
- **Debounced Resize**: Uses debounced resize events for optimal performance
- **Visibility API**: Checks viewport when user returns to tab
- **Touch Gesture Support**: Maintains touch functionality during transitions
- **Accessibility**: Preserves accessibility features across dashboard versions

## Implementation Details

### JavaScript Components

#### 1. Core Detection Class (`responsive-dashboard.js`)
```javascript
class ResponsiveDashboard {
    constructor() {
        this.config = {
            mobileBreakpoint: 768,
            redirectCooldown: 2000,
            debounceDelay: 250,
            orientationChangeDelay: 500
        };
    }
}
```

#### 2. Event Listeners
- **Window Resize**: Debounced resize detection
- **Orientation Change**: Device rotation handling
- **Page Visibility**: Tab focus/blur detection

#### 3. Detection Logic
```javascript
checkResponsiveRedirection(isInitialCheck = false, isDevToolsTriggered = false) {
    // Cooldown check (shorter for dev tools)
    // Manual override check
    // Auto-redirect loop prevention
    // Viewport size evaluation
    // Redirection execution
}
```

#### 4. Developer Tools Detection
```javascript
isDevToolsOpen() {
    // Multiple detection methods
    // Outer vs inner dimension comparison
    // Browser-specific indicators
    // Threshold-based detection
}

startDevToolsMonitoring() {
    // Periodic monitoring every 500ms
    // Dimension change detection
    // Automatic redirect triggering
}
```

### Server-Side Integration

#### 1. Enhanced Views (`patients/views.py`)
```python
@login_required
def dashboard_view(request):
    # Enhanced mobile detection with responsive support
    is_mobile_request = request.GET.get('mobile') == '1'
    force_desktop = request.GET.get('desktop') == '1'
    auto_redirect = request.GET.get('auto_redirect') == '1'
    
    # Redirect logic with parameter preservation
```

#### 2. URL Parameter Handling
- `?mobile=1`: Force mobile dashboard
- `?desktop=1`: Force desktop dashboard
- `?auto_redirect=1`: Indicates automatic redirect (prevents loops)

### Template Integration

#### 1. Script Inclusion
Both dashboard templates include the responsive detection script:
```html
<!-- Responsive Dashboard Detection -->
<script src="{% static 'js/responsive-dashboard.js' %}"></script>
```

#### 2. Automatic Initialization
The system automatically initializes when DOM is ready on dashboard pages.

## Configuration

### Breakpoints
- **Mobile**: ≤768px viewport width
- **Tablet**: 769px - 1024px viewport width
- **Desktop**: >1024px viewport width

### Timing Settings
- **Resize Debounce**: 250ms
- **Redirect Cooldown**: 2000ms (2 seconds)
- **Orientation Change Delay**: 500ms

### Customization
```javascript
// Update configuration
window.responsiveDashboard.updateConfig({
    mobileBreakpoint: 800,
    redirectCooldown: 3000
});
```

## Usage Examples

### 1. Automatic Detection
```
User visits /dashboard/ on mobile device
→ Automatically redirected to /dashboard/mobile/

User resizes browser window from 1200px to 600px
→ Automatically redirected to mobile dashboard
```

### 2. Manual Override
```
/dashboard/?desktop=1
→ Forces desktop dashboard regardless of viewport size

/dashboard/mobile/?mobile=1
→ Forces mobile dashboard regardless of viewport size
```

### 3. Parameter Preservation
```
/dashboard/?search=patient&status=active
→ Redirects to /dashboard/mobile/?search=patient&status=active&auto_redirect=1
```

## Testing

### Test Page
Access `/dashboard/responsive-test/` for comprehensive testing interface:

- **Real-time State Display**: Shows current viewport, dashboard type, and detection status
- **Manual Controls**: Buttons to trigger manual checks and view internal state
- **Event Logging**: Real-time log of detection events and redirects
- **Direct Navigation**: Links to test different dashboard configurations

### Browser Developer Tools Testing

#### Basic Developer Tools Testing
1. Open dashboard in desktop browser (>768px width)
2. Open developer tools (F12)
3. Enable device simulation
4. Select mobile device (e.g., iPhone)
5. Observe automatic redirect to mobile dashboard
6. **Close developer tools (F12 again)**
7. **Observe immediate automatic redirect back to desktop dashboard**

#### Advanced Developer Tools Testing
1. Start on desktop dashboard
2. Open dev tools and simulate mobile device
3. Navigate around mobile dashboard
4. Add query parameters (e.g., `?search=test&filter=active`)
5. Close developer tools
6. Verify redirect to desktop dashboard with parameters preserved
7. Verify URL shows `?search=test&filter=active&auto_redirect=1&devtools_redirect=1`

#### Edge Case Testing
1. **Rapid Dev Tools Toggle**: Open and close dev tools quickly - should respect cooldown
2. **Manual Override**: Add `?desktop=1`, open dev tools, close dev tools - should stay on desktop
3. **Mixed Scenarios**: Resize window while dev tools are open, then close dev tools

### Manual Window Resizing
1. Open dashboard in desktop browser
2. Manually resize browser window below 768px width
3. Observe automatic redirect to mobile dashboard
4. Resize window above 768px width
5. Observe automatic redirect back to desktop dashboard

## API Reference

### Public Methods

#### `triggerCheck()`
Manually trigger a responsive detection check:
```javascript
window.responsiveDashboard.triggerCheck();
```

#### `getState()`
Get current detection state:
```javascript
const state = window.responsiveDashboard.getState();
console.log(state);
```

#### `setEnabled(enabled)`
Enable/disable responsive detection:
```javascript
window.responsiveDashboard.setEnabled(false); // Disable
window.responsiveDashboard.setEnabled(true);  // Enable
```

#### `forceDashboardType(type)`
Force a specific dashboard type:
```javascript
window.responsiveDashboard.forceDashboardType('mobile');
window.responsiveDashboard.forceDashboardType('desktop');
```

#### `triggerDevToolsCheck()`
Manually trigger a developer tools state check:
```javascript
window.responsiveDashboard.triggerDevToolsCheck();
```

#### `getDevToolsStatus()`
Get current developer tools status:
```javascript
const status = window.responsiveDashboard.getDevToolsStatus();
console.log(status);
// Returns: { isOpen: boolean, outerDimensions: {}, innerDimensions: {}, dimensionDifference: {} }
```

#### `destroy()`
Cleanup all timers and event listeners:
```javascript
window.responsiveDashboard.destroy();
```

### Events

The system logs all detection events to the browser console for debugging:
- Viewport resize events
- Redirect decisions
- Manual override detection
- Cooldown period notifications

## Troubleshooting

### Common Issues

1. **Rapid Redirects**: Cooldown period prevents this (2-second minimum between redirects)
2. **Redirect Loops**: Auto-redirect flags prevent infinite loops
3. **Parameter Loss**: System preserves all query parameters during redirects
4. **Manual Override Ignored**: Check for conflicting URL parameters

### Debug Information
Enable console logging to see detailed detection information:
```javascript
// All detection events are automatically logged to console
// Check browser developer tools console for detailed logs
```

## Browser Compatibility

- **Modern Browsers**: Full support (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- **Legacy Browsers**: Graceful degradation (manual navigation still works)
- **Mobile Browsers**: Full support including touch gestures and orientation changes

## Performance Considerations

- **Debounced Events**: Resize events are debounced to prevent excessive checks
- **Efficient Detection**: Minimal DOM queries and calculations
- **Memory Management**: Event listeners properly cleaned up
- **Network Optimization**: Redirects preserve browser cache and session state
