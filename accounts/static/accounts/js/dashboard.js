// Custom Dashboard JavaScript for Smart Account Management System
// Original implementation - no external dependencies

document.addEventListener('DOMContentLoaded', function() {
    setupDashboard();
});

function setupDashboard() {
    initializeFinancialCharts();
    setupUserInteractions();
    startRealTimeUpdates();
    displayWelcomeMessage();
}

function initializeFinancialCharts() {
    createSpendingChart();
    createIncomeExpenseChart();
}

function createSpendingChart() {
    const chartElement = document.getElementById('categoryChart');
    if (!chartElement) return;
    
    const chartData = extractCategoryData();
    
    new Chart(chartElement, {
        type: 'doughnut',
        data: {
            labels: chartData.categories,
            datasets: [{
                data: chartData.amounts,
                backgroundColor: generateChartColors(chartData.categories.length)
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: £${context.parsed}`;
                        }
                    }
                }
            }
        }
    });
}

function createIncomeExpenseChart() {
    const chartElement = document.getElementById('monthlyChart');
    if (!chartElement) return;
    
    const chartData = extractMonthlyData();
    
    new Chart(chartElement, {
        type: 'line',
        data: {
            labels: chartData.months,
            datasets: [{
                label: 'Income',
                data: chartData.income,
                borderColor: '#22c55e',
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                fill: true
            }, {
                label: 'Expenses',
                data: chartData.expenses,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '£' + value;
                        }
                    }
                }
            }
        }
    });
}

function extractCategoryData() {
    const dataElement = document.getElementById('category-data');
    if (dataElement) {
        return JSON.parse(dataElement.textContent);
    }
    return {
        categories: ['Food', 'Transport', 'Entertainment', 'Bills'],
        amounts: [300, 150, 100, 200]
    };
}

function extractMonthlyData() {
    const dataElement = document.getElementById('monthly-data');
    if (dataElement) {
        return JSON.parse(dataElement.textContent);
    }
    return {
        months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        income: [2500, 2600, 2450, 2700, 2550, 2650],
        expenses: [1800, 1900, 1750, 2000, 1850, 1920]
    };
}

function generateChartColors(count) {
    const baseColors = ['#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6', '#06b6d4'];
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    return colors;
}

function setupUserInteractions() {
    setupButtonActions();
    setupCardAnimations();
    setupTransactionFilters();
}

function setupButtonActions() {
    const actionButtons = document.querySelectorAll('.btn-lg');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const buttonText = this.textContent.trim();
            handleButtonClick(buttonText, event);
        });
    });
}

function handleButtonClick(buttonText, event) {
    switch(buttonText) {
        case 'Add Transaction':
            navigateToPage('/add-transaction/');
            break;
        case 'Add Account':
            navigateToPage('/add-account/');
            break;
        case 'Add Budget':
            navigateToPage('/add-budget/');
            break;
        case 'View Reports':
            navigateToPage('/transactions/');
            break;
        default:
            showUserMessage('Feature coming soon!', 'info');
    }
}

function navigateToPage(url) {
    window.location.href = url;
}

function setupCardAnimations() {
    const cards = document.querySelectorAll('.summary-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
}

function setupTransactionFilters() {
    const searchInput = createSearchInput();
    if (searchInput) {
        searchInput.addEventListener('input', filterTransactionTable);
    }
}

function createSearchInput() {
    const tableHeader = document.querySelector('.card-header');
    if (!tableHeader || document.getElementById('transaction-search')) return null;
    
    const searchContainer = document.createElement('div');
    searchContainer.className = 'd-flex align-items-center';
    
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.id = 'transaction-search';
    searchInput.className = 'form-control form-control-sm';
    searchInput.placeholder = 'Search transactions...';
    searchInput.style.width = '200px';
    
    searchContainer.appendChild(searchInput);
    tableHeader.appendChild(searchContainer);
    
    return searchInput;
}

function filterTransactionTable(event) {
    const searchTerm = event.target.value.toLowerCase();
    const tableRows = document.querySelectorAll('tbody tr');
    
    tableRows.forEach(row => {
        const rowText = row.textContent.toLowerCase();
        row.style.display = rowText.includes(searchTerm) ? '' : 'none';
    });
}

function startRealTimeUpdates() {
    updateCurrentTime();
    setInterval(updateCurrentTime, 60000);
    
    // Auto-refresh dashboard every 5 minutes
    setInterval(refreshDashboardData, 300000);
}

function updateCurrentTime() {
    const timeElement = document.querySelector('.text-muted');
    if (timeElement) {
        const now = new Date();
        const timeString = now.toLocaleDateString('en-GB', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        timeElement.textContent = `Here's your financial overview • ${timeString}`;
    }
}

function refreshDashboardData() {
    showUserMessage('Dashboard refreshed!', 'success');
    animateValueCounters();
}

function animateValueCounters() {
    const valueElements = document.querySelectorAll('.summary-card h3');
    valueElements.forEach(element => {
        const finalValue = parseFloat(element.textContent.replace(/[£,]/g, ''));
        if (isNaN(finalValue)) return;
        
        animateNumber(element, 0, finalValue, 1500);
    });
}

function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    const isNegative = element.textContent.includes('-');
    
    function updateValue(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const currentValue = start + (end - start) * progress;
        
        const prefix = isNegative ? '-£' : '£';
        element.textContent = prefix + currentValue.toLocaleString('en-GB', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }
    
    requestAnimationFrame(updateValue);
}

function displayWelcomeMessage() {
    console.log('Smart Account Management Dashboard Ready');
    
    // Show brief loading state
    const loadingElements = document.querySelectorAll('.card');
    loadingElements.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function exportFinancialData() {
    const reportData = collectReportData();
    const csvContent = convertToCSV(reportData);
    downloadFile(csvContent, 'financial_report.csv');
    showUserMessage('Report exported successfully!', 'success');
}

function collectReportData() {
    const transactions = [];
    const tableRows = document.querySelectorAll('tbody tr');
    
    tableRows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 4) {
            transactions.push({
                date: cells[0].textContent.trim(),
                description: cells[1].textContent.trim(),
                category: cells[2].textContent.trim(),
                amount: cells[3].textContent.trim()
            });
        }
    });
    
    return transactions;
}

function convertToCSV(data) {
    const headers = ['Date', 'Description', 'Category', 'Amount'];
    const rows = [headers.join(',')];
    
    data.forEach(item => {
        const row = [
            `"${item.date}"`,
            `"${item.description}"`,
            `"${item.category}"`,
            `"${item.amount}"`
        ];
        rows.push(row.join(','));
    });
    
    return rows.join('\n');
}

function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

function showUserMessage(message, type) {
    const messageElement = document.createElement('div');
    messageElement.className = `alert alert-${type}`;
    messageElement.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        min-width: 300px;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
    `;
    messageElement.textContent = message;
    
    document.body.appendChild(messageElement);
    
    setTimeout(() => {
        messageElement.style.opacity = '1';
        messageElement.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 300);
    }, 3000);
}

// Keyboard shortcuts for power users
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey || event.metaKey) {
        switch(event.key) {
            case 'n':
                event.preventDefault();
                navigateToPage('/add-transaction/');
                break;
            case 'e':
                event.preventDefault();
                exportFinancialData();
                break;
            case 'r':
                event.preventDefault();
                refreshDashboardData();
                break;
        }
    }
});

// Add custom styles for animations
const customStyles = `
    .summary-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .alert {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .card {
        transition: all 0.5s ease;
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = customStyles;
document.head.appendChild(styleSheet);