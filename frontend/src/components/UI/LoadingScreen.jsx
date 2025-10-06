import React from 'react'
import { useGameStore } from '../../stores/gameStore'
import './LoadingScreen.css'

/**
 * Full-screen loading overlay
 */
export default function LoadingScreen() {
  const isLoading = useGameStore(state => state.isLoading)
  const loadingMessage = useGameStore(state => state.loadingMessage)

  if (!isLoading) return null

  return (
    <div className="loading-screen">
      <div className="loading-content">
        <div className="loader">
          <div className="earth-spinner"></div>
          <div className="satellite-spinner">🛰️</div>
        </div>
        <h3>{loadingMessage || 'Chargement...'}</h3>
        <p className="loading-subtitle">Données satellites NASA en cours de traitement</p>
      </div>
    </div>
  )
}
