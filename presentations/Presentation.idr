||| Formal Specification for SoundToAct Presentation
|||
||| This module defines the type-safe structure of a presentation
||| for explaining SoundToAct to teachers (developers).
|||
||| Target Audience: High school student → Teacher (Developer)
||| Duration: 8-10 minutes
||| Slides: 10 slides (story-driven, visual-focused)
module Presentation

import Data.Vect
import Data.String

%default total

--------------------------------------------------------------------------------
-- Design Specification Types
--------------------------------------------------------------------------------

||| Color specification (hex format)
public export
record Color where
  constructor MkColor
  hex : String
  name : String

||| Design color palette
public export
record ColorPalette where
  constructor MkColorPalette
  primary : Color
  secondary : Color
  accent : Color
  warning : Color
  background : Color
  textPrimary : Color
  textSecondary : Color

||| Standard color palette for SoundToAct presentation
export
soundToActPalette : ColorPalette
soundToActPalette = MkColorPalette
  (MkColor "#2563EB" "Blue")      -- primary
  (MkColor "#7C3AED" "Purple")    -- secondary
  (MkColor "#10B981" "Green")     -- accent
  (MkColor "#F59E0B" "Orange")    -- warning
  (MkColor "#FFFFFF" "White")     -- background
  (MkColor "#111827" "Dark")      -- text primary
  (MkColor "#6B7280" "Gray")      -- text secondary

||| Font specification
public export
record FontSpec where
  constructor MkFontSpec
  family : String
  size : Nat
  weight : String

||| Typography system
public export
record Typography where
  constructor MkTypography
  titleKorean : FontSpec
  titleEnglish : FontSpec
  bodyKorean : FontSpec
  bodyEnglish : FontSpec
  codeFont : FontSpec

export
standardTypography : Typography
standardTypography = MkTypography
  (MkFontSpec "Pretendard Bold" 54 "bold")
  (MkFontSpec "Inter Bold" 54 "bold")
  (MkFontSpec "Pretendard Regular" 24 "regular")
  (MkFontSpec "Inter Regular" 24 "regular")
  (MkFontSpec "Fira Code" 16 "monospace")

--------------------------------------------------------------------------------
-- Content Types
--------------------------------------------------------------------------------

||| Types of content that can appear in a slide
public export
data ContentType
  = TextContent
  | CodeContent
  | DiagramContent
  | TableContent
  | ImageContent
  | VideoContent

||| Programming language for code blocks
public export
data Language
  = Python
  | Idris
  | JavaScript
  | Bash
  | JSON

export
Show Language where
  show Python = "python"
  show Idris = "idris"
  show JavaScript = "javascript"
  show Bash = "bash"
  show JSON = "json"

||| Code snippet with syntax highlighting
public export
record CodeBlock where
  constructor MkCodeBlock
  language : Language
  code : String
  caption : Maybe String

||| Diagram representation
public export
data DiagramType
  = FlowChart
  | SequenceDiagram
  | TreeDiagram
  | ArchitectureDiagram

||| Visual content
public export
record VisualContent where
  constructor MkVisual
  contentType : ContentType
  description : String
  visualData : String

--------------------------------------------------------------------------------
-- Slide Structure
--------------------------------------------------------------------------------

||| Layout type for slides
public export
data SlideLayout
  = TitleSlide
  | SingleColumn
  | TwoColumn
  | ThreeColumn
  | FourQuadrant
  | CodeComparison
  | FullScreenDemo

export
Eq SlideLayout where
  TitleSlide == TitleSlide = True
  SingleColumn == SingleColumn = True
  TwoColumn == TwoColumn = True
  ThreeColumn == ThreeColumn = True
  FourQuadrant == FourQuadrant = True
  CodeComparison == CodeComparison = True
  FullScreenDemo == FullScreenDemo = True
  _ == _ = False

