# SoundToAct

음성 인식 기반 자동화 앱 - 특정 키워드를 감지하면 자동으로 행동을 실행합니다.

## 설치

```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -e .
```

**중요:** PyAudio 설치 전에 PortAudio가 필요합니다:
```bash
# macOS
brew install portaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# Windows
# pip가 자동으로 처리합니다
```

## 사용법

```bash
python main.py
```

프로그램이 시작되면:
1. 주변 소음을 측정합니다 (2초)
2. 등록된 키워드를 표시합니다
3. 연속적으로 듣고 키워드를 감지합니다

### 기본 키워드

- "엄마" → 엄마한테 전화
- "음악" → 음악 재생
- "불꺼" → 조명 끄기

## 프로토타입 특징

✅ 한국어 음성 인식 (Google Speech API)
✅ 실시간 연속 청취
✅ 키워드 기반 액션 트리거
✅ 주변 소음 자동 보정
✅ 쉬운 키워드-액션 등록 시스템

## 다음 단계

- [ ] FastAPI 백엔드 추가
- [ ] React 프론트엔드 개발
- [ ] 실제 전화 통합 (Twilio)
- [ ] 데이터베이스 (사용자/액션 저장)
- [ ] WebSocket 실시간 통신
- [ ] 더 정확한 음성 인식 (Whisper)