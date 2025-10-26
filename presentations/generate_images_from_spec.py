#!/usr/bin/env python3
"""
Image Generator from ImageSpec.idr
Generates all 17 images with exact specifications from the Idris spec
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math


# Try to load fonts
def get_font(size, bold=False):
    """Get appropriate font for the system"""
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size)
    except:
        try:
            if bold:
                return ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", size)
            return ImageFont.truetype("/Library/Fonts/Arial.ttf", size)
        except:
            return ImageFont.load_default()


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def draw_arrow(draw, start, end, color, width=5):
    """Draw an arrow from start to end"""
    # Draw line
    draw.line([start, end], fill=color, width=width)

    # Calculate arrow head
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    arrow_length = 20
    arrow_angle = math.pi / 6

    # Arrow head points
    p1 = (
        end[0] - arrow_length * math.cos(angle - arrow_angle),
        end[1] - arrow_length * math.sin(angle - arrow_angle)
    )
    p2 = (
        end[0] - arrow_length * math.cos(angle + arrow_angle),
        end[1] - arrow_length * math.sin(angle + arrow_angle)
    )

    draw.polygon([end, p1, p2], fill=color)


def create_waveform_animation(output_path):
    """Slide 1: Waveform animation"""
    img = Image.new('RGBA', (1200, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw multiple waves with different amplitudes
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


def create_mic_icon_large(output_path):
    """Slide 1: Large microphone icon"""
    img = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Microphone body
    draw.ellipse([100, 50, 200, 150], fill=hex_to_rgb('#2563EB'), outline=hex_to_rgb('#1E40AF'), width=3)
    draw.ellipse([100, 80, 200, 180], fill=hex_to_rgb('#2563EB'), outline=hex_to_rgb('#1E40AF'), width=3)

    # Microphone stand
    draw.line([150, 180, 150, 240], fill=hex_to_rgb('#1E40AF'), width=6)
    draw.arc([120, 200, 180, 240], 0, 180, fill=hex_to_rgb('#1E40AF'), width=6)

    # Base
    draw.ellipse([120, 235, 180, 250], fill=hex_to_rgb('#1E40AF'))

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_morning_illustration(output_path):
    """Slide 2: Morning routine illustration"""
    img = Image.new('RGB', (800, 500), hex_to_rgb('#FFF7ED'))
    draw = ImageDraw.Draw(img)
    font_large = get_font(60)
    font_medium = get_font(36)

    # Sun
    draw.ellipse([50, 50, 150, 150], fill=hex_to_rgb('#F59E0B'))

    # Person (simplified)
    draw.ellipse([350, 200, 450, 300], fill=hex_to_rgb('#2563EB'))  # Head
    draw.rectangle([375, 300, 425, 400], fill=hex_to_rgb('#2563EB'))  # Body

    # Text
    draw.text((400, 450), "바쁜 아침", font=font_large, fill=hex_to_rgb('#EA580C'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_complex_process(output_path):
    """Slide 2: Complex manual process diagram"""
    img = Image.new('RGB', (800, 400), hex_to_rgb('#FEF2F2'))
    draw = ImageDraw.Draw(img)
    font_large = get_font(48, bold=True)
    font_medium = get_font(32)

    # Draw 5 steps with arrows
    step_positions = [(100, 200), (250, 200), (400, 200), (550, 200), (700, 200)]

    for i, pos in enumerate(step_positions):
        # Step circle
        draw.ellipse([pos[0]-30, pos[1]-30, pos[0]+30, pos[1]+30],
                     fill=hex_to_rgb('#F97316'), outline=hex_to_rgb('#EA580C'), width=3)
        draw.text(pos, str(i+1), font=font_medium, fill=hex_to_rgb('#FFFFFF'), anchor="mm")

        # Arrow to next step
        if i < len(step_positions) - 1:
            draw_arrow(draw, (pos[0]+35, pos[1]), (step_positions[i+1][0]-35, pos[1]),
                      hex_to_rgb('#EA580C'), width=4)

    # Title
    draw.text((400, 50), "복잡한 과정: 5단계", font=font_large, fill=hex_to_rgb('#EA580C'), anchor="mm")
    draw.text((400, 350), "2분 소요!", font=font_medium, fill=hex_to_rgb('#DC2626'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_question_mark(output_path):
    """Slide 3: Large question mark icon"""
    img = Image.new('RGB', (600, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(400, bold=True)

    # Question mark
    draw.text((300, 280), "?", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    # Glow effect
    for offset in range(5, 0, -1):
        alpha_img = Image.new('RGBA', (600, 600), (0, 0, 0, 0))
        alpha_draw = ImageDraw.Draw(alpha_img)
        alpha_draw.text((300, 280), "?", font=font_huge, fill=(37, 99, 235, 50-offset*10), anchor="mm")
        img.paste(alpha_img, (0, 0), alpha_img)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_speech_bubble_mom(output_path):
    """Slide 3: Speech bubble with '엄마'"""
    img = Image.new('RGB', (600, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(120, bold=True)

    # Speech bubble
    bubble_coords = [100, 80, 500, 280]
    draw.rounded_rectangle(bubble_coords, radius=30, fill=hex_to_rgb('#EFF6FF'),
                          outline=hex_to_rgb('#2563EB'), width=5)

    # Bubble tail
    tail_points = [(250, 280), (280, 350), (320, 280)]
    draw.polygon(tail_points, fill=hex_to_rgb('#EFF6FF'), outline=hex_to_rgb('#2563EB'))

    # Text
    draw.text((300, 180), "엄마", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_light_bulb(output_path):
    """Slide 3: Light bulb with sparkles"""
    img = Image.new('RGB', (600, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(400)

    # Light bulb
    draw.ellipse([180, 100, 420, 340], fill=hex_to_rgb('#FEF3C7'), outline=hex_to_rgb('#F59E0B'), width=5)
    draw.rectangle([250, 340, 350, 400], fill=hex_to_rgb('#D97706'), outline=hex_to_rgb('#B45309'), width=3)
    draw.rectangle([230, 400, 370, 440], fill=hex_to_rgb('#78350F'))

    # Sparkles
    sparkle_positions = [(100, 150), (500, 150), (150, 300), (450, 300)]
    for pos in sparkle_positions:
        draw.line([pos[0]-20, pos[1], pos[0]+20, pos[1]], fill=hex_to_rgb('#F59E0B'), width=4)
        draw.line([pos[0], pos[1]-20, pos[0], pos[1]+20], fill=hex_to_rgb('#F59E0B'), width=4)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_logo(output_path):
    """Slide 4: SoundToAct logo"""
    img = Image.new('RGB', (800, 300), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(80, bold=True)
    font_medium = get_font(40)

    # Logo text with gradient effect (simulated)
    draw.text((400, 120), "SoundToAct", font=font_huge, fill=hex_to_rgb('#2563EB'), anchor="mm")

    # Icon: Sound wave + Action arrow
    # Sound wave
    for i in range(5):
        x = 80 + i * 15
        draw.line([x, 200, x, 200-30-i*5], fill=hex_to_rgb('#10B981'), width=5)

    # Arrow
    draw_arrow(draw, (180, 215), (250, 215), hex_to_rgb('#7C3AED'), width=6)

    # Tagline
    draw.text((400, 230), "말 한마디로 움직이는 세상", font=font_medium,
             fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_demo_placeholder(output_path):
    """Slide 4: Demo video placeholder"""
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

    # Play triangle
    triangle = [(460, 260), (460, 340), (540, 300)]
    draw.polygon(triangle, fill=hex_to_rgb('#FFFFFF'))

    # Text
    draw.text((500, 450), "데모 영상", font=font_large, fill=hex_to_rgb('#374151'), anchor="mm")
    draw.text((500, 520), '"엄마한테 전화해줘"', font=font_medium, fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_three_steps(output_path):
    """Slide 5: Three-step process diagram"""
    img = Image.new('RGB', (1200, 500), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_num = get_font(80, bold=True)
    font_title = get_font(40, bold=True)
    font_icon = get_font(60)

    steps = [
        {'num': '1', 'title': '듣기', 'icon': '🎤', 'color': '#2563EB', 'x': 150},
        {'num': '2', 'title': '이해하기', 'icon': '🧠', 'color': '#7C3AED', 'x': 600},
        {'num': '3', 'title': '실행하기', 'icon': '⚡', 'color': '#10B981', 'x': 1050},
    ]

    for i, step in enumerate(steps):
        # Number circle
        draw.ellipse([step['x']-75, 50, step['x']+75, 200],
                    fill=hex_to_rgb(step['color']), outline=hex_to_rgb('#111827'), width=4)
        draw.text((step['x'], 125), step['num'], font=font_num,
                 fill=hex_to_rgb('#FFFFFF'), anchor="mm")

        # Title
        draw.text((step['x'], 280), step['title'], font=font_title,
                 fill=hex_to_rgb(step['color']), anchor="mm")

        # Icon
        draw.text((step['x'], 370), step['icon'], font=font_icon, anchor="mm")

        # Arrow to next step
        if i < len(steps) - 1:
            draw_arrow(draw, (step['x']+85, 125), (steps[i+1]['x']-85, 125),
                      hex_to_rgb('#111827'), width=5)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_live_demo(output_path):
    """Slide 6: Live demo placeholder"""
    img = Image.new('RGB', (1200, 700), hex_to_rgb('#1F2937'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(120, bold=True)
    font_large = get_font(60)

    # Center text
    draw.text((600, 250), "LIVE", font=font_huge, fill=hex_to_rgb('#EF4444'), anchor="mm")
    draw.text((600, 380), "DEMO", font=font_huge, fill=hex_to_rgb('#FFFFFF'), anchor="mm")

    # Pulsing circle effect
    for radius in [180, 200, 220]:
        draw.ellipse([600-radius, 350-radius, 600+radius, 350+radius],
                    outline=hex_to_rgb('#EF4444'), width=3)

    # Instructions
    draw.text((600, 550), '실제로 작동하는 모습을 보여드리겠습니다',
             font=font_large, fill=hex_to_rgb('#9CA3AF'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_before_after(output_path):
    """Slide 7: Before/After comparison"""
    img = Image.new('RGB', (1200, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_title = get_font(64, bold=True)
    font_large = get_font(48, bold=True)
    font_medium = get_font(40)

    # Before section (left)
    before_color = hex_to_rgb('#FEE2E2')
    draw.rectangle([0, 0, 595, 600], fill=before_color)
    draw.text((300, 80), "Before", font=font_title, fill=hex_to_rgb('#DC2626'), anchor="mm")
    draw.text((300, 200), "2분 걸림", font=font_large, fill=hex_to_rgb('#991B1B'), anchor="mm")

    # Complex steps
    for i in range(5):
        y = 280 + i * 60
        draw.rectangle([80, y, 520, y+40], fill=hex_to_rgb('#FCA5A5'),
                      outline=hex_to_rgb('#DC2626'), width=2)
        draw.text((300, y+20), f"단계 {i+1}", font=font_medium,
                 fill=hex_to_rgb('#7F1D1D'), anchor="mm")

    # After section (right)
    after_color = hex_to_rgb('#D1FAE5')
    draw.rectangle([605, 0, 1200, 600], fill=after_color)
    draw.text((900, 80), "After", font=font_title, fill=hex_to_rgb('#059669'), anchor="mm")
    draw.text((900, 200), "2초!", font=font_large, fill=hex_to_rgb('#047857'), anchor="mm")

    # Simple action
    draw.rectangle([680, 310, 1120, 390], fill=hex_to_rgb('#34D399'),
                  outline=hex_to_rgb('#059669'), width=3)
    draw.text((900, 350), '"엄마한테 전화해줘"', font=font_medium,
             fill=hex_to_rgb('#064E3B'), anchor="mm")

    # Speed comparison
    draw.text((900, 480), "60배 빨라짐!", font=font_large,
             fill=hex_to_rgb('#047857'), anchor="mm")

    # Divider line
    draw.line([600, 0, 600, 600], fill=hex_to_rgb('#6B7280'), width=5)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_inclusive_tech(output_path):
    """Slide 8: Inclusive technology - three personas"""
    img = Image.new('RGB', (1200, 500), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_title = get_font(48, bold=True)
    font_medium = get_font(36)

    # Title
    draw.text((600, 50), "모두를 위한 기술", font=font_title,
             fill=hex_to_rgb('#10B981'), anchor="mm")

    # Three personas
    personas = [
        {'title': '어르신', 'desc': '큰 글씨 필요없이', 'x': 200},
        {'title': '직장인', 'desc': '운전 중에도', 'x': 600},
        {'title': '장애인', 'desc': '손 사용 불편해도', 'x': 1000},
    ]

    for persona in personas:
        # Person icon (simplified)
        draw.ellipse([persona['x']-50, 150, persona['x']+50, 250],
                    fill=hex_to_rgb('#3B82F6'), outline=hex_to_rgb('#1E40AF'), width=3)
        draw.rectangle([persona['x']-60, 250, persona['x']+60, 350],
                      fill=hex_to_rgb('#7C3AED'), outline=hex_to_rgb('#5B21B6'), width=3)

        # Text
        draw.text((persona['x'], 380), persona['title'], font=font_medium,
                 fill=hex_to_rgb('#111827'), anchor="mm")
        draw.text((persona['x'], 430), persona['desc'], font=font_medium,
                 fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_world_connections(output_path):
    """Slide 9: World with connections"""
    img = Image.new('RGB', (800, 600), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)

    # Earth (center circle)
    earth_center = (400, 300)
    earth_radius = 150
    draw.ellipse([earth_center[0]-earth_radius, earth_center[1]-earth_radius,
                  earth_center[0]+earth_radius, earth_center[1]+earth_radius],
                 fill=hex_to_rgb('#3B82F6'), outline=hex_to_rgb('#10B981'), width=8)

    # Connection nodes around earth
    angles = [0, 45, 90, 135, 180, 225, 270, 315]
    node_distance = 250

    for angle_deg in angles:
        angle = math.radians(angle_deg)
        node_x = earth_center[0] + node_distance * math.cos(angle)
        node_y = earth_center[1] + node_distance * math.sin(angle)

        # Connection line
        line_start = (
            earth_center[0] + earth_radius * math.cos(angle),
            earth_center[1] + earth_radius * math.sin(angle)
        )
        draw.line([line_start, (node_x, node_y)], fill=hex_to_rgb('#10B981'), width=4)

        # Node circle
        node_radius = 25
        draw.ellipse([node_x-node_radius, node_y-node_radius,
                     node_x+node_radius, node_y+node_radius],
                    fill=hex_to_rgb('#7C3AED'), outline=hex_to_rgb('#5B21B6'), width=3)

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_bright_future(output_path):
    """Slide 9: Bright future illustration"""
    img = Image.new('RGB', (800, 600), hex_to_rgb('#FEF3C7'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(80, bold=True)

    # Rising sun
    draw.ellipse([200, 300, 600, 700], fill=hex_to_rgb('#F59E0B'),
                outline=hex_to_rgb('#D97706'), width=5)

    # Light rays
    for angle_deg in range(0, 180, 20):
        angle = math.radians(angle_deg)
        start_x = 400 + 150 * math.cos(angle)
        start_y = 500 + 150 * math.sin(angle)
        end_x = 400 + 300 * math.cos(angle)
        end_y = 500 + 300 * math.sin(angle)
        draw.line([(start_x, start_y), (end_x, end_y)],
                 fill=hex_to_rgb('#FBBF24'), width=8)

    # Text
    draw.text((400, 150), "밝은 미래", font=font_huge,
             fill=hex_to_rgb('#D97706'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_qr_code(output_path):
    """Slide 10: QR code placeholder"""
    img = Image.new('RGB', (400, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_medium = get_font(32)

    # QR code pattern (simplified)
    grid_size = 20
    cell_size = 15
    margin = 50

    # Simplified QR pattern
    import random
    random.seed(42)  # Consistent pattern
    for i in range(grid_size):
        for j in range(grid_size):
            if random.random() > 0.5:
                x = margin + j * cell_size
                y = margin + i * cell_size
                draw.rectangle([x, y, x+cell_size-2, y+cell_size-2],
                             fill=hex_to_rgb('#111827'))

    # Corner squares (typical QR markers)
    marker_size = 4 * cell_size
    for corner in [(margin, margin), (margin + 16*cell_size, margin),
                   (margin, margin + 16*cell_size)]:
        draw.rectangle([corner[0], corner[1], corner[0]+marker_size, corner[1]+marker_size],
                      outline=hex_to_rgb('#111827'), width=2)
        draw.rectangle([corner[0]+cell_size, corner[1]+cell_size,
                       corner[0]+marker_size-cell_size, corner[1]+marker_size-cell_size],
                      fill=hex_to_rgb('#111827'))

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def create_final_logo(output_path):
    """Slide 10: Final logo with tagline"""
    img = Image.new('RGB', (800, 400), hex_to_rgb('#FFFFFF'))
    draw = ImageDraw.Draw(img)
    font_huge = get_font(90, bold=True)
    font_large = get_font(48)
    font_medium = get_font(36)

    # Logo
    draw.text((400, 150), "SoundToAct", font=font_huge,
             fill=hex_to_rgb('#2563EB'), anchor="mm")

    # Tagline
    draw.text((400, 250), "말 한마디로 움직이는 세상", font=font_large,
             fill=hex_to_rgb('#7C3AED'), anchor="mm")

    # Bottom text
    draw.text((400, 330), "함께 만들어가요", font=font_medium,
             fill=hex_to_rgb('#6B7280'), anchor="mm")

    img.save(output_path)
    print(f"  ✓ Created: {output_path.name}")


def main():
    """Generate all images from ImageSpec.idr specifications"""
    base_dir = Path(__file__).parent
    images_dir = base_dir / 'images'
    images_dir.mkdir(exist_ok=True)

    print("="*60)
    print("Image Generator from ImageSpec.idr")
    print("="*60)
    print(f"\nGenerating 17 images to: {images_dir}")
    print()

    # Generate all images
    image_specs = [
        ('wave_animation.png', create_waveform_animation),
        ('mic_icon_large.png', create_mic_icon_large),
        ('morning_illustration.png', create_morning_illustration),
        ('complex_process.png', create_complex_process),
        ('question_mark.png', create_question_mark),
        ('speech_bubble_mom.png', create_speech_bubble_mom),
        ('light_bulb.png', create_light_bulb),
        ('logo.png', create_logo),
        ('demo_placeholder.png', create_demo_placeholder),
        ('three_steps.png', create_three_steps),
        ('live_demo.png', create_live_demo),
        ('before_after.png', create_before_after),
        ('inclusive_tech.png', create_inclusive_tech),
        ('world_connections.png', create_world_connections),
        ('bright_future.png', create_bright_future),
        ('qr_code.png', create_qr_code),
        ('final_logo.png', create_final_logo),
    ]

    for filename, create_func in image_specs:
        output_path = images_dir / filename
        create_func(output_path)

    print()
    print("="*60)
    print("✓ All 17 images generated successfully!")
    print("="*60)
    print(f"\nImages saved to: {images_dir}")


if __name__ == '__main__':
    main()
