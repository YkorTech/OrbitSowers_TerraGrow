import * as THREE from 'three'

/**
 * Convert latitude/longitude to 3D position on sphere
 * @param {number} lat - Latitude in degrees
 * @param {number} lon - Longitude in degrees
 * @param {number} radius - Sphere radius
 * @returns {THREE.Vector3} 3D position
 */
export function latLonToVector3(lat, lon, radius = 1) {
  const phi = (90 - lat) * (Math.PI / 180)
  const theta = (lon + 180) * (Math.PI / 180)

  const x = -(radius * Math.sin(phi) * Math.cos(theta))
  const y = radius * Math.cos(phi)
  const z = radius * Math.sin(phi) * Math.sin(theta)

  return new THREE.Vector3(x, y, z)
}

/**
 * Convert 3D position on sphere to latitude/longitude
 * @param {THREE.Vector3} point - 3D position
 * @returns {{lat: number, lon: number}} Coordinates
 */
export function vector3ToLatLon(point) {
  const { x, y, z } = point.normalize()

  const lat = 90 - Math.acos(y) * (180 / Math.PI)
  const lon = ((270 + Math.atan2(x, z) * (180 / Math.PI)) % 360) - 180

  return { lat, lon }
}

/**
 * Calculate camera position to look at a lat/lon point
 * @param {number} lat - Latitude
 * @param {number} lon - Longitude
 * @param {number} distance - Camera distance from target
 * @returns {THREE.Vector3} Camera position
 */
export function getCameraPositionForRegion(lat, lon, distance = 2) {
  const targetPoint = latLonToVector3(lat, lon, 1)

  // Position camera along the direction from earth center to target
  return targetPoint.clone().multiplyScalar(distance)
}

/**
 * Get region name from coordinates using reverse geocoding
 * @param {number} lat
 * @param {number} lon
 * @returns {Promise<string>} Region name
 */
export async function getRegionName(lat, lon) {
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`,
      {
        headers: {
          'User-Agent': 'TerraGrow Academy'
        }
      }
    )
    const data = await response.json()
    return data.display_name || `${lat.toFixed(2)}°, ${lon.toFixed(2)}°`
  } catch (error) {
    console.error('Geocoding error:', error)
    return `${lat.toFixed(2)}°, ${lon.toFixed(2)}°`
  }
}

/**
 * Find closest popular region to given coordinates
 * @param {number} lat
 * @param {number} lon
 * @param {Array} popularRegions - Array of {name, lat, lon, climate}
 * @returns {Object|null} Closest region or null
 */
export function findClosestPopularRegion(lat, lon, popularRegions) {
  let minDistance = Infinity
  let closest = null

  popularRegions.forEach(region => {
    const distance = calculateDistance(lat, lon, region.lat, region.lon)
    if (distance < minDistance && distance < 50) { // Within 50km
      minDistance = distance
      closest = region
    }
  })

  return closest
}

/**
 * Calculate distance between two lat/lon points (Haversine formula)
 * @param {number} lat1
 * @param {number} lon1
 * @param {number} lat2
 * @param {number} lon2
 * @returns {number} Distance in kilometers
 */
export function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371 // Earth radius in km

  const dLat = ((lat2 - lat1) * Math.PI) / 180
  const dLon = ((lon2 - lon1) * Math.PI) / 180

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2)

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

  return R * c
}
