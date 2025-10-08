import React, { Suspense } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, useGLTF, Environment } from '@react-three/drei'
import { useGameStore } from '../../stores/gameStore'
import { AVAILABLE_CROPS } from '../../config/crops'
import './CropSelector.css'

/**
 * Crop selector with 3D model preview
 */
export default function CropSelector({ climate }) {
  const selectedCrop = useGameStore(state => state.selectedCrop)
  const setSelectedCrop = useGameStore(state => state.setSelectedCrop)

  // Get recommended crops based on climate
  const recommendedCrops = climate
    ? AVAILABLE_CROPS.filter(crop =>
        crop.climate.some(c => climate.toLowerCase().includes(c))
      )
    : []

  // Check if current crop is recommended
  const isRecommended = recommendedCrops.some(c => c.id === selectedCrop.id)

  return (
    <div className="crop-selector">
      <h3 className="crop-selector-title">Select Your Crop</h3>

      {/* 3D Preview */}
      <div className="crop-preview-3d">
        <Canvas
          camera={{ position: [0, 0.5, 4], fov: 45 }}
          gl={{ antialias: true, alpha: true }}
        >
          <Suspense fallback={null}>
            <CropModel3D crop={selectedCrop} />
            <Environment preset="sunset" />
            <ambientLight intensity={0.6} />
            <directionalLight position={[3, 3, 3]} intensity={1.2} />
            <OrbitControls
              enableZoom={false}
              enablePan={false}
              autoRotate
              autoRotateSpeed={1.5}
              minPolarAngle={Math.PI / 3}
              maxPolarAngle={Math.PI / 2.1}
            />
          </Suspense>
        </Canvas>

        <div className="crop-preview-label">
          <span className="crop-icon">{selectedCrop.icon}</span>
          <span className="crop-name">{selectedCrop.name}</span>
          {!isRecommended && recommendedCrops.length > 0 && (
            <span className="not-recommended-badge">⚠️</span>
          )}
        </div>
      </div>

      {/* Crop Description */}
      <div className="crop-description">
        <p>{selectedCrop.description}</p>
        <div className="crop-stats">
          <span>💧 {selectedCrop.waterNeed}</span>
          <span>🌿 {selectedCrop.nitrogenNeed}</span>
        </div>
      </div>

      {/* Crop Grid Selection - Always show ALL crops */}
      <div className="crop-grid">
        {AVAILABLE_CROPS.map((crop) => {
          const recommended = recommendedCrops.some(c => c.id === crop.id)
          return (
            <button
              key={crop.id}
              className={`crop-card ${selectedCrop.id === crop.id ? 'selected' : ''} ${recommended ? 'recommended' : ''}`}
              onClick={() => setSelectedCrop(crop)}
            >
              <div className="crop-card-icon">{crop.icon}</div>
              <div className="crop-card-name">{crop.name}</div>
              {recommended && <div className="recommended-star">✨</div>}
            </button>
          )
        })}
      </div>

      {climate && recommendedCrops.length > 0 && (
        <div className="climate-recommendation">
          Crops marked with ★ are recommended for <strong>{climate}</strong> climate
          <br />
          <small>You can grow any crop, but recommended ones yield better results!</small>
        </div>
      )}
    </div>
  )
}

/**
 * 3D Model component for selected crop
 */
function CropModel3D({ crop }) {
  const { scene } = useGLTF(crop.model)

  // Adjust scale and position per crop for optimal preview
  let previewScale = crop.scale * 1.0
  let yPosition = -crop.yOffset * 0.6

  // Special adjustments for specific crops
  if (crop.id === 'wheat') {
    previewScale = 0.9
    yPosition = -0.2
  }
  if (crop.id === 'corn') {
    previewScale = 0.85
    yPosition = 0
  }
  if (crop.id === 'sunflower') {
    previewScale = 0.6
    yPosition = -0.1
  }
  if (crop.id === 'tomato') {
    previewScale = 0.8
    yPosition = 0
  }
  if (crop.id === 'lettuce') {
    previewScale = 0.12
    yPosition = -0.1
  }
  if (crop.id === 'rice') {
    previewScale = 0.9
    yPosition = -0.1
  }

  return (
    <group position={[0, yPosition, 0]} scale={previewScale}>
      <primitive object={scene.clone()} />
    </group>
  )
}

// Preload all crop models
AVAILABLE_CROPS.forEach(crop => {
  useGLTF.preload(crop.model)
})
