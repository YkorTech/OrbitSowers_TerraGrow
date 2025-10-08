import React, { useState, useEffect } from 'react'
import { useGameStore } from '../../stores/gameStore'
import './TutorialModal.css'

/**
 * Tutorial Modal - First Launch
 * Educates users about NASA satellite data
 */
export default function TutorialModal() {
  const showTutorial = useGameStore(state => state.showTutorial)
  const setShowTutorial = useGameStore(state => state.setShowTutorial)

  const [currentSlide, setCurrentSlide] = useState(0)

  useEffect(() => {
    // Check if tutorial was already completed
    const tutorialCompleted = localStorage.getItem('terragrow_tutorial_completed')

    if (!tutorialCompleted) {
      // Show tutorial after 1 second
      setTimeout(() => setShowTutorial(true), 1000)
    }
  }, [setShowTutorial])

  const slides = [
    {
      icon: '🌍',
      title: 'Welcome to TerraGrow Academy',
      description: 'Learn sustainable farming using real NASA satellite data from 2024.',
      highlight: 'Play with historical weather and vegetation data'
    },
    {
      icon: '🛰️',
      title: 'NASA POWER Weather Data',
      description: 'Get real temperature, rainfall, and humidity from NASA satellites.',
      highlight: 'Historical data: Spring & Summer 2024'
    },
    {
      icon: '📊',
      title: 'MODIS Vegetation Monitoring',
      description: 'See how healthy crops were in 2024 using NASA MODIS satellite (250m resolution).',
      highlight: 'NDVI = Normalized Difference Vegetation Index (0.0-1.0)'
    },
    {
      icon: '',
      title: 'Make Smart Decisions',
      description: 'Manage irrigation and fertilizer. Compare your results to real 2024 satellite observations.',
      highlight: 'Ready to start?'
    }
  ]

  const handleNext = () => {
    if (currentSlide < slides.length - 1) {
      setCurrentSlide(currentSlide + 1)
    } else {
      handleComplete()
    }
  }

  const handleSkip = () => {
    handleComplete()
  }

  const handleComplete = () => {
    localStorage.setItem('terragrow_tutorial_completed', 'true')
    setCurrentSlide(0) // Reset for next time
    setShowTutorial(false)
  }

  if (!showTutorial) return null

  const slide = slides[currentSlide]

  return (
    <div className="tutorial-overlay">
      <div className="tutorial-modal">
        <button className="tutorial-skip" onClick={handleSkip}>
          Skip Tutorial
        </button>

        <div className="tutorial-content">
          <div className="tutorial-icon">{slide.icon}</div>

          <h2>{slide.title}</h2>

          <p className="tutorial-description">{slide.description}</p>

          <div className="tutorial-highlight">
            {slide.highlight}
          </div>

          <div className="tutorial-progress">
            {slides.map((_, idx) => (
              <div
                key={idx}
                className={`progress-dot ${idx === currentSlide ? 'active' : ''} ${idx < currentSlide ? 'completed' : ''}`}
              />
            ))}
          </div>
        </div>

        <div className="tutorial-actions">
          {currentSlide > 0 && (
            <button className="btn-tutorial secondary" onClick={() => setCurrentSlide(currentSlide - 1)}>
              ← Back
            </button>
          )}

          <button className="btn-tutorial primary" onClick={handleNext}>
            {currentSlide < slides.length - 1 ? 'Next →' : 'Start Growing!'}
          </button>
        </div>

        <div className="tutorial-footer">
          <img src="/assets/logos/nasa_logo.png" alt="NASA" className="tutorial-nasa-logo" />
          <span>Powered by NASA Earth Observations</span>
        </div>
      </div>
    </div>
  )
}
