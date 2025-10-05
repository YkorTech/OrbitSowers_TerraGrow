import React from 'react'
import { useGameStore } from '../../stores/gameStore'
import './Header.css'

/**
 * Top header bar
 */
export default function Header() {
  const view = useGameStore(state => state.view)
  const gameState = useGameStore(state => state.gameState)
  const resetGame = useGameStore(state => state.resetGame)

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="logo">TerraGrow Academy</h1>
        <p className="tagline">Cultivating the future through the eyes of NASA.</p>
      </div>

      <div className="header-center">
        {view === 'game' && gameState && (
          <div className="game-stats">
            <div className="stat">
              <span className="stat-label">Semaine</span>
              <span className="stat-value">{gameState.week || 1}</span>
              <span className="stat-max">/ 12</span>
            </div>
            <div className="stat">
              <span className="stat-label">Budget</span>
              <span className="stat-value">${gameState.budget || 2000}</span>
            </div>
          </div>
        )}
      </div>

      <div className="header-right">
        {view !== 'globe' && (
          <button className="btn-back" onClick={resetGame}>
            ← Retour au globe
          </button>
        )}
        <span className="team-badge">OrbitSowers Labs</span>
      </div>
    </header>
  )
}
