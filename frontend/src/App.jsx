import { useState, useEffect } from 'react'
import './App.css'
import VoiceRecorder from './components/VoiceRecorder'
import KeywordManager from './components/KeywordManager'
import StatusBar from './components/StatusBar'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [keywords, setKeywords] = useState([])
  const [status, setStatus] = useState({ is_listening: false, registered_keywords: [] })
  const [loading, setLoading] = useState(false)

  // Fetch keywords and status
  const fetchKeywords = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/keywords`)
      const data = await response.json()
      setKeywords(data)
    } catch (error) {
      console.error('Failed to fetch keywords:', error)
    }
  }

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/status`)
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      console.error('Failed to fetch status:', error)
    }
  }

  useEffect(() => {
    fetchKeywords()
    fetchStatus()
    // Refresh every 5 seconds
    const interval = setInterval(() => {
      fetchStatus()
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleListen = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/listen`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ timeout: 10, phrase_time_limit: 10 })
      })
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Failed to listen:', error)
      return null
    } finally {
      setLoading(false)
    }
  }

  const handleAddKeyword = async (keyword, actionType, actionParams) => {
    try {
      const response = await fetch(`${API_BASE_URL}/keywords`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keyword,
          action_type: actionType,
          action_params: actionParams
        })
      })
      if (response.ok) {
        await fetchKeywords()
        await fetchStatus()
      }
    } catch (error) {
      console.error('Failed to add keyword:', error)
    }
  }

  const handleDeleteKeyword = async (keyword) => {
    try {
      const response = await fetch(`${API_BASE_URL}/keywords/${keyword}`, {
        method: 'DELETE'
      })
      if (response.ok) {
        await fetchKeywords()
        await fetchStatus()
      }
    } catch (error) {
      console.error('Failed to delete keyword:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎤 SoundToAct</h1>
        <p className="subtitle">음성으로 작업을 트리거하세요</p>
      </header>

      <div className="container">
        <StatusBar status={status} />

        <div className="main-content">
          <VoiceRecorder
            onListen={handleListen}
            loading={loading}
          />

          <KeywordManager
            keywords={keywords}
            onAddKeyword={handleAddKeyword}
            onDeleteKeyword={handleDeleteKeyword}
          />
        </div>
      </div>
    </div>
  )
}

export default App