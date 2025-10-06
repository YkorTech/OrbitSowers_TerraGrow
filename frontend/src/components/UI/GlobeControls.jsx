import React, { useState } from 'react'
import { useGameStore } from '../../stores/gameStore'
import { latLonToVector3, getRegionName } from '../../utils/coordinates'
import './GlobeControls.css'

/**
 * UI controls for globe - Geolocation button
 */
export default function GlobeControls() {
  const setSelectedRegion = useGameStore(state => state.setSelectedRegion)
  const setCameraTarget = useGameStore(state => state.setCameraTarget)
  const setLoading = useGameStore(state => state.setLoading)

  const [geolocating, setGeolocating] = useState(false)
  const [error, setError] = useState(null)

  const handleGeolocation = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser')
      return
    }

    setGeolocating(true)
    setError(null)
    setLoading(true, 'Detecting your position...')

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude
        const lon = position.coords.longitude

        console.log(`Geolocation: ${lat.toFixed(2)}°, ${lon.toFixed(2)}°`)

        // Get region name
        const regionName = await getRegionName(lat, lon)

        // Calculate 3D position
        const pos3D = latLonToVector3(lat, lon, 1)

        // Set selected region
        setSelectedRegion({
          name: regionName,
          lat,
          lon,
          position: pos3D,
          climate: 'Loading...',
          flag: '📍'
        })

        // Set camera target for zoom
        setCameraTarget({
          position: pos3D,
          lat,
          lon
        })

        setGeolocating(false)
        setLoading(false)
      },
      (error) => {
        console.error('Geolocation error:', error)
        setError('Unable to get your position')
        setGeolocating(false)
        setLoading(false)
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    )
  }

  return (
    <div className="globe-controls">
      <button
        className="btn-geolocation"
        onClick={handleGeolocation}
        disabled={geolocating}
      >
        {geolocating ? (
          <>
            <span className="spinner-icon">⏳</span>
            Locating...
          </>
        ) : (
          <>
            <span className="location-icon">📍</span>
            My Location
          </>
        )}
      </button>

      {error && (
        <div className="geolocation-error">
          {error}
        </div>
      )}

      <div className="controls-hint">
        Click on a region or use your location
      </div>
    </div>
  )
}
