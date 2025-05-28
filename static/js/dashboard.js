// Dashboard JavaScript

let statusChart = null;
let priorityChart = null;

function initializeDashboard() {
    console.log('Initializing dashboard...');
    
    // Initialize charts
    initializeStatusChart();
    initializePriorityChart();
    
    // Initialize animations
    animateMetrics();
    
    // Initialize refresh functionality
    initializeRefresh();
    
    // Initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function initializeStatusChart() {
    const canvas = document.getElementById('statusChart');
    if (!canvas || !window.dashboardData) return;
    
    const ctx = canvas.getContext('2d');
    const data = window.dashboardData.statusData;
    
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['To Do', 'In Progress', 'Completed'],
            datasets: [{
                data: [data.todo, data.inProgress, data.completed],
                backgroundColor: [
                    '#6c757d', // Gray for todo
                    '#ffc107', // Warning for in progress
                    '#36B37E'  // Success for completed
                ],
                borderWidth: 0,
                hoverBorderWidth: 3,
                hoverBorderColor: '#ffffff'
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
                            family: 'Inter, sans-serif',
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#36B37E',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((context.parsed / total) * 100).toFixed(1) : 0;
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 1000
            },
            cutout: '60%'
        }
    });
}

function initializePriorityChart() {
    const canvas = document.getElementById('priorityChart');
    if (!canvas || !window.dashboardData) return;
    
    const ctx = canvas.getContext('2d');
    const data = window.dashboardData.priorityData;
    
    priorityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Low', 'Medium', 'High', 'Urgent'],
            datasets: [{
                label: 'Tasks',
                data: [data.low, data.medium, data.high, data.urgent],
                backgroundColor: [
                    '#0052CC', // Primary blue for low
                    '#36B37E', // Success green for medium
                    '#FF8B00', // Warning orange for high
                    '#FF5630'  // Urgent red for urgent
                ],
                borderRadius: 4,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    borderColor: '#36B37E',
                    borderWidth: 1,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            family: 'Inter, sans-serif'
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
}

function animateMetrics() {
    const metricValues = document.querySelectorAll('.metric-value');
    
    metricValues.forEach(element => {
        const finalValue = parseInt(element.textContent) || parseFloat(element.textContent) || 0;
        const isPercentage = element.textContent.includes('%');
        let currentValue = 0;
        const increment = finalValue / 30; // Animate over 30 frames
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                currentValue = finalValue;
                clearInterval(timer);
            }
            
            if (isPercentage) {
                element.textContent = currentValue.toFixed(1) + '%';
            } else {
                element.textContent = Math.floor(currentValue);
            }
        }, 50);
    });
}

function initializeRefresh() {
    // Add refresh button functionality
    const refreshBtn = document.getElementById('refreshDashboard');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>Refreshing...';
            
            // Simulate refresh (in a real app, this would fetch new data)
            setTimeout(() => {
                location.reload();
            }, 1000);
        });
    }
    
    // Auto-refresh every 5 minutes
    setInterval(() => {
        console.log('Auto-refreshing dashboard data...');
        // In a real application, you would fetch new data here
        // updateDashboardData();
    }, 5 * 60 * 1000);
}

function updateDashboardData() {
    // This function would fetch new data from the server
    // and update the charts without a full page reload
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            updateCharts(data);
            updateMetrics(data);
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
        });
}

function updateCharts(data) {
    if (statusChart && data.statusData) {
        statusChart.data.datasets[0].data = [
            data.statusData.todo,
            data.statusData.inProgress,
            data.statusData.completed
        ];
        statusChart.update('none'); // No animation for updates
    }
    
    if (priorityChart && data.priorityData) {
        priorityChart.data.datasets[0].data = [
            data.priorityData.low,
            data.priorityData.medium,
            data.priorityData.high,
            data.priorityData.urgent
        ];
        priorityChart.update('none');
    }
}

function updateMetrics(data) {
    // Update metric values
    const elements = {
        totalTasks: document.querySelector('[data-metric="total"]'),
        completedTasks: document.querySelector('[data-metric="completed"]'),
        inProgressTasks: document.querySelector('[data-metric="progress"]'),
        completionRate: document.querySelector('[data-metric="rate"]')
    };
    
    Object.keys(elements).forEach(key => {
        const element = elements[key];
        if (element && data[key] !== undefined) {
            element.textContent = data[key];
        }
    });
}

function exportDashboard() {
    // Export functionality for dashboard data
    const dashboardData = {
        timestamp: new Date().toISOString(),
        metrics: window.dashboardData,
        charts: {
            status: statusChart?.data,
            priority: priorityChart?.data
        }
    };
    
    const dataStr = JSON.stringify(dashboardData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `dashboard-export-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
}

function createProgressRing(percentage, size = 60) {
    const radius = (size - 4) / 2;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (percentage / 100) * circumference;
    
    return `
        <svg class="progress-ring" width="${size}" height="${size}">
            <circle
                class="progress-ring__circle"
                stroke="#e5e7eb"
                stroke-width="3"
                fill="transparent"
                r="${radius}"
                cx="${size / 2}"
                cy="${size / 2}"
            />
            <circle
                class="progress-ring__progress"
                stroke="#36B37E"
                stroke-width="3"
                fill="transparent"
                r="${radius}"
                cx="${size / 2}"
                cy="${size / 2}"
                stroke-dasharray="${circumference} ${circumference}"
                stroke-dashoffset="${offset}"
                transform="rotate(-90 ${size / 2} ${size / 2})"
            />
        </svg>
    `;
}

// Responsive chart handling
function handleResize() {
    if (statusChart) {
        statusChart.resize();
    }
    if (priorityChart) {
        priorityChart.resize();
    }
}

// Initialize resize handling
window.addEventListener('resize', handleResize);

// Clean up charts when page unloads
window.addEventListener('beforeunload', function() {
    if (statusChart) {
        statusChart.destroy();
    }
    if (priorityChart) {
        priorityChart.destroy();
    }
});

// Export functions for global use
window.initializeDashboard = initializeDashboard;
window.exportDashboard = exportDashboard;
window.updateDashboardData = updateDashboardData;
