import React, { useRef, useMemo, Suspense } from 'react'
import { useFrame, useLoader } from '@react-three/fiber'
import { TextureLoader, RepeatWrapping } from 'three'
import { useGLTF, Sky, Text, Environment } from '@react-three/drei'
import { useGameStore } from '../../stores/gameStore'
import * as THREE from 'three'

/**
 * Enhanced 3D field scene with realistic textures and models
 */
export default function FieldScene() {
  const gameState = useGameStore(state => state.gameState)
  const ndvi = gameState?.crop?.ndvi || 0.15

  return (
    <Suspense fallback={null}>
      <group position={[0, -0.8, 0]}>
        {/* Enhanced ground with textures */}
        <Ground />

        {/* Crop plants (wheat or corn) */}
        <CropField ndvi={ndvi} />

        {/* Atmospheric elements */}
        <Atmosphere />

        {/* NDVI indicator */}
        <Text
          position={[0, 2, 0]}
          fontSize={0.2}
          color={ndvi > 0.6 ? '#10b981' : ndvi > 0.3 ? '#f59e0b' : '#ef4444'}
          anchorX="center"
          anchorY="middle"
          outlineWidth={0.02}
          outlineColor="#000000"
        >
          NDVI: {ndvi.toFixed(2)}
        </Text>
      </group>
    </Suspense>
  )
}

/**
 * Enhanced ground with realistic soil textures
 */
function Ground() {
  // Load soil textures
  const [soilDiffuse, soilNormal, grassDiffuse] = useLoader(TextureLoader, [
    '/textures/brown_mud_02_diff_1k.jpg',
    '/textures/brown_mud_02_nor_dx_1k.jpg',
    '/textures/leafy_grass_diff_1k.jpg'
  ])

  // Configure texture repeat and wrapping
  useMemo(() => {
    [soilDiffuse, soilNormal, grassDiffuse].forEach(texture => {
      texture.wrapS = texture.wrapT = RepeatWrapping
      texture.repeat.set(4, 4)
    })
  }, [soilDiffuse, soilNormal, grassDiffuse])

  return (
    <group>
      {/* Main soil plane with displacement */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[8, 8, 128, 128]} />
        <meshStandardMaterial
          map={soilDiffuse}
          normalMap={soilNormal}
          normalScale={[0.5, 0.5]}
          roughness={0.9}
          metalness={0.1}
          displacementMap={soilNormal}
          displacementScale={0.05}
        />
      </mesh>

      {/* Grass patches around the field */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]} receiveShadow>
        <planeGeometry args={[9, 9, 64, 64]} />
        <meshStandardMaterial
          map={grassDiffuse}
          transparent
          opacity={0.3}
          roughness={0.95}
          alphaTest={0.1}
        />
      </mesh>
    </group>
  )
}

/**
 * Crop field with 3D models (based on user selection)
 */
function CropField({ ndvi }) {
  const plantsRef = useRef()
  const selectedCrop = useGameStore(state => state.selectedCrop)

  // Load the selected crop model
  const cropModel = useGLTF(selectedCrop.model)
  const yOffset = selectedCrop.yOffset
  const cropScale = selectedCrop.scale

  // Generate plant positions in a grid
  const plantPositions = useMemo(() => {
    const positions = []
    const rows = 4
    const cols = 4
    const spacing = 1.2

    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const x = (col - cols / 2 + 0.5) * spacing
        const z = (row - rows / 2 + 0.5) * spacing

        // Add random offset for natural look
        const offsetX = (Math.random() - 0.5) * 0.3
        const offsetZ = (Math.random() - 0.5) * 0.3

        positions.push({
          position: [x + offsetX, z + offsetZ],
          rotation: Math.random() * Math.PI * 2,
          scale: 0.8 + Math.random() * 0.4 // Random scale variation
        })
      }
    }
    return positions
  }, [])

  // Wind animation
  useFrame(({ clock }) => {
    if (plantsRef.current) {
      plantsRef.current.children.forEach((plant, i) => {
        const time = clock.getElapsedTime()
        const offset = i * 0.1
        plant.rotation.z = Math.sin(time * 0.8 + offset) * 0.08
        plant.rotation.x = Math.cos(time * 0.5 + offset) * 0.05
      })
    }
  })

  // Health color tint
  const healthColor = useMemo(() => {
    if (ndvi > 0.6) return new THREE.Color(0.9, 1.0, 0.9) // Healthy green tint
    if (ndvi > 0.3) return new THREE.Color(1.0, 0.95, 0.8) // Yellowish
    return new THREE.Color(1.0, 0.85, 0.8) // Reddish brown
  }, [ndvi])

  return (
    <group ref={plantsRef}>
      {plantPositions.map((plant, i) => (
        <group
          key={i}
          position={[plant.position[0], yOffset, plant.position[1]]}
          rotation={[0, plant.rotation, 0]}
          scale={plant.scale * cropScale * (0.5 + ndvi * 0.8)} // Scale based on health and crop config
        >
          <primitive object={cropModel.scene.clone()} />
          {/* Add color tint overlay */}
          <mesh scale={0.01}>
            <sphereGeometry args={[1, 8, 8]} />
            <meshBasicMaterial color={healthColor} transparent opacity={0.2} />
          </mesh>
        </group>
      ))}
    </group>
  )
}

/**
 * Atmospheric elements (sky, fog, lighting)
 */
function Atmosphere() {
  return (
    <>
      {/* Sky background */}
      <Sky
        distance={450000}
        sunPosition={[5, 1, 8]}
        inclination={0.6}
        azimuth={0.25}
      />

      {/* Fog for depth */}
      <fog attach="fog" args={['#d4e5f7', 10, 50]} />

      {/* Lighting setup */}
      <ambientLight intensity={0.4} />
      <directionalLight
        position={[5, 5, 5]}
        intensity={1.2}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={20}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />
      <hemisphereLight args={['#87ceeb', '#8B4513', 0.6]} />

      {/* Environment map for reflections */}
      <Environment preset="sunset" />
    </>
  )
}

// Preload all models - handled by crops config now
