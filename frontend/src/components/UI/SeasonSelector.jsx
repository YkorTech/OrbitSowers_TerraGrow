import React from 'react'
import './SeasonSelector.css'

/**
 * Season Selector Component
 * Allows user to choose between Spring 2024 and Summer 2024
 */
export default function SeasonSelector({ selected, onChange }) {
  const seasons = [
    {
      id: 'spring_2024',
      name: 'Spring 2024',
      icon: '',
      description: 'Mar-May',
      color: '#4CAF50'
    },
    {
      id: 'summer_2024',
      name: 'Summer 2024',
      icon: '',
      description: 'Jun-Aug',
      color: '#FF9800'
    }
  ]

  return (
    <div className="season-selector">
      <label className="season-label">Select Season:</label>
      <div className="season-options">
        {seasons.map(season => (
          <button
            key={season.id}
            className={`season-option ${selected === season.id ? 'selected' : ''}`}
            onClick={() => onChange(season.id)}
            style={{
              borderColor: selected === season.id ? season.color : '#ddd'
            }}
          >
            <span className="season-icon">{season.icon}</span>
            <div className="season-info">
              <div className="season-name">{season.name}</div>
              <div className="season-desc">{season.description}</div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
