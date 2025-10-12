import { useState } from 'react'
import './VoiceRecorder.css'

function VoiceRecorder({ onListen, loading }) {
  const [result, setResult] = useState(null)
  const [isRecording, setIsRecording] = useState(false)
  const [history, setHistory] = useState([])
  const [testText, setTestText] = useState('엄마')

  const handleStartRecording = async () => {
    setIsRecording(true)
    setResult(null)

    const timestamp = new Date().toLocaleTimeString('ko-KR')
    const data = await onListen()

    setIsRecording(false)
    setResult(data)

    // Add to history
    const historyItem = {
      timestamp,
      recognized: data?.recognized_text || '',
      triggered: data?.triggered_keywords || [],
      success: data?.success || false
    }
    setHistory(prev => [historyItem, ...prev].slice(0, 5)) // Keep last 5
  }

  const handleTestMode = async () => {
    setIsRecording(true)
    setResult(null)

    const timestamp = new Date().toLocaleTimeString('ko-KR')

    try {
      const response = await fetch(`http://localhost:8000/listen/test?text=${encodeURIComponent(testText)}`, {
        method: 'POST',
      })
      const data = await response.json()

      setIsRecording(false)
      setResult(data)

      // Add to history
      const historyItem = {
        timestamp,
        recognized: data?.recognized_text || '',
        triggered: data?.triggered_keywords || [],
        success: data?.success || false
      }
      setHistory(prev => [historyItem, ...prev].slice(0, 5))
    } catch (error) {
      console.error('Test mode error:', error)
      setIsRecording(false)
    }
  }

  return (
    <div className="voice-recorder card">
      <h2>🎙️ 음성 인식</h2>

      <div className="recorder-controls">
        <button
          className={`record-button ${isRecording ? 'recording' : ''}`}
          onClick={handleStartRecording}
          disabled={loading || isRecording}
        >
          {isRecording ? (
            <>
              <span className="pulse"></span>
              듣는 중... (10초)
            </>
          ) : (
            '🎤 말하기 시작'
          )}
        </button>
      </div>

      {result && (
        <div className="result-box">
          <h3>📋 최신 결과:</h3>
          {result.recognized_text ? (
            <>
              <div className="recognized-text">
                <strong>인식된 텍스트:</strong>
                <div className="text-value">"{result.recognized_text}"</div>
              </div>
              {result.triggered_keywords.length > 0 ? (
                <div className="triggered-keywords">
                  <strong>✅ 트리거된 키워드:</strong>
                  <div className="keyword-badges">
                    {result.triggered_keywords.map((kw, idx) => (
                      <span key={idx} className="keyword-badge success">
                        {kw}
                      </span>
                    ))}
                  </div>
                  {result.action_messages && result.action_messages.length > 0 && (
                    <div className="action-messages">
                      {result.action_messages.map((msg, idx) => (
                        <div key={idx} className="action-message">
                          {msg}
                        </div>
                      ))}
                    </div>
                  )}
                  <div className="success-message">
                    🎉 액션이 실행되었습니다!
                  </div>
                </div>
              ) : (
                <div className="no-match">
                  ⚠️ 매칭된 키워드가 없습니다
                  <div className="hint">등록된 키워드를 다시 확인해보세요</div>
                </div>
              )}
            </>
          ) : (
            <div className="no-recognition">
              <div className="error-icon">❌</div>
              <strong>음성을 인식하지 못했습니다</strong>
              <div className="troubleshooting">
                <p>문제 해결 방법:</p>
                <ul>
                  <li>마이크 권한이 허용되어 있는지 확인</li>
                  <li>더 크고 명확하게 말해보세요</li>
                  <li>조용한 환경에서 시도해보세요</li>
                  <li>마이크와의 거리를 5-10cm로 유지</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      )}

      {history.length > 0 && (
        <div className="history-box">
          <h3>📜 최근 기록 (최대 5개)</h3>
          <div className="history-list">
            {history.map((item, idx) => (
              <div key={idx} className="history-item">
                <div className="history-time">{item.timestamp}</div>
                <div className="history-content">
                  {item.recognized ? (
                    <>
                      <span className="history-text">"{item.recognized}"</span>
                      {item.triggered.length > 0 && (
                        <span className="history-badges">
                          {item.triggered.map((kw, i) => (
                            <span key={i} className="mini-badge">{kw}</span>
                          ))}
                        </span>
                      )}
                    </>
                  ) : (
                    <span className="history-failed">인식 실패</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="test-mode-box">
        <h3>🧪 테스트 모드 (음성 인식 없이 테스트)</h3>
        <div className="test-controls">
          <input
            type="text"
            value={testText}
            onChange={(e) => setTestText(e.target.value)}
            placeholder="테스트할 텍스트 입력"
            disabled={isRecording}
          />
          <button
            className="test-button"
            onClick={handleTestMode}
            disabled={isRecording || !testText}
          >
            🧪 테스트 실행
          </button>
        </div>
        <p className="test-hint">
          마이크 없이 키워드 매칭을 테스트할 수 있습니다
        </p>
      </div>

      <div className="help-text">
        <p><strong>💡 사용 팁:</strong></p>
        <p>1. 버튼을 클릭하세요</p>
        <p>2. 1초 기다린 후 또렷하게 말하세요</p>
        <p>3. 예: "엄-마" (천천히, 명확하게)</p>
      </div>
    </div>
  )
}

export default VoiceRecorder
