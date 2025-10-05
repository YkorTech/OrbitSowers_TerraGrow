import React, { useRef, useEffect } from 'react'
import { useThree, useFrame } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { useSpring, animated, config } from '@react-spring/three'
import { useGameStore } from '../../stores/gameStore'
import { getCameraPositionForRegion } from '../../utils/coordinates'
import * as THREE from 'three'

/**
 * Camera controller with smooth animations
 */
export default function CameraController() {
  const { camera } = useThree()
  const controlsRef = useRef()

  const view = useGameStore(state => state.view)
  const cameraTarget = useGameStore(state => state.cameraTarget)
  const setView = useGameStore(state => state.setView)

  // Default camera positions for different views
  const getCameraPosition = () => {
    if (view === 'globe') {
      // If we have a target region, zoom to it
      if (cameraTarget) {
        const vec3 = getCameraPositionForRegion(
          cameraTarget.lat,
          cameraTarget.lon,
          1.6 // Closer zoom for better visibility
        )
        // Convert Vector3 to array for @react-spring
        return [vec3.x, vec3.y, vec3.z]
      }
      // Default: view whole Earth
      return [0, 0, 3]
    }

    if (view === 'game') {
      // Field view camera position
      return [0, 2, 3]
    }

    if (view === 'results') {
      // Results view - keep globe in background
      return [0, 0, 3]
    }

    return [0, 0, 3]
  }

  const getTargetPosition = () => {
    if (view === 'globe' && cameraTarget) {
      const pos = cameraTarget.position
      // Convert Vector3 to array if needed
      if (pos && typeof pos === 'object' && 'x' in pos) {
        return [pos.x, pos.y, pos.z]
      }
      return pos
    }

    if (view === 'game') {
      return [0, 0, 0] // Look at field center
    }

    return [0, 0, 0] // Look at Earth center
  }

  // Animated camera position with smooth transition
  const { position } = useSpring({
    position: getCameraPosition(),
    config: { ...config.slow, tension: 120, friction: 40 },
    onChange: () => {
      // Update orbit controls target during animation
      if (controlsRef.current) {
        const target = getTargetPosition()
        controlsRef.current.target.set(...target)
        controlsRef.current.update()
      }
    }
  })

  useEffect(() => {
    if (camera && controlsRef.current) {
      const target = getTargetPosition()
      controlsRef.current.target.set(...target)
      controlsRef.current.update()
    }
  }, [view, cameraTarget, camera])

  return (
    <>
      {/* Animated camera */}
      <animated.perspectiveCamera
        position={position}
        fov={45}
        near={0.1}
        far={1000}
      />

      {/* Orbit controls for mouse interaction */}
      <OrbitControls
        ref={controlsRef}
        enablePan={false}
        enableZoom={true}
        enableRotate={true}
        minDistance={1.3}
        maxDistance={view === 'globe' ? 5 : 10}
        rotateSpeed={0.5}
        zoomSpeed={0.8}
      />
    </>
  )
}
