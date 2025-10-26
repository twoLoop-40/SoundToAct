#!/usr/bin/env python3
"""
PowerPoint Generator with Real Images

Creates presentation with actual images inserted into slides.
"""

import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


# Color palette
COLORS = {
    'primary': RGBColor(37, 99, 235),
    'secondary': RGBColor(124, 58, 237),
    'accent': RGBColor(16, 185, 129),
    'warning': RGBColor(245, 158, 11),
    'text_primary': RGBColor(17, 24, 39),
    'text_secondary': RGBColor(107, 114, 128),
}


def create_title_slide(prs, slide_data, images_dir):
    """Create title slide with images"""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Title
    left = Inches(1)
    top = Inches(2)
    width = Inches(8)
    height = Inches(1.5)

    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = slide_data['title']
    p.font.size = Pt(72)
    p.font.bold = True
    p.font.color.rgb = COLORS['primary']
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    if slide_data.get('subtitle'):
        sub_box = slide.shapes.add_textbox(left, Inches(3.5), width, Inches(0.8))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = slide_data['subtitle']
        p.font.size = Pt(36)
        p.font.color.rgb = COLORS['text_secondary']
        p.alignment = PP_ALIGN.CENTER

    # Add waveform image if available
    wave_img = images_dir / 'wave_animation.png'
    if wave_img.exists():
        slide.shapes.add_picture(
            str(wave_img),
            Inches(1.5), Inches(5),
            width=Inches(7)
        )

    # Add mic icon
    mic_img = images_dir / 'mic_icon_large.png'
    if mic_img.exists():
        slide.shapes.add_picture(
            str(mic_img),
            Inches(8), Inches(0.5),
            height=Inches(1.5)
        )

    # Content at bottom
    content = slide_data.get('content', [])
    if content:
        text_box = slide.shapes.add_textbox(left, Inches(6.5), width, Inches(0.5))
        tf = text_box.text_frame
        for i, line in enumerate(content):
            if line.strip():
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.font.size = Pt(24)
                p.font.color.rgb = COLORS['text_primary']
                p.alignment = PP_ALIGN.CENTER

    return slide


def create_visual_slide(prs, slide_data, images_dir):
    """Create slide with large images"""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Title
    left = Inches(0.5)
    top = Inches(0.3)
    width = Inches(9)
    height = Inches(0.8)

    title_box = slide.shapes.add_textbox(left, top, width, height)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = slide_data['title']
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLORS['primary']
    p.alignment = PP_ALIGN.CENTER

    # Subtitle if exists
    current_top = Inches(1.1)
    if slide_data.get('subtitle'):
        sub_box = slide.shapes.add_textbox(left, current_top, width, Inches(0.5))
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = slide_data['subtitle']
        p.font.size = Pt(28)
        p.font.color.rgb = COLORS['text_secondary']
        p.alignment = PP_ALIGN.CENTER
        current_top += Inches(0.6)

    # Map visual descriptions to image files
    image_map = {
        # Slide 1: Title
        '음성 웨이브폼 애니메이션': 'wave_animation.png',
        '마이크 아이콘 (큼직하게)': 'mic_icon_large.png',
        # Slide 2: Problem
        '아침 일러스트': 'morning_illustration.png',
        '복잡한 과정 다이어그램 (5단계)': 'complex_process.png',
        '만화 스타일 일러스트: 침대에서 일어나는 학생': 'morning_illustration.png',
        '복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치': 'complex_process.png',
        "시계 아이콘: '2분 소요'": 'complex_process.png',
        # Slide 3: Idea
        '큰 물음표 아이콘': 'question_mark.png',
        '말풍선 안에 \'엄마\'': 'speech_bubble_mom.png',
        '빛나는 효과 (반짝이는 전구)': 'light_bulb.png',
        # Slide 4: Solution
        'SoundToAct 로고': 'logo.png',
        '프로젝트 로고 (크게)': 'logo.png',
        '데모 영상 스크린샷': 'demo_placeholder.png',
        "10초 데모 영상: '엄마' → 전화 걸림": 'demo_placeholder.png',
        'Before/After 비교 이미지': 'before_after.png',
        # Slide 5: How
        '1단계: 듣기 - 마이크 아이콘 + 음성 웨이브': 'three_steps.png',
        '2단계: 이해하기 - AI 뇌 + 키워드 매칭': 'three_steps.png',
        '3단계: 실행하기 - 액션 아이콘 (전화, 음악, 조명)': 'three_steps.png',
        '화살표로 연결된 3단계 플로우': 'three_steps.png',
        # Slide 6: Demo
        '라이브 데모 화면': 'live_demo.png',
        '실제 사용 데모 영상 (30초)': 'live_demo.png',
        '데모 스크린샷 (백업)': 'demo_placeholder.png',
        # Slide 7: Impact
        'Before: 복잡한 과정 (2분)': 'before_after.png',
        'After: 말 한마디 (2초)': 'before_after.png',
        '숫자 강조: 60배 빨라짐': 'before_after.png',
        '하루 30분 절약': 'before_after.png',
        # Slide 8: For Others
        '시나리오 1: 어르신 - 큰 글씨 필요없이': 'inclusive_tech.png',
        '시나리오 2: 바쁜 직장인 - 운전 중에도': 'inclusive_tech.png',
        '시나리오 3: 장애인 - 손 사용 불편해도': 'inclusive_tech.png',
        '모두를 위한 기술': 'inclusive_tech.png',
        # Slide 9: Dream
        '지구 아이콘 + 연결된 사람들': 'world_connections.png',
        '밝은 미래 일러스트': 'bright_future.png',
        # Slide 10: Thank You
        'QR 코드 (GitHub 링크)': 'qr_code.png',
        'SoundToAct 로고 (작게)': 'final_logo.png',
    }

    visuals = slide_data.get('visuals', [])

    # Find the primary image to display
    primary_image = None
    for visual in visuals:
        if visual in image_map:
            img_file = images_dir / image_map[visual]
            if img_file.exists():
                primary_image = img_file
                break

    # If we have an image, display it large
    if primary_image:
        # Center large image
        img_width = Inches(7)
        img_height = Inches(4.5)
        img_left = Inches(1.5)
        img_top = current_top

        slide.shapes.add_picture(
            str(primary_image),
            img_left, img_top,
            width=img_width
        )
        current_top += img_height + Inches(0.3)
    else:
        # Create placeholder boxes for visuals
        num_visuals = len(visuals)
        if num_visuals > 0:
            if num_visuals <= 2:
                # Large boxes side by side
                box_width = Inches(4) if num_visuals == 2 else Inches(7)
                for i, visual in enumerate(visuals[:2]):
                    box_left = Inches(1) if num_visuals == 1 else Inches(0.5 + i * 4.5)
                    shape = slide.shapes.add_shape(
                        1,  # Rectangle
                        box_left, current_top, box_width, Inches(3.5)
                    )
                    shape.fill.solid()
                    shape.fill.fore_color.rgb = RGBColor(240, 245, 255)
                    shape.line.color.rgb = COLORS['primary']
                    shape.line.width = Pt(3)

                    tf = shape.text_frame
                    tf.word_wrap = True
                    p = tf.paragraphs[0]
                    p.text = visual
                    p.font.size = Pt(18)
                    p.font.color.rgb = COLORS['text_secondary']
                    p.alignment = PP_ALIGN.CENTER
            else:
                # Grid layout for multiple visuals
                for i, visual in enumerate(visuals[:4]):
                    row = i // 2
                    col = i % 2
                    box_left = Inches(0.5 + col * 4.75)
                    box_top = current_top + row * Inches(2.3)

                    shape = slide.shapes.add_shape(
                        1,
                        box_left, box_top, Inches(4.5), Inches(2)
                    )
                    shape.fill.solid()
                    shape.fill.fore_color.rgb = RGBColor(240, 245, 255)
                    shape.line.color.rgb = COLORS['primary']
                    shape.line.width = Pt(2)

                    tf = shape.text_frame
                    tf.word_wrap = True
                    p = tf.paragraphs[0]
                    p.text = visual
                    p.font.size = Pt(14)
                    p.font.color.rgb = COLORS['text_secondary']
                    p.alignment = PP_ALIGN.CENTER

    # Content text at bottom
    content = slide_data.get('content', [])
    if content and any(c.strip() for c in content):
        text_box = slide.shapes.add_textbox(
            Inches(1), Inches(6.5), Inches(8), Inches(0.8)
        )
        tf = text_box.text_frame
        tf.word_wrap = True

        for i, line in enumerate(content):
            if line.strip():
                if i == 0:
                    p = tf.paragraphs[0]
                else:
                    p = tf.add_paragraph()
                p.text = line
                p.font.size = Pt(22)
                p.font.color.rgb = COLORS['text_primary']
                p.alignment = PP_ALIGN.CENTER

    return slide


def create_presentation_from_json(json_path, images_dir, output_path):
    """Create PowerPoint presentation with images from JSON"""

    # Load JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Create presentation
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    metadata = data['metadata']
    slides_data = data['slides']

    print(f"Creating presentation: {metadata['title']}")
    print(f"Total slides: {metadata['total_slides']}")
    print(f"Images directory: {images_dir}")
    print()

    # Create each slide
    for slide_data in slides_data:
        slide_num = slide_data['number']
        layout = slide_data['layout']

        print(f"  Creating slide {slide_num}: {slide_data['title']} ({layout})")

        # Choose slide creation function
        if layout == 'TitleSlide':
            slide = create_title_slide(prs, slide_data, images_dir)
        else:
            slide = create_visual_slide(prs, slide_data, images_dir)

    # Save presentation
    prs.save(output_path)
    print(f"\n✓ Presentation saved: {output_path}")

    return output_path


def main():
    """Main function"""
    base_dir = Path(__file__).parent
    json_path = base_dir / 'output' / 'presentation_from_idris.json'
    images_dir = base_dir / 'images'
    output_path = base_dir / 'output' / 'SoundToAct_Presentation_WithImages.pptx'

    if not json_path.exists():
        print(f"Error: JSON file not found: {json_path}")
        return

    if not images_dir.exists():
        print(f"Error: Images directory not found: {images_dir}")
        print("Please run generate_images.py first")
        return

    print("="*60)
    print("PowerPoint Generator with Images")
    print("="*60)
    print()

    create_presentation_from_json(json_path, images_dir, output_path)

    print()
    print("="*60)
    print("DONE!")
    print("="*60)
    print(f"\nYou can now open: {output_path}")


if __name__ == '__main__':
    main()
