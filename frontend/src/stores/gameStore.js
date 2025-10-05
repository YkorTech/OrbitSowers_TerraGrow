import { create } from 'zustand'
import { AVAILABLE_CROPS } from '../config/crops'

/**
 * Global game state management with Zustand
 */
export const useGameStore = create((set) => ({
  // View management
  view: 'globe', // 'globe' | 'transition' | 'game' | 'results'
  setView: (view) => set({ view }),

  // Selected region
  selectedRegion: null,
  setSelectedRegion: (region) => set({ selectedRegion: region }),

  // Selected crop (user choice)
  selectedCrop: AVAILABLE_CROPS[1], // Default to corn (maize)
  setSelectedCrop: (crop) => set({ selectedCrop: crop }),

  // Game state (from Flask API)
  gameState: null,
  sessionId: null,
  setGameState: (state, sessionId) => set({ gameState: state, sessionId }),

  // Harvest results
  harvestResults: null,
  setHarvestResults: (results) => set({ harvestResults: results }),

  // Loading
  isLoading: false,
  loadingMessage: '',
  setLoading: (isLoading, message = '') => set({ isLoading, loadingMessage: message }),

  // Camera animation
  cameraTarget: null,
  setCameraTarget: (target) => set({ cameraTarget: target }),

  // Region data cache
  regionDataCache: {},
  cacheRegionData: (regionId, data) => set((state) => ({
    regionDataCache: { ...state.regionDataCache, [regionId]: data }
  })),

  // Reset game
  resetGame: () => set({
    view: 'globe',
    selectedRegion: null,
    selectedCrop: AVAILABLE_CROPS[1], // Reset to corn
    gameState: null,
    sessionId: null,
    cameraTarget: null,
    harvestResults: null
  })
}))
