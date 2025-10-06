/**
 * TerraGrow Academy - Location Selection
 */

let selectedLocation = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Location selection initialized');

    // Load popular regions
    await loadPopularRegions();

    // Setup event listeners
    setupEventListeners();
});

/**
 * Load popular regions
 */
async function loadPopularRegions() {
    try {
        const regions = await api.getPopularRegions();
        const grid = document.getElementById('popular-grid');

        grid.innerHTML = regions.map(region => `
            <div class="region-card" data-lat="${region.lat}" data-lon="${region.lon}" data-name="${region.name}" data-climate="${region.climate}">
                <h4>${region.name}</h4>
                <p>🌡️ ${region.climate}</p>
            </div>
        `).join('');

        // Add click handlers
        document.querySelectorAll('.region-card').forEach(card => {
            card.addEventListener('click', () => {
                const lat = parseFloat(card.dataset.lat);
                const lon = parseFloat(card.dataset.lon);
                const name = card.dataset.name;
                const climate = card.dataset.climate;

                selectLocation(lat, lon, name, climate);
            });
        });

    } catch (error) {
        console.error('Failed to load popular regions:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Geolocation button
    const geoBtn = document.getElementById('geolocate-btn');
    geoBtn.addEventListener('click', handleGeolocation);

    // Search input
    const searchInput = document.getElementById('location-search');
    const searchBtn = document.getElementById('search-btn');

    searchInput.addEventListener('input', debounce(handleSearch, 500));
    searchBtn.addEventListener('click', () => handleSearch());

    // Start button
    const startBtn = document.getElementById('start-btn');
    startBtn.addEventListener('click', startGame);
}

/**
 * Handle geolocation
 */
function handleGeolocation() {
    if (!navigator.geolocation) {
        alert('La géolocalisation n\'est pas supportée par votre navigateur');
        return;
    }

    const btn = document.getElementById('geolocate-btn');
    btn.textContent = '📍 Détection en cours...';
    btn.disabled = true;

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            // Get location name
            try {
                const results = await api.searchLocation(`${lat},${lon}`);
                const name = results[0]?.name || `Position (${lat.toFixed(2)}, ${lon.toFixed(2)})`;
                const climate = 'Climat local';

                selectLocation(lat, lon, name, climate);
            } catch (error) {
                selectLocation(lat, lon, `Position (${lat.toFixed(2)}, ${lon.toFixed(2)})`, 'Climat local');
            }

            btn.textContent = '📍 Détecter ma position';
            btn.disabled = false;
        },
        (error) => {
            alert('Impossible de déterminer votre position');
            btn.textContent = '📍 Détecter ma position';
            btn.disabled = false;
        }
    );
}

/**
 * Handle search
 */
async function handleSearch() {
    const searchInput = document.getElementById('location-search');
    const query = searchInput.value.trim();

    if (query.length < 3) {
        document.getElementById('search-results').innerHTML = '';
        return;
    }

    try {
        const results = await api.searchLocation(query);
        displaySearchResults(results);
    } catch (error) {
        console.error('Search failed:', error);
    }
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    const container = document.getElementById('search-results');

    if (results.length === 0) {
        container.innerHTML = '<div class="search-result-item">Aucun résultat trouvé</div>';
        return;
    }

    container.innerHTML = results.map(result => `
        <div class="search-result-item" data-lat="${result.lat}" data-lon="${result.lon}" data-name="${result.name}">
            📍 ${result.name}
        </div>
    `).join('');

    // Add click handlers
    document.querySelectorAll('.search-result-item').forEach(item => {
        item.addEventListener('click', () => {
            const lat = parseFloat(item.dataset.lat);
            const lon = parseFloat(item.dataset.lon);
            const name = item.dataset.name;

            selectLocation(lat, lon, name, 'Climat local');
            document.getElementById('search-results').innerHTML = '';
            document.getElementById('location-search').value = '';
        });
    });
}

/**
 * Select a location
 */
function selectLocation(lat, lon, name, climate) {
    selectedLocation = { lat, lon, name, climate };

    // Store in localStorage
    localStorage.setItem('terragrow_location', JSON.stringify(selectedLocation));

    // Update UI
    const selectedDiv = document.getElementById('selected-location');
    document.getElementById('selected-name').textContent = name;
    document.getElementById('selected-climate').textContent = `🌡️ ${climate}`;

    selectedDiv.style.display = 'block';

    // Scroll to selection
    selectedDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Start game
 */
async function startGame() {
    if (!selectedLocation) {
        alert('Veuillez sélectionner une région');
        return;
    }

    const btn = document.getElementById('start-btn');
    btn.textContent = '🌱 Initialisation...';
    btn.disabled = true;

    try {
        await api.initGame(selectedLocation.lat, selectedLocation.lon);

        // Redirect to game
        window.location.href = 'game.html';

    } catch (error) {
        alert(`Erreur: ${error.message}`);
        btn.textContent = '🌱 Commencer à cultiver';
        btn.disabled = false;
    }
}

/**
 * Debounce utility
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
