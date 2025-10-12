# SoundToAct 🎤

음성으로 액션을 트리거하는 자동화 앱입니다. 특정 키워드를 말하면 자동으로 미리 설정된 동작이 실행됩니다.

예: "엄마" → 엄마에게 전화 걸기, "음악" → 음악 재생, "불꺼" → 불 끄기

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.13+
- Node.js 20+
- PortAudio (macOS의 경우)

### 1. 저장소 이동

```bash
cd /Users/joonho/PyCharmMiscProject/SoundToAct
```

### 2. 백엔드 설치

```bash
# PortAudio 설치 (macOS - 마이크 입력용)
brew install portaudio

# Python 의존성 설치
uv sync
```

### 3. 프론트엔드 설치

```bash
cd frontend
npm install
cd ..
```

### 4. 실행하기

**터미널 1 - 백엔드 서버 실행:**
```bash
uv run python main.py server --reload
```

**터미널 2 - 프론트엔드 실행:**
```bash
cd frontend
npm run dev
```

### 5. 앱 열기

브라우저에서 http://localhost:3000 열기

## 📖 사용 방법

### 웹 인터페이스 사용

1. **키워드 등록하기**
   - 왼쪽 "키워드 관리" 패널에서 키워드 추가
   - 키워드 입력 (예: "엄마")
   - 액션 타입 선택 (call, music, lights)
   - 파라미터 입력 (JSON 형식):
     ```json
     {
       "contact": "엄마",
       "number": "01012345678"
     }
     ```
   - "키워드 추가" 클릭

2. **음성 인식 테스트**
   - "🎤 말하기 시작" 버튼 클릭
   - 1초 기다린 후 명확하게 말하기
   - 인식 결과 및 트리거된 액션 확인

3. **테스트 모드 (마이크 없이 테스트)**
   - 하단 "테스트 모드" 섹션 사용
   - 텍스트 입력 후 "🧪 테스트 실행" 클릭
   - 키워드 매칭 확인

### CLI 모드 (터미널에서 직접 사용)

```bash
# CLI 모드로 실행
uv run python main.py cli

# 프롬프트에 따라 키워드와 액션 등록
# 음성 인식 시작
```

## 🎯 지원하는 액션 타입

### 1. call (전화 걸기)
```json
{
  "contact": "엄마",
  "number": "01012345678"
}
```

### 2. music (음악 재생)
```json
{
  "song": "좋아하는 노래",
  "playlist": "플레이리스트 이름"
}
```

### 3. lights (조명 제어)
```json
{
  "state": "on",
  "room": "거실"
}
```

## 🔧 고급 사용법

### API 직접 호출

백엔드 API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다.

**키워드 등록:**
```bash
curl -X POST "http://localhost:8000/keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "엄마",
    "action_type": "call",
    "action_params": {"contact": "엄마", "number": "01012345678"}
  }'
```

**음성 인식 실행:**
```bash
curl -X POST "http://localhost:8000/listen" \
  -H "Content-Type: application/json" \
  -d '{"timeout": 5, "phrase_time_limit": 5}'
```

**테스트 모드 (음성 인식 없이):**
```bash
curl -X POST "http://localhost:8000/listen/test?text=엄마"
```

### 마이크 문제 해결

마이크가 작동하지 않는 경우:

```bash
# 마이크 진단 스크립트 실행
uv run python test_microphone.py
```

이 스크립트는:
- 사용 가능한 마이크 목록 표시
- 마이크 초기화 테스트
- 주변 소음 레벨 측정
- 오디오 캡처 및 음성 인식 테스트

## 🎤 음성 인식 팁

1. **명확하게 발음**: 천천히, 또렷하게 말하세요
2. **적절한 거리**: 마이크로부터 5-10cm 거리 유지
3. **조용한 환경**: 배경 소음 최소화
4. **짧은 키워드**: 1-2음절 키워드가 가장 잘 인식됩니다
5. **Whisper 사용**: 로컬에서 실행되는 OpenAI Whisper 모델이 Google API보다 더 정확합니다

## 🏗️ 프로젝트 구조