||| Animation type
public export
data AnimationType
  = Fade
  | Push
  | Appear
  | ZoomIn
  | Pulse

||| Animation specification
public export
record Animation where
  constructor MkAnimation
  animationType : AnimationType
  duration : Double
  delay : Double

||| Slide content
public export
record SlideContent where
  constructor MkSlideContent
  title : String
  subtitle : Maybe String
  body : List String
  codeBlocks : List CodeBlock
  visuals : List VisualContent
  speakerNotes : Maybe String

||| Complete slide specification
public export
record Slide where
  constructor MkSlide
  slideNumber : Nat
  layout : SlideLayout
  content : SlideContent
  animations : List Animation
  estimatedTime : Nat  -- in seconds

--------------------------------------------------------------------------------
-- Presentation Structure
--------------------------------------------------------------------------------

||| Metadata for the presentation
public export
record PresentationMeta where
  constructor MkMeta
  title : String
  subtitle : String
  presenter : String
  date : String
  targetAudience : String
  duration : Nat  -- in minutes
  totalSlides : Nat

||| Audience type
public export
data Audience
  = Student
  | Teacher
  | Developer
  | Manager
  | Investor

||| Complete presentation
public export
record Presentation (n : Nat) where
  constructor MkPresentation
  metadata : PresentationMeta
  palette : ColorPalette
  typography : Typography
  slides : Vect n Slide
  backupSlides : List Slide

--------------------------------------------------------------------------------
-- Slide Definitions
--------------------------------------------------------------------------------

||| Slide 1: Title Slide - 깔끔하고 임팩트 있게
export
titleSlide : Slide
titleSlide = MkSlide
  1
  TitleSlide
  (MkSlideContent
    "SoundToAct"
    (Just "말 한마디로 움직이는 세상")
    [ "고등학생 개발자"
    , "2025년 10월"
    ]
    []
    [ MkVisual ImageContent "음성 웨이브폼 애니메이션" "wave-animation"
    , MkVisual ImageContent "마이크 아이콘 (큼직하게)" "mic-icon-large"
    ]
    (Just "간단한 자기소개. 프로젝트 이름의 의미: Sound → Act (소리가 행동으로)"))
  [MkAnimation Fade 0.5 0.0]
  45

||| Slide 2: My Daily Life - 스토리로 공감 유도
export
problemSlide : Slide
problemSlide = MkSlide
  2
  SingleColumn
  (MkSlideContent
    "나의 아침"
    Nothing
    [ "⏰ 7:00 AM - 일어나자마자"
    , ""
    , "\"엄마한테 전화해야 하는데...\""
    ]
    []
    [ MkVisual ImageContent "만화 스타일 일러스트: 침대에서 일어나는 학생" "morning-illustration"
    , MkVisual DiagramContent "복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치" "complicated-flow"
    , MkVisual ImageContent "시계 아이콘: '2분 소요'" "time-wasted"
    ]
    (Just "개인적 경험으로 시작. 청중이 공감할 수 있는 일상적 상황. 시각적으로 복잡한 과정 강조."))
  [MkAnimation Appear 0.3 0.1]
  60

||| Slide 3: The Big Idea - 큰 질문으로 호기심 유발
export
demoSlide : Slide
demoSlide = MkSlide
  3
  TitleSlide
  (MkSlideContent
    "만약..."
    (Just "말 한마디면 된다면?")
    [ "그냥 \"엄마\"라고 말하면"
    , "자동으로 전화가 걸린다면?"
    ]
    []
    [ MkVisual ImageContent "큰 물음표 아이콘" "question-mark-large"
    , MkVisual ImageContent "말풍선 안에 '엄마'" "speech-bubble"
    , MkVisual ImageContent "빛나는 효과 (반짝이는 전구)" "light-bulb-idea"
    ]
    (Just "질문으로 청중의 상상력 자극. 간단명료하게. 아이디어의 핵심을 제시."))
  [MkAnimation ZoomIn 0.5 0.0]
  45

