// Mobile CRUD Testing Utilities - Ethiopian Hospital ERP

class MobileCRUDTester {
    constructor() {
        this.testResults = [];
        this.currentModule = null;
        this.testStartTime = null;
        this.isTestingMode = false;
        
        // Test configuration
        this.testConfig = {
            timeout: 10000, // 10 seconds timeout for each test
            retryAttempts: 3,
            delayBetweenTests: 1000, // 1 second delay between tests
            touchTargetMinSize: 44, // Minimum touch target size in pixels
            formValidationTimeout: 5000
        };
        
        // Initialize testing utilities
        this.initTestingUtilities();
    }
    
    initTestingUtilities() {
        console.log('Initializing Mobile CRUD Testing Utilities...');
        
        // Add testing controls to the page if in development mode
        if (this.isDevelopmentMode()) {
            this.addTestingControls();
        }
        
        // Initialize touch target validation
        this.initTouchTargetValidation();
        
        // Initialize form validation testing
        this.initFormValidationTesting();
        
        // Initialize navigation testing
        this.initNavigationTesting();
    }
    
    isDevelopmentMode() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.search.includes('debug=1');
    }
    
    addTestingControls() {
        // Create floating test control panel
        const testPanel = document.createElement('div');
        testPanel.id = 'mobileCRUDTestPanel';
        testPanel.className = 'mobile-crud-test-panel';
        testPanel.innerHTML = `
            <div class="test-panel-header">
                <h6><i class="fas fa-vial"></i> CRUD Tests</h6>
                <button class="btn-close" onclick="this.parentElement.parentElement.style.display='none'"></button>
            </div>
            <div class="test-panel-body">
                <div class="test-module-selector">
                    <select id="testModuleSelect" class="form-select form-select-sm">
                        <option value="">Select Module</option>
                        <option value="patients">Patients</option>
                        <option value="appointments">Appointments</option>
                        <option value="doctors">Doctors</option>
                        <option value="billing">Billing</option>
                        <option value="pharmacy">Pharmacy</option>
                    </select>
                </div>
                <div class="test-actions">
                    <button class="btn btn-primary btn-sm" onclick="mobileCRUDTester.runAllTests()">
                        <i class="fas fa-play"></i> Run All
                    </button>
                    <button class="btn btn-info btn-sm" onclick="mobileCRUDTester.runModuleTests()">
                        <i class="fas fa-cog"></i> Test Module
                    </button>
                    <button class="btn btn-warning btn-sm" onclick="mobileCRUDTester.validateCurrentPage()">
                        <i class="fas fa-check"></i> Validate Page
                    </button>
                </div>
                <div class="test-results" id="testResults">
                    <small class="text-muted">No tests run yet</small>
                </div>
            </div>
        `;
        
        // Add styles
        const testStyles = document.createElement('style');
        testStyles.textContent = `
            .mobile-crud-test-panel {
                position: fixed;
                top: 80px;
                right: 10px;
                width: 280px;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 150, 57, 0.2);
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                z-index: 9999;
                font-size: 0.8rem;
            }
            .test-panel-header {
                display: flex;
                justify-content: between;
                align-items: center;
                padding: 8px 12px;
                background: var(--ethiopia-green);
                color: white;
                border-radius: 8px 8px 0 0;
            }
            .test-panel-header h6 {
                margin: 0;
                font-size: 0.9rem;
                flex: 1;
            }
            .test-panel-body {
                padding: 12px;
            }
            .test-module-selector {
                margin-bottom: 8px;
            }
            .test-actions {
                display: flex;
                gap: 4px;
                margin-bottom: 8px;
            }
            .test-actions .btn {
                flex: 1;
                font-size: 0.7rem;
                padding: 4px 8px;
            }
            .test-results {
                max-height: 200px;
                overflow-y: auto;
                font-size: 0.7rem;
            }
            .test-result-item {
                padding: 4px 8px;
                margin: 2px 0;
                border-radius: 4px;
                border-left: 3px solid;
            }
            .test-result-pass {
                background: rgba(40, 167, 69, 0.1);
                border-left-color: #28a745;
            }
            .test-result-fail {
                background: rgba(220, 53, 69, 0.1);
                border-left-color: #dc3545;
            }
            .test-result-warning {
                background: rgba(255, 193, 7, 0.1);
                border-left-color: #ffc107;
            }
        `;
        
        document.head.appendChild(testStyles);
        document.body.appendChild(testPanel);
        
        // Make panel draggable
        this.makeDraggable(testPanel);
    }
    
    makeDraggable(element) {
        let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        const header = element.querySelector('.test-panel-header');
        
        header.onmousedown = dragMouseDown;
        
        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
        }
        
        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.right = "auto";
            element.style.left = (element.offsetLeft - pos1) + "px";
        }
        
        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
    
    // ===== TOUCH TARGET VALIDATION =====
    initTouchTargetValidation() {
        this.touchTargetValidator = {
            validate: () => this.validateTouchTargets(),
            highlight: (element) => this.highlightTouchTarget(element),
            getMinSize: () => this.testConfig.touchTargetMinSize
        };
    }
    
    validateTouchTargets() {
        const results = [];
        const interactiveElements = document.querySelectorAll(
            'button, a, input[type="button"], input[type="submit"], input[type="reset"], ' +
            '[role="button"], .btn, .mobile-action-btn, .mobile-nav-link'
        );
        
        interactiveElements.forEach((element, index) => {
            const rect = element.getBoundingClientRect();
            const minSize = this.testConfig.touchTargetMinSize;
            
            const result = {
                element: element,
                index: index,
                width: rect.width,
                height: rect.height,
                isValid: rect.width >= minSize && rect.height >= minSize,
                selector: this.getElementSelector(element)
            };
            
            results.push(result);
            
            if (!result.isValid) {
                this.highlightTouchTarget(element, 'invalid');
            }
        });
        
        return results;
    }
    
    highlightTouchTarget(element, type = 'valid') {
        const highlight = document.createElement('div');
        highlight.className = `touch-target-highlight touch-target-${type}`;
        highlight.style.cssText = `
            position: absolute;
            pointer-events: none;
            border: 2px solid ${type === 'valid' ? '#28a745' : '#dc3545'};
            background: ${type === 'valid' ? 'rgba(40, 167, 69, 0.1)' : 'rgba(220, 53, 69, 0.1)'};
            z-index: 10000;
            border-radius: 4px;
        `;
        
        const rect = element.getBoundingClientRect();
        highlight.style.left = (rect.left + window.scrollX) + 'px';
        highlight.style.top = (rect.top + window.scrollY) + 'px';
        highlight.style.width = rect.width + 'px';
        highlight.style.height = rect.height + 'px';
        
        document.body.appendChild(highlight);
        
        // Remove highlight after 3 seconds
        setTimeout(() => {
            if (highlight.parentNode) {
                highlight.parentNode.removeChild(highlight);
            }
        }, 3000);
    }
    
    // ===== FORM VALIDATION TESTING =====
    initFormValidationTesting() {
        this.formValidator = {
            validateAll: () => this.validateAllForms(),
            testRequired: (form) => this.testRequiredFields(form),
            testInputTypes: (form) => this.testInputTypes(form),
            testSubmission: (form) => this.testFormSubmission(form)
        };
    }
    
    validateAllForms() {
        const forms = document.querySelectorAll('form');
        const results = [];
        
        forms.forEach((form, index) => {
            const formResult = {
                form: form,
                index: index,
                selector: this.getElementSelector(form),
                requiredFields: this.testRequiredFields(form),
                inputTypes: this.testInputTypes(form),
                accessibility: this.testFormAccessibility(form)
            };
            
            results.push(formResult);
        });
        
        return results;
    }
    
    testRequiredFields(form) {
        const requiredFields = form.querySelectorAll('[required]');
        const results = [];
        
        requiredFields.forEach(field => {
            const result = {
                field: field,
                name: field.name || field.id,
                type: field.type || field.tagName.toLowerCase(),
                hasLabel: !!form.querySelector(`label[for="${field.id}"]`),
                hasValidation: field.hasAttribute('pattern') || field.hasAttribute('min') || field.hasAttribute('max'),
                selector: this.getElementSelector(field)
            };
            
            results.push(result);
        });
        
        return results;
    }
    
    testInputTypes(form) {
        const inputs = form.querySelectorAll('input');
        const results = [];
        
        inputs.forEach(input => {
            const result = {
                input: input,
                type: input.type,
                isMobileFriendly: this.isMobileFriendlyInput(input),
                hasAutocomplete: input.hasAttribute('autocomplete'),
                fontSize: window.getComputedStyle(input).fontSize,
                preventZoom: parseFloat(window.getComputedStyle(input).fontSize) >= 16
            };
            
            results.push(result);
        });
        
        return results;
    }
    
    isMobileFriendlyInput(input) {
        const mobileFriendlyTypes = ['tel', 'email', 'url', 'number', 'date', 'time', 'datetime-local'];
        return mobileFriendlyTypes.includes(input.type) || input.inputMode;
    }
    
    testFormAccessibility(form) {
        const results = {
            hasFieldsets: form.querySelectorAll('fieldset').length > 0,
            hasLegends: form.querySelectorAll('legend').length > 0,
            labelsCount: form.querySelectorAll('label').length,
            inputsCount: form.querySelectorAll('input, select, textarea').length,
            hasSubmitButton: !!form.querySelector('button[type="submit"], input[type="submit"]')
        };
        
        return results;
    }
    
    // ===== NAVIGATION TESTING =====
    initNavigationTesting() {
        this.navigationTester = {
            testAllLinks: () => this.testAllNavigationLinks(),
            testMobileMenu: () => this.testMobileMenu(),
            testBreadcrumbs: () => this.testBreadcrumbs()
        };
    }
    
    testAllNavigationLinks() {
        const links = document.querySelectorAll('a[href]');
        const results = [];
        
        links.forEach((link, index) => {
            const result = {
                link: link,
                index: index,
                href: link.href,
                text: link.textContent.trim(),
                hasIcon: !!link.querySelector('i, svg'),
                isExternal: link.hostname !== window.location.hostname,
                isMobileOptimized: link.href.includes('mobile=1'),
                selector: this.getElementSelector(link)
            };
            
            results.push(result);
        });
        
        return results;
    }
    
    // ===== UTILITY METHODS =====
    getElementSelector(element) {
        if (element.id) return `#${element.id}`;
        if (element.className) return `.${element.className.split(' ')[0]}`;
        return element.tagName.toLowerCase();
    }
    
    logTestResult(test, status, message, details = null) {
        const result = {
            test: test,
            status: status, // 'pass', 'fail', 'warning'
            message: message,
            details: details,
            timestamp: new Date().toISOString(),
            module: this.currentModule
        };
        
        this.testResults.push(result);
        console.log(`[CRUD Test] ${status.toUpperCase()}: ${test} - ${message}`, details);
        
        // Update UI if test panel exists
        this.updateTestResultsUI(result);
        
        return result;
    }
    
    updateTestResultsUI(result) {
        const resultsContainer = document.getElementById('testResults');
        if (!resultsContainer) return;
        
        const resultElement = document.createElement('div');
        resultElement.className = `test-result-item test-result-${result.status}`;
        resultElement.innerHTML = `
            <div><strong>${result.test}</strong></div>
            <div>${result.message}</div>
            <small class="text-muted">${new Date(result.timestamp).toLocaleTimeString()}</small>
        `;
        
        resultsContainer.appendChild(resultElement);
        resultsContainer.scrollTop = resultsContainer.scrollHeight;
    }
    
    // ===== PUBLIC TEST METHODS =====
    async runAllTests() {
        console.log('Starting comprehensive mobile CRUD tests...');
        this.isTestingMode = true;
        this.testStartTime = Date.now();
        
        try {
            // Test touch targets
            await this.runTouchTargetTests();
            
            // Test forms
            await this.runFormTests();
            
            // Test navigation
            await this.runNavigationTests();
            
            // Test current page specific functionality
            await this.runPageSpecificTests();
            
            this.logTestResult('All Tests', 'pass', 'Comprehensive testing completed successfully');
        } catch (error) {
            this.logTestResult('All Tests', 'fail', `Testing failed: ${error.message}`, error);
        } finally {
            this.isTestingMode = false;
            const duration = Date.now() - this.testStartTime;
            console.log(`Mobile CRUD testing completed in ${duration}ms`);
        }
    }
    
    async runTouchTargetTests() {
        const results = this.validateTouchTargets();
        const invalidTargets = results.filter(r => !r.isValid);
        
        if (invalidTargets.length === 0) {
            this.logTestResult('Touch Targets', 'pass', `All ${results.length} interactive elements meet minimum size requirements`);
        } else {
            this.logTestResult('Touch Targets', 'fail', `${invalidTargets.length} elements below minimum size (${this.testConfig.touchTargetMinSize}px)`, invalidTargets);
        }
    }
    
    async runFormTests() {
        const results = this.validateAllForms();
        
        results.forEach((formResult, index) => {
            const issues = [];
            
            // Check required fields have labels
            const unlabeledRequired = formResult.requiredFields.filter(f => !f.hasLabel);
            if (unlabeledRequired.length > 0) {
                issues.push(`${unlabeledRequired.length} required fields without labels`);
            }
            
            // Check mobile-friendly inputs
            const nonMobileFriendly = formResult.inputTypes.filter(i => !i.isMobileFriendly && !i.preventZoom);
            if (nonMobileFriendly.length > 0) {
                issues.push(`${nonMobileFriendly.length} inputs may cause zoom on mobile`);
            }
            
            if (issues.length === 0) {
                this.logTestResult(`Form ${index + 1}`, 'pass', 'Form validation passed');
            } else {
                this.logTestResult(`Form ${index + 1}`, 'warning', issues.join(', '), formResult);
            }
        });
    }
    
    async runNavigationTests() {
        const results = this.testAllNavigationLinks();
        const mobileOptimized = results.filter(r => r.isMobileOptimized).length;
        const total = results.length;
        
        if (mobileOptimized / total > 0.8) {
            this.logTestResult('Navigation', 'pass', `${mobileOptimized}/${total} links are mobile-optimized`);
        } else {
            this.logTestResult('Navigation', 'warning', `Only ${mobileOptimized}/${total} links are mobile-optimized`);
        }
    }
    
    async runPageSpecificTests() {
        const currentPage = this.detectCurrentPage();
        this.currentModule = currentPage.module;
        
        switch (currentPage.type) {
            case 'list':
                await this.testListPage();
                break;
            case 'detail':
                await this.testDetailPage();
                break;
            case 'add':
            case 'edit':
                await this.testFormPage();
                break;
            case 'delete':
                await this.testDeletePage();
                break;
            default:
                this.logTestResult('Page Detection', 'warning', `Unknown page type: ${currentPage.type}`);
        }
    }
    
    detectCurrentPage() {
        const path = window.location.pathname;
        const search = window.location.search;
        
        // Detect module
        let module = 'unknown';
        if (path.includes('/patients/')) module = 'patients';
        else if (path.includes('/appointments/')) module = 'appointments';
        else if (path.includes('/doctors/')) module = 'doctors';
        else if (path.includes('/billing/')) module = 'billing';
        else if (path.includes('/pharmacy/')) module = 'pharmacy';
        
        // Detect page type
        let type = 'unknown';
        if (path.includes('/add/')) type = 'add';
        else if (path.includes('/edit/')) type = 'edit';
        else if (path.includes('/delete/')) type = 'delete';
        else if (path.match(/\/\d+\/$/)) type = 'detail';
        else if (path.endsWith('/') || search.includes('mobile=1')) type = 'list';
        
        return { module, type, path, search };
    }
    
    async testListPage() {
        // Test search functionality
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search" i]');
        if (searchInput) {
            this.logTestResult('List Page - Search', 'pass', 'Search input found');
        } else {
            this.logTestResult('List Page - Search', 'warning', 'No search input found');
        }
        
        // Test pagination
        const pagination = document.querySelector('.pagination, .mobile-pagination');
        if (pagination) {
            this.logTestResult('List Page - Pagination', 'pass', 'Pagination found');
        }
        
        // Test add button
        const addButton = document.querySelector('a[href*="/add/"], button[onclick*="add"]');
        if (addButton) {
            this.logTestResult('List Page - Add Button', 'pass', 'Add button found');
        } else {
            this.logTestResult('List Page - Add Button', 'fail', 'No add button found');
        }
    }
    
    async testDetailPage() {
        // Test edit button
        const editButton = document.querySelector('a[href*="/edit/"], button[onclick*="edit"]');
        if (editButton) {
            this.logTestResult('Detail Page - Edit Button', 'pass', 'Edit button found');
        }
        
        // Test delete button
        const deleteButton = document.querySelector('a[href*="/delete/"], button[onclick*="delete"]');
        if (deleteButton) {
            this.logTestResult('Detail Page - Delete Button', 'pass', 'Delete button found');
        }
        
        // Test back navigation
        const backButton = document.querySelector('a[href*="list"], .btn[onclick*="back"], .fa-arrow-left');
        if (backButton) {
            this.logTestResult('Detail Page - Back Navigation', 'pass', 'Back navigation found');
        }
    }
    
    async testFormPage() {
        const forms = document.querySelectorAll('form');
        if (forms.length === 0) {
            this.logTestResult('Form Page', 'fail', 'No forms found on form page');
            return;
        }
        
        const form = forms[0];
        
        // Test submit button
        const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitButton) {
            this.logTestResult('Form Page - Submit Button', 'pass', 'Submit button found');
        } else {
            this.logTestResult('Form Page - Submit Button', 'fail', 'No submit button found');
        }
        
        // Test cancel button
        const cancelButton = form.querySelector('a[href*="list"], button[type="button"]');
        if (cancelButton) {
            this.logTestResult('Form Page - Cancel Button', 'pass', 'Cancel button found');
        }
        
        // Test CSRF token
        const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfToken) {
            this.logTestResult('Form Page - CSRF Token', 'pass', 'CSRF token found');
        } else {
            this.logTestResult('Form Page - CSRF Token', 'fail', 'CSRF token missing');
        }
    }
    
    async testDeletePage() {
        // Test confirmation mechanism
        const confirmCheckbox = document.querySelector('input[type="checkbox"][required]');
        const confirmButton = document.querySelector('button[type="submit"]');
        
        if (confirmCheckbox && confirmButton) {
            this.logTestResult('Delete Page - Confirmation', 'pass', 'Confirmation mechanism found');
        } else {
            this.logTestResult('Delete Page - Confirmation', 'warning', 'Weak confirmation mechanism');
        }
        
        // Test cancel option
        const cancelButton = document.querySelector('a[href*="detail"], a[href*="list"]');
        if (cancelButton) {
            this.logTestResult('Delete Page - Cancel Option', 'pass', 'Cancel option found');
        }
    }
    
    async runModuleTests() {
        const moduleSelect = document.getElementById('testModuleSelect');
        const selectedModule = moduleSelect?.value;
        
        if (!selectedModule) {
            alert('Please select a module to test');
            return;
        }
        
        this.currentModule = selectedModule;
        console.log(`Running tests for ${selectedModule} module...`);
        
        // Run module-specific tests
        await this.runPageSpecificTests();
    }
    
    async validateCurrentPage() {
        console.log('Validating current page...');
        
        // Run quick validation
        await this.runTouchTargetTests();
        await this.runFormTests();
        await this.runNavigationTests();
        
        this.logTestResult('Page Validation', 'pass', 'Current page validation completed');
    }
}

// Global instance
window.MobileCRUDTester = MobileCRUDTester;

// Auto-initialize if in development mode
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.search.includes('debug=1')) {
        window.mobileCRUDTester = new MobileCRUDTester();
        console.log('Mobile CRUD Tester initialized in development mode');
    }
});
