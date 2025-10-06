import React, { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useGLTF } from '@react-three/drei'

/**
 * Satellite orbiting Earth
 */
export default function Satellite() {
  const satelliteRef = useRef()

  // Load satellite model
  const { scene } = useGLTF('/models/satellite.glb')

  // Orbit animation
  useFrame(({ clock }) => {
    if (!satelliteRef.current) return

    const t = clock.getElapsedTime()

    // Circular orbit around Earth
    const radius = 1.5
    const speed = 0.3

    satelliteRef.current.position.x = Math.cos(t * speed) * radius
    satelliteRef.current.position.z = Math.sin(t * speed) * radius
    satelliteRef.current.position.y = 0.3

    // Rotate satellite to face forward in orbit
    satelliteRef.current.rotation.y = -t * speed + Math.PI / 2

    // Slight tilt (realistic satellite attitude)
    satelliteRef.current.rotation.x = 0.1
  })

  return (
    <group ref={satelliteRef}>
      <primitive
        object={scene.clone()}
        scale={0.015} // Increased scale for better visibility
      />
      {/* Point light to make satellite more visible */}
      <pointLight position={[0, 0, 0]} intensity={0.3} color="#ffffff" distance={1.5} />
    </group>
  )
}

// Preload model
useGLTF.preload('/models/satellite.glb')
