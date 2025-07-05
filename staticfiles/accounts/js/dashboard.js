// Smart Account Management Dashboard JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all dashboard components
    initializeCharts();
    initializeAnimations();
    initializeInteractivity();
    initializeCounters();
    updateDateTime();
    
    // Update time every minute
    setInterval(updateDateTime, 60000);
});

// Chart Configuration and Initialization
function initializeCharts() {
    
    // Category Spending Pie Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['Food & Dining', 'Transportation', 'Entertainment', 'Shopping', 'Bills & Utilities', 'Healthcare'],
                datasets: [{
                    data: [450, 180, 120, 380, 250, 95],
                    backgroundColor: [
                        '#FF6B6B', // Food - Red
                        '#4ECDC4', // Transportation - Teal
                        '#45B7D1', // Entertainment - Blue
                        '#96CEB4', // Shopping - Green
                        '#FECA57', // Bills - Yellow
                        '#FF9FF3'  // Healthcare - Pink
                    ],
                    borderWidth: 0,
                    cutout: '60%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true,
                            font: {
                                family: 'Inter',
                                size: 12,
                                weight: '500'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#667eea',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: $${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    // Income vs Expenses Line Chart
    const trendCtx = document.getElementById('trendChart');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Income',
                    data: [8500, 8750, 9200, 8900, 9100, 8750, 9300, 9500, 9200, 8800, 9000, 8750],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#667eea',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }, {
                    label: 'Expenses',
                    data: [3200, 3400, 3100, 3500, 3300, 3240, 3600, 3450, 3380, 3290, 3150, 3240],
                    borderColor: '#FF6B6B',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#FF6B6B',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                family: 'Inter',
                                size: 12,
                                weight: '500'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#667eea',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: $${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                family: 'Inter',
                                size: 11
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            font: {
                                family: 'Inter',
                                size: 11
                            },
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeOutQuart'
                }
            }
        });
    }
}

