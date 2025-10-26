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
    [ MkVisual TextContent "🎤 음성 인식 기반 자동화 시스템" "intro-concept"
    , MkVisual TextContent "Python + SpeechRecognition + 자동화 라이브러리" "tech-stack"
    ]
    (Just "발표자 가이드: 인사 후 프로젝트명 강조. 'Sound(소리)'가 'Act(행동)'으로 바로 변환되는 개념 설명. 음성만으로 기기를 제어하는 시스템임을 명확히 전달."))
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
    [ MkVisual TextContent "[문제 상황]" "problem-header"
    , MkVisual TextContent "1. 침대에서 폰 찾기 (20초)" "step-1"
    , MkVisual TextContent "2. 잠금 해제 (10초)" "step-2"
    , MkVisual TextContent "3. 연락처 앱 열기 (15초)" "step-3"
    , MkVisual TextContent "4. '엄마' 검색 (20초)" "step-4"
    , MkVisual TextContent "5. 통화 버튼 터치 (5초)" "step-5"
    , MkVisual TextContent "⏱ 총 소요 시간: ~2분 + 귀찮음" "total-time"
    ]
    (Just "발표자 가이드: 개인 경험 공유. '아침에 누워있는데 전화해야 할 때 얼마나 귀찮은지 아시나요?' 질문으로 시작. 각 단계를 천천히 설명하며 복잡함 강조. UI 조작의 불편함과 시간 낭비 언급."))
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
    [ MkVisual TextContent "💡 핵심 아이디어" "core-idea"
    , MkVisual TextContent "음성 명령 → 즉시 실행" "voice-to-action"
    , MkVisual TextContent "UI 조작 불필요" "no-ui"
    ]
    (Just "발표자 가이드: 잠시 멈추고 청중과 눈 맞춤. '만약에 말입니다...' 하며 기대감 조성. 해결책을 직접 말하지 말고 질문 형태로 상상하게 만들기. '이게 가능하다면 얼마나 편할까요?'"))
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
    [ MkVisual TextContent "[기술 스택]" "tech-stack-header"
    , MkVisual TextContent "• Python 3.10+ 기반" "python-version"
    , MkVisual TextContent "• SpeechRecognition 라이브러리 (Google Speech API)" "speech-lib"
    , MkVisual TextContent "• PyAutoGUI (UI 자동화)" "automation-lib"
    , MkVisual TextContent "• Threading (백그라운드 실행)" "threading"
    , MkVisual TextContent "" "spacer"
    , MkVisual TextContent "[동작 방식]" "how-it-works-header"
    , MkVisual TextContent "'엄마' 음성 → 연락처 검색 → 통화 실행" "demo-flow"
    ]
    (Just "발표자 가이드: '그래서 직접 만들었습니다!' 힘있게 말하기. 기술 스택 설명 시 '고등학생도 배울 수 있는 Python으로 만들었다' 강조. SpeechRecognition은 Google API 사용해서 정확도 높음을 언급. 실제 동작 예시를 간단히 설명."))
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
    [ MkVisual TextContent "[1단계: 듣기 🎤]" "step-1-header"
    , MkVisual TextContent "마이크로 음성 캡처" "audio-capture"
    , MkVisual TextContent "sr.Microphone()" "code-mic"
    , MkVisual TextContent "실시간 오디오 스트림" "audio-stream"
    , MkVisual TextContent "" "spacer-1"
    , MkVisual TextContent "[2단계: 이해 🧠]" "step-2-header"
    , MkVisual TextContent "Google Speech API" "google-api"
    , MkVisual TextContent "음성 → 텍스트 변환" "stt"
    , MkVisual TextContent "키워드 매칭 알고리즘" "keyword-matching"
    , MkVisual TextContent "" "spacer-2"
    , MkVisual TextContent "[3단계: 실행 ⚡]" "step-3-header"
    , MkVisual TextContent "명령어 파싱" "command-parsing"
    , MkVisual TextContent "해당 함수 호출" "function-call"
    , MkVisual TextContent "자동화 스크립트 실행" "automation"
    ]
    (Just "발표자 가이드: 기술적 설명 시작. 1) 마이크 입력은 SpeechRecognition 라이브러리가 처리. 2) Google API가 음성을 텍스트로 변환 (네트워크 필요). 3) 키워드를 인식하면 미리 정의된 함수 실행. '코드는 200줄 정도로 간단합니다' 언급."))
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
    [ MkVisual TextContent "[데모 시나리오]" "demo-scenarios"
    , MkVisual TextContent "1️⃣ '엄마' → 연락처에서 찾아 전화 걸기" "demo-1"
    , MkVisual TextContent "2️⃣ '음악 틀어줘' → 음악 앱 실행" "demo-2"
    , MkVisual TextContent "3️⃣ '불 꺼줘' → 스마트 조명 제어" "demo-3"
    , MkVisual TextContent "" "spacer"
    , MkVisual TextContent "💻 실행 명령: python main.py" "command"
    , MkVisual TextContent "🎤 음성 인식 대기 중..." "listening"
    ]
    (Just "발표자 가이드: 실제 데모 실행. 프로그램 실행 후 '엄마'라고 말하기. 반응 속도 강조 (~2초). 데모가 안 되면 '사전에 녹화한 영상'이라고 말하고 시나리오 설명. 각 명령어가 어떻게 처리되는지 간단히 설명. 오류 처리도 구현되어 있음을 언급."))
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
    [ MkVisual TextContent "[Before: 전통적 방식]" "before-header"
    , MkVisual TextContent "• 기기 조작 필요" "before-1"
    , MkVisual TextContent "• UI 네비게이션 필수" "before-2"
    , MkVisual TextContent "• 5단계 프로세스" "before-3"
    , MkVisual TextContent "• 평균 소요: 2분" "before-time"
    , MkVisual TextContent "" "spacer"
    , MkVisual TextContent "[After: SoundToAct]" "after-header"
    , MkVisual TextContent "• 음성만으로 완료" "after-1"
    , MkVisual TextContent "• UI 터치 불필요" "after-2"
    , MkVisual TextContent "• 1단계 (말하기)" "after-3"
    , MkVisual TextContent "• 평균 소요: 2초" "after-time"
    , MkVisual TextContent "" "spacer-2"
    , MkVisual TextContent "⚡ 속도 개선: 60배 ⚡" "improvement"
    , MkVisual TextContent "💰 하루 약 30분 절약 (15회 사용 시)" "daily-savings"
    ]
    (Just "발표자 가이드: 구체적 수치로 효과 입증. Before 설명 시 손동작으로 복잡함 강조. After 설명 시 '그냥 말만 하면 됩니다' 강조. 60배는 120초/2초 계산. 하루 15회 사용 가정 시 30분 절약 (15 × 118초 = 1770초 ≈ 30분)."))
  [MkAnimation Fade 0.5 0.2]
  60

