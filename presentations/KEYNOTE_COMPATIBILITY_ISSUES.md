# Keynote Compatibility Issues

## 문제 상황

python-pptx로 생성한 PowerPoint 파일이 Mac Keynote에서 열리지 않음

### 에러 메시지
```
'SoundToAct_Presentation_Final.pptx'을(를) 가져올 수 없습니다.
```

### 환경
- OS: macOS (Darwin 24.6.0)
- Python: 3.13.5
- python-pptx: 1.0.2
- 설치된 앱: Keynote (PowerPoint 없음)

## 시도한 해결 방법

### 1. AUTO_SHAPE 제거
- 변경: `MSO_SHAPE.ROUNDED_RECTANGLE` → 일반 `TEXT_BOX`
- 결과: ❌ 여전히 열리지 않음

### 2. Extended Attributes 제거
```bash
xattr -c file.pptx
```
- 결과: ❌ 여전히 열리지 않음

### 3. 초간단 버전 생성
- 기본 템플릿 사용
- 텍스트 박스만 사용
- 모든 커스텀 도형 제거
- 결과: ❌ 여전히 열리지 않음

### 4. 성공한 케이스
- `TEST_Simple.pptx` (28KB): ✅ 열림
  - 1개 슬라이드
  - 2개 텍스트 박스만
  - 최소한의 내용

## 문제 원인 추정

1. **슬라이드 수**: 간단한 1슬라이드는 열리지만 10슬라이드는 안 열림
2. **한글 인코딩**: 한글 텍스트가 많을 때 Keynote 호환성 문제
3. **python-pptx 한계**: Keynote는 Microsoft PowerPoint와 100% 호환이 아님

## 다음 시도할 방법

### 방법 1: LibreOffice 사용
```bash
# LibreOffice로 변환
libreoffice --headless --convert-to pptx input.odp
```

### 방법 2: Microsoft PowerPoint 설치
- Microsoft 365 구독 또는 PowerPoint 단독 구매

### 방법 3: PDF 변환
```python
# python-pptx로 생성 후 외부 도구로 PDF 변환
```

### 방법 4: HTML 프레젠테이션
- reveal.js 또는 impress.js 사용
- 웹 브라우저에서 프레젠테이션

### 방법 5: Google Slides API
- Google Slides로 직접 생성
- 브라우저에서 열기 또는 PowerPoint로 다운로드

## 현재 작업 파일

### JSON 데이터 (✅ 완료)
- `output/presentation_from_idris.json`
- Presentation.idr의 모든 내용 포함
- 기술 스택, 발표자 노트 포함

### Python 생성 스크립트 (✅ 작동)
- `slides_from_idris.py` - JSON 생성
- `create_text_based_ppt.py` - PowerPoint 생성 (Keynote 호환 안 됨)
- `create_simple_compatible_ppt.py` - 간단 버전 (Keynote 호환 안 됨)

### 생성된 파일
- `SoundToAct_TextBased_Presentation.pptx` - Python 검증 성공, Keynote 실패
- `SoundToAct_Simple.pptx` - Python 검증 성공, Keynote 실패
- `TEST_Simple.pptx` - ✅ Keynote 성공 (1슬라이드만)

## 권장 해결책

**단기**: Microsoft PowerPoint 설치 또는 LibreOffice 사용
**장기**: Google Slides API 또는 HTML 프레젠테이션으로 전환
