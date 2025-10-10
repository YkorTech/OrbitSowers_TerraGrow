import React from 'react'
import { useGameStore } from '../../stores/gameStore'
import TeamModal from './TeamModal'
import './Header.css'

/**
 * Top header bar
 */
export default function Header() {
  const view = useGameStore(state => state.view)
  const gameState = useGameStore(state => state.gameState)
  const resetGame = useGameStore(state => state.resetGame)
  const setShowTutorial = useGameStore(state => state.setShowTutorial)
  const setShowEducationalPanel = useGameStore(state => state.setShowEducationalPanel)
  const showTeamModal = useGameStore(state => state.showTeamModal)
  const setShowTeamModal = useGameStore(state => state.setShowTeamModal)

  const handleShowTutorial = () => {
    // Reset tutorial completion to show it again
    localStorage.removeItem('terragrow_tutorial_completed')
    setShowTutorial(true)
  }

  return (
    <>
      <header className="header">
        <div className="header-left">
          <h1 className="logo">TerraGrow Academy</h1>
          <p className="tagline">Cultivating the future through the eyes of NASA.</p>
        </div>

        <div className="header-center">
          {view === 'game' && gameState && (
            <div className="game-stats">
              <div className="stat">
                <span className="stat-label">Week</span>
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
          <button
            className="btn-icon"
            onClick={handleShowTutorial}
            title="Tutorial"
          >
            ?
          </button>

          <button
            className="btn-icon"
            onClick={() => setShowEducationalPanel(true)}
            title="Learn about NASA data"
          >
            Learn
          </button>

          {view !== 'globe' && (
            <button className="btn-back" onClick={resetGame}>
              ← Back to Globe
            </button>
          )}

          <button
            className="team-badge-button"
            onClick={() => setShowTeamModal(true)}
            title="About OrbitSowers Labs Team"
          >
            <img
              src="/assets/logos/orbitsowers_logo.png"
              alt="OrbitSowers Labs"
              className="team-logo-img"
            />
          </button>
        </div>
      </header>

      <TeamModal />
    </>
  )
}
