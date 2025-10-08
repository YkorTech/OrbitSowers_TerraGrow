import React from 'react'
import './NASABadge.css'

/**
 * NASA Data Source Badge Component
 * Displays NASA logo and data attribution
 */
export default function NASABadge({ sources = [], compact = false }) {
  if (compact) {
    return (
      <div className="nasa-badge compact">
        <img src="/assets/logos/nasa_logo.png" alt="NASA" className="nasa-logo-compact" />
        <span className="badge-text">Data: NASA Earth Observations</span>
      </div>
    )
  }

  return (
    <div className="nasa-badge-panel">
      <div className="panel-header">
        <div className="header-logos">
          <img src="/assets/logos/nasa_logo.png" alt="NASA" className="nasa-logo-large" />
          <img src="/assets/logos/nasa_power_logo.png" alt="NASA POWER" className="nasa-power-logo" />
        </div>
        <div className="header-text">
          <h3>NASA Earth Observations</h3>
          <p>This game uses real satellite data from NASA</p>
        </div>
      </div>

      <div className="data-sources">
        {sources.map((source, idx) => (
          <div key={idx} className="data-source-item">
            <div className="source-icon">{source.icon}</div>
            <div className="source-info">
              <div className="source-name">{source.name}</div>
              <div className="source-desc">{source.description}</div>
              {source.resolution && (
                <div className="source-meta">
                  Resolution: {source.resolution}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="panel-footer">
        <a
          href="https://power.larc.nasa.gov/"
          target="_blank"
          rel="noopener noreferrer"
          className="source-link"
        >
          🔗 NASA POWER
        </a>
        <a
          href="https://modis.gsfc.nasa.gov/"
          target="_blank"
          rel="noopener noreferrer"
          className="source-link"
        >
          🔗 MODIS Terra
        </a>
      </div>
    </div>
  )
}

/**
 * Get default data sources
 */
export function getDefaultDataSources() {
  return [
    {
      icon: '🌡️',
      name: 'NASA POWER',
      description: 'Weather data (temperature, precipitation, humidity)',
      resolution: '0.5° × 0.625° daily'
    },
    {
      icon: '🛰️',
      name: 'MODIS Terra',
      description: 'Vegetation index (NDVI, EVI) from satellite imagery',
      resolution: '250m every 16 days'
    }
  ]
}
