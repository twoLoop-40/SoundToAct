#!/usr/bin/env python3
"""
PPT Content Generator for SoundToAct Presentation

This script reads the presentation specification (PRESENTATION_SPEC.md)
and generates structured content that can be used to create PowerPoint slides.
"""

import re
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from pathlib import Path


@dataclass
class Slide:
    """Represents a single slide in the presentation"""
    number: int
    title: str
    subtitle: Optional[str]
    layout: str
    content: List[str]
    code_blocks: List[Dict[str, str]]
    visuals: List[str]
    speaker_notes: Optional[str]
    estimated_time: int  # in seconds


@dataclass
class Presentation:
    """Represents the complete presentation"""
    title: str
    subtitle: str
    presenter: str
    date: str
    target_audience: str
    duration: str
    total_slides: int
    slides: List[Slide]

    def to_dict(self):
        """Convert presentation to dictionary"""
        return {
            'metadata': {
                'title': self.title,
                'subtitle': self.subtitle,
                'presenter': self.presenter,
                'date': self.date,
                'target_audience': self.target_audience,
                'duration': self.duration,
                'total_slides': self.total_slides
            },
            'slides': [asdict(slide) for slide in self.slides]
        }

    def to_json(self, indent=2):
        """Convert presentation to JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_markdown(self):
        """Convert presentation to markdown format"""
        md = f"# {self.title}\n\n"
        md += f"**{self.subtitle}**\n\n"
        md += f"- **발표자**: {self.presenter}\n"
        md += f"- **대상**: {self.target_audience}\n"
        md += f"- **시간**: {self.duration}\n"
        md += f"- **슬라이드 수**: {self.total_slides}\n\n"
        md += "---\n\n"

        for slide in self.slides:
            md += f"## Slide {slide.number}: {slide.title}\n\n"
            if slide.subtitle:
                md += f"*{slide.subtitle}*\n\n"

            md += f"**Layout**: {slide.layout}\n\n"

            if slide.content:
                md += "**Content**:\n"
                for line in slide.content:
                    md += f"{line}\n"
                md += "\n"

            if slide.code_blocks:
                for code in slide.code_blocks:
                    md += f"```{code.get('language', '')}\n"
                    md += code.get('code', '') + "\n"
                    md += "```\n\n"

            if slide.visuals:
                md += "**Visuals**:\n"
                for visual in slide.visuals:
                    md += f"- {visual}\n"
                md += "\n"

            if slide.speaker_notes:
                md += f"**Speaker Notes**: {slide.speaker_notes}\n\n"

            md += f"**Estimated Time**: {slide.estimated_time}s\n\n"
            md += "---\n\n"

        return md


def parse_specification(spec_path: Path) -> Presentation:
    """Parse PRESENTATION_SPEC.md and extract slide information"""

    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata
    metadata = {}
    meta_pattern = r'- \*\*([^*]+)\*\*: (.+)'
    for match in re.finditer(meta_pattern, content):
        key = match.group(1)
        value = match.group(2)
        metadata[key] = value

    # Parse slides
    slides = []
    slide_pattern = r'### 슬라이드 (\d+): ([^\n]+)'
    slide_matches = list(re.finditer(slide_pattern, content))

    for i, match in enumerate(slide_matches):
        slide_num = int(match.group(1))
        slide_title = match.group(2)

        # Get content between this slide and the next
        start = match.end()
        end = slide_matches[i + 1].start() if i + 1 < len(slide_matches) else content.find('## 디자인 가이드라인')
        slide_content = content[start:end]

        # Extract slide components
        subtitle = extract_subtitle(slide_content)
        layout = extract_layout(slide_content)
        body = extract_body(slide_content)
        code_blocks = extract_code_blocks(slide_content)
        visuals = extract_visuals(slide_content)
        speaker_notes = extract_speaker_notes(slide_content)
        estimated_time = estimate_time(slide_content)

        slide = Slide(
            number=slide_num,
            title=slide_title,
            subtitle=subtitle,
            layout=layout,
            content=body,
            code_blocks=code_blocks,
            visuals=visuals,
            speaker_notes=speaker_notes,
            estimated_time=estimated_time
        )
        slides.append(slide)

    presentation = Presentation(
        title="SoundToAct",
        subtitle="음성으로 트리거하는 자동화 시스템",
        presenter=metadata.get('발표자', 'TBD'),
        date="2025-10-26",
        target_audience=metadata.get('대상 청중', '선생님, 개발자'),
        duration=metadata.get('예상 발표 시간', '10-15분'),
        total_slides=int(metadata.get('슬라이드 수', '12').replace('장', '')),
        slides=slides
    )

    return presentation


def extract_subtitle(content: str) -> Optional[str]:
    """Extract subtitle from slide content"""
    match = re.search(r'\*\*부제목\*\*\n```\n(.+?)\n```', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_layout(content: str) -> str:
    """Determine slide layout from visual description"""
    if '타이틀' in content or 'TitleSlide' in content:
        return 'TitleSlide'
    elif '4개' in content and ('박스' in content or '그리드' in content):
        return 'FourQuadrant'
    elif '3개' in content and '컬럼' in content:
        return 'ThreeColumn'
    elif '2개' in content or '좌우' in content:
        return 'TwoColumn'
    elif '전체' in content or '데모' in content:
        return 'FullScreenDemo'
    else:
        return 'SingleColumn'


def extract_body(content: str) -> List[str]:
    """Extract body content from slide"""
    lines = []

    # Extract content sections
    sections = [
        r'\*\*내용\*\*\n(.+?)(?=\n\*\*|\n---|\Z)',
        r'\*\*시나리오.*?\*\*\n(.+?)(?=\n\*\*|\n---|\Z)',
        r'\*\*핵심.*?\*\*\n(.+?)(?=\n\*\*|\n---|\Z)',
        r'\*\*메트릭.*?\*\*\n(.+?)(?=\n\*\*|\n---|\Z)',
    ]

    for pattern in sections:
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            # Clean up and split by lines
            for line in match.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('```'):
                    lines.append(line)

    return lines


def extract_code_blocks(content: str) -> List[Dict[str, str]]:
    """Extract code blocks from slide content"""
    code_blocks = []
    pattern = r'```(\w+)?\n(.+?)\n```'

    for match in re.finditer(pattern, content, re.DOTALL):
        language = match.group(1) or 'text'
        code = match.group(2).strip()
        code_blocks.append({
            'language': language,
            'code': code
        })

    return code_blocks


def extract_visuals(content: str) -> List[str]:
    """Extract visual descriptions from slide"""
    visuals = []

    # Look for visual section
    visual_match = re.search(r'\*\*비주얼\*\*\n(.+?)(?=\n---|\n\*\*|\Z)', content, re.DOTALL)
    if visual_match:
        visual_content = visual_match.group(1)
        for line in visual_content.split('\n'):
            line = line.strip()
            if line.startswith('-'):
                visuals.append(line[1:].strip())

    return visuals


def extract_speaker_notes(content: str) -> Optional[str]:
    """Extract speaker notes if present"""
    # This is a placeholder - actual speaker notes would need to be added to the spec
    return None


def estimate_time(content: str) -> int:
    """Estimate presentation time for slide in seconds"""
    # Simple heuristic based on content length
    word_count = len(content.split())
    # Assume 150 words per minute speaking speed
    estimated_seconds = (word_count / 150) * 60
    # Minimum 30 seconds, maximum 5 minutes
    return max(30, min(300, int(estimated_seconds)))


def main():
    """Main function to generate presentation content"""
    # Get spec file path
    spec_path = Path(__file__).parent / 'PRESENTATION_SPEC.md'

    if not spec_path.exists():
        print(f"Error: Specification file not found: {spec_path}")
        return

    print("Parsing presentation specification...")
    presentation = parse_specification(spec_path)

    print(f"✓ Parsed {presentation.total_slides} slides")
    print(f"✓ Total slides found: {len(presentation.slides)}")

    # Generate outputs
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)

    # Save as JSON
    json_path = output_dir / 'presentation.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(presentation.to_json())
    print(f"✓ Generated JSON: {json_path}")

    # Save as Markdown
    md_path = output_dir / 'presentation.md'
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(presentation.to_markdown())
    print(f"✓ Generated Markdown: {md_path}")

    # Print summary
    print("\n" + "="*60)
    print("PRESENTATION SUMMARY")
    print("="*60)
    print(f"Title: {presentation.title}")
    print(f"Slides: {len(presentation.slides)}")
    print(f"Duration: {presentation.duration}")
    print(f"Target: {presentation.target_audience}")
    print("\nSlides:")
    for slide in presentation.slides:
        print(f"  {slide.number}. {slide.title} ({slide.layout}) - {slide.estimated_time}s")
    print("="*60)


if __name__ == '__main__':
    main()
