/**
 * TerraGrow Academy - Game Logic
 */

let gameState = null;
let ndviChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Game initialized');

    // Load game state
    await loadGameState();

    // Setup event listeners
    setupEventListeners();

    // Initialize chart
    initializeChart();
});

/**
 * Load game state from API
 */
async function loadGameState() {
    try {
        console.log('Loading game state...');
        const state = await api.getState();
        console.log('Game state loaded:', state);
        gameState = state;

        updateUI();

    } catch (error) {
        console.error('Failed to load game state:', error);
        alert('Erreur de chargement. Retour à la sélection de région.');
        window.location.href = 'index.html';
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Slider updates
    const irrigationSlider = document.getElementById('irrigation-slider');
    const fertilizerSlider = document.getElementById('fertilizer-slider');

    irrigationSlider.addEventListener('input', updateCosts);
    fertilizerSlider.addEventListener('input', updateCosts);

    // Validate button
    const validateBtn = document.getElementById('validate-btn');
    validateBtn.addEventListener('click', validateWeek);
}

/**
 * Update UI with current game state
 */
function updateUI() {
    if (!gameState) {
        console.error('No game state available');
        return;
    }

    try {
        // Header
        document.getElementById('region-name').textContent = gameState.region?.name || 'Région inconnue';
        document.getElementById('current-week').textContent = gameState.week || 1;
        document.getElementById('budget').textContent = `$${gameState.budget || 0}`;

        // Crop info
        if (gameState.crop) {
            document.getElementById('crop-name').textContent = gameState.crop.name || 'Culture';

            // NDVI
            const ndvi = gameState.crop.ndvi || 0.15;
            document.getElementById('ndvi-value').textContent = ndvi.toFixed(3);
            document.getElementById('ndvi-fill').style.width = `${Math.min((ndvi / 0.85) * 100, 100)}%`;

            // Health status
            const health = gameState.crop.health;
            const healthEmojis = {
                'healthy': 'Saine',
                'stressed': 'Stressée',
                'critical': 'Critique'
            };
            document.getElementById('health-status').textContent = healthEmojis[health] || 'En croissance';
        }

        // Soil data
        if (gameState.soil) {
            document.getElementById('moisture').textContent = gameState.soil.moisture?.toFixed(1) || '0.0';
            document.getElementById('moisture-status').textContent = gameState.soil.status || 'N/A';
            document.getElementById('nitrogen').textContent = gameState.soil.nitrogen?.toFixed(1) || '0.0';
        }

        // Update chart
        updateChart();
    } catch (error) {
        console.error('Error updating UI:', error);
    }
}

/**
 * Update costs based on slider values
 */
function updateCosts() {
    const irrigation = parseInt(document.getElementById('irrigation-slider').value);
    const fertilizer = parseInt(document.getElementById('fertilizer-slider').value);

    // Update displays
    document.getElementById('irrigation-value').textContent = irrigation;
    document.getElementById('fertilizer-value').textContent = fertilizer;

    // Calculate costs
    const irrigationCost = irrigation * 3.5;
    const fertilizerCost = fertilizer * 1.2;
    const totalCost = irrigationCost + fertilizerCost;

    document.getElementById('irrigation-cost').textContent = irrigationCost.toFixed(2);
    document.getElementById('fertilizer-cost').textContent = fertilizerCost.toFixed(2);
    document.getElementById('total-cost').textContent = totalCost.toFixed(2);

    // Check if over budget
    const validateBtn = document.getElementById('validate-btn');
    if (totalCost > gameState.budget) {
        validateBtn.disabled = true;
        validateBtn.textContent = '❌ Budget insuffisant';
    } else {
        validateBtn.disabled = false;
        validateBtn.textContent = '✅ Valider la semaine';
    }
}

/**
 * Validate week and perform action
 */
async function validateWeek() {
    const irrigation = parseInt(document.getElementById('irrigation-slider').value);
    const fertilizer = parseInt(document.getElementById('fertilizer-slider').value);

    // Show loading
    document.getElementById('loading').style.display = 'flex';

    try {
        const result = await api.performAction(irrigation, fertilizer);

        // Update game state
        gameState.week = result.week;
        gameState.budget = result.budget;
        gameState.crop = result.crop;
        gameState.soil = result.soil;
        gameState.ndvi_history.push(result.crop.ndvi);

        // Update UI
        updateUI();

        // Display messages
        displayMessages(result.messages);

        // Display event if any
        if (result.event) {
            displayEvent(result.event);
        }

        // Reset sliders
        document.getElementById('irrigation-slider').value = 0;
        document.getElementById('fertilizer-slider').value = 0;
        updateCosts();

        // Check if game complete
        if (result.is_complete) {
            setTimeout(() => {
                window.location.href = 'results.html';
            }, 2000);
        }

    } catch (error) {
        alert(`Erreur: ${error.message}`);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}

/**
 * Display messages
 */
function displayMessages(messages) {
    const container = document.getElementById('messages');

    messages.forEach(msg => {
        const div = document.createElement('div');
        div.className = `message ${msg.type}`;
        div.textContent = msg.text;
        container.appendChild(div);
    });

    // Keep only last 5 messages
    while (container.children.length > 5) {
        container.removeChild(container.firstChild);
    }

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

/**
 * Display event
 */
function displayEvent(event) {
    const div = document.createElement('div');
    div.className = 'message event';
    div.innerHTML = `
        <strong>${event.icon} ${event.name}</strong><br>
        ${event.description}<br>
        <em>${event.effect}</em>
    `;
    document.getElementById('messages').appendChild(div);
}

/**
 * Initialize NDVI chart
 */
function initializeChart() {
    const ctx = document.getElementById('ndvi-chart').getContext('2d');

    ndviChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Sem 1'],
            datasets: [{
                label: 'NDVI',
                data: [gameState?.crop?.ndvi || 0.15],
                borderColor: '#2ECC71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
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
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `NDVI: ${context.parsed.y.toFixed(3)}`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Update chart with new data
 */
function updateChart() {
    if (!ndviChart || !gameState) return;

    const weeks = Array.from({ length: gameState.week }, (_, i) => `Sem ${i + 1}`);
    const ndviData = gameState.ndvi_history || [];

    ndviChart.data.labels = weeks;
    ndviChart.data.datasets[0].data = ndviData;

    // Update color based on health
    const avgNDVI = ndviData.reduce((a, b) => a + b, 0) / ndviData.length;
    if (avgNDVI >= 0.6) {
        ndviChart.data.datasets[0].borderColor = '#2ECC71';
        ndviChart.data.datasets[0].backgroundColor = 'rgba(46, 204, 113, 0.2)';
    } else if (avgNDVI >= 0.4) {
        ndviChart.data.datasets[0].borderColor = '#F1C40F';
        ndviChart.data.datasets[0].backgroundColor = 'rgba(241, 196, 15, 0.2)';
    } else {
        ndviChart.data.datasets[0].borderColor = '#E74C3C';
        ndviChart.data.datasets[0].backgroundColor = 'rgba(231, 76, 60, 0.2)';
    }

    ndviChart.update();
}
