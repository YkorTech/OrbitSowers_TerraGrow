import React, { Suspense } from 'react'
import { Environment, Stars } from '@react-three/drei'
import EarthGlobe from './EarthGlobe'
import Satellite from './Satellite'
import CameraController from './CameraController'
import FieldScene from '../Field/FieldScene'
import Lights from './Lights'
import { useGameStore } from '../../stores/gameStore'

/**
 * Main 3D Scene - switches between globe view and field view
 */
export default function Scene() {
  const { view } = useGameStore()

  return (
    <Suspense fallback={null}>
      {/* Lighting */}
      <Lights />

      {/* Star background */}
      <Stars
        radius={300}
        depth={60}
        count={5000}
        factor={7}
        saturation={0}
        fade
      />

      {/* Camera controller */}
      <CameraController />

      {/* Conditional scene rendering based on view */}
      {view === 'globe' && (
        <>
          <EarthGlobe />
          <Satellite />
        </>
      )}

      {view === 'game' && (
        <FieldScene />
      )}

      {view === 'results' && (
        <FieldScene />
      )}

      {/* Environment lighting (HDR) */}
      <Environment preset="sunset" />
    </Suspense>
  )
}
