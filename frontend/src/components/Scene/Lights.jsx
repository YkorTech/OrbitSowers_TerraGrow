import React from 'react'

/**
 * Scene lighting setup
 */
export default function Lights() {
  return (
    <>
      {/* Main sunlight (directional) */}
      <directionalLight
        position={[5, 3, 5]}
        intensity={1.5}
        castShadow
        shadow-mapSize={[2048, 2048]}
      />

      {/* Ambient light (soft fill) */}
      <ambientLight intensity={0.3} />

      {/* Hemisphere light (sky + ground) */}
      <hemisphereLight
        color="#ffffff"
        groundColor="#444444"
        intensity={0.5}
        position={[0, 50, 0]}
      />

      {/* Subtle backlight */}
      <pointLight position={[-5, 2, -5]} intensity={0.5} color="#4a90e2" />
    </>
  )
}
