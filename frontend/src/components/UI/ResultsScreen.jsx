import React from 'react'
import { useGameStore } from '../../stores/gameStore'
import { logger } from '../../utils/logger'
import './ResultsScreen.css'

/**
 * Results screen shown after harvest (12 weeks completed)
 */
export default function ResultsScreen({ harvestResults }) {
  const resetGame = useGameStore(state => state.resetGame)

  logger.log('ResultsScreen rendering with:', harvestResults)

  if (!harvestResults) {
    logger.warn('ResultsScreen: harvestResults is null/undefined')
    return null
  }

  const {
    yield: cropYield = 0,
    sustainability_score = 0,
    stars = 0,
    recommendations = [],
    ndvi_history = []
  } = harvestResults

  logger.log('Parsed results:', { cropYield, sustainability_score, stars, recommendations, ndvi_history })

  // Calculate grade based on stars
  const getGrade = (stars) => {
    if (stars >= 4.5) return { letter: 'S', color: '#FFD700', label: 'Excellent!' }
    if (stars >= 3.5) return { letter: 'A', color: '#10b981', label: 'Great!' }
    if (stars >= 2.5) return { letter: 'B', color: '#4ade80', label: 'Good!' }
    if (stars >= 1.5) return { letter: 'C', color: '#f59e0b', label: 'Fair' }
    return { letter: 'D', color: '#ef4444', label: 'Needs improvement' }
  }

  const grade = getGrade(stars)

  return (
    <div className="results-overlay">
      <div className="results-container">
        <div className="results-header">
          <h1>Harvest Complete!</h1>
          <p className="subtitle">Your results after 12 weeks</p>
        </div>

        {/* Grade */}
        <div className="grade-section">
          <div className="grade-circle" style={{ borderColor: grade.color }}>
            <span className="grade-letter" style={{ color: grade.color }}>{grade.letter}</span>
          </div>
          <p className="grade-label" style={{ color: grade.color }}>{grade.label}</p>
          <div className="stars">
            {[...Array(5)].map((_, i) => (
              <span key={i} className={i < Math.floor(stars) ? 'star filled' : 'star'}>⭐</span>
            ))}
          </div>
          <p className="stars-count">{stars.toFixed(1)} / 5.0</p>
        </div>

        {/* Stats */}
        <div className="results-stats">
          <div className="stat-card">
            <div className="stat-icon">🌾</div>
            <div className="stat-label">Yield</div>
            <div className="stat-value">{cropYield.toFixed(1)} t/ha</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🌿</div>
            <div className="stat-label">Sustainability</div>
            <div className="stat-value">{sustainability_score.toFixed(0)}%</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-label">Final NDVI</div>
            <div className="stat-value">
              {ndvi_history.length > 0 ? ndvi_history[ndvi_history.length - 1].toFixed(2) : '0.00'}
            </div>
          </div>
        </div>

        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <div className="recommendations-section">
            <h3>Recommendations</h3>
            <ul className="recommendations-list">
              {recommendations.map((rec, index) => {
                // Support both string and object formats
                const text = typeof rec === 'string' ? rec : rec.text || JSON.stringify(rec)
                const type = typeof rec === 'object' ? rec.type : 'info'
                const icon = type === 'warning' ? '⚠️' : type === 'success' ? '✅' : type === 'info' ? 'ℹ️' : '💡'

                return (
                  <li key={index}>
                    <span style={{ marginRight: '8px' }}>{icon}</span>
                    {text}
                  </li>
                )
              })}
            </ul>
          </div>
        )}

        {/* Actions */}
        <div className="results-actions">
          <button
            className="btn-replay"
            onClick={resetGame}
          >
            New Game
          </button>
        </div>

        <p className="footer-text">
          Thanks for playing TerraGrow Academy!
        </p>
      </div>
    </div>
  )
}