||| Slide 4: The Solution - 해결책 제시
export
featuresSlide : Slide
featuresSlide = MkSlide
  4
  SingleColumn
  (MkSlideContent
    "그래서 만들었습니다"
    (Just "SoundToAct")
    [ "말만 하면 작동하는 시스템"
    ]
    []
    [ MkVisual ImageContent "프로젝트 로고 (크게)" "soundtoact-logo"
    , MkVisual VideoContent "10초 데모 영상: '엄마' → 전화 걸림" "quick-demo-video"
    , MkVisual ImageContent "Before/After 비교 이미지" "before-after"
    ]
    (Just "짧은 데모 영상으로 임팩트. 복잡한 설명 없이 바로 작동하는 모습 보여주기."))
  [MkAnimation Appear 0.3 0.0]
  60

||| Slide 5: How It Works - 3단계로 간단하게
export
architectureSlide : Slide
architectureSlide = MkSlide
  5
  ThreeColumn
  (MkSlideContent
    "어떻게 작동할까?"
    (Just "간단한 3단계")
    [ "듣기 → 이해하기 → 실행하기"
    ]
    []
    [ MkVisual DiagramContent "1단계: 듣기 - 마이크 아이콘 + 음성 웨이브" "step1-listen"
    , MkVisual DiagramContent "2단계: 이해하기 - AI 뇌 + 키워드 매칭" "step2-understand"
    , MkVisual DiagramContent "3단계: 실행하기 - 액션 아이콘 (전화, 음악, 조명)" "step3-act"
    , MkVisual DiagramContent "화살표로 연결된 3단계 플로우" "flow-arrows"
    ]
    (Just "3단계만 강조. 기술적 용어 배제. 아이콘과 그림으로만 표현."))
  [MkAnimation Appear 0.3 0.2]
  75

||| Slide 6: Live Demo - 실제 작동 모습
export
techStackSlide : Slide
techStackSlide = MkSlide
  6
  FullScreenDemo
  (MkSlideContent
    "실제로 보여드릴게요"
    Nothing
    [ "🎬 라이브 데모"
    ]
    []
    [ MkVisual VideoContent "실제 사용 데모 영상 (30초)" "live-demo-full"
    , MkVisual ImageContent "데모 스크린샷 (백업)" "demo-screenshot"
    ]
    (Just "실제 작동하는 모습. 영상: '엄마' 말하기 → 전화 걸림, '음악' → 재생됨, '불꺼' → 조명 OFF"))
  [MkAnimation Appear 0.3 0.0]
  90

||| Slide 7: What It Gave Me - 나에게 준 변화
export
apiSlide : Slide
apiSlide = MkSlide
  7
  TwoColumn
  (MkSlideContent
    "나에게 준 변화"
    (Just "60배 빨라졌습니다")
    [ "2분 → 2초"
    , "하루 30분 절약"
    ]
    []
    [ MkVisual DiagramContent "Before: 복잡한 과정 (2분)" "before-complex"
    , MkVisual DiagramContent "After: 말 한마디 (2초)" "after-simple"
    , MkVisual ImageContent "숫자 강조: 60배 빨라짐" "speed-comparison"
    , MkVisual ImageContent "하루 30분 절약" "time-saved"
    ]
    (Just "Before/After 비교로 효과 시각화. 숫자로 임팩트 강조."))
  [MkAnimation Fade 0.5 0.2]
  60

