import React, { useState } from 'react'
import { Html } from '@react-three/drei'
import { latLonToVector3 } from '../../utils/coordinates'
import { useGameStore } from '../../stores/gameStore'

// Popular regions (from backend config)
const POPULAR_REGIONS = [
  { id: 'yaounde', name: 'Yaoundé', lat: 3.87, lon: 11.52, flag: '🇨🇲', climate: 'Tropical' },
  { id: 'maroua', name: 'Maroua', lat: 10.6, lon: 14.3, flag: '🇨🇲', climate: 'Sahélien' },
  { id: 'douala', name: 'Douala', lat: 4.05, lon: 9.7, flag: '🇨🇲', climate: 'Équatorial' },
  { id: 'montreal', name: 'Montréal', lat: 45.5, lon: -73.6, flag: '🇨🇦', climate: 'Continental' },
  { id: 'nairobi', name: 'Nairobi', lat: -1.28, lon: 36.82, flag: '🇰🇪', climate: 'Tropical' },
  { id: 'kano', name: 'Kano', lat: 12.0, lon: 8.52, flag: '🇳🇬', climate: 'Sahélien' },
  { id: 'addis', name: 'Addis-Abeba', lat: 9.03, lon: 38.74, flag: '🇪🇹', climate: 'Montagne' },
  { id: 'punjab', name: 'Punjab', lat: 30.73, lon: 76.78, flag: '🇮🇳', climate: 'Subtropical' },
  { id: 'saopaulo', name: 'São Paulo', lat: -23.55, lon: -46.63, flag: '🇧🇷', climate: 'Subtropical' },
  { id: 'iowa', name: 'Iowa', lat: 41.88, lon: -93.1, flag: '🇺🇸', climate: 'Continental' },
  { id: 'beauce', name: 'Beauce', lat: 48.44, lon: 1.48, flag: '🇫🇷', climate: 'Océanique' },
  { id: 'dhaka', name: 'Dhaka', lat: 23.81, lon: 90.41, flag: '🇧🇩', climate: 'Tropical' },
  { id: 'pampas', name: 'Pampas', lat: -34.6, lon: -58.38, flag: '🇦🇷', climate: 'Tempéré' },
  { id: 'prairies', name: 'Prairies', lat: 50.45, lon: -104.62, flag: '🇨🇦', climate: 'Continental' },
  { id: 'garoua', name: 'Garoua', lat: 9.3, lon: 13.4, flag: '🇨🇲', climate: 'Sahélien' }
]

/**
 * Display clickable markers for popular regions on the globe
 */
export default function RegionMarkers() {
  const setSelectedRegion = useGameStore(state => state.setSelectedRegion)
  const setCameraTarget = useGameStore(state => state.setCameraTarget)
  const showEducationalPanel = useGameStore(state => state.showEducationalPanel)
  const showTutorial = useGameStore(state => state.showTutorial)
  const [hoveredId, setHoveredId] = useState(null)

  // Hide labels when any modal is open
  const hideLabels = showEducationalPanel || showTutorial

  const handleRegionClick = (region) => {
    const position = latLonToVector3(region.lat, region.lon, 1)

    // Set selected region
    setSelectedRegion({
      name: region.name,
      lat: region.lat,
      lon: region.lon,
      position: position,
      climate: region.climate,
      flag: region.flag
    })

    // Set camera target for zoom animation
    setCameraTarget({
      position: position,
      lat: region.lat,
      lon: region.lon
    })
  }

  return (
    <group>
      {POPULAR_REGIONS.map(region => {
        const position = latLonToVector3(region.lat, region.lon, 1.05)
        const isHovered = hoveredId === region.id

        return (
          <mesh
            key={region.id}
            position={position}
            onClick={(e) => {
              e.stopPropagation()
              handleRegionClick(region)
            }}
            onPointerOver={(e) => {
              e.stopPropagation()
              setHoveredId(region.id)
              document.body.style.cursor = 'pointer'
            }}
            onPointerOut={() => {
              setHoveredId(null)
              document.body.style.cursor = 'default'
            }}
          >
            {/* Larger clickable sphere */}
            <sphereGeometry args={[isHovered ? 0.025 : 0.018, 16, 16]} />
            <meshStandardMaterial
              color={isHovered ? "#4ade80" : "#ff6b35"}
              emissive={isHovered ? "#4ade80" : "#ff6b35"}
              emissiveIntensity={isHovered ? 0.8 : 0.5}
              transparent
              opacity={isHovered ? 1 : 0.9}
            />

            {/* Label */}
            {!hideLabels && (
              <Html
                distanceFactor={0.5}
                style={{
                  pointerEvents: 'none',
                  userSelect: 'none',
                  fontSize: isHovered ? '12px' : '10px',
                  color: 'white',
                  background: isHovered ? 'rgba(16, 185, 129, 0.9)' : 'rgba(0, 0, 0, 0.7)',
                  padding: isHovered ? '4px 8px' : '2px 6px',
                  borderRadius: '4px',
                  whiteSpace: 'nowrap',
                  fontWeight: isHovered ? '600' : '400',
                  transition: 'all 0.2s ease',
                  border: isHovered ? '1px solid rgba(74, 222, 128, 0.5)' : 'none',
                  zIndex: 1
                }}
              >
                {region.flag} {region.name}
              </Html>
            )}
          </mesh>
        )
      })}
    </group>
  )
}

export { POPULAR_REGIONS }
