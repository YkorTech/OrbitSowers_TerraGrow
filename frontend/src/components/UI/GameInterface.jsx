import React, { useState } from 'react'
import { useGameStore } from '../../stores/gameStore'
import { useGameActions } from '../../hooks/useNASAData'
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

  const irrigationCost = irrigation * 3.5
  const fertilizerCost = fertilizer * 1.2
  const totalCost = irrigationCost + fertilizerCost

  const handleValidateWeek = async () => {
    try {
      const result = await submitAction(irrigation, fertilizer)

      console.log('Week validated:', result.week, 'is_complete:', result.is_complete)

      // Update game state
      setGameState(result, sessionId)

      // Reset sliders
      setIrrigation(0)
      setFertilizer(0)

      // Check if game is complete (week 12 finished)
      // Backend should return is_complete=true AFTER week 12 is played
      if (result.is_complete) {
        console.log('Game complete! Triggering harvest...')
        setTimeout(() => {
          handleHarvest()
        }, 1500)
      }
    } catch (error) {
      console.error('Action failed:', error)
      alert('Error: ' + error.message)
    }
  }

  const handleHarvest = async () => {
    try {
      console.log('🌾 Starting harvest...')
      const results = await harvest()
      console.log('✅ Harvest results received:', results)

      // Store results
      setHarvestResults(results)
      console.log('📊 Results stored in state')

      // Switch to results view
      setView('results')
      console.log('🎯 View switched to results')
    } catch (error) {
      console.error('Harvest failed:', error)
      alert('Harvest error: ' + error.message)
    }
  }

  const crop = gameState?.crop || {}
  const soil = gameState?.soil || {}
  const week = gameState?.week || 1
  const budget = gameState?.budget || 2000

  return (
    <div className="game-interface">
      {/* Top info bar - Compact stats */}
      <div className="info-bar">
        <div className="stat-compact">
          <span className="stat-compact-icon">📅</span>
          <div className="stat-compact-content">
            <span className="stat-compact-label">Week</span>
            <span className="stat-compact-value">{week}/12</span>
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

          <button
            className="btn-validate"
            onClick={handleValidateWeek}
            disabled={isProcessing || totalCost > budget}
          >
            {isProcessing ? 'Simulating...' : 'Validate Week ' + week}
          </button>

          {totalCost > budget && (
            <p className="error-budget">Insufficient budget</p>
          )}
        </div>
      </div>
    </div>
  )
}
