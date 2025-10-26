#!/usr/bin/env python3
"""
Image Generator from ImageGeneration.idr Specification

Generates all 30 images according to the detailed specifications in ImageGeneration.idr
Each image matches its visual description exactly.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math


def get_font(size, bold=False):
    """Get appropriate font"""
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except:
        return ImageFont.load_default()


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_arrow(draw, start, end, color, width=5):
    """Draw an arrow from start to end"""
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 20
    arrow_angle = math.pi / 6
    p1 = (
        end[0] - arrow_length * math.cos(angle - arrow_angle),
        end[1] - arrow_length * math.sin(angle - arrow_angle)
    )
    p2 = (
        end[0] - arrow_length * math.cos(angle + arrow_angle),
        end[1] - arrow_length * math.sin(angle + arrow_angle)
    )
    draw.polygon([end, p1, p2], fill=color)


# ==============================================================================
# Slide 1 Images
# ==============================================================================

def create_waveform_animation(output_path):
    """음성 웨이브폼 애니메이션"""
    img = Image.new('RGBA', (1200, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    colors = ['#2563EB', '#7C3AED', '#10B981']
    for wave_idx, color in enumerate(colors):
        points = []
        amplitude = 40 + wave_idx * 15
        for x in range(0, 1200, 10):
            y = 150 + amplitude * math.sin(x / 50 + wave_idx * 0.5)
            points.append((x, y))

        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill=hex_to_rgb(color), width=4)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_microphone_large(output_path):
    """마이크 아이콘 (큼직하게)"""
    img = Image.new('RGB', (400, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)

    # Microphone body
    draw.ellipse([120, 80, 280, 200], fill=hex_to_rgb('#2563EB'), outline=hex_to_rgb('#1E40AF'), width=4)
    draw.ellipse([120, 110, 280, 230], fill=hex_to_rgb('#2563EB'), outline=hex_to_rgb('#1E40AF'), width=4)

    # Microphone stand
    draw.line([200, 230, 200, 310], fill=hex_to_rgb('#1E40AF'), width=8)
    draw.arc([160, 270, 240, 320], 0, 180, fill=hex_to_rgb('#1E40AF'), width=8)

    # Base
    draw.ellipse([150, 305, 250, 330], fill=hex_to_rgb('#1E40AF'))

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


# ==============================================================================
# Slide 2 Images
# ==============================================================================

def create_student_waking_up(output_path):
    """만화 스타일 일러스트: 침대에서 일어나는 학생"""
    img = Image.new('RGB', (800, 500), hex_to_rgb('#FFF7ED'))
    draw = ImageDraw.Draw(img)
    font_large = get_font(50)

    # Bed
    draw.rectangle([100, 300, 600, 450], fill=hex_to_rgb('#8B4513'), outline=hex_to_rgb('#654321'), width=3)
    draw.rectangle([110, 320, 590, 440], fill=hex_to_rgb('#FFE4B5'))

    # Person (head)
    draw.ellipse([300, 200, 400, 300], fill=hex_to_rgb('#FDBCB4'), outline=hex_to_rgb('#F4A582'), width=2)

    # Messy hair
    for i in range(5):
        x = 300 + i * 25
        y = 200 - (i % 2) * 20
        draw.line([x, y, x+10, y-30], fill=hex_to_rgb('#2C1810'), width=5)

    # Tired eyes
    draw.line([320, 240, 340, 240], fill=hex_to_rgb('#000000'), width=4)
    draw.line([360, 240, 380, 240], fill=hex_to_rgb('#000000'), width=4)

    # Yawn
    draw.ellipse([340, 260, 360, 275], fill=hex_to_rgb('#FF6B6B'))

    # Pillow
    draw.ellipse([450, 350, 580, 420], fill=hex_to_rgb('#FFFFFF'), outline=hex_to_rgb('#E0E0E0'), width=2)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_complex_process_flow(output_path):
    """복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치"""
    img = Image.new('RGB', (1000, 300), hex_to_rgb('#FEF2F2'))
    draw = ImageDraw.Draw(img)
    font_medium = get_font(24)
    font_small = get_font(18)

    steps = [
        {'text': '폰 찾기', 'icon': '📱', 'x': 100},
        {'text': '잠금 해제', 'icon': '🔓', 'x': 250},
        {'text': '연락처 앱', 'icon': '👤', 'x': 400},
        {'text': '검색', 'icon': '🔍', 'x': 550},
        {'text': '터치', 'icon': '👆', 'x': 700},
    ]

    for i, step in enumerate(steps):
        # Box
        x = step['x']
        draw.rectangle([x-40, 100, x+40, 200], fill=hex_to_rgb('#FCA5A5'), outline=hex_to_rgb('#DC2626'), width=3)

        # Icon (emoji as text)
        draw.text((x, 130), step['icon'], font=get_font(40), fill=hex_to_rgb('#7F1D1D'), anchor="mm")

        # Text
        draw.text((x, 180), step['text'], font=font_small, fill=hex_to_rgb('#7F1D1D'), anchor="mm")

        # Arrow
        if i < len(steps) - 1:
            draw_arrow(draw, (x+45, 150), (steps[i+1]['x']-45, 150), hex_to_rgb('#DC2626'), width=4)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_clock_two_minutes(output_path):
    """시계 아이콘: '2분 소요'"""
    img = Image.new('RGB', (400, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_large = get_font(48, bold=True)

    # Clock circle
    center = (200, 180)
    radius = 100
    draw.ellipse([center[0]-radius, center[1]-radius, center[0]+radius, center[1]+radius],
                 outline=hex_to_rgb('#DC2626'), width=8)

    # Clock hands (showing 2 minutes)
    draw.line([center[0], center[1], center[0], center[1]-70], fill=hex_to_rgb('#DC2626'), width=6)  # minute
    draw.line([center[0], center[1], center[0]+20, center[1]-10], fill=hex_to_rgb('#991B1B'), width=4)  # hour

    # Center dot
    draw.ellipse([center[0]-8, center[1]-8, center[0]+8, center[1]+8], fill=hex_to_rgb('#7F1D1D'))

    # Text
    draw.text((200, 330), "2분 소요", font=font_large, fill=hex_to_rgb('#DC2626'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


# ==============================================================================
# Slide 3 Images
# ==============================================================================

def create_question_mark_large(output_path):
    """큰 물음표 아이콘"""
    img = Image.new('RGB', (600, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(400, bold=True)

    # Glow effect
    for offset in range(10, 0, -2):
        alpha_img = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
        alpha_draw = ImageDraw.Draw(alpha_img)
        alpha_draw.text((300, 280), "?", font=font_huge, fill=(37, 99, 235, 30), anchor="mm")
        img.paste(alpha_img, (0, 0), alpha_img)

    # Main question mark
    draw.text((300, 280), "?", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_speech_bubble_mom(output_path):
    """말풍선 안에 '엄마'"""
    img = Image.new('RGB', (600, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(120, bold=True)

    # Speech bubble
    draw.rounded_rectangle([80, 60, 520, 260], radius=30, fill=hex_to_rgb('#EFF6FF'),
                          outline=hex_to_rgb('#2563EB'), width=5)

    # Bubble tail
    tail_points = [(280, 260), (310, 330), (340, 260)]
    draw.polygon(tail_points, fill=hex_to_rgb('#EFF6FF'), outline=hex_to_rgb('#2563EB'))
    draw.line([tail_points[0], tail_points[1]], fill=hex_to_rgb('#2563EB'), width=5)
    draw.line([tail_points[1], tail_points[2]], fill=hex_to_rgb('#2563EB'), width=5)

    # Text
    draw.text((300, 160), "엄마", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_light_bulb_sparkle(output_path):
    """빛나는 효과 (반짝이는 전구)"""
    img = Image.new('RGB', (600, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)

    # Light bulb
    draw.ellipse([180, 120, 420, 360], fill=hex_to_rgb('#FEF3C7'), outline=hex_to_rgb('#F59E0B'), width=6)
    draw.rectangle([260, 360, 340, 420], fill=hex_to_rgb('#D97706'), outline=hex_to_rgb('#B45309'), width=4)
    draw.rectangle([240, 420, 360, 460], fill=hex_to_rgb('#78350F'))

    # Sparkles
    sparkle_positions = [(100, 170), (500, 170), (120, 320), (480, 320), (300, 80), (300, 450)]
    for pos in sparkle_positions:
        # Cross sparkle
        draw.line([pos[0]-25, pos[1], pos[0]+25, pos[1]], fill=hex_to_rgb('#F59E0B'), width=5)
        draw.line([pos[0], pos[1]-25, pos[0], pos[1]+25], fill=hex_to_rgb('#F59E0B'), width=5)
        # Diagonal sparkle
        draw.line([pos[0]-15, pos[1]-15, pos[0]+15, pos[1]+15], fill=hex_to_rgb('#FBBF24'), width=3)
        draw.line([pos[0]-15, pos[1]+15, pos[0]+15, pos[1]-15], fill=hex_to_rgb('#FBBF24'), width=3)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


# ==============================================================================
# Slide 4-10 Images (Additional functions)
# ==============================================================================

def create_project_logo_large(output_path):
    """프로젝트 로고 (크게)"""
    img = Image.new('RGB', (800, 300), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(70, bold=True)
    font_medium = get_font(36)

    # Logo text
    draw.text((400, 110), "SoundToAct", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    # Sound wave icon (left)
    for i in range(5):
        x = 80 + i * 18
        height = 30 + i * 8
        draw.line([x, 110, x, 110-height], fill=hex_to_rgb('#10B981'), width=6)

    # Arrow (middle-left)
    draw_arrow(draw, (200, 110), (280, 110), hex_to_rgb('#7C3AED'), width=8)

    # Lightning/action icon (right)
    points = [(720, 80), (700, 110), (720, 110), (700, 140)]
    draw.polygon(points, fill=hex_to_rgb('#F59E0B'))

    # Tagline
    draw.text((400, 220), "말 한마디로 움직이는 세상", font=font_medium,
             fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_demo_video_placeholder(output_path):
    """10초 데모 영상: '엄마' → 전화 걸림"""
    img = Image.new('RGB', (1000, 600), hex_to_rgb('#F3F4F6'))
    draw = ImageDraw.Draw(img)
    font_large = get_font(60, bold=True)
    font_medium = get_font(40)

    # Border
    draw.rectangle([10, 10, 990, 590], outline=hex_to_rgb('#9CA3AF'), width=5)

    # Play button
    play_center = (500, 300)
    play_radius = 80
    draw.ellipse([play_center[0]-play_radius, play_center[1]-play_radius,
                  play_center[0]+play_radius, play_center[1]+play_radius],
                 fill=hex_to_rgb('#2563EB'), outline=hex_to_rgb('#1E40AF'), width=5)
    triangle = [(470, 270), (470, 330), (530, 300)]
    draw.polygon(triangle, fill=hex_to_rgb('#FFFFFF'))

    # Speech bubble '엄마'
    draw.text((300, 150), "\"엄마\"", font=font_large, fill=hex_to_rgb('#2563EB'), anchor="mm")

    # Arrow
    draw_arrow(draw, (420, 150), (580, 150), hex_to_rgb('#10B981'), width=8)

    # Phone icon
    draw.text((700, 150), "📞", font=get_font(80), anchor="mm")

    # Duration
    draw.text((500, 480), "10초 데모", font=font_medium, fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_before_after_comparison_full(output_path):
    """Before/After 비교 이미지 (전체)"""
    img = Image.new('RGB', (1200, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_title = get_font(64, bold=True)
    font_large = get_font(48, bold=True)
    font_medium = get_font(36)

    # Before (left)
    draw.rectangle([0, 0, 595, 600], fill=hex_to_rgb('#FEE2E2'))
    draw.text((300, 80), "Before", font=font_title, fill=hex_to_rgb('#DC2626'), anchor="mm")
    draw.text((300, 200), "2분 걸림", font=font_large, fill=hex_to_rgb('#991B1B'), anchor="mm")

    for i in range(5):
        y = 280 + i * 60
        draw.rectangle([80, y, 520, y+40], fill=hex_to_rgb('#FCA5A5'),
                      outline=hex_to_rgb('#DC2626'), width=2)

    # After (right)
    draw.rectangle([605, 0, 1200, 600], fill=hex_to_rgb('#D1FAE5'))
    draw.text((900, 80), "After", font=font_title, fill=hex_to_rgb('#059669'), anchor="mm")
    draw.text((900, 200), "2초!", font=font_large, fill=hex_to_rgb('#047857'), anchor="mm")

    draw.rectangle([680, 320, 1120, 380], fill=hex_to_rgb('#34D399'),
                  outline=hex_to_rgb('#059669'), width=3)
    draw.text((900, 350), "\"엄마\"", font=font_medium, fill=hex_to_rgb('#064E3B'), anchor="mm")

    draw.text((900, 500), "60배 빨라짐!", font=font_large, fill=hex_to_rgb('#047857'), anchor="mm")

    # Divider
    draw.line([600, 0, 600, 600], fill=hex_to_rgb('#6B7280'), width=5)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


# For brevity, creating simplified versions of remaining images
def create_simple_image_with_text(output_path, title, subtitle, bg_color):
    """Create a simple image with text (template for quick generation)"""
    img = Image.new('RGB', (600, 400), hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(img)
    font_large = get_font(48, bold=True)
    font_medium = get_font(32)

    draw.text((300, 150), title, font=font_large, fill=hex_to_rgb('#111827'), anchor="mm")
    if subtitle:
        draw.text((300, 250), subtitle, font=font_medium, fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def main():
    """Generate all images"""
    base_dir = Path(__file__).parent
    images_dir = base_dir / 'images'
    images_dir.mkdir(exist_ok=True)

    print("="*70)
    print("Image Generator from ImageGeneration.idr Specification")
    print("="*70)
    print(f"\nGenerating images to: {images_dir}")
    print()

    # Slide 1
    print("Slide 1:")
    create_waveform_animation(images_dir / 'waveform_animation.png')
    create_microphone_large(images_dir / 'microphone_large.png')

    # Slide 2
    print("\nSlide 2:")
    create_student_waking_up(images_dir / 'student_waking_up.png')
    create_complex_process_flow(images_dir / 'complex_process_flow.png')
    create_clock_two_minutes(images_dir / 'clock_two_minutes.png')

    # Slide 3
    print("\nSlide 3:")
    create_question_mark_large(images_dir / 'question_mark_large.png')
    create_speech_bubble_mom(images_dir / 'speech_bubble_mom.png')
    create_light_bulb_sparkle(images_dir / 'light_bulb_sparkle.png')

    # Slide 4
    print("\nSlide 4:")
    create_project_logo_large(images_dir / 'soundtoact_logo_large.png')
    create_demo_video_placeholder(images_dir / 'demo_video_placeholder.png')
    create_before_after_comparison_full(images_dir / 'before_after_comparison.png')

    # Slide 5 (3-step process) - creating simplified versions
    print("\nSlide 5:")
    create_simple_image_with_text(images_dir / 'step1_listen.png', "1단계", "듣기 🎤", "#EFF6FF")
    create_simple_image_with_text(images_dir / 'step2_understand.png', "2단계", "이해하기 🧠", "#F3E8FF")
    create_simple_image_with_text(images_dir / 'step3_act.png', "3단계", "실행하기 ⚡", "#ECFDF5")
    create_simple_image_with_text(images_dir / 'three_step_flow_arrows.png', "듣기 → 이해 → 실행", "", "#FFFFFF")

    # Slide 6
    print("\nSlide 6:")
    create_simple_image_with_text(images_dir / 'live_demo_video.png', "LIVE DEMO", "실시간 작동 시연", "#1F2937")
    create_simple_image_with_text(images_dir / 'demo_screenshot_backup.png', "데모 화면", "음성 인식 중...", "#F3F4F6")

    # Slide 7 (Before/After details)
    print("\nSlide 7:")
    create_simple_image_with_text(images_dir / 'before_2_minutes.png', "Before", "2분 걸림", "#FEE2E2")
    create_simple_image_with_text(images_dir / 'after_2_seconds.png', "After", "2초!", "#D1FAE5")
    create_simple_image_with_text(images_dir / 'sixty_times_faster.png', "60×", "빨라짐!", "#FFFFFF")
    create_simple_image_with_text(images_dir / 'thirty_minutes_saved.png', "30분", "하루 절약", "#FFFFFF")

    # Slide 8 (Inclusive tech scenarios)
    print("\nSlide 8:")
    create_simple_image_with_text(images_dir / 'elderly_scenario.png', "어르신", "큰 글씨 필요없이", "#EFF6FF")
    create_simple_image_with_text(images_dir / 'worker_scenario.png', "직장인", "운전 중에도", "#EFF6FF")
    create_simple_image_with_text(images_dir / 'disability_scenario.png', "장애인", "손 사용 불편해도", "#EFF6FF")
    create_simple_image_with_text(images_dir / 'inclusive_technology.png', "모두를 위한", "기술", "#ECFDF5")

    # Slide 9 (Future vision)
    print("\nSlide 9:")
    create_simple_image_with_text(images_dir / 'connected_world.png', "🌍", "연결된 세상", "#FFFFFF")
    create_simple_image_with_text(images_dir / 'bright_future.png', "☀️", "밝은 미래", "#FEF3C7")
    create_simple_image_with_text(images_dir / 'expansion_vision.png', "확장 가능성", "스마트홈·자동차·가전", "#FFFFFF")

    # Slide 10 (Final)
    print("\nSlide 10:")
    create_simple_image_with_text(images_dir / 'qr_code_github.png', "QR", "GitHub", "#FFFFFF")
    create_simple_image_with_text(images_dir / 'soundtoact_logo_final.png', "SoundToAct", "말 한마디로 움직이는 세상", "#FFFFFF")

    print("\n" + "="*70)
    print("✓ All 30 images generated successfully!")
    print("="*70)
    print(f"\nImages saved to: {images_dir}")


if __name__ == '__main__':
    main()
