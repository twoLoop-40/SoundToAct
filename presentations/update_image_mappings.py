#!/usr/bin/env python3
"""
Image Mapping Updater

Creates correct image mappings from visual descriptions to generated image files
"""

# Complete mapping from visual descriptions to image files
IMAGE_MAPPING = {
    # Slide 1
    "음성 웨이브폼 애니메이션": "waveform_animation.png",
    "마이크 아이콘 (큼직하게)": "microphone_large.png",

    # Slide 2
    "만화 스타일 일러스트: 침대에서 일어나는 학생": "student_waking_up.png",
    "복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치": "complex_process_flow.png",
    "시계 아이콘: '2분 소요'": "clock_two_minutes.png",

    # Slide 3
    "큰 물음표 아이콘": "question_mark_large.png",
    "말풍선 안에 '엄마'": "speech_bubble_mom.png",
    "빛나는 효과 (반짝이는 전구)": "light_bulb_sparkle.png",

    # Slide 4
    "프로젝트 로고 (크게)": "soundtoact_logo_large.png",
    "10초 데모 영상: '엄마' → 전화 걸림": "demo_video_placeholder.png",
    "Before/After 비교 이미지": "before_after_comparison.png",

    # Slide 5
    "1단계: 듣기 - 마이크 아이콘 + 음성 웨이브": "step1_listen.png",
    "2단계: 이해하기 - AI 뇌 + 키워드 매칭": "step2_understand.png",
    "3단계: 실행하기 - 액션 아이콘 (전화, 음악, 조명)": "step3_act.png",
    "화살표로 연결된 3단계 플로우": "three_step_flow_arrows.png",

    # Slide 6
    "실제 사용 데모 영상 (30초)": "live_demo_video.png",
    "데모 스크린샷 (백업)": "demo_screenshot_backup.png",

    # Slide 7
    "Before: 복잡한 과정 (2분)": "before_2_minutes.png",
    "After: 말 한마디 (2초)": "after_2_seconds.png",
    "숫자 강조: 60배 빨라짐": "sixty_times_faster.png",
    "하루 30분 절약": "thirty_minutes_saved.png",

    # Slide 8
    "시나리오 1: 어르신 - 큰 글씨 필요없이": "elderly_scenario.png",
    "시나리오 2: 바쁜 직장인 - 운전 중에도": "worker_scenario.png",
    "시나리오 3: 장애인 - 손 사용 불편해도": "disability_scenario.png",
    "모두를 위한 기술": "inclusive_technology.png",

    # Slide 9
    "지구 아이콘 + 연결된 사람들": "connected_world.png",
    "밝은 미래 이미지": "bright_future.png",
    "확장 가능성: 스마트홈, 자동차, 가전제품...": "expansion_vision.png",

    # Slide 10
    "QR 코드 (GitHub)": "qr_code_github.png",
    "SoundToAct 로고": "soundtoact_logo_final.png",
}

def generate_mapping_code():
    """Generate Python code for the image mapping"""
    print("# Image mapping - copy this into create_pptx_with_images.py")
    print("image_map = {")
    for desc, filename in IMAGE_MAPPING.items():
        print(f"    '{desc}': '{filename}',")
    print("}")
    print(f"\n# Total mappings: {len(IMAGE_MAPPING)}")

if __name__ == '__main__':
    generate_mapping_code()