// Initialize Animations
function initializeAnimations() {
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Add slide animations to rows
    const rows = document.querySelectorAll('.row');
    rows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.2}s`;
        if (index % 2 === 0) {
            row.classList.add('slide-in-left');
        } else {
            row.classList.add('slide-in-right');
        }
    });

    // Animate progress bars
    setTimeout(() => {
        const progressBars = document.querySelectorAll('.progress-bar');
        progressBars.forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }, 1000);
}

// Initialize Interactive Features
function initializeInteractivity() {
    
    // Quick Action Buttons
    const quickActionButtons = document.querySelectorAll('.btn-lg');
    quickActionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
            
            // Handle button actions
            const buttonText = this.textContent.trim();
            handleQuickAction(buttonText);
        });
    });

    // Summary card hover effects
    const summaryCards = document.querySelectorAll('.summary-card');
    summaryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Table row click effects
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            // Remove active class from all rows
            tableRows.forEach(r => r.classList.remove('table-active'));
            // Add active class to clicked row
            this.classList.add('table-active');
            
            // Show transaction details (placeholder)
            showTransactionDetails(this);
        });
    });

    // Search functionality for transactions
    addSearchFunctionality();
    
    // Auto-refresh data every 5 minutes
    setInterval(refreshDashboardData, 300000);
}

// Handle Quick Actions
function handleQuickAction(action) {
    switch(action) {
        case 'Add Income':
            showAddIncomeModal();
            break;
        case 'Add Expense':
            showAddExpenseModal();
            break;
        case 'Transfer Money':
            showTransferModal();
            break;
        case 'Export Report':
            exportReport();
            break;
        default:
            console.log('Unknown action:', action);
    }
}

// Show modals (placeholders for now)
function showAddIncomeModal() {
    showNotification('Add Income modal would open here', 'info');
}

function showAddExpenseModal() {
    showNotification('Add Expense modal would open here', 'info');
}

function showTransferModal() {
    showNotification('Transfer Money modal would open here', 'info');
}

// Export Report functionality
function exportReport() {
    showNotification('Exporting report...', 'info');
    
    // Simulate export process
    setTimeout(() => {
        const data = gatherReportData();
        downloadCSV(data, 'financial-report.csv');
        showNotification('Report exported successfully!', 'success');
    }, 1500);
}

// Gather report data
function gatherReportData() {
    return [
        ['Date', 'Description', 'Category', 'Amount', 'Type'],
        ['Jan 15, 2025', 'Grocery Shopping', 'Food', '-85.50', 'Expense'],
        ['Jan 14, 2025', 'Salary Deposit', 'Income', '3500.00', 'Income'],
        ['Jan 13, 2025', 'Gas Station', 'Transport', '-45.20', 'Expense'],
        ['Jan 12, 2025', 'Coffee Shop', 'Food', '-12.75', 'Expense'],
        ['Jan 11, 2025', 'Freelance Payment', 'Income', '750.00', 'Income']
    ];
}

// Download CSV file
function downloadCSV(data, filename) {
    const csvContent = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Show transaction details
function showTransactionDetails(row) {
    const cells = row.querySelectorAll('td');
    const transactionData = {
        date: cells[0].textContent,
        description: cells[1].textContent,
        category: cells[2].textContent,
        amount: cells[3].textContent,
        type: cells[4].textContent
    };
    
    showNotification(`Selected: ${transactionData.description} - ${transactionData.amount}`, 'info');
}

// Add search functionality
function addSearchFunctionality() {
    // Create search input if it doesn't exist
    const searchContainer = document.querySelector('.card-header');
    if (searchContainer && !document.getElementById('transactionSearch')) {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.id = 'transactionSearch';
        searchInput.className = 'form-control form-control-sm';
        searchInput.placeholder = 'Search transactions...';
        searchInput.style.width = '200px';
        
        searchInput.addEventListener('input', filterTransactions);
        searchContainer.appendChild(searchInput);
    }
}

// Filter transactions based on search
function filterTransactions(e) {
    const searchTerm = e.target.value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Initialize animated counters
function initializeCounters() {
    const counters = document.querySelectorAll('.summary-card h3');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.textContent.replace(/[$,]/g, ''));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            const isNegative = counter.textContent.includes('-');
            const prefix = isNegative ? '-$' : '$';
            counter.textContent = prefix + current.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }, 16);
    });
}

// Update date and time
function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    
    // Add current time to welcome message if element exists
    const welcomeSection = document.querySelector('.container-fluid .text-muted');
    if (welcomeSection) {
        const baseText = "Here's your financial overview for this month";
        welcomeSection.textContent = `${baseText} • Updated: ${now.toLocaleDateString('en-US', options)}`;
    }
}

// Refresh dashboard data
function refreshDashboardData() {
    showNotification('Refreshing dashboard data...', 'info');
    
    // Simulate data refresh
    setTimeout(() => {
        // Update summary cards with new data (placeholder)
        updateSummaryCards();
        showNotification('Dashboard updated successfully!', 'success');
    }, 1000);
}

// Update summary cards with new data
function updateSummaryCards() {
    // This would typically fetch new data from the server
    // For now, just add a small random variation to demonstrate
    const summaryValues = document.querySelectorAll('.summary-card h3');
    
    summaryValues.forEach(value => {
        const currentValue = parseFloat(value.textContent.replace(/[$,]/g, ''));
        const variation = (Math.random() - 0.5) * 100; // ±$50 variation
        const newValue = Math.max(0, currentValue + variation);
        
        const isNegative = value.textContent.includes('-');
        const prefix = isNegative ? '-$' : '$';
        value.textContent = prefix + newValue.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    });
}

// Show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add ripple effect CSS
const rippleCSS = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        transform: scale(0);
        animation: rippleEffect 0.6s linear;
        background-color: rgba(255, 255, 255, 0.3);
        pointer-events: none;
    }
    
    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .notification {
        animation: slideInRight 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + I for Add Income
    if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
        e.preventDefault();
        showAddIncomeModal();
    }
    
    // Ctrl/Cmd + E for Add Expense
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        showAddExpenseModal();
    }
    
    // Ctrl/Cmd + R for Refresh
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        refreshDashboardData();
    }
});

// Print functionality
function printDashboard() {
    window.print();
}

// Export dashboard as PDF (placeholder)
function exportAsPDF() {
    showNotification('PDF export functionality would be implemented here', 'info');
}

// Console welcome message
console.log('%c🚀 Smart Account Management Dashboard Loaded!', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cKeyboard Shortcuts:', 'color: #333; font-weight: bold;');
console.log('Ctrl/Cmd + I: Add Income');
console.log('Ctrl/Cmd + E: Add Expense');
console.log('Ctrl/Cmd + R: Refresh Dashboard');
