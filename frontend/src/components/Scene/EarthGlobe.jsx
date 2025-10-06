import React, { useRef, useState } from 'react'
import { useFrame, useLoader } from '@react-three/fiber'
import { TextureLoader } from 'three'
import * as THREE from 'three'
import RegionMarkers from './RegionMarkers'

/**
 * Interactive Earth Globe - click on region markers to select
 */
export default function EarthGlobe() {
  const earthGroupRef = useRef() // Group containing Earth, clouds, and markers
  const meshRef = useRef()
  const cloudsRef = useRef()
  const [hovered, setHovered] = useState(false)

  // Load Earth textures
  const [dayMap, nightMap, cloudsMap] = useLoader(TextureLoader, [
    '/textures/2k_earth_daymap.jpg',
    '/textures/2k_earth_nightmap.jpg',
    '/textures/2k_earth_clouds.jpg'
  ])

  // Slow auto-rotation (entire Earth group including markers)
  useFrame(() => {
    if (earthGroupRef.current) {
      earthGroupRef.current.rotation.y += 0.0005
    }
  })

  // Note: Click handler removed - users must click on region markers or use geolocation
  // This prevents clicking on oceans or invalid areas

  return (
    <group ref={earthGroupRef}>
      {/* Main Earth sphere */}
      <mesh
        ref={meshRef}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[1, 64, 64]} />

        {/* Day/Night material */}
        <meshStandardMaterial
          map={dayMap}
          emissiveMap={nightMap}
          emissive={new THREE.Color(0x444444)}
          emissiveIntensity={hovered ? 0.3 : 0.2}
          roughness={0.7}
          metalness={0.1}
        />
      </mesh>

      {/* Clouds layer (slightly larger sphere) */}
      <mesh ref={cloudsRef}>
        <sphereGeometry args={[1.01, 64, 64]} />
        <meshStandardMaterial
          map={cloudsMap}
          transparent
          opacity={0.4}
          depthWrite={false}
        />
      </mesh>

      {/* Region markers - will rotate with Earth */}
      <RegionMarkers />
    </group>
  )
}