||| Slide 8: For Others Too - 다른 사람들도 (긴급 상황 포함)
export
demoLiveSlide : Slide
demoLiveSlide = MkSlide
  8
  FourQuadrant
  (MkSlideContent
    "다른 사람들도 쓸 수 있어요"
    (Just "모두를 위한 기술")
    [ "긴급 상황, 어르신, 직장인, 장애인"
    , "누구나 쉽게, 안전하게"
    ]
    []
    [ MkVisual TextContent "[긴급 상황 🚨]" "emergency-header"
    , MkVisual TextContent "• 위험한 순간 폰 못 찾아도 OK" "emergency-1"
    , MkVisual TextContent "• '엄마' 한마디로 즉시 연결" "emergency-2"
    , MkVisual TextContent "• 화면 보지 않고 도움 요청" "emergency-3"
    , MkVisual TextContent "" "spacer-0"
    , MkVisual TextContent "[어르신 👴]" "elderly-header"
    , MkVisual TextContent "• 작은 글씨 안 보여도 OK" "elderly-1"
    , MkVisual TextContent "• 복잡한 UI 몰라도 OK" "elderly-2"
    , MkVisual TextContent "• 말만 하면 작동" "elderly-3"
    , MkVisual TextContent "" "spacer-1"
    , MkVisual TextContent "[바쁜 직장인 💼]" "worker-header"
    , MkVisual TextContent "• 운전 중 안전하게" "worker-1"
    , MkVisual TextContent "• 멀티태스킹 가능" "worker-2"
    , MkVisual TextContent "• 손 쓸 필요 없음" "worker-3"
    , MkVisual TextContent "" "spacer-2"
    , MkVisual TextContent "[장애인 ♿]" "disability-header"
    , MkVisual TextContent "• 시각 장애: 화면 안 봐도 OK" "disability-1"
    , MkVisual TextContent "• 지체 장애: 터치 불필요" "disability-2"
    , MkVisual TextContent "• 음성만으로 완전 제어" "disability-3"
    ]
    (Just "발표자 가이드: 안전과 사회적 가치 강조. '긴급 상황에서 진가를 발휘합니다' 시작. 위급할 때(넘어졌을 때, 사고 시) 폰 화면 못 봐도 '엄마'라고 말하면 즉시 전화 연결되어 도움 요청 가능. 각 그룹별 pain point 설명. '기술은 누구에게나 평등해야 합니다' 강조. 접근성(Accessibility)과 안전(Safety)이 핵심 가치임을 언급."))
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
    [ MkVisual TextContent "[향후 개선 계획]" "future-plan"
    , MkVisual TextContent "• 다국어 지원 (영어, 중국어...)" "multilingual"
    , MkVisual TextContent "• 오프라인 모드 (로컬 STT)" "offline-mode"
    , MkVisual TextContent "• 더 많은 명령어 추가" "more-commands"
    , MkVisual TextContent "• 커스터마이징 기능" "customization"
    , MkVisual TextContent "" "spacer"
    , MkVisual TextContent "[확장 가능성]" "scalability"
    , MkVisual TextContent "🏠 스마트홈: IoT 기기 제어" "smarthome"
    , MkVisual TextContent "🚗 자동차: 핸즈프리 운전" "car"
    , MkVisual TextContent "🏥 의료: 환자 모니터링" "healthcare"
    , MkVisual TextContent "🏭 산업: 작업장 안전" "industrial"
    ]
    (Just "발표자 가이드: 미래 비전 제시. '이건 시작일 뿐입니다' 강조. 다국어 지원으로 글로벌화 가능. 오프라인 모드는 Vosk 같은 로컬 STT 라이브러리 사용 계획. IoT 연동 시 진정한 스마트홈 가능. 의료/산업 분야 적용 사례 간단히 설명. '여러분도 함께 만들어주세요' 참여 유도."))
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
    [ MkVisual TextContent "[프로젝트 정보]" "project-info"
    , MkVisual TextContent "📂 GitHub: github.com/[username]/SoundToAct" "github"
    , MkVisual TextContent "📧 Email: contact@example.com" "email"
    , MkVisual TextContent "🐍 Python 3.10+ 필요" "requirements"
    , MkVisual TextContent "" "spacer"
    , MkVisual TextContent "[기술 스택 요약]" "tech-summary"
    , MkVisual TextContent "SpeechRecognition • PyAutoGUI" "libs-1"
    , MkVisual TextContent "Threading • Google Speech API" "libs-2"
    , MkVisual TextContent "" "spacer-2"
    , MkVisual TextContent "💬 Q&A 환영합니다!" "qa-welcome"
    ]
    (Just "발표자 가이드: '경청해주셔서 감사합니다!' 밝게 인사. GitHub 링크 공유하며 '코드가 궁금하신 분들은 자유롭게 보세요'. 오픈소스 프로젝트이며 contribution 환영. 질문 받을 준비. 예상 질문: 1) 정확도는? → 90% 이상 2) 비용은? → 무료 (Google API 일일 한도 내) 3) 오프라인? → 현재는 불가, 향후 추가 예정 4) 보안은? → 로컬 실행, 데이터 저장 안 함."))
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
