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
            "음성 웨이브폼 애니메이션",
            "마이크 아이콘 (큼직하게)"
        ],
        "speaker_notes": "간단한 자기소개. 프로젝트 이름의 의미: Sound → Act (소리가 행동으로)",
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
            "만화 스타일 일러스트: 침대에서 일어나는 학생",
            "복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치",
            "시계 아이콘: '2분 소요'"
        ],
        "speaker_notes": "개인적 경험으로 시작. 청중이 공감할 수 있는 일상적 상황. 시각적으로 복잡한 과정 강조.",
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
            "큰 물음표 아이콘",
            "말풍선 안에 '엄마'",
            "빛나는 효과 (반짝이는 전구)"
        ],
        "speaker_notes": "질문으로 청중의 상상력 자극. 간단명료하게. 아이디어의 핵심을 제시.",
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
            "프로젝트 로고 (크게)",
            "10초 데모 영상: '엄마' → 전화 걸림",
            "Before/After 비교 이미지"
        ],
        "speaker_notes": "짧은 데모 영상으로 임팩트. 복잡한 설명 없이 바로 작동하는 모습 보여주기.",
        "estimated_time": 60
    },
    # Slide 5: How It Works - 3단계로 간단하게
    {
        "number": 5,
        "title": "어떻게 작동할까?",
        "subtitle": None,
        "layout": "ThreeColumn",
        "content": [],
        "code_blocks": [],
        "visuals": [
            "1단계: 듣기 - 마이크 아이콘 + 음성 웨이브",
            "2단계: 이해하기 - AI 뇌 + 키워드 매칭",
            "3단계: 실행하기 - 액션 아이콘 (전화, 음악, 조명)",
            "화살표로 연결된 3단계 플로우"
        ],
        "speaker_notes": "3단계만 강조. 기술적 용어 배제. 아이콘과 그림으로만 표현.",
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
            "실제 사용 데모 영상 (30초)",
            "데모 스크린샷 (백업)"
        ],
        "speaker_notes": "실제 작동하는 모습. 영상: '엄마' 말하기 → 전화 걸림, '음악' → 재생됨, '불꺼' → 조명 OFF",
        "estimated_time": 90
    },
    # Slide 7: What It Gave Me - 나에게 준 변화
    {
        "number": 7,
        "title": "나에게 준 변화",
        "subtitle": None,
        "layout": "TwoColumn",
        "content": [],
        "code_blocks": [],
        "visuals": [
            "Before: 복잡한 과정 (2분)",
            "After: 말 한마디 (2초)",
            "숫자 강조: 60배 빨라짐",
            "하루 30분 절약"
        ],
        "speaker_notes": "Before/After 비교로 효과 시각화. 숫자로 임팩트 강조.",
        "estimated_time": 60
    },
    # Slide 8: For Others Too - 다른 사람들도
    {
        "number": 8,
        "title": "다른 사람들도 쓸 수 있어요",
        "subtitle": None,
        "layout": "ThreeColumn",
        "content": [],
        "code_blocks": [],
        "visuals": [
            "시나리오 1: 어르신 - 큰 글씨 필요없이",
            "시나리오 2: 바쁜 직장인 - 운전 중에도",
            "시나리오 3: 장애인 - 손 사용 불편해도",
            "모두를 위한 기술"
        ],
        "speaker_notes": "사회적 가치 강조. 다양한 사람들이 혜택 받을 수 있음. 포용적 기술.",
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
            "지구 아이콘 + 연결된 사람들",
            "밝은 미래 이미지",
            "확장 가능성: 스마트홈, 자동차, 가전제품..."
        ],
        "speaker_notes": "개인적 비전 제시. 기술의 사회적 가치. 청중에게 영감 주기.",
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
            "QR 코드 (GitHub)",
            "SoundToAct 로고"
        ],
        "speaker_notes": "감사 인사. 영감을 주는 마무리 멘트. GitHub QR 코드 제공.",
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
