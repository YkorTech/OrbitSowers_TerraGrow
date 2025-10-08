import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import Scene from './components/Scene/Scene'
import LoadingScreen from './components/UI/LoadingScreen'
import Header from './components/UI/Header'
import Footer from './components/UI/Footer'
import TutorialModal from './components/UI/TutorialModal'
import EducationalPanel from './components/UI/EducationalPanel'
import RegionCard from './components/UI/RegionCard'
import GameInterface from './components/UI/GameInterface'
import ResultsScreen from './components/UI/ResultsScreen'
import GlobeControls from './components/UI/GlobeControls'
import { useGameStore } from './stores/gameStore'
import { logger } from './utils/logger'

function App() {
  const { view, selectedRegion, gameState, harvestResults } = useGameStore()

  // Debug logs
  React.useEffect(() => {
    logger.log('App state:', { view, hasGameState: !!gameState, hasHarvestResults: !!harvestResults })
  }, [view, gameState, harvestResults])

  return (
    <div className="app">
      {/* Header always visible */}
      <Header />

      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 0, 3], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
        shadows
      >
        <Scene />
      </Canvas>

      {/* UI Overlays based on current view */}
      {view === 'globe' && !selectedRegion && (
        <GlobeControls />
      )}

      {view === 'globe' && selectedRegion && (
        <RegionCard region={selectedRegion} />
      )}

      {view === 'game' && gameState && (
        <GameInterface gameState={gameState} />
      )}

      {view === 'results' && harvestResults && (
        <ResultsScreen harvestResults={harvestResults} />
      )}

      {view === 'results' && !harvestResults && (
        <div style={{
          position: 'fixed',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          color: 'white',
          fontSize: '2rem',
          zIndex: 9999,
          background: 'rgba(255, 0, 0, 0.8)',
          padding: '20px',
          borderRadius: '10px'
        }}>
          ⚠️ Erreur: harvestResults manquant!
        </div>
      )}

      {/* Footer - visible on globe view */}
      {view === 'globe' && <Footer />}

      {/* Educational Panel - Global access */}
      <EducationalPanel />

      {/* Tutorial Modal - First launch */}
      <TutorialModal />

      {/* Loading screen */}
      <LoadingScreen />
    </div>
  )
}

export default App