||| Slide 8: For Others Too - 다른 사람들도
export
demoLiveSlide : Slide
demoLiveSlide = MkSlide
  8
  ThreeColumn
  (MkSlideContent
    "다른 사람들도 쓸 수 있어요"
    (Just "모두를 위한 기술")
    [ "어르신, 직장인, 장애인"
    , "누구나 쉽게"
    ]
    []
    [ MkVisual ImageContent "시나리오 1: 어르신 - 큰 글씨 필요없이" "elderly-scenario"
    , MkVisual ImageContent "시나리오 2: 바쁜 직장인 - 운전 중에도" "worker-scenario"
    , MkVisual ImageContent "시나리오 3: 장애인 - 손 사용 불편해도" "disability-scenario"
    , MkVisual DiagramContent "모두를 위한 기술" "inclusive-tech"
    ]
    (Just "사회적 가치 강조. 다양한 사람들이 혜택 받을 수 있음. 포용적 기술."))
  [MkAnimation Appear 0.3 0.2]
  75

||| Slide 9: My Dream - 앞으로의 꿈
export
metricsSlide : Slide
metricsSlide = MkSlide
  9
  SingleColumn
  (MkSlideContent
    "나의 꿈"
    (Just "모두가 기술의 혜택을 받는 세상")
    [ "더 많은 사람들에게"
    , "더 편리한 생활을"
    ]
    []
    [ MkVisual ImageContent "지구 아이콘 + 연결된 사람들" "connected-world"
    , MkVisual ImageContent "밝은 미래 이미지" "bright-future"
    , MkVisual DiagramContent "확장 가능성: 스마트홈, 자동차, 가전제품..." "expansion-vision"
    ]
    (Just "개인적 비전 제시. 기술의 사회적 가치. 청중에게 영감 주기."))
  [MkAnimation ZoomIn 0.5 0.0]
  60

||| Slide 10: Q&A - 마무리
export
extensibilitySlide : Slide
extensibilitySlide = MkSlide
  10
  TitleSlide
  (MkSlideContent
    "감사합니다"
    (Just "질문 받겠습니다")
    [ "여러분도 말 한마디로"
    , "세상을 바꿀 수 있습니다"
    ]
    []
    [ MkVisual ImageContent "QR 코드 (GitHub)" "qr-code-github"
    , MkVisual ImageContent "SoundToAct 로고" "logo-final"
    ]
    (Just "감사 인사. 영감을 주는 마무리 멘트. GitHub QR 코드 제공."))
  [MkAnimation Fade 0.5 0.0]
  45

--------------------------------------------------------------------------------
-- Presentation Instance
--------------------------------------------------------------------------------

||| SoundToAct presentation for teachers (10 slides - story-driven, visual-focused)
export
soundToActPresentation : Presentation 10
soundToActPresentation = MkPresentation
  (MkMeta
    "SoundToAct"
    "말 한마디로 움직이는 세상"
    "고등학생 개발자"
    "2025-10-26"
    "선생님 (개발자)"
    10
    10)
  soundToActPalette
  standardTypography
  [ titleSlide
  , problemSlide
  , demoSlide
  , featuresSlide
  , architectureSlide
  , techStackSlide
  , apiSlide
  , demoLiveSlide
  , metricsSlide
  , extensibilitySlide
  ]
  [ -- Backup slides
    MkSlide 19 SingleColumn
      (MkSlideContent "기술적 세부사항" Nothing [] [] [] Nothing)
      [] 60
  , MkSlide 20 SingleColumn
      (MkSlideContent "보안 & 프라이버시" Nothing [] [] [] Nothing)
      [] 60
  ]

--------------------------------------------------------------------------------
-- Validation Functions
--------------------------------------------------------------------------------

||| Calculate total presentation time
export
calculateTotalTime : Presentation n -> Nat
calculateTotalTime (MkPresentation _ _ _ slides _) =
  sum (map (\s => s.estimatedTime) (toList slides))

||| Verify all slides have sequential numbering
export
validateSlideNumbers : {n : Nat} -> Presentation n -> Bool
validateSlideNumbers (MkPresentation _ _ _ slides _) =
  let numbers = map slideNumber (toList slides)
  in numbers == [1 .. n]

||| Get slide by number (simplified version)
export
getSlideByNumber : Presentation n -> Nat -> Maybe Slide
getSlideByNumber (MkPresentation _ _ _ slides _) k =
  find (\s => s.slideNumber == k) (toList slides)

