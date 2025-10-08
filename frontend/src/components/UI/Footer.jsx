import React from 'react'
import './Footer.css'

/**
 * Footer Component
 * Displays team logo, NASA Space Apps logo, and attribution
 */
export default function Footer() {
  return (
    <footer className="app-footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>TerraGrow Academy</h4>
          <p>Learn sustainable farming with NASA satellite data</p>
        </div>

        <div className="footer-logos">
          <a
            href="https://www.spaceappschallenge.org/"
            target="_blank"
            rel="noopener noreferrer"
            className="logo-link"
          >
            <img
              src="/assets/logos/space_apps_logo.png"
              alt="NASA Space Apps Challenge"
              className="footer-logo space-apps-logo"
            />
          </a>

          <div className="team-logo">
            <img
              src="/assets/logos/orbitsowers_logo.png"
              alt="OrbitSowers Team"
              className="footer-logo team-logo-img"
            />
          </div>
        </div>

        <div className="footer-section">
          <h4>Data Sources</h4>
          <ul className="footer-links">
            <li>
              <a href="https://power.larc.nasa.gov/" target="_blank" rel="noopener noreferrer">
                NASA POWER
              </a>
            </li>
            <li>
              <a href="https://modis.gsfc.nasa.gov/" target="_blank" rel="noopener noreferrer">
                MODIS Terra
              </a>
            </li>
            <li>
              <a href="https://appeears.earthdatacloud.nasa.gov/" target="_blank" rel="noopener noreferrer">
                AppEEARS
              </a>
            </li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>
          Built for NASA Space Apps Challenge 2025 • Team OrbitSowers
        </p>
        <p className="data-attribution">
          All satellite data provided by NASA Earth Observations
        </p>
      </div>
    </footer>
  )
}
