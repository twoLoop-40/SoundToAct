#!/usr/bin/env python3
"""
Generate visual elements for presentation slides

Creates custom images, icons, and diagrams for each slide
using PIL (Pillow) and downloads free images from Unsplash.
"""

import os
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io


# Color palette
COLORS = {
    'primary': (37, 99, 235),      # Blue
    'secondary': (124, 58, 237),   # Purple
    'accent': (16, 185, 129),      # Green
    'warning': (245, 158, 11),     # Orange
    'bg_light': (255, 255, 255),   # White
    'bg_dark': (31, 41, 55),       # Dark gray
    'text': (17, 24, 39),          # Almost black
}


def create_gradient_background(width, height, color1, color2):
    """Create a gradient background"""
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.rectangle([(0, i), (width, i + 1)], fill=(r, g, b))

    return image


def create_icon_microphone(size=400):
    """Create a microphone icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Microphone body
    mic_color = COLORS['primary']
    center_x, center_y = size // 2, size // 2

    # Main microphone capsule
    draw.rounded_rectangle(
        [(center_x - 60, center_y - 120), (center_x + 60, center_y + 40)],
        radius=60, fill=mic_color
    )

    # Stand
    draw.rectangle(
        [(center_x - 10, center_y + 40), (center_x + 10, center_y + 120)],
        fill=mic_color
    )

    # Base
    draw.ellipse(
        [(center_x - 80, center_y + 100), (center_x + 80, center_y + 130)],
        fill=mic_color
    )

    # Grid lines on mic
    for i in range(-2, 3):
        y = center_y + i * 30
        draw.line(
            [(center_x - 40, y), (center_x + 40, y)],
            fill=(255, 255, 255, 180), width=3
        )

    return img


def create_waveform(width=800, height=200):
    """Create audio waveform visualization"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    import math
    mid_y = height // 2

    # Draw waveform
    for x in range(0, width, 3):
        amplitude = 60 * math.sin(x / 30) * (1 + 0.3 * math.sin(x / 100))
        y1 = int(mid_y - amplitude)
        y2 = int(mid_y + amplitude)

        # Gradient effect
        color_intensity = int(255 * (x / width))
        color = (COLORS['primary'][0], COLORS['primary'][1], color_intensity)

        draw.line([(x, y1), (x, y2)], fill=color, width=2)

    return img


def create_lightbulb_icon(size=400):
    """Create light bulb icon for ideas"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x, center_y = size // 2, size // 2

    # Bulb
    draw.ellipse(
        [(center_x - 80, center_y - 100), (center_x + 80, center_y + 60)],
        fill=COLORS['warning'], outline=COLORS['text'], width=5
    )

    # Base
    draw.rectangle(
        [(center_x - 40, center_y + 60), (center_x + 40, center_y + 100)],
        fill=COLORS['text']
    )

    # Light rays
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        import math
        rad = math.radians(angle)
        x1 = center_x + int(100 * math.cos(rad))
        y1 = center_y + int(100 * math.sin(rad))
        x2 = center_x + int(150 * math.cos(rad))
        y2 = center_y + int(150 * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=COLORS['warning'], width=8)

    return img


def create_question_mark(size=400):
    """Create question mark icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try to use a font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 300)
    except:
        font = ImageFont.load_default()

    # Draw question mark
    text = "?"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((size - text_width) // 2, (size - text_height) // 2 - 50)
    draw.text(position, text, fill=COLORS['secondary'], font=font)

    return img


def create_speech_bubble(width=600, height=300, text="엄마"):
    """Create speech bubble with text"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Bubble
    draw.rounded_rectangle(
        [(50, 50), (width - 50, height - 100)],
        radius=30, fill=COLORS['bg_light'], outline=COLORS['primary'], width=5
    )

    # Tail
    draw.polygon(
        [(100, height - 100), (80, height - 50), (150, height - 100)],
        fill=COLORS['bg_light'], outline=COLORS['primary']
    )

    # Text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 100)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (width - text_width) // 2
    text_y = (height - 100 - text_height) // 2 + 50

    draw.text((text_x, text_y), text, fill=COLORS['text'], font=font)

    return img


def create_before_after_comparison(width=800, height=400):
    """Create Before/After comparison visual"""
    img = Image.new('RGB', (width, height), COLORS['bg_light'])
    draw = ImageDraw.Draw(img)

    mid_x = width // 2

    # Before (left side) - complicated
    draw.rectangle([(0, 0), (mid_x - 10, height)], fill=(250, 200, 200))

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((50, 50), "Before", fill=COLORS['warning'], font=font_large)
    draw.text((50, 150), "2분 소요", fill=COLORS['text'], font=font_small)

    # Draw complex process arrows
    for i in range(5):
        y = 220 + i * 30
        draw.rectangle([(50, y), (mid_x - 60, y + 20)], fill=COLORS['warning'])
        if i < 4:
            draw.polygon(
                [(mid_x - 100, y + 30), (mid_x - 80, y + 25), (mid_x - 100, y + 20)],
                fill=COLORS['warning']
            )

    # After (right side) - simple
    draw.rectangle([(mid_x + 10, 0), (width, height)], fill=(200, 250, 200))

    draw.text((mid_x + 50, 50), "After", fill=COLORS['accent'], font=font_large)
    draw.text((mid_x + 50, 150), "2초!", fill=COLORS['text'], font=font_small)

    # Single arrow
    draw.rectangle([(mid_x + 50, 220), (width - 50, 260)], fill=COLORS['accent'])

    # 60x faster
    draw.text((mid_x + 50, 300), "60배 빠름!", fill=COLORS['accent'], font=font_small)

    return img


def create_three_step_diagram(width=1200, height=400):
    """Create 3-step process diagram"""
    img = Image.new('RGB', (width, height), COLORS['bg_light'])
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        font_num = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except:
        font_title = ImageFont.load_default()
        font_num = ImageFont.load_default()

    step_width = width // 3
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['accent']]
    steps = ["듣기", "이해하기", "실행하기"]

    for i in range(3):
        x = i * step_width + 50

        # Circle with number
        draw.ellipse(
            [(x, 50), (x + 150, 200)],
            fill=colors[i]
        )

        # Number
        num_text = str(i + 1)
        bbox = draw.textbbox((0, 0), num_text, font=font_num)
        num_width = bbox[2] - bbox[0]
        draw.text((x + 75 - num_width // 2, 90), num_text, fill=(255, 255, 255), font=font_num)

        # Step name
        draw.text((x, 250), steps[i], fill=colors[i], font=font_title)

        # Arrow to next step
        if i < 2:
            arrow_x = x + 200
            draw.polygon(
                [(arrow_x, 120), (arrow_x + 80, 120), (arrow_x + 100, 125), (arrow_x + 80, 130), (arrow_x, 130)],
                fill=COLORS['text']
            )

    return img


def create_inclusive_tech_diagram(width=900, height=400):
    """Create inclusive technology diagram showing different users"""
    img = Image.new('RGB', (width, height), COLORS['bg_light'])
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 30)
    except:
        font = ImageFont.load_default()

    # Three personas
    personas = [
        ("어르신", (150, 200)),
        ("직장인", (450, 200)),
        ("장애인", (750, 200))
    ]

    for i, (name, pos) in enumerate(personas):
        # Draw person icon (simple circle + body)
        # Head
        draw.ellipse(
            [(pos[0] - 40, pos[1] - 100), (pos[0] + 40, pos[1] - 20)],
            fill=COLORS['primary']
        )

        # Body
        draw.rectangle(
            [(pos[0] - 50, pos[1] - 20), (pos[0] + 50, pos[1] + 50)],
            fill=COLORS['secondary']
        )

        # Label
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((pos[0] - text_width // 2, pos[1] + 80), name, fill=COLORS['text'], font=font)

    # Center text
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/AppleSDGothicNeo.ttc", 50)
    except:
        font_large = ImageFont.load_default()

    center_text = "모두를 위한 기술"
    bbox = draw.textbbox((0, 0), center_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, 30), center_text, fill=COLORS['accent'], font=font_large)

    return img


def create_world_connections(width=800, height=600):
    """Create world with connected people icon"""
    img = Image.new('RGB', (width, height), COLORS['bg_light'])
    draw = ImageDraw.Draw(img)

    # Center circle (globe)
    center_x, center_y = width // 2, height // 2
    radius = 150

    draw.ellipse(
        [(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)],
        fill=COLORS['primary'], outline=COLORS['accent'], width=5
    )

    # Draw connections (lines radiating out)
    import math
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1 = center_x + int(radius * math.cos(rad))
        y1 = center_y + int(radius * math.sin(rad))
        x2 = center_x + int((radius + 100) * math.cos(rad))
        y2 = center_y + int((radius + 100) * math.sin(rad))

        draw.line([(x1, y1), (x2, y2)], fill=COLORS['accent'], width=3)

        # Small circle at end (person)
        draw.ellipse(
            [(x2 - 20, y2 - 20), (x2 + 20, y2 + 20)],
            fill=COLORS['secondary']
        )

    return img


def download_unsplash_image(query, width=800, height=600):
    """Download free image from Unsplash (no API key needed for basic usage)"""
    # Unsplash Source URL (free, no API key needed)
    url = f"https://source.unsplash.com/{width}x{height}/?{query}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            return img
    except Exception as e:
        print(f"Failed to download image for '{query}': {e}")

    return None


def generate_all_images():
    """Generate all images for presentation"""
    output_dir = Path(__file__).parent / 'images'
    output_dir.mkdir(exist_ok=True)

    print("="*60)
    print("GENERATING PRESENTATION IMAGES")
    print("="*60)

    images = {
        # Slide 1: Title
        'wave_animation.png': lambda: create_waveform(1000, 300),
        'mic_icon_large.png': lambda: create_icon_microphone(500),

        # Slide 2: Morning
        'morning_wake_up.jpg': lambda: download_unsplash_image('student,morning,bed', 800, 600),

        # Slide 3: Big idea
        'question_mark.png': lambda: create_question_mark(500),
        'speech_bubble_mom.png': lambda: create_speech_bubble(600, 300, "엄마"),
        'light_bulb.png': lambda: create_lightbulb_icon(500),

        # Slide 4: Solution
        'demo_video_placeholder.jpg': lambda: download_unsplash_image('phone,calling', 800, 600),

        # Slide 5: How it works
        'three_steps.png': lambda: create_three_step_diagram(1200, 400),

        # Slide 6: Demo
        'live_demo.jpg': lambda: download_unsplash_image('technology,voice', 1000, 600),

        # Slide 7: Impact
        'before_after.png': lambda: create_before_after_comparison(1000, 500),

        # Slide 8: For others
        'inclusive_tech.png': lambda: create_inclusive_tech_diagram(900, 400),

        # Slide 9: Dream
        'world_connections.png': lambda: create_world_connections(800, 600),
        'bright_future.jpg': lambda: download_unsplash_image('future,technology,bright', 800, 600),
    }

    for filename, generator in images.items():
        filepath = output_dir / filename
        print(f"Creating {filename}...")

        try:
            img = generator()
            if img:
                img.save(filepath)
                print(f"  ✓ Saved to {filepath}")
            else:
                print(f"  ✗ Failed to generate")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print("="*60)
    print(f"✓ Images saved to: {output_dir}")
    print("="*60)


if __name__ == '__main__':
    generate_all_images()
