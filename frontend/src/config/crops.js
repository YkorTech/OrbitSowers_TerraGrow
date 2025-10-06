/**
 * Available crops configuration
 * Each crop has its 3D model, display properties, and characteristics
 */

export const AVAILABLE_CROPS = [
  {
    id: 'wheat',
    name: 'Wheat',
    nameEn: 'Wheat',
    icon: '🌾',
    model: '/models/wheat.glb',
    scale: 1.0,
    yOffset: 0.5,
    description: 'Cold-resistant cereal crop (optimal 18°C)',
    climate: ['continental', 'temperate'],
    waterNeed: 'Medium (450mm/season)',
    nitrogenNeed: 'Medium (120 kg/ha)',
    color: '#F4E4C1'
  },
  {
    id: 'corn',
    name: 'Corn',
    nameEn: 'Corn',
    icon: '🌽',
    model: '/models/corn.glb',
    scale: 1.0,
    yOffset: 0,
    description: 'Versatile crop for warm climates (optimal 25°C)',
    climate: ['tropical', 'subtropical', 'temperate'],
    waterNeed: 'High (500mm/season)',
    nitrogenNeed: 'High (150 kg/ha)',
    color: '#FFD700'
  },
  {
    id: 'rice',
    name: 'Rice',
    nameEn: 'Rice',
    icon: '🍚',
    model: '/models/rice_plant.glb',
    scale: 1.0,
    yOffset: 0.2,
    description: 'Aquatic tropical crop, high water needs (optimal 28°C)',
    climate: ['tropical', 'subtropical'],
    waterNeed: 'Very High (700mm/season)',
    nitrogenNeed: 'Medium (130 kg/ha)',
    color: '#E8F5E9'
  },
  {
    id: 'sunflower',
    name: 'Sunflower',
    nameEn: 'Sunflower',
    icon: '🌻',
    model: '/models/sunflower.glb',
    scale: 0.8,
    yOffset: 0.3,
    description: 'Drought-resistant oilseed crop (optimal 22°C)',
    climate: ['temperate', 'continental', 'subtropical'],
    waterNeed: 'Low (350mm/season)',
    nitrogenNeed: 'Low (90 kg/ha)',
    color: '#FFA726'
  },
  {
    id: 'tomato',
    name: 'Tomato',
    nameEn: 'Tomato',
    icon: '🍅',
    model: '/models/tomato.glb',
    scale: 0.9,
    yOffset: 0.1,
    description: 'Intensive market garden crop (optimal 24°C)',
    climate: ['subtropical', 'temperate', 'tropical'],
    waterNeed: 'Very High (550mm/season)',
    nitrogenNeed: 'Very High (160 kg/ha)',
    color: '#FF6B6B'
  },
  {
    id: 'lettuce',
    name: 'Lettuce',
    nameEn: 'Lettuce',
    icon: '🥬',
    model: '/models/lettuce.glb',
    scale: 1.0,
    yOffset: 0.05,
    description: 'Fast-growing vegetable, prefers cool weather (optimal 16°C)',
    climate: ['temperate', 'continental'],
    waterNeed: 'Low (300mm/season)',
    nitrogenNeed: 'Low (80 kg/ha)',
    color: '#81C784'
  }
]

/**
 * Get crop by ID
 */
export function getCropById(cropId) {
  return AVAILABLE_CROPS.find(crop => crop.id === cropId) || AVAILABLE_CROPS[0]
}

/**
 * Get recommended crops for a climate
 */
export function getRecommendedCrops(climate) {
  if (!climate) return AVAILABLE_CROPS

  const climateLower = climate.toLowerCase()
  return AVAILABLE_CROPS.filter(crop =>
    crop.climate.some(c => climateLower.includes(c))
  )
}

/**
 * Get default crop for a climate
 */
export function getDefaultCrop(climate) {
  const recommended = getRecommendedCrops(climate)
  return recommended[0] || AVAILABLE_CROPS[0]
}
