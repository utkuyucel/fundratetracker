// Dashboard JavaScript functionality

class FedRateDashboard {
    constructor() {
        this.currentPeriod = '1year';
        this.initEventListeners();
        this.loadChart();
    }

    initEventListeners() {
        // Period selection buttons
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectPeriod(e.target.dataset.period);
            });
        });
        
        // Moving average toggles
        const toggle30MA = document.getElementById('toggle30MA');
        const toggle90MA = document.getElementById('toggle90MA');
        const toggle365MA = document.getElementById('toggle365MA');
        
        if (toggle30MA) {
            toggle30MA.addEventListener('change', () => {
                this.toggleMovingAverage('30-Day Moving Average', toggle30MA.checked);
            });
        }
        
        if (toggle90MA) {
            toggle90MA.addEventListener('change', () => {
                this.toggleMovingAverage('90-Day Moving Average', toggle90MA.checked);
            });
        }
        
        if (toggle365MA) {
            toggle365MA.addEventListener('change', () => {
                this.toggleMovingAverage('365-Day Moving Average', toggle365MA.checked);
            });
        }
    }
    
    toggleMovingAverage(traceName, visible) {
        const chartDiv = document.getElementById('timeSeriesChart');
        if (!chartDiv || !chartDiv.data) return;
        
        // Find the trace index
        const traceIndex = chartDiv.data.findIndex(trace => trace.name === traceName);
        if (traceIndex === -1) return;
        
        // Update visibility
        Plotly.restyle(chartDiv, {
            visible: visible ? true : 'legendonly'
        }, [traceIndex]);
    }

    selectPeriod(period) {
        // Update button states
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-primary');
        });
        
        const selectedBtn = document.querySelector(`[data-period="${period}"]`);
        if (selectedBtn) {
            selectedBtn.classList.remove('btn-outline-primary');
            selectedBtn.classList.add('btn-primary');
        }

        this.currentPeriod = period;
        this.loadChart();
    }

    async loadChart() {
        try {
            // Show loading state
            const chartDiv = document.getElementById('timeSeriesChart');
            chartDiv.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading"></div></div>';

            // Fetch data
            const response = await fetch(`/api/chart-data?period=${this.currentPeriod}`);
            const data = await response.json();

            if (!data.dates || data.dates.length === 0) {
                chartDiv.innerHTML = '<div class="alert alert-warning">No data available for the selected period.</div>';
                return;
            }

            // Prepare main data trace
            const mainTrace = {
                x: data.dates,
                y: data.rates,
                type: 'scatter',
                mode: 'lines+markers',
                name: 'Federal Funds Rate',
                line: {
                    color: '#0d6efd',
                    width: 2
                },
                marker: {
                    size: 4,
                    color: '#0d6efd'
                },
                hovertemplate: '<b>%{x}</b><br>' +
                              'Rate: %{y:.2f}%<br>' +
                              '<extra></extra>'
            };

            // Create moving average traces
            const traces = [mainTrace];
            
            // Only add moving averages if they exist in the data
            if (data.moving_averages) {
                // 30-day moving average
                if (data.moving_averages.ma_30.some(val => val !== null)) {
                    traces.push({
                        x: data.dates,
                        y: data.moving_averages.ma_30,
                        type: 'scatter',
                        mode: 'lines',
                        name: '30-Day Moving Average',
                        line: {
                            color: '#198754', // Bootstrap success color
                            width: 2,
                            dash: 'solid'
                        },
                        hovertemplate: '<b>%{x}</b><br>' +
                                      '30-Day Avg: %{y:.2f}%<br>' +
                                      '<extra></extra>'
                    });
                }
                
                // 90-day moving average
                if (data.moving_averages.ma_90.some(val => val !== null)) {
                    traces.push({
                        x: data.dates,
                        y: data.moving_averages.ma_90,
                        type: 'scatter',
                        mode: 'lines',
                        name: '90-Day Moving Average',
                        line: {
                            color: '#dc3545', // Bootstrap danger color
                            width: 2,
                            dash: 'dot'
                        },
                        hovertemplate: '<b>%{x}</b><br>' +
                                      '90-Day Avg: %{y:.2f}%<br>' +
                                      '<extra></extra>'
                    });
                }
                
                // 365-day moving average
                if (data.moving_averages.ma_365.some(val => val !== null)) {
                    traces.push({
                        x: data.dates,
                        y: data.moving_averages.ma_365,
                        type: 'scatter',
                        mode: 'lines',
                        name: '365-Day Moving Average',
                        line: {
                            color: '#ffc107', // Bootstrap warning color
                            width: 2,
                            dash: 'dashdot'
                        },
                        hovertemplate: '<b>%{x}</b><br>' +
                                      '365-Day Avg: %{y:.2f}%<br>' +
                                      '<extra></extra>'
                    });
                }
            }

            const layout = {
                title: {
                    text: 'Federal Funds Rate Over Time',
                    font: { size: 16, color: '#333' }
                },
                xaxis: {
                    title: 'Date',
                    gridcolor: '#e9ecef',
                    showgrid: true
                },
                yaxis: {
                    title: 'Rate (%)',
                    gridcolor: '#e9ecef',
                    showgrid: true
                },
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                margin: { t: 50, r: 20, b: 50, l: 60 },
                hovermode: 'closest',
                showlegend: true,
                legend: {
                    orientation: 'h',
                    x: 0.5,
                    xanchor: 'center',
                    y: 1.1
                }
            };

            const config = {
                responsive: true,
                displayModeBar: false
            };

            // Create the plot with all traces
            Plotly.newPlot('timeSeriesChart', traces, layout, config);

        } catch (error) {
            console.error('Error loading chart:', error);
            document.getElementById('timeSeriesChart').innerHTML = 
                '<div class="alert alert-danger">Error loading chart data. Please try again.</div>';
        }
    }

    // Utility function to format numbers
    formatNumber(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    }

    // Refresh data function
    async refreshData() {
        try {
            // Could trigger ETL pipeline refresh here
            const response = await fetch('/api/pipeline/trigger', { method: 'POST' });
            if (response.ok) {
                // Reload the page after successful refresh
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
                
                // Show success message
                this.showAlert('Data refresh initiated. Page will reload shortly.', 'success');
            } else {
                this.showAlert('Failed to refresh data. Please try again.', 'danger');
            }
        } catch (error) {
            console.error('Error refreshing data:', error);
            this.showAlert('Error refreshing data. Please check your connection.', 'danger');
        }
    }

    // Show alert messages
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container-fluid');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new FedRateDashboard();
});

// Add refresh button functionality if it exists
document.addEventListener('DOMContentLoaded', () => {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            window.dashboard.refreshData();
        });
    }
});
