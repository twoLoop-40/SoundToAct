#!/usr/bin/env python3
"""
Generate presentation JSON from Idris specification

This script manually converts the Idris slide definitions
into Python data structures and exports to JSON.

NEW DESIGN: Story-driven, visual-focused presentation
- Minimal text
- Maximum visuals
- Motivation, impact, purpose over technical details
"""

import json
from pathlib import Path


# Slide definitions (mirroring Presentation.idr - 10 slides, story-driven)
SLIDES = [
    # Slide 1: Title - 깔끔하고 임팩트 있게
    {
        "number": 1,
        "title": "SoundToAct",
        "subtitle": "말 한마디로 움직이는 세상",
        "layout": "TitleSlide",
        "content": [
            "고등학생 개발자 [이름]",
            "2025년 10월"
        ],
        "code_blocks": [],
        "visuals": [
            "🎤 음성 인식 기반 자동화 시스템",
            "Python + SpeechRecognition + 자동화 라이브러리"
        ],
        "speaker_notes": "발표자 가이드: 인사 후 프로젝트명 강조. 'Sound(소리)'가 'Act(행동)'으로 바로 변환되는 개념 설명. 음성만으로 기기를 제어하는 시스템임을 명확히 전달.",
        "estimated_time": 45
    },
    # Slide 2: My Daily Life - 스토리로 공감 유도
    {
        "number": 2,
        "title": "나의 아침",
        "subtitle": None,
        "layout": "SingleColumn",
        "content": [
            "⏰ 7:00 AM - 일어나자마자",
            "",
            "\"엄마한테 전화해야 하는데...\""
        ],
        "code_blocks": [],
        "visuals": [
            "[문제 상황]",
            "1. 침대에서 폰 찾기 (20초)",
            "2. 잠금 해제 (10초)",
            "3. 연락처 앱 열기 (15초)",
            "4. '엄마' 검색 (20초)",
            "5. 통화 버튼 터치 (5초)",
            "⏱ 총 소요 시간: ~2분 + 귀찮음"
        ],
        "speaker_notes": "발표자 가이드: 개인 경험 공유. '아침에 누워있는데 전화해야 할 때 얼마나 귀찮은지 아시나요?' 질문으로 시작. 각 단계를 천천히 설명하며 복잡함 강조. UI 조작의 불편함과 시간 낭비 언급.",
        "estimated_time": 60
    },
    # Slide 3: The Big Idea - 큰 질문으로 호기심 유발
    {
        "number": 3,
        "title": "만약...",
        "subtitle": "말 한마디면 된다면?",
        "layout": "TitleSlide",
        "content": [
            "그냥 \"엄마\"라고 말하면",
            "자동으로 전화가 걸린다면?"
        ],
        "code_blocks": [],
        "visuals": [
            "💡 핵심 아이디어",
            "음성 명령 → 즉시 실행",
            "UI 조작 불필요"
        ],
        "speaker_notes": "발표자 가이드: 잠시 멈추고 청중과 눈 맞춤. '만약에 말입니다...' 하며 기대감 조성. 해결책을 직접 말하지 말고 질문 형태로 상상하게 만들기. '이게 가능하다면 얼마나 편할까요?'",
        "estimated_time": 45
    },
    # Slide 4: The Solution - 해결책 제시
    {
        "number": 4,
        "title": "그래서 만들었습니다",
        "subtitle": "SoundToAct",
        "layout": "SingleColumn",
        "content": [
            "말만 하면 작동하는 시스템"
        ],
        "code_blocks": [],
        "visuals": [
            "[기술 스택]",
            "• Python 3.10+ 기반",
            "• SpeechRecognition 라이브러리 (Google Speech API)",
            "• PyAutoGUI (UI 자동화)",
            "• Threading (백그라운드 실행)",
            "",
            "[동작 방식]",
            "'엄마' 음성 → 연락처 검색 → 통화 실행"
        ],
        "speaker_notes": "발표자 가이드: '그래서 직접 만들었습니다!' 힘있게 말하기. 기술 스택 설명 시 '고등학생도 배울 수 있는 Python으로 만들었다' 강조. SpeechRecognition은 Google API 사용해서 정확도 높음을 언급. 실제 동작 예시를 간단히 설명.",
        "estimated_time": 60
    },
    # Slide 5: How It Works - 3단계로 간단하게
    {
        "number": 5,
        "title": "어떻게 작동할까?",
        "subtitle": "간단한 3단계",
        "layout": "ThreeColumn",
        "content": [
            "듣기 → 이해하기 → 실행하기"
        ],
        "code_blocks": [],
        "visuals": [
            "[1단계: 듣기 🎤]",
            "마이크로 음성 캡처",
            "sr.Microphone()",
            "실시간 오디오 스트림",
            "",
            "[2단계: 이해 🧠]",
            "Google Speech API",
            "음성 → 텍스트 변환",
            "키워드 매칭 알고리즘",
            "",
            "[3단계: 실행 ⚡]",
            "명령어 파싱",
            "해당 함수 호출",
            "자동화 스크립트 실행"
        ],
        "speaker_notes": "발표자 가이드: 기술적 설명 시작. 1) 마이크 입력은 SpeechRecognition 라이브러리가 처리. 2) Google API가 음성을 텍스트로 변환 (네트워크 필요). 3) 키워드를 인식하면 미리 정의된 함수 실행. '코드는 200줄 정도로 간단합니다' 언급.",
        "estimated_time": 75
    },
    # Slide 6: Live Demo - 실제 작동 모습
    {
        "number": 6,
        "title": "실제로 보여드릴게요",
        "subtitle": None,
        "layout": "FullScreenDemo",
        "content": [
            "🎬 라이브 데모"
        ],
        "code_blocks": [],
        "visuals": [
            "[데모 시나리오]",
            "1️⃣ '엄마' → 연락처에서 찾아 전화 걸기",
            "2️⃣ '음악 틀어줘' → 음악 앱 실행",
            "3️⃣ '불 꺼줘' → 스마트 조명 제어",
            "",
            "💻 실행 명령: python main.py",
            "🎤 음성 인식 대기 중..."
        ],
        "speaker_notes": "발표자 가이드: 실제 데모 실행. 프로그램 실행 후 '엄마'라고 말하기. 반응 속도 강조 (~2초). 데모가 안 되면 '사전에 녹화한 영상'이라고 말하고 시나리오 설명. 각 명령어가 어떻게 처리되는지 간단히 설명. 오류 처리도 구현되어 있음을 언급.",
        "estimated_time": 90
    },
    # Slide 7: What It Gave Me - 나에게 준 변화
    {
        "number": 7,
        "title": "나에게 준 변화",
        "subtitle": "60배 빨라졌습니다",
        "layout": "TwoColumn",
        "content": [
            "2분 → 2초",
            "하루 30분 절약"
        ],
        "code_blocks": [],
        "visuals": [
            "[Before: 전통적 방식]",
            "• 기기 조작 필요",
            "• UI 네비게이션 필수",
            "• 5단계 프로세스",
            "• 평균 소요: 2분",
            "",
            "[After: SoundToAct]",
            "• 음성만으로 완료",
            "• UI 터치 불필요",
            "• 1단계 (말하기)",
            "• 평균 소요: 2초",
            "",
            "⚡ 속도 개선: 60배 ⚡",
            "💰 하루 약 30분 절약 (15회 사용 시)"
        ],
        "speaker_notes": "발표자 가이드: 구체적 수치로 효과 입증. Before 설명 시 손동작으로 복잡함 강조. After 설명 시 '그냥 말만 하면 됩니다' 강조. 60배는 120초/2초 계산. 하루 15회 사용 가정 시 30분 절약 (15 × 118초 = 1770초 ≈ 30분).",
        "estimated_time": 60
    },
    # Slide 8: For Others Too - 다른 사람들도
    {
        "number": 8,
        "title": "다른 사람들도 쓸 수 있어요",
        "subtitle": "모두를 위한 기술",
        "layout": "ThreeColumn",
        "content": [
            "어르신, 직장인, 장애인",
            "누구나 쉽게"
        ],
        "code_blocks": [],
        "visuals": [
            "[어르신 👴]",
            "• 작은 글씨 안 보여도 OK",
            "• 복잡한 UI 몰라도 OK",
            "• 말만 하면 작동",
            "",
            "[바쁜 직장인 💼]",
            "• 운전 중 안전하게",
            "• 멀티태스킹 가능",
            "• 손 쓸 필요 없음",
            "",
            "[장애인 ♿]",
            "• 시각 장애: 화면 안 봐도 OK",
            "• 지체 장애: 터치 불필요",
            "• 음성만으로 완전 제어"
        ],
        "speaker_notes": "발표자 가이드: 사회적 가치 강조. '기술은 누구에게나 평등해야 합니다' 시작. 각 그룹별 pain point 설명. 실제 사용자 피드백 있으면 언급. '접근성(Accessibility)'이 핵심 가치임을 강조. 유니버설 디자인 개념 간단히 소개.",
        "estimated_time": 75
    },
    # Slide 9: My Dream - 앞으로의 꿈
    {
        "number": 9,
        "title": "나의 꿈",
        "subtitle": "모두가 기술의 혜택을 받는 세상",
        "layout": "SingleColumn",
        "content": [
            "더 많은 사람들에게",
            "더 편리한 생활을"
        ],
        "code_blocks": [],
        "visuals": [
            "[향후 개선 계획]",
            "• 다국어 지원 (영어, 중국어...)",
            "• 오프라인 모드 (로컬 STT)",
            "• 더 많은 명령어 추가",
            "• 커스터마이징 기능",
            "",
            "[확장 가능성]",
            "🏠 스마트홈: IoT 기기 제어",
            "🚗 자동차: 핸즈프리 운전",
            "🏥 의료: 환자 모니터링",
            "🏭 산업: 작업장 안전"
        ],
        "speaker_notes": "발표자 가이드: 미래 비전 제시. '이건 시작일 뿐입니다' 강조. 다국어 지원으로 글로벌화 가능. 오프라인 모드는 Vosk 같은 로컬 STT 라이브러리 사용 계획. IoT 연동 시 진정한 스마트홈 가능. 의료/산업 분야 적용 사례 간단히 설명. '여러분도 함께 만들어주세요' 참여 유도.",
        "estimated_time": 60
    },
    # Slide 10: Q&A - 마무리
    {
        "number": 10,
        "title": "감사합니다",
        "subtitle": "질문 받겠습니다",
        "layout": "TitleSlide",
        "content": [
            "여러분도 말 한마디로",
            "세상을 바꿀 수 있습니다"
        ],
        "code_blocks": [],
        "visuals": [
            "[프로젝트 정보]",
            "📂 GitHub: github.com/[username]/SoundToAct",
            "📧 Email: contact@example.com",
            "🐍 Python 3.10+ 필요",
            "",
            "[기술 스택 요약]",
            "SpeechRecognition • PyAutoGUI",
            "Threading • Google Speech API",
            "",
            "💬 Q&A 환영합니다!"
        ],
        "speaker_notes": "발표자 가이드: '경청해주셔서 감사합니다!' 밝게 인사. GitHub 링크 공유하며 '코드가 궁금하신 분들은 자유롭게 보세요'. 오픈소스 프로젝트이며 contribution 환영. 질문 받을 준비. 예상 질문: 1) 정확도는? → 90% 이상 2) 비용은? → 무료 (Google API 일일 한도 내) 3) 오프라인? → 현재는 불가, 향후 추가 예정 4) 보안은? → 로컬 실행, 데이터 저장 안 함.",
        "estimated_time": 45
    }
]

