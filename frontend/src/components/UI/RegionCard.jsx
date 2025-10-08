import React, { useEffect, useState } from 'react'
import { useGameStore } from '../../stores/gameStore'
import { useNASAData } from '../../hooks/useNASAData'
import CropSelector from './CropSelector'
import SeasonSelector from './SeasonSelector'
import './RegionCard.css'

/**
 * Card displaying region information after globe click
 */
export default function RegionCard({ region }) {
  const setView = useGameStore(state => state.setView)
  const setGameState = useGameStore(state => state.setGameState)
  const setLoading = useGameStore(state => state.setLoading)
  const selectedCrop = useGameStore(state => state.selectedCrop)

  const [selectedSeason, setSelectedSeason] = useState('spring_2024')

  const { data, loading, error } = useNASAData(
    region.lat,
    region.lon,
    selectedCrop.id,
    selectedSeason,
    null // region_id determined by backend based on lat/lon
  )

  const handleStartGame = () => {
    if (!data) return

    setLoading(true, 'Initializing game...')

    // Store game state
    setGameState(data.state, data.session_id)

    // Transition to game view
    setTimeout(() => {
      setView('game')
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="region-card">
      <div className="region-card-header">
        <h2>{region.name}</h2>
        <p className="region-coords">
          {region.lat.toFixed(2)}°, {region.lon.toFixed(2)}°
        </p>
      </div>

      <div className="region-card-body">
        {loading && (
          <div className="loading-data">
            <div className="spinner-small"></div>
            <p>Loading NASA data...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}

        {data && (
          <>
            <div className="region-info">
              <div className="info-item">
                <span className="info-label">Climate</span>
                <span className="info-value">{data.state.region.climate}</span>
              </div>

              <div className="info-item">
                <span className="info-label">Temperature</span>
                <span className="info-value">
                  {data.weather_preview?.[0]?.temperature || 25}°C
                </span>
              </div>

              <div className="info-item">
                <span className="info-label">Precipitation</span>
                <span className="info-value">
                  {data.weather_preview?.[0]?.precipitation || 10} mm
                </span>
              </div>
            </div>

            {/* Season Selector */}
            <SeasonSelector
              selected={selectedSeason}
              onChange={setSelectedSeason}
            />

            {/* Crop Selector with 3D preview */}
            <CropSelector climate={data.state.region.climate} />

            {/* Data Source Badge - Small */}
            <div className="data-source-compact">
              <span className="source-icon">🛰️</span>
              <span>NASA POWER + MODIS 2024</span>
            </div>

            <button
              className="btn-start-game"
              onClick={handleStartGame}
            >
              Start Growing {selectedCrop.icon}
            </button>
          </>
        )}
      </div>
    </div>
  )
}
