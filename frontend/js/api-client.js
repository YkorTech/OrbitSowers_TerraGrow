/**
 * TerraGrow Academy - API Client
 * Handles communication with backend API
 */

class TerraGrowAPI {
    constructor() {
        this.baseURL = 'http://localhost:5000/api';
        this.sessionId = null;
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }

    /**
     * Search for a location
     */
    async searchLocation(query) {
        try {
            const response = await fetch(`${this.baseURL}/search-location?q=${encodeURIComponent(query)}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.results || [];
        } catch (error) {
            console.error('Location search failed:', error);
            throw error;
        }
    }

    /**
     * Get popular regions
     */
    async getPopularRegions() {
        try {
            const response = await fetch(`${this.baseURL}/popular-regions`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.regions || [];
        } catch (error) {
            console.error('Failed to fetch popular regions:', error);
            return [];
        }
    }

    /**
     * Initialize a new game
     */
    async initGame(lat, lon, cropType = null) {
        try {
            const response = await fetch(`${this.baseURL}/init`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    lat: lat,
                    lon: lon,
                    crop_type: cropType
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to initialize game');
            }

            const data = await response.json();
            this.sessionId = data.session_id;

            // Store session in localStorage
            localStorage.setItem('terragrow_session', this.sessionId);

            return data;
        } catch (error) {
            console.error('Game initialization failed:', error);
            throw error;
        }
    }

    /**
     * Perform a weekly action
     */
    async performAction(irrigation, fertilizer) {
        if (!this.sessionId) {
            // Try to recover from localStorage
            this.sessionId = localStorage.getItem('terragrow_session');
            if (!this.sessionId) {
                throw new Error('No active game session');
            }
        }

        try {
            const response = await fetch(`${this.baseURL}/action`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    irrigation: irrigation,
                    fertilizer: fertilizer
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Action failed');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Action failed:', error);
            throw error;
        }
    }

    /**
     * Harvest and get final scores
     */
    async harvest() {
        if (!this.sessionId) {
            this.sessionId = localStorage.getItem('terragrow_session');
            if (!this.sessionId) {
                throw new Error('No active game session');
            }
        }

        try {
            const response = await fetch(`${this.baseURL}/harvest?session_id=${this.sessionId}`);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Harvest failed');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Harvest failed:', error);
            throw error;
        }
    }

    /**
     * Get current game state
     */
    async getState() {
        if (!this.sessionId) {
            this.sessionId = localStorage.getItem('terragrow_session');
            if (!this.sessionId) {
                throw new Error('No active game session');
            }
        }

        try {
            const response = await fetch(`${this.baseURL}/state?session_id=${this.sessionId}`);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to get state');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Failed to get state:', error);
            throw error;
        }
    }

    /**
     * Clear session
     */
    clearSession() {
        this.sessionId = null;
        localStorage.removeItem('terragrow_session');
    }
}

// Create global instance
const api = new TerraGrowAPI();
