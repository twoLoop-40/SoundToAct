import './StatusBar.css'

function StatusBar({ status }) {
  return (
    <div className="status-bar">
      <div className="status-item">
        <span className="status-label">상태:</span>
        <span className={`status-badge ${status.is_listening ? 'listening' : 'idle'}`}>
          {status.is_listening ? '🔴 듣는 중' : '⚪ 대기 중'}
        </span>
      </div>
      <div className="status-item">
        <span className="status-label">등록된 키워드:</span>
        <span className="status-value">{status.registered_keywords?.length || 0}개</span>
      </div>
    </div>
  )
}

export default StatusBar
