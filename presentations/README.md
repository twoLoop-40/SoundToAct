# SoundToAct Presentation Generator

Complete workflow for generating a type-safe, validated PowerPoint presentation using Idris2 specifications.

## Overview

This project uses **formal specifications in Idris2** to ensure type-safety and correctness of the presentation structure, content, and images. All images and slides are validated against the specifications.

## Workflow

```
Idris2 Specs → JSON → Images → PowerPoint → Validation
```

### 1. Define Specifications (Idris2)

- **`Presentation.idr`**: Main presentation structure (10 slides)
  - Story-driven narrative
  - Visual-focused design
  - Minimal text, maximum impact

- **`ImageSpec.idr`**: Detailed image specifications
  - Text elements (content, position, size, color)
  - Shape elements (type, position, size, colors)
  - All 17 images fully specified

### 2. Compile and Validate Specs

```bash
idris2 --check Presentation.idr
idris2 --check ImageSpec.idr
```

Type-safe compilation ensures correctness at specification level.

### 3. Generate JSON from Idris

```bash
python3 slides_from_idris.py
```

Converts Idris definitions to JSON format for Python consumption.
Output: `output/presentation_from_idris.json`

### 4. Generate Images

```bash
python3 generate_images_from_spec.py
```

Creates all 17 images following ImageSpec.idr specifications:
- Waveform animations
- Icons (mic, question mark, light bulb)
- Process diagrams (3-step flow, complex process)
- Comparison charts (before/after)
- Illustrations (morning, inclusive tech, world connections)
- Logo and branding
- Demo placeholders
- QR code

Output: `images/*.png` (17 images)

### 5. Create PowerPoint

```bash
python3 create_pptx_with_images.py
```

Generates final PowerPoint with all images and content.
Output: `output/SoundToAct_Presentation_WithImages.pptx`

### 6. Validate Against Specifications

```bash
python3 validate_ppt.py
```

Validates that:
- Slide count matches specification
- All expected images are present
- Text content matches specification
- All image files exist

Exit code: 0 if validation passes, 1 if issues found.

## File Structure

```
presentations/
├── README.md                           # This file
│
├── Presentation.idr                    # Main presentation specification
├── ImageSpec.idr                       # Image specifications
├── PRESENTATION_SPEC.md                # Human-readable spec
│
├── slides_from_idris.py                # Idris → JSON converter
├── generate_images_from_spec.py        # Image generator
├── create_pptx_with_images.py          # PowerPoint generator
├── validate_ppt.py                     # Validation script
│
├── images/                             # Generated images (17 files)
│   ├── wave_animation.png
│   ├── mic_icon_large.png
│   ├── three_steps.png
│   ├── before_after.png
│   └── ...
│
├── output/                             # Generated files
│   ├── presentation_from_idris.json    # Intermediate JSON
│   └── SoundToAct_Presentation_WithImages.pptx
│
├── build/                              # Idris2 build artifacts
└── archive/                            # Old versions
```

## Design Principles

### Story-Driven Narrative

1. **Title**: Hook the audience
2. **Problem**: Personal story (relatable)
3. **Idea**: The "aha!" moment
4. **Solution**: Introduce SoundToAct
5. **How**: Simple 3-step process
6. **Demo**: Show, don't just tell
7. **Impact**: Before/After comparison
8. **For Others**: Safety & Inclusive design (Emergency situations, elderly, workers, disabilities)
9. **Dream**: Bigger vision
10. **Thank You**: Call to action

### Visual-Focused Design

- Minimal text (2-4 lines per slide)
- 1-4 visuals per slide
- High contrast colors
- Large, clear images
- Emoji for emotion

### Type-Safety

- Idris2 ensures specifications are well-formed
- Dependent types prevent common errors
- Total functions guarantee termination
- Validation script ensures implementation matches spec

## Requirements

```bash
# Idris2 (for specification)
brew install idris2

# Python dependencies (for generation)
pip install python-pptx Pillow
```

## Quick Start

```bash
# Full workflow
idris2 --check Presentation.idr
idris2 --check ImageSpec.idr
python3 slides_from_idris.py
python3 generate_images_from_spec.py
python3 create_pptx_with_images.py
python3 validate_ppt.py
```

If validation passes (100% success rate), you're done!

## Customization

### Add New Slides

1. Update `Presentation.idr` with new slide definition
2. Recompile: `idris2 --check Presentation.idr`
3. Update `slides_from_idris.py` if needed
4. Regenerate everything

### Add New Images

1. Add specification to `ImageSpec.idr`
2. Recompile: `idris2 --check ImageSpec.idr`
3. Update `generate_images_from_spec.py` with new image function
4. Update `create_pptx_with_images.py` with new mapping
5. Regenerate and validate

### Modify Design

Update color palette in `create_pptx_with_images.py`:

```python
COLORS = {
    'primary': RGBColor(37, 99, 235),    # Blue
    'secondary': RGBColor(124, 58, 237),  # Purple
    'accent': RGBColor(16, 185, 129),     # Green
    'warning': RGBColor(245, 158, 11),    # Orange
}
```

## Key Features

### Safety-First Design (Slide 8)

The presentation now emphasizes **emergency safety** as a core use case:

**🚨 Emergency Situations:**
- Voice activation works even when you can't find your phone
- Say "Mom" to instantly call for help in dangerous situations
- No need to look at the screen - hands-free emergency contact

**Additional Use Cases:**
- 👴 **Elderly**: No need to read small text or navigate complex UIs
- 💼 **Busy Workers**: Hands-free operation while driving or multitasking
- ♿ **Disabilities**: Full voice control for visual/physical impairments

This positions SoundToAct not just as a convenience tool, but as a **safety and accessibility solution**.

## Validation Results

Latest validation (2025-10-26):
```
Checks passed: 48/48
Success rate: 100.0%
✓ All validations passed!
```

## License

MIT License - See parent directory

## Author

Created for the SoundToAct project - voice-activated automation for everyone.