# Metadata
METADATA = {
    "title": "SoundToAct",
    "subtitle": "말 한마디로 움직이는 세상",
    "presenter": "고등학생 개발자",
    "date": "2025-10-26",
    "target_audience": "선생님 (개발자)",
    "duration": "8-10분",
    "total_slides": 10
}


def create_presentation_json():
    """Create presentation JSON from Idris-defined slides"""
    presentation = {
        "metadata": METADATA,
        "slides": SLIDES
    }
    return presentation


def main():
    """Generate JSON and save to file"""
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)

    presentation = create_presentation_json()

    # Save as JSON
    json_path = output_dir / 'presentation_from_idris.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(presentation, f, ensure_ascii=False, indent=2)

    print("="*60)
    print("STORY-DRIVEN, VISUAL-FOCUSED PRESENTATION")
    print("="*60)
    print(f"✓ Generated: {json_path}")
    print(f"✓ Metadata: {METADATA['title']} - {METADATA['total_slides']} slides")
    print(f"✓ Duration: {METADATA['duration']}")
    print(f"✓ Design: Visual-heavy, minimal text")
    print()
    print("Story Arc:")
    for i, slide in enumerate(SLIDES, 1):
        visuals_count = len(slide.get('visuals', []))
        text_lines = len(slide.get('content', []))
        print(f"  {i}. {slide['title']:30} | {visuals_count} visuals, {text_lines} text lines | {slide['estimated_time']}s")
    print("="*60)


if __name__ == '__main__':
    main()