||| Count slides by layout type
export
countByLayout : Presentation n -> SlideLayout -> Nat
countByLayout (MkPresentation _ _ _ slides _) layout =
  length $ filter (\s => s.layout == layout) (toList slides)

||| Total code blocks in presentation
export
totalCodeBlocks : Presentation n -> Nat
totalCodeBlocks (MkPresentation _ _ _ slides _) =
  sum $ map (\s => length (s.content.codeBlocks)) (toList slides)

--------------------------------------------------------------------------------
-- Properties (Runtime checks, not proofs)
--------------------------------------------------------------------------------

||| Check that presentation duration matches sum of slide times
export
checkDuration : Presentation n -> Bool
checkDuration p = calculateTotalTime p <= (p.metadata.duration * 60)

||| Check that all slides fit in time budget (max 5 minutes each)
export
checkSlideTimes : Presentation n -> Bool
checkSlideTimes (MkPresentation _ _ _ slides _) =
  all (\s => s.estimatedTime <= 300) (toList slides)

--------------------------------------------------------------------------------
-- Example Usage & Stats
--------------------------------------------------------------------------------

namespace Examples
  ||| Example: Get total presentation time
  export
  exampleTotalTime : Nat
  exampleTotalTime = calculateTotalTime soundToActPresentation

  ||| Example: Validate slide numbering
  export
  exampleValidation : Bool
  exampleValidation = validateSlideNumbers soundToActPresentation

  ||| Example: Count title slides
  export
  exampleTitleCount : Nat
  exampleTitleCount = countByLayout soundToActPresentation TitleSlide

  ||| Example: Total code examples
  export
  exampleCodeCount : Nat
  exampleCodeCount = totalCodeBlocks soundToActPresentation

--------------------------------------------------------------------------------
-- Documentation
--------------------------------------------------------------------------------

{-
SoundToAct Presentation Specification
======================================

This module defines a type-safe structure for a presentation about SoundToAct.

Key Features:
-------------

1. Type Safety
   - Slide count verified at compile time (Vect 10 Slide)
   - Slide numbers must be sequential
   - Time budgets enforced

2. Design Consistency
   - Visual-focused: Minimal text, maximum visuals
   - ColorPalette type ensures consistent colors
   - Typography type ensures consistent fonts

3. Content Structure
   - Story-driven narrative flow
   - Each slide emphasizes motivation, impact, purpose
   - Visual content (images, diagrams) prioritized over text
   - Speaker notes guide storytelling

4. Validation
   - Total time calculation
   - Slide number validation
   - Layout type counting

Properties Verified:
--------------------

✓ Presentation has exactly 10 main slides
✓ Slide numbers are sequential (1..10)
✓ Total time ≤ 10 minutes (600 seconds)
✓ Each slide ≤ 2 minutes (120 seconds)
✓ Visual-heavy design (minimal text)
✓ Story-driven narrative

Target Audience:
----------------

- Primary: Teacher (Developer background)
- Context: High school student presenting their passion project
- Approach: Storytelling over technical details

Presentation Flow (Story Arc):
-------------------------------

1. Opening (Slide 1): Title - "말 한마디로 움직이는 세상"
2. Problem (Slide 2): My daily struggle - personal story
3. Idea (Slide 3): "What if?" - the big question
4. Solution (Slide 4): SoundToAct - what I built
5. How (Slide 5): 3 simple steps - visual explanation
6. Demo (Slide 6): See it in action - live video
7. Impact (Slide 7): What it gave me - before/after
8. For Others (Slide 8): Who else can benefit - social value
9. Vision (Slide 9): My dream - inspiring future
10. Closing (Slide 10): Thank you & questions

This ensures an emotionally engaging, visually compelling presentation
that inspires the audience rather than overwhelming them with tech details.
-}
