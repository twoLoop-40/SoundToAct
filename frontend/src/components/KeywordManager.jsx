import { useState } from 'react'
import './KeywordManager.css'

const ACTION_TYPES = [
  { value: 'call', label: '📞 전화', params: { contact: '', number: '' } },
  { value: 'music', label: '🎵 음악', params: { song: '', playlist: '' } },
  { value: 'lights', label: '💡 조명', params: { state: 'off', room: '' } },
]

function KeywordManager({ keywords, onAddKeyword, onDeleteKeyword }) {
  const [showForm, setShowForm] = useState(false)
  const [newKeyword, setNewKeyword] = useState('')
  const [actionType, setActionType] = useState('call')
  const [actionParams, setActionParams] = useState({ contact: '', number: '' })

  const handleActionTypeChange = (type) => {
    setActionType(type)
    const selected = ACTION_TYPES.find(a => a.value === type)
    setActionParams(selected.params)
  }

  const handleParamChange = (key, value) => {
    setActionParams(prev => ({ ...prev, [key]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!newKeyword.trim()) return

    await onAddKeyword(newKeyword, actionType, actionParams)
    setNewKeyword('')
    setShowForm(false)
  }

  return (
    <div className="keyword-manager card">
      <div className="section-header">
        <h2>📋 등록된 키워드</h2>
        <button
          className="btn-add"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? '취소' : '+ 추가'}
        </button>
      </div>

      {showForm && (
        <form className="keyword-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>키워드</label>
            <input
              type="text"
              value={newKeyword}
              onChange={(e) => setNewKeyword(e.target.value)}
              placeholder="예: 엄마, 음악, 불꺼"
              required
            />
          </div>

          <div className="form-group">
            <label>액션 타입</label>
            <select
              value={actionType}
              onChange={(e) => handleActionTypeChange(e.target.value)}
            >
              {ACTION_TYPES.map(action => (
                <option key={action.value} value={action.value}>
                  {action.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>액션 파라미터</label>
            {actionType === 'call' && (
              <div className="param-inputs">
                <input
                  type="text"
                  placeholder="연락처 이름"
                  value={actionParams.contact}
                  onChange={(e) => handleParamChange('contact', e.target.value)}
                />
                <input
                  type="text"
                  placeholder="전화번호"
                  value={actionParams.number}
                  onChange={(e) => handleParamChange('number', e.target.value)}
                />
              </div>
            )}
            {actionType === 'music' && (
              <div className="param-inputs">
                <input
                  type="text"
                  placeholder="노래 제목"
                  value={actionParams.song}
                  onChange={(e) => handleParamChange('song', e.target.value)}
                />
                <input
                  type="text"
                  placeholder="플레이리스트"
                  value={actionParams.playlist}
                  onChange={(e) => handleParamChange('playlist', e.target.value)}
                />
              </div>
            )}
            {actionType === 'lights' && (
              <div className="param-inputs">
                <select
                  value={actionParams.state}
                  onChange={(e) => handleParamChange('state', e.target.value)}
                >
                  <option value="on">켜기</option>
                  <option value="off">끄기</option>
                </select>
                <input
                  type="text"
                  placeholder="방 (예: 거실, 침실)"
                  value={actionParams.room}
                  onChange={(e) => handleParamChange('room', e.target.value)}
                />
              </div>
            )}
          </div>

          <button type="submit" className="btn-submit">
            키워드 등록
          </button>
        </form>
      )}

      <div className="keyword-list">
        {keywords.length === 0 ? (
          <p className="empty-message">등록된 키워드가 없습니다</p>
        ) : (
          keywords.map((keyword, idx) => (
            <div key={idx} className="keyword-item">
              <span className="keyword-name">{keyword}</span>
              <button
                className="btn-delete"
                onClick={() => onDeleteKeyword(keyword)}
              >
                🗑️
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default KeywordManager
