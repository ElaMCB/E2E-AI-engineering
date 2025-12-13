/**
 * Visitor Tracking and Analytics
 * Tracks page views, visitor information, and user interactions
 */

// Google Analytics 4 (GA4) - Replace with your Measurement ID
const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX'; // Replace with your actual GA4 Measurement ID

// Initialize Google Analytics if ID is provided
if (GA_MEASUREMENT_ID && GA_MEASUREMENT_ID !== 'G-XXXXXXXXXX') {
    // Google Analytics 4
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID, {
        'page_path': window.location.pathname,
        'page_title': document.title
    });
    
    // Load GA4 script
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(script);
}

// Simple visitor counter using visitor-badge API
function updateVisitorCounter() {
    // Footer visitor counter - display as text
    const footerCounter = document.getElementById('footer-visitor-counter');
    if (footerCounter) {
        // Try multiple counter services for reliability
        const counterServices = [
            // Service 1: countapi.xyz (primary)
            () => fetch('https://api.countapi.xyz/hit/ElaMCB/E2E-AI-engineering')
                .then(response => response.json())
                .then(data => data && data.value !== undefined ? data.value : null),
            
            // Service 2: visitor-badge API (fallback - we'll extract from image)
            () => {
                return new Promise((resolve) => {
                    const img = new Image();
                    img.crossOrigin = 'anonymous';
                    img.onload = function() {
                        // Try to extract count from image if possible
                        // For now, just use a placeholder
                        resolve(null);
                    };
                    img.onerror = () => resolve(null);
                    img.src = 'https://visitor-badge.laobi.icu/badge?page_id=ElaMCB/E2E-AI-engineering';
                    setTimeout(() => resolve(null), 2000);
                });
            }
        ];
        
        // Try services in order
        let serviceIndex = 0;
        const tryNextService = () => {
            if (serviceIndex >= counterServices.length) {
                // All services failed, show badge image as last resort
                const img = document.createElement('img');
                img.src = 'https://visitor-badge.laobi.icu/badge?page_id=ElaMCB/E2E-AI-engineering';
                img.alt = 'Visitor count';
                img.style.border = 'none';
                img.style.verticalAlign = 'middle';
                img.style.marginLeft = '5px';
                img.style.height = '18px';
                footerCounter.innerHTML = '';
                footerCounter.appendChild(img);
                return;
            }
            
            counterServices[serviceIndex]()
                .then(count => {
                    if (count !== null) {
                        footerCounter.textContent = count.toLocaleString();
                    } else {
                        serviceIndex++;
                        tryNextService();
                    }
                })
                .catch(() => {
                    serviceIndex++;
                    tryNextService();
                });
        };
        
        tryNextService();
    }
}


// Track page views
function trackPageView() {
    const pageInfo = {
        path: window.location.pathname,
        title: document.title,
        referrer: document.referrer,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        language: navigator.language,
        screenWidth: window.screen.width,
        screenHeight: window.screen.height
    };
    
    // Log to console (for debugging)
    console.log('Page view tracked:', pageInfo);
    
    // Send to analytics if GA4 is configured
    if (typeof gtag !== 'undefined') {
        gtag('event', 'page_view', {
            page_path: pageInfo.path,
            page_title: pageInfo.title
        });
    }
    
    // Store in localStorage for local tracking
    try {
        const views = JSON.parse(localStorage.getItem('pageViews') || '[]');
        views.push(pageInfo);
        // Keep only last 100 views
        if (views.length > 100) {
            views.shift();
        }
        localStorage.setItem('pageViews', JSON.stringify(views));
    } catch (e) {
        console.error('Error storing page view:', e);
    }
}

// Track clicks on external links
function trackExternalLinks() {
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href && !link.href.startsWith(window.location.origin)) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'click', {
                    event_category: 'outbound',
                    event_label: link.href,
                    transport_type: 'beacon'
                });
            }
        }
    });
}

// Track time on page
let startTime = Date.now();
window.addEventListener('beforeunload', function() {
    const timeOnPage = Math.round((Date.now() - startTime) / 1000);
    if (typeof gtag !== 'undefined') {
        gtag('event', 'timing_complete', {
            name: 'time_on_page',
            value: timeOnPage
        });
    }
});

// Initialize tracking when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        trackPageView();
        updateVisitorCounter();
        trackExternalLinks();
    });
} else {
    trackPageView();
    updateVisitorCounter();
    trackExternalLinks();
}

