import React, { useState } from 'react'
import { useGameStore } from '../../stores/gameStore'
import './EducationalPanel.css'

/**
 * Educational Panel Component
 * Accordion with NASA satellite data explanations
 */
export default function EducationalPanel() {
  const showEducationalPanel = useGameStore(state => state.showEducationalPanel)
  const setShowEducationalPanel = useGameStore(state => state.setShowEducationalPanel)

  const [expandedSection, setExpandedSection] = useState(null)

  const sections = [
    {
      id: 'ndvi',
      icon: '',
      title: 'What is NDVI?',
      content: [
        {
          subtitle: 'Definition',
          text: 'NDVI (Normalized Difference Vegetation Index) measures vegetation health from space using satellite imagery.'
        },
        {
          subtitle: 'How it works',
          text: 'Healthy plants reflect more near-infrared light and absorb visible red light. NDVI calculates this difference: (NIR - Red) / (NIR + Red).'
        },
        {
          subtitle: 'Scale',
          text: '0.0 = Bare soil, water, or snow\n0.2-0.3 = Sparse vegetation\n0.6-0.8 = Dense, healthy crops\n0.8-1.0 = Very dense vegetation (forests)'
        },
        {
          subtitle: 'MODIS Terra Satellite',
          text: 'NASA MODIS sensor captures NDVI every 16 days at 250m resolution. This game uses real 2024 MODIS data!'
        }
      ]
    },
    {
      id: 'weather',
      icon: '',
      title: 'NASA POWER Weather Data',
      content: [
        {
          subtitle: 'What is NASA POWER?',
          text: 'The Prediction Of Worldwide Energy Resources (POWER) project provides solar and meteorological data from NASA research.'
        },
        {
          subtitle: 'Data for Farmers',
          text: 'Temperature: Daily min/max/average helps plan planting and harvesting.\nPrecipitation: Rainfall totals guide irrigation decisions.\nHumidity & Wind: Affect disease risk and water loss.'
        },
        {
          subtitle: 'Resolution',
          text: 'Spatial: 0.5° × 0.625° (about 50km grid)\nTemporal: Daily measurements since 1981\n\nThis game uses real Spring & Summer 2024 data!'
        }
      ]
    },
    {
      id: 'impact',
      icon: '',
      title: 'Real-World Agricultural Impact',
      content: [
        {
          subtitle: 'Crop Monitoring',
          text: 'Farmers use NDVI to detect stressed crops early, often before visible to the human eye. This allows targeted treatment.'
        },
        {
          subtitle: 'Water Management',
          text: 'Combining NDVI with weather data optimizes irrigation. Healthy crops (high NDVI) with low rainfall signal need for water.'
        },
        {
          subtitle: 'Yield Prediction',
          text: 'NDVI trends during growing season correlate with final yield. Researchers use satellite data to forecast harvests globally.'
        },
        {
          subtitle: 'Climate Adaptation',
          text: 'Historical NASA data helps farmers adapt to climate change by analyzing long-term trends and extreme weather patterns.'
        }
      ]
    },
    {
      id: 'learn',
      icon: '',
      title: 'Learn More from NASA',
      content: [
        {
          subtitle: 'NASA ARSET Training',
          text: 'Free online courses on using satellite data for agriculture, disaster management, and more.',
          link: 'https://appliedsciences.nasa.gov/what-we-do/capacity-building/arset'
        },
        {
          subtitle: 'NASA POWER Documentation',
          text: 'Detailed information about weather parameters and how to access the data.',
          link: 'https://power.larc.nasa.gov/'
        },
        {
          subtitle: 'MODIS Vegetation Index',
          text: 'Scientific background on how MODIS calculates NDVI and EVI.',
          link: 'https://modis.gsfc.nasa.gov/data/dataprod/mod13.php'
        },
        {
          subtitle: 'AppEEARS Data Tool',
          text: 'Extract and explore NASA satellite data for any location on Earth.',
          link: 'https://appeears.earthdatacloud.nasa.gov/'
        }
      ]
    }
  ]

  const toggleSection = (id) => {
    setExpandedSection(expandedSection === id ? null : id)
  }

  if (!showEducationalPanel) return null

  return (
    <div className="educational-panel-overlay" onClick={() => setShowEducationalPanel(false)}>
      <div className="educational-panel" onClick={(e) => e.stopPropagation()}>
        <div className="panel-header-bar">
          <h2>Learn About NASA Satellite Data</h2>
          <button className="panel-close" onClick={() => setShowEducationalPanel(false)}>✕</button>
        </div>

        <div className="panel-body">
          {sections.map(section => (
            <div key={section.id} className="edu-section">
              <button
                className={`section-header ${expandedSection === section.id ? 'expanded' : ''}`}
                onClick={() => toggleSection(section.id)}
              >
                <span className="section-icon">{section.icon}</span>
                <span className="section-title">{section.title}</span>
                <span className="section-arrow">{expandedSection === section.id ? '▼' : '▶'}</span>
              </button>

              {expandedSection === section.id && (
                <div className="section-content">
                  {section.content.map((item, idx) => (
                    <div key={idx} className="content-item">
                      <h4>{item.subtitle}</h4>
                      <p>{item.text}</p>
                      {item.link && (
                        <a
                          href={item.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="external-link"
                        >
                          Visit Resource →
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="panel-footer-bar">
          <img src="/assets/logos/nasa_logo.png" alt="NASA" className="footer-nasa-logo" />
          <span>All data provided by NASA Earth Observations</span>
        </div>
      </div>
    </div>
  )
}