```
SoundToAct/
├── app/
│   ├── api.py              # FastAPI 서버
│   ├── models.py           # Pydantic 모델
│   ├── actions.py          # 액션 핸들러
│   └── voice_listener.py   # 음성 인식 로직
├── frontend/
│   ├── src/
│   │   ├── components/     # React 컴포넌트
│   │   └── App.jsx         # 메인 앱
│   └── package.json
├── tests/                  # 테스트 코드
├── main.py                 # 엔트리 포인트
├── pyproject.toml          # Python 의존성
└── README.md               # 이 파일
```

## 🧪 테스트 실행

```bash
# 모든 테스트 실행
uv run pytest

# 커버리지와 함께 실행
uv run pytest --cov=app --cov-report=html

# 특정 테스트만 실행
uv run pytest tests/test_api.py
```

## 🔍 로그 확인

서버 로그는 실행 중인 터미널에 실시간으로 표시됩니다:

```
🎤 Listening... Speak now!
✓ Audio captured, recognizing...
🔍 Using Whisper (OpenAI) for recognition...
✅ Whisper recognized: '엄마'
Keyword '엄마' detected! Triggering action...
🤙 엄마에게 전화를 걸었습니다.
```

## 🛠️ 개발자 가이드

### 새로운 액션 추가하기

1. `app/actions.py`에 새로운 액션 메서드 추가:

```python
@staticmethod
def my_custom_action(params: dict):
    """Handle custom action"""
    param1 = params.get("param1", "default")
    message = f"🎯 커스텀 액션 실행: {param1}"
    logger.info(message)
    print(message)
    return {"status": "success", "action": "custom", "message": message}
```

2. `_register_default_actions()`에 등록:

```python
def _register_default_actions(self):
    self.register("call", self.call_action)
    self.register("music", self.play_music_action)
    self.register("lights", self.lights_action)
    self.register("custom", self.my_custom_action)  # 추가
```

3. 프론트엔드에서 사용:

```json
{
  "keyword": "커스텀",
  "action_type": "custom",
  "action_params": {"param1": "테스트"}
}
```

## ✅ 구현된 기능

- ✅ 한국어 음성 인식 (Whisper + Google Speech API)
- ✅ 실시간 음성 감지
- ✅ 키워드 기반 액션 트리거
- ✅ RESTful API (FastAPI)
- ✅ React 웹 인터페이스
- ✅ 키워드 동적 등록/삭제
- ✅ 액션 레지스트리 시스템
- ✅ 테스트 모드 (마이크 없이 테스트)
- ✅ 완전한 테스트 커버리지 (81%)

## 📋 향후 개발 계획

- [ ] 실제 전화 API 연동 (Twilio)
- [ ] 음악 플레이어 API 연동 (Spotify)
- [ ] 스마트 홈 API 연동 (HomeKit, SmartThings)
- [ ] 지속적 음성 인식 모드 (백그라운드)
- [ ] 여러 언어 지원
- [ ] 모바일 앱
- [ ] 사용자 인증 시스템
- [ ] 액션 실행 이력 저장

## ❓ 문제 해결

### 음성 인식이 실패하는 경우

1. **마이크 권한 확인**:
   - 시스템 설정 → 개인정보 보호 → 마이크
   - 터미널/브라우저에 권한 허용

2. **Whisper 모델 다운로드 확인**:
   - 첫 실행 시 139MB 모델 자동 다운로드
   - 로그에서 다운로드 진행 상황 확인

3. **마이크 테스트**:
   ```bash
   uv run python test_microphone.py
   ```

### 포트 충돌

백엔드(8000) 또는 프론트엔드(3000) 포트가 이미 사용 중인 경우:

```bash
# 백엔드 다른 포트로 실행
uv run python main.py server --port 8080

# 프론트엔드 vite.config.js에서 포트 수정
```

### soundfile 모듈 오류

Whisper가 작동하지 않고 "No module named 'soundfile'" 오류가 발생하는 경우:

```bash
uv add soundfile
```

## 📄 라이선스

이 프로젝트는 개인 학습 및 개발용입니다.

## 🤝 기여

버그 리포트 및 기능 제안은 GitHub Issues를 통해 제출해주세요.

---

**즐거운 음성 자동화 경험 되세요! 🎉**
