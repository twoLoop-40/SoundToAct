# SoundToAct

**음성으로 트리거하는 자동화 시스템**

- **발표자**: TBD
- **대상**: 선생님, 개발자
- **시간**: 10-15분
- **슬라이드 수**: 12

---

## Slide 1: 타이틀

*Voice-Triggered Automation System*

**Layout**: SingleColumn

```text
SoundToAct
음성으로 트리거하는 자동화 시스템
```

```text
Voice-Triggered Automation System
```

**Visuals**:
- 음성 웨이브폼 배경 이미지
- 마이크 아이콘
- 미니멀한 그라데이션

**Estimated Time**: 30s

---

## Slide 2: 문제 정의

**Layout**: ThreeColumn

**Content**:
1. **일상의 반복 작업**
- "엄마에게 전화해야지..." → 연락처 찾기 → 전화 걸기
- "음악 틀어야지..." → 앱 열기 → 검색 → 재생
2. **기존 솔루션의 한계**
- Siri/Google Assistant: 제한된 통합, 커스터마이징 어려움
- IFTTT/Zapier: 음성 트리거 부재, 복잡한 설정
3. **우리의 접근**
- 🎯 단순한 키워드로 즉시 실행
- 🔧 완전한 커스터마이징
- 🔒 타입 안전성 보장

```text
왜 음성 자동화인가?
```

**Visuals**:
- 3개의 컬럼 레이아웃 (문제 / 기존 방식 / 우리 방식)
- 아이콘: 🎤 💡 ⚙️

**Estimated Time**: 33s

---

## Slide 3: 데모 시나리오

**Layout**: FullScreenDemo

**Content**:
👤 사용자: "엄마"
🤖 시스템: [음성 인식] → [키워드 매칭] → [전화 걸기 액션]
📱 결과: 엄마에게 자동 전화 연결
👤 사용자: "음악"
🤖 시스템: [Whisper 인식] → [음악 재생 액션]
🎵 결과: 좋아하는 플레이리스트 재생
👤 사용자: "불꺼"
🤖 시스템: [Google Speech] → [스마트홈 연동]
💡 결과: 전체 조명 OFF

```text
실제 사용 시나리오
```

```text
👤 사용자: "엄마"
🤖 시스템: [음성 인식] → [키워드 매칭] → [전화 걸기 액션]
📱 결과: 엄마에게 자동 전화 연결
```

```text
👤 사용자: "음악"
🤖 시스템: [Whisper 인식] → [음악 재생 액션]
🎵 결과: 좋아하는 플레이리스트 재생
```

```text
👤 사용자: "불꺼"
🤖 시스템: [Google Speech] → [스마트홈 연동]
💡 결과: 전체 조명 OFF
```

**Visuals**:
- 플로우차트 스타일
- 각 단계별 아이콘
- 시간 흐름 표시 (타임라인)

**Estimated Time**: 35s

---

## Slide 4: 핵심 기능

**Layout**: FourQuadrant

```text
핵심 기능
```

**Visuals**:
- 4개의 동일한 크기 박스
- 각 박스마다 대표 아이콘
- 간단한 수치/통계

**Estimated Time**: 37s

---

## Slide 5: 기술 아키텍처 (High-Level)

**Layout**: SingleColumn

```text
시스템 아키텍처
```

```text
┌─────────────┐
│   사용자     │ "엄마"
└──────┬──────┘
       │ 음성
       ▼
┌─────────────────┐
│  VoiceListener  │ 🎤
│  - Whisper      │
│  - Google API   │
└────────┬────────┘
         │ 인식된 텍스트
         ▼
┌─────────────────┐
│ Keyword Matcher │ 🔍
│ (case-insensitive)│
└────────┬────────┘
         │ 매칭된 키워드
         ▼
┌─────────────────┐
│ ActionRegistry  │ ⚙️
│ - Call          │
│ - Music         │
│ - Lights        │
└────────┬────────┘
         │ 실행
         ▼
┌─────────────────┐
│   액션 실행     │ ✅
└─────────────────┘
```

**Visuals**:
- 상하 플로우 다이어그램
- 각 컴포넌트 박스
- 화살표로 데이터 흐름 표시

**Estimated Time**: 36s

---

## Slide 6: 기술 스택

**Layout**: ThreeColumn

```text
기술 스택
```

**Visuals**:
- 3개 컬럼
- 기술 로고 아이콘
- 버전 정보 표시

**Estimated Time**: 30s

---

## Slide 7: API & 통합

**Layout**: SingleColumn

```text
RESTful API
```

```text
POST   /keywords               키워드 등록
GET    /keywords               키워드 목록
DELETE /keywords/{keyword}     키워드 삭제

POST   /listen                 음성 인식 (1회)
POST   /listen/test?text=엄마  테스트 (마이크 없이)

GET    /status                 시스템 상태
```

```json
// POST /keywords
{
  "keyword": "엄마",
  "action_type": "call",
  "action_params": {
    "contact": "엄마",
    "number": "01012345678"
  }
}

// Response
{
  "keyword": "엄마",
  "action_type": "call",
  "is_active": true
}
```

**Visuals**:
- 엔드포인트 리스트
- JSON 예제
- API 문서 스크린샷

**Estimated Time**: 34s

---

## Slide 8: 데모 & 라이브 코딩

**Layout**: FullScreenDemo

```text
🎬 라이브 데모
```

**Visuals**:
- 스크린샷/비디오
- 터미널 화면
- 브라우저 UI

**Estimated Time**: 37s

---

## Slide 9: 성능 & 통계

**Layout**: SingleColumn

```text
성능 지표
```

**Visuals**:
- 막대 그래프
- 숫자 강조
- 깔끔한 테이블

**Estimated Time**: 33s

---

## Slide 10: 확장 가능성

**Layout**: ThreeColumn

```text
확장 시나리오
```

```python
# 커스텀 액션 추가
def custom_action(params: dict) -> ActionResult:
    name = params.get("name", "사용자")
    return ActionResult(
        status="success",
        action_type="custom",
        message=f"안녕하세요 {name}님"
    )

# 액션 등록
listener.register_action("custom", custom_action)
```

**Visuals**:
- 3개 컬럼
- 각 방향별 아이콘
- 코드 예제

**Estimated Time**: 40s

---

## Slide 11: 향후 로드맵

**Layout**: SingleColumn

```text
로드맵
```

**Visuals**:
- 타임라인 그래프
- 각 항목 상태 표시 (✅/🔄/📋)
- 마일스톤 강조

**Estimated Time**: 39s

---

## Slide 12: Q&A

**Layout**: FullScreenDemo

```text
Q & A
```

```text
질문이 있으신가요?
Questions?
```

**Visuals**:
- 미니멀 디자인
- 큰 폰트
- QR 코드
- 연락처 정보

**Estimated Time**: 30s

---

