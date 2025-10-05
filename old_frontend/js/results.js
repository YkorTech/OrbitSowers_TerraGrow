/**
 * TerraGrow Academy - Results Page
 */

let finalChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Results page initialized');

    // Load results
    await loadResults();

    // Setup event listeners
    setupEventListeners();
});

/**
 * Load and display results
 */
async function loadResults() {
    try {
        const scores = await api.harvest();

        // Display scores
        displayScores(scores);

        // Display chart
        displayChart(scores.ndvi_history);

        // Display recommendations
        displayRecommendations(scores.recommendations);

    } catch (error) {
        console.error('Failed to load results:', error);
        alert('Erreur de chargement des résultats');
    }
}

/**
 * Display scores
 */
function displayScores(scores) {
    // Yield
    document.getElementById('yield-value').textContent = scores.yield;
    document.getElementById('regional-avg').textContent = scores.regional_avg;

    const yieldDiff = scores.yield_diff;
    const yieldDiffEl = document.getElementById('yield-diff');
    yieldDiffEl.textContent = `${yieldDiff > 0 ? '+' : ''}${yieldDiff}%`;
    yieldDiffEl.style.color = yieldDiff > 0 ? '#2ECC71' : '#E74C3C';

    // Sustainability
    document.getElementById('sustainability-score').textContent = scores.sustainability_score;
    document.getElementById('water-efficiency').textContent = scores.water_efficiency;
    document.getElementById('nitrogen-efficiency').textContent = scores.nitrogen_efficiency;

    // Stars
    const stars = '⭐'.repeat(scores.stars);
    document.getElementById('stars-display').textContent = stars;

    const starTexts = {
        1: 'Peut mieux faire',
        2: 'Correct',
        3: 'Bien',
        4: 'Très bien',
        5: 'Excellent !'
    };
    document.getElementById('stars-text').textContent = starTexts[scores.stars] || 'Bien';

    // Budget
    document.getElementById('budget-remaining').textContent = scores.budget_remaining;
}

/**
 * Display NDVI chart
 */
function displayChart(ndviHistory) {
    const ctx = document.getElementById('final-ndvi-chart').getContext('2d');

    const weeks = ndviHistory.map((_, i) => `Semaine ${i + 1}`);

    finalChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weeks,
            datasets: [{
                label: 'NDVI',
                data: ndviHistory,
                borderColor: '#2ECC71',
                backgroundColor: 'rgba(46, 204, 113, 0.2)',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#2ECC71'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `NDVI: ${context.parsed.y.toFixed(3)}`;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        healthyLine: {
                            type: 'line',
                            yMin: 0.6,
                            yMax: 0.6,
                            borderColor: '#2ECC71',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Sain (>0.6)',
                                enabled: true,
                                position: 'end'
                            }
                        },
                        stressLine: {
                            type: 'line',
                            yMin: 0.4,
                            yMax: 0.4,
                            borderColor: '#F1C40F',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                content: 'Stress (0.4)',
                                enabled: true,
                                position: 'end'
                            }
                        }
                    }
                }
            }
        }
    });
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const container = document.getElementById('recommendations');

    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p>Aucune recommandation disponible</p>';
        return;
    }

    container.innerHTML = recommendations.map(rec => `
        <div class="recommendation ${rec.type}">
            ${rec.text}
        </div>
    `).join('');
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Replay button
    document.getElementById('replay-btn').addEventListener('click', () => {
        // Clear session and reload location
        api.clearSession();
        window.location.href = 'index.html';
    });

    // Change region button
    document.getElementById('change-region-btn').addEventListener('click', () => {
        // Clear everything
        api.clearSession();
        localStorage.removeItem('terragrow_location');
        window.location.href = 'index.html';
    });
}
