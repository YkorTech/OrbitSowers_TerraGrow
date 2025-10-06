import { useState, useEffect } from 'react'
import { initializeGame, performAction, getHarvestResults } from '../utils/apiClient'

/**
 * Hook to manage NASA data fetching and game initialization
 */
export function useNASAData(lat, lon, cropId = null) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (lat === null || lon === null) return

    setLoading(true)
    setError(null)

    // Pass crop ID to backend
    initializeGame(lat, lon, cropId)
      .then(response => {
        setData(response)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [lat, lon, cropId])

  return { data, loading, error }
}

/**
 * Hook to manage game actions
 */
export function useGameActions(sessionId) {
  const [isProcessing, setIsProcessing] = useState(false)

  const submitAction = async (irrigation, fertilizer) => {
    if (!sessionId) {
      throw new Error('No active game session')
    }

    setIsProcessing(true)

    try {
      const result = await performAction(sessionId, irrigation, fertilizer)
      setIsProcessing(false)
      return result
    } catch (error) {
      setIsProcessing(false)
      throw error
    }
  }

  const harvest = async () => {
    if (!sessionId) {
      throw new Error('No active game session')
    }

    setIsProcessing(true)

    try {
      const results = await getHarvestResults(sessionId)
      setIsProcessing(false)
      return results
    } catch (error) {
      setIsProcessing(false)
      throw error
    }
  }

  return {
    submitAction,
    harvest,
    isProcessing
  }
}
