import React, { useState } from 'react'
import { useGameStore } from '../../stores/gameStore'
import { useGameActions } from '../../hooks/useNASAData'
import { logger } from '../../utils/logger'
import './GameInterface.css'

/**
 * Main game interface during farming phase
 */
export default function GameInterface({ gameState }) {
  const sessionId = useGameStore(state => state.sessionId)
  const setGameState = useGameStore(state => state.setGameState)
  const setView = useGameStore(state => state.setView)
  const setHarvestResults = useGameStore(state => state.setHarvestResults)

  const { submitAction, harvest, isProcessing } = useGameActions(sessionId)

  const [irrigation, setIrrigation] = useState(0)
  const [fertilizer, setFertilizer] = useState(0)
  const [showHarvestButton, setShowHarvestButton] = useState(false)
  const [gameComplete, setGameComplete] = useState(false)

  const irrigationCost = irrigation * 1.5  // Updated cost (gameplay balance)
  const fertilizerCost = fertilizer * 1.2
  const totalCost = irrigationCost + fertilizerCost

  const handleValidateWeek = async () => {
    try {
      const result = await submitAction(irrigation, fertilizer)

      logger.log('Week', result.week_played, 'validated. Next week:', result.week, 'is_complete:', result.is_complete)

      // Update game state
      setGameState(result, sessionId)

      // Reset sliders
      setIrrigation(0)
      setFertilizer(0)

      // Check if game is complete (week 12 finished)
      if (result.is_complete) {
        logger.log('Game complete! Week 12 finished. Showing harvest button after delay...')
        setGameComplete(true)  // Disable button immediately
        setTimeout(() => {
          setShowHarvestButton(true)
        }, 2000)  // 2 seconds to see week 12 results
      }
    } catch (error) {
      logger.error('Action failed:', error)
      // Don't show error if game is already complete (expected behavior)
      if (!error.message.includes('already completed')) {
        alert('Error: ' + error.message)
      }
    }
  }

  const handleHarvest = async () => {
    try {
      logger.log('Starting harvest...')
      const results = await harvest()
      logger.log('Harvest results received:', results)

      // Store results
      setHarvestResults(results)
      logger.log('Results stored in state')

      // Switch to results view
      setView('results')
      logger.log('View switched to results')
    } catch (error) {
      logger.error('Harvest failed:', error)
      alert('Harvest error: ' + error.message)
    }
  }

  const crop = gameState?.crop || {}
  const soil = gameState?.soil || {}
  const week = gameState?.week || 1
  const budget = gameState?.budget || 2000

  // Display week (cap at 12 for UI)
  const displayWeek = Math.min(week, 12)

  return (
    <div className="game-interface">
      {/* Top info bar - Compact stats */}
      <div className="info-bar">
        <div className="stat-compact">
          <span className="stat-compact-icon">📅</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">Week</span>
            <span className="stat-compact-value">{displayWeek}/12</span>
          </div>
        </div>

        <div className="stat-compact">
          <span className="stat-compact-icon">🌱</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">NDVI</span>
            <span className="stat-compact-value" style={{
              color: crop.ndvi > 0.6 ? '#10b981' : crop.ndvi > 0.3 ? '#f59e0b' : '#ef4444'
            }}>
              {(crop.ndvi || 0.15).toFixed(2)}
            </span>
          </div>
        </div>

        <div className="stat-compact">
          <span className="stat-compact-icon">💧</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">Moisture</span>
            <span className="stat-compact-value">{(soil.moisture || 50).toFixed(0)}%</span>
          </div>
        </div>

        <div className="stat-compact">
          <span className="stat-compact-icon">🌿</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">Nitrogen</span>
            <span className="stat-compact-value">{(soil.nitrogen || 80).toFixed(0)} kg</span>
          </div>
        </div>

        <div className="stat-compact">
          <span className="stat-compact-icon">💰</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">Budget</span>
            <span className="stat-compact-value">${budget.toFixed(0)}</span>
          </div>
        </div>
      </div>


      {/* Bottom control bar */}
      <div className="control-bar">
        {/* Irrigation Control */}
        <div className="control-card">
          <h4>💧 Irrigation</h4>
          <input
            type="range"
            min="0"
            max="30"
            step="5"
            value={irrigation}
            onChange={(e) => setIrrigation(Number(e.target.value))}
            className="slider"
            disabled={isProcessing}
          />
          <div className="slider-labels">
            <span>0</span>
            <span>30 mm</span>
          </div>
          <p className="slider-value">{irrigation} mm</p>
          <p className="cost">Cost: ${irrigationCost.toFixed(2)}</p>
        </div>

        {/* Fertilization Control */}
        <div className="control-card">
          <h4>🌿 Fertilizer</h4>
          <input
            type="range"
            min="0"
            max="100"
            step="10"
            value={fertilizer}
            onChange={(e) => setFertilizer(Number(e.target.value))}
            className="slider"
            disabled={isProcessing}
          />
          <div className="slider-labels">
            <span>0</span>
            <span>100 kg</span>
          </div>
          <p className="slider-value">{fertilizer} kg N/ha</p>
          <p className="cost">Cost: ${fertilizerCost.toFixed(2)}</p>
        </div>

        {/* Validate Section */}
        <div className="control-card validate-section">
          <div className="budget-info">
            <div>
              <div className="budget-label">Week Total</div>
              <div className="cost-summary-total">${totalCost.toFixed(2)}</div>
            </div>
            <div>
              <div className="budget-label">Remaining</div>
              <div className="budget-value">${Math.max(0, budget - totalCost).toFixed(2)}</div>
            </div>
          </div>

          {showHarvestButton ? (
            <button
              className="btn-validate btn-harvest"
              onClick={handleHarvest}
              disabled={isProcessing}
              style={{
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                fontSize: '1.1em',
                fontWeight: 'bold'
              }}
            >
              🌾 View Harvest Results
            </button>
          ) : (
            <button
              className="btn-validate"
              onClick={handleValidateWeek}
              disabled={isProcessing || totalCost > budget || gameComplete}
            >
              {gameComplete ? 'Season Complete! ✓' : (isProcessing ? 'Simulating...' : 'Validate Week ' + displayWeek)}
            </button>
          )}

          {totalCost > budget && !gameComplete && (
            <p className="error-budget">Insufficient budget</p>
          )}

          {gameComplete && !showHarvestButton && (
            <p style={{ color: '#10b981', marginTop: '10px', fontWeight: 'bold' }}>
              ✓ Week 12 complete! Preparing results...
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
