const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

/**
 * Fetch wrapper with error handling
 */
async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'API request failed')
    }

    return await response.json()
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error)
    throw error
  }
}

/**
 * Initialize game session
 * @param {number} lat
 * @param {number} lon
 * @param {string} cropType - Optional crop type
 * @returns {Promise<Object>} Game state
 */
export async function initializeGame(lat, lon, cropType = null) {
  return fetchAPI('/init', {
    method: 'POST',
    body: JSON.stringify({ lat, lon, crop_type: cropType })
  })
}

/**
 * Perform weekly action
 * @param {string} sessionId
 * @param {number} irrigation - mm
 * @param {number} fertilizer - kg N/ha
 * @returns {Promise<Object>} Updated state
 */
export async function performAction(sessionId, irrigation, fertilizer) {
  return fetchAPI('/action', {
    method: 'POST',
    body: JSON.stringify({
      session_id: sessionId,
      irrigation,
      fertilizer
    })
  })
}

/**
 * Get harvest results
 * @param {string} sessionId
 * @returns {Promise<Object>} Final scores
 */
export async function getHarvestResults(sessionId) {
  return fetchAPI(`/harvest?session_id=${sessionId}`)
}

/**
 * Search location
 * @param {string} query
 * @returns {Promise<Array>} Search results
 */
export async function searchLocation(query) {
  return fetchAPI(`/search-location?q=${encodeURIComponent(query)}`)
}

/**
 * Get popular regions
 * @returns {Promise<Array>} Popular regions
 */
export async function getPopularRegions() {
  return fetchAPI('/popular-regions')
}

/**
 * Get current game state
 * @param {string} sessionId
 * @returns {Promise<Object>} Game state
 */
export async function getGameState(sessionId) {
  return fetchAPI(`/state?session_id=${sessionId}`)
}

export default {
  initializeGame,
  performAction,
  getHarvestResults,
  searchLocation,
  getPopularRegions,
  getGameState
}
