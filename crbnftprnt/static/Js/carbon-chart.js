document.addEventListener('DOMContentLoaded', function() {
    
    const loadChart = async () => {
        
        if (typeof Chart === 'undefined') {
           
            await new Promise((resolve) => {
                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js';
                script.onload = resolve;
                document.head.appendChild(script);
            });
        }

        
        const canvas = document.getElementById('carbonChart');
        if (!canvas) {
            console.error('Carbon chart canvas not found');
            return;
        }

        const ctx = canvas.getContext('2d');

       
        try {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Transport', 'Energy', 'Food', 'Shopping', 'Home'],
                    datasets: [{
                        label: 'Global Average',
                        data: [8.2, 6.3, 4.7, 3.8, 2.9],
                        backgroundColor: 'rgba(239, 68, 68, 0.8)',
                        borderWidth: 0,
                        borderRadius: 4,
                        barThickness: 30
                    }, {
                        label: 'Your Footprint',
                        data: [6.5, 4.8, 3.9, 2.6, 2.1],
                        backgroundColor: 'rgba(34, 197, 94, 0.8)',
                        borderWidth: 0,
                        borderRadius: 4,
                        barThickness: 30
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 2000
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                            labels: {
                                padding: 20,
                                font: {
                                    size: 14
                                }
                            }
                        },
                        title: {
                            display: true,
                            text: 'Carbon Footprint Comparison',
                            padding: 20,
                            font: {
                                size: 18,
                                weight: 'bold'
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Tonnes CO2/year',
                                font: {
                                    size: 14,
                                    weight: 'bold'
                                }
                            },
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
        } catch (error) {
            console.error('Error creating chart:', error);
        }
    };

    loadChart();
});