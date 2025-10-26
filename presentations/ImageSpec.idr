||| Image Specifications for SoundToAct Presentation
|||
||| This module defines the exact content and layout for each image
||| used in the presentation. Every text, color, position is specified.

module ImageSpec

import Data.Vect

%default total

--------------------------------------------------------------------------------
-- Image Content Types
--------------------------------------------------------------------------------

||| Text element with specific font size and color
public export
record TextElement where
  constructor MkText
  content : String
  fontSize : Nat
  color : String  -- hex color
  position : (Nat, Nat)  -- (x, y) in pixels
  alignment : String  -- "left", "center", "right"

||| Shape element (rectangle, circle, arrow, etc.)
public export
data ShapeType = Rectangle | Circle | Arrow | Line | RoundedRect

public export
record ShapeElement where
  constructor MkShape
  shapeType : ShapeType
  position : (Nat, Nat)
  size : (Nat, Nat)  -- (width, height)
  fillColor : String
  strokeColor : String
  strokeWidth : Nat

||| Complete image specification
public export
record ImageSpec where
  constructor MkImageSpec
  filename : String
  width : Nat
  height : Nat
  backgroundColor : String
  texts : List TextElement
  shapes : List ShapeElement
  description : String

--------------------------------------------------------------------------------
-- Slide 1: Title Slide Images
--------------------------------------------------------------------------------

||| Waveform animation image
export
waveformSpec : ImageSpec
waveformSpec = MkImageSpec
  "wave_animation.png"
  1000 300
  "#FFFFFF"
  []
  []
  "음성 웨이브폼: 파란색 그라데이션 파동, 왼쪽에서 오른쪽으로 진폭 변화"

||| Large microphone icon
export
microphoneSpec : ImageSpec
microphoneSpec = MkImageSpec
  "mic_icon_large.png"
  500 500
  "transparent"
  []
  [ MkShape Circle (250, 150) (120, 120) "#2563EB" "#2563EB" 0  -- Mic head
  , MkShape Rectangle (220, 270) (60, 120) "#2563EB" "#2563EB" 0  -- Mic body
  , MkShape Rectangle (190, 390) (120, 40) "#2563EB" "#2563EB" 0  -- Mic base
  ]
  "큰 파란색 마이크 아이콘, 심플한 디자인"

--------------------------------------------------------------------------------
-- Slide 2: Morning Scene
--------------------------------------------------------------------------------

||| Morning illustration - student waking up
export
morningIllustrationSpec : ImageSpec
morningIllustrationSpec = MkImageSpec
  "morning_illustration.png"
  800 600
  "#FFF5E6"
  [ MkText "7:00 AM" 48 "#111827" (50, 50) "left"
  , MkText "😴" 120 "#111827" (350, 200) "center"
  ]
  [ MkShape RoundedRect (200, 350) (400, 150) "#8B4513" "#000000" 3  -- Bed
  , MkShape Circle (400, 250) (80, 80) "#FFE4B5" "#000000" 2  -- Head
  ]
  "침대에서 막 일어난 학생, 아침 7시"

||| Complex phone process flow
export
complexProcessSpec : ImageSpec
complexProcessSpec = MkImageSpec
  "complex_process.png"
  800 400
  "#FFFFFF"
  [ MkText "1. 폰 찾기" 24 "#111827" (50, 50) "left"
  , MkText "2. 잠금 해제" 24 "#111827" (50, 120) "left"
  , MkText "3. 연락처 앱 열기" 24 "#111827" (50, 190) "left"
  , MkText "4. 검색하기" 24 "#111827" (50, 260) "left"
  , MkText "5. 터치해서 전화" 24 "#111827" (50, 330) "left"
  , MkText "= 2분 소요 😓" 32 "#F59E0B" (500, 180) "center"
  ]
  [ MkShape Arrow (300, 75) (100, 20) "#F59E0B" "#F59E0B" 3
  , MkShape Arrow (300, 145) (100, 20) "#F59E0B" "#F59E0B" 3
  , MkShape Arrow (300, 215) (100, 20) "#F59E0B" "#F59E0B" 3
  , MkShape Arrow (300, 285) (100, 20) "#F59E0B" "#F59E0B" 3
  ]
  "복잡한 전화 걸기 과정, 5단계, 화살표 연결, 2분 강조"

--------------------------------------------------------------------------------
-- Slide 3: Big Idea
--------------------------------------------------------------------------------

||| Large question mark icon
export
questionMarkSpec : ImageSpec
questionMarkSpec = MkImageSpec
  "question_mark.png"
  500 500
  "transparent"
  [ MkText "?" 300 "#7C3AED" (150, 50) "center"
  ]
  []
  "큰 보라색 물음표, 중앙 배치"

||| Speech bubble with "엄마"
export
speechBubbleSpec : ImageSpec
speechBubbleSpec = MkImageSpec
  "speech_bubble.png"
  600 300
  "transparent"
  [ MkText "엄마" 100 "#111827" (300, 120) "center"
  ]
  [ MkShape RoundedRect (100, 80) (400, 150) "#FFFFFF" "#2563EB" 5  -- Bubble
  ]
  "말풍선 안에 '엄마' 텍스트, 파란 테두리"

||| Light bulb with rays for idea
export
lightBulbSpec : ImageSpec
lightBulbSpec = MkImageSpec
  "light_bulb.png"
  500 500
  "transparent"
  [ MkText "💡" 200 "#F59E0B" (150, 100) "center"
  ]
  []
  "빛나는 전구 아이콘, 주황색, 빛 효과"

--------------------------------------------------------------------------------
-- Slide 4: Solution
--------------------------------------------------------------------------------

||| SoundToAct logo
export
logoSpec : ImageSpec
logoSpec = MkImageSpec
  "soundtoact_logo.png"
  600 400
  "#FFFFFF"
  [ MkText "SoundToAct" 72 "#2563EB" (300, 150) "center"
  , MkText "🎤 → ⚡" 80 "#10B981" (300, 250) "center"
  ]
  []
  "프로젝트 로고, 파란색 텍스트, 마이크에서 번개로 변환"

||| Demo video placeholder with before/after
export
demoPlaceholderSpec : ImageSpec
demoPlaceholderSpec = MkImageSpec
  "demo_placeholder.png"
  800 600
  "#F0F0F0"
  [ MkText "Before" 40 "#F59E0B" (150, 100) "center"
  , MkText "📱 🔍 👆 📞" 60 "#666666" (150, 200) "center"
  , MkText "복잡함" 28 "#F59E0B" (150, 350) "center"
  , MkText "After" 40 "#10B981" (650, 100) "center"
  , MkText "🎤 \"엄마\"" 60 "#2563EB" (650, 200) "center"
  , MkText "간단!" 28 "#10B981" (650, 350) "center"
  , MkText "→" 80 "#111827" (400, 250) "center"
  ]
  []
  "Before/After 비교: 왼쪽 복잡한 과정, 오른쪽 간단한 음성"

--------------------------------------------------------------------------------
-- Slide 5: How It Works - 3 Steps
--------------------------------------------------------------------------------

||| Three-step process diagram
export
threeStepsSpec : ImageSpec
threeStepsSpec = MkImageSpec
  "three_steps.png"
  1200 500
  "#FFFFFF"
  [ MkText "1" 80 "#FFFFFF" (150, 120) "center"
  , MkText "듣기" 40 "#2563EB" (150, 300) "center"
  , MkText "🎤" 60 "#2563EB" (150, 370) "center"
  , MkText "2" 80 "#FFFFFF" (600, 120) "center"
  , MkText "이해하기" 40 "#7C3AED" (600, 300) "center"
  , MkText "🧠" 60 "#7C3AED" (600, 370) "center"
  , MkText "3" 80 "#FFFFFF" (1050, 120) "center"
  , MkText "실행하기" 40 "#10B981" (1050, 300) "center"
  , MkText "⚡" 60 "#10B981" (1050, 370) "center"
  ]
  [ MkShape Circle (150, 120) (150, 150) "#2563EB" "#2563EB" 0  -- Step 1
  , MkShape Circle (600, 120) (150, 150) "#7C3AED" "#7C3AED" 0  -- Step 2
  , MkShape Circle (1050, 120) (150, 150) "#10B981" "#10B981" 0  -- Step 3
  , MkShape Arrow (300, 170) (200, 30) "#111827" "#111827" 3  -- Arrow 1→2
  , MkShape Arrow (750, 170) (200, 30) "#111827" "#111827" 3  -- Arrow 2→3
  ]
  "3단계 프로세스: 1.듣기(파랑), 2.이해하기(보라), 3.실행하기(초록), 화살표 연결"

--------------------------------------------------------------------------------
-- Slide 6: Live Demo
--------------------------------------------------------------------------------

||| Live demo screen capture placeholder
export
liveDemoSpec : ImageSpec
liveDemoSpec = MkImageSpec
  "live_demo.png"
  1000 600
  "#1F2937"
  [ MkText "🎬 LIVE DEMO" 60 "#FFFFFF" (500, 100) "center"
  , MkText "\"엄마\" 🎤" 72 "#10B981" (500, 250) "center"
  , MkText "↓" 80 "#FFFFFF" (500, 350) "center"
  , MkText "📞 전화 연결됨!" 48 "#10B981" (500, 470) "center"
  ]
  []
  "라이브 데모 화면: '엄마' 음성 → 전화 연결, 어두운 배경"

--------------------------------------------------------------------------------
-- Slide 7: Before/After Impact
--------------------------------------------------------------------------------

||| Before/After comparison with numbers
export
beforeAfterSpec : ImageSpec
beforeAfterSpec = MkImageSpec
  "before_after.png"
  1000 600
  "#FFFFFF"
  [ MkText "Before" 50 "#F59E0B" (200, 50) "center"
  , MkText "2분" 72 "#F59E0B" (200, 200) "center"
  , MkText "5단계" 36 "#666666" (200, 300) "left"
  , MkText "After" 50 "#10B981" (800, 50) "center"
  , MkText "2초" 72 "#10B981" (800, 200) "center"
  , MkText "1단계" 36 "#666666" (800, 300) "left"
  , MkText "→" 80 "#111827" (500, 200) "center"
  , MkText "60배 빨라짐!" 48 "#10B981" (500, 450) "center"
  , MkText "하루 30분 절약" 36 "#2563EB" (500, 530) "center"
  ]
  [ MkShape Rectangle (50, 100) (350, 350) "#FFEBE6" "#F59E0B" 3  -- Before box
  , MkShape Rectangle (650, 100) (350, 350) "#E6FFE6" "#10B981" 3  -- After box
  ]
  "Before/After 비교: 2분→2초, 60배 빨라짐, 하루 30분 절약"

--------------------------------------------------------------------------------
-- Slide 8: For Others - Inclusive Technology
--------------------------------------------------------------------------------

||| Inclusive technology for three user groups
export
inclusiveTechSpec : ImageSpec
inclusiveTechSpec = MkImageSpec
  "inclusive_tech.png"
  1200 500
  "#FFFFFF"
  [ MkText "어르신" 36 "#111827" (200, 400) "center"
  , MkText "큰 글씨 필요 없이" 24 "#666666" (200, 450) "center"
  , MkText "직장인" 36 "#111827" (600, 400) "center"
  , MkText "운전 중에도" 24 "#666666" (600, 450) "center"
  , MkText "장애인" 36 "#111827" (1000, 400) "center"
  , MkText "손 사용 불편해도" 24 "#666666" (1000, 450) "center"
  , MkText "모두를 위한 기술" 52 "#10B981" (600, 50) "center"
  ]
  [ -- Person 1: Elderly
    MkShape Circle (200, 200) (80, 80) "#2563EB" "#2563EB" 0  -- Head
  , MkShape Rectangle (170, 280) (60, 100) "#7C3AED" "#7C3AED" 0  -- Body
    -- Person 2: Worker
  , MkShape Circle (600, 200) (80, 80) "#2563EB" "#2563EB" 0
  , MkShape Rectangle (570, 280) (60, 100) "#7C3AED" "#7C3AED" 0
    -- Person 3: Disabled
  , MkShape Circle (1000, 200) (80, 80) "#2563EB" "#2563EB" 0
  , MkShape Rectangle (970, 280) (60, 100) "#7C3AED" "#7C3AED" 0
  ]
  "3가지 사용자 그룹: 어르신, 직장인, 장애인. 각각 사람 아이콘 + 설명"

--------------------------------------------------------------------------------
-- Slide 9: My Dream - World Connections
--------------------------------------------------------------------------------

||| World with connected people
export
worldConnectionsSpec : ImageSpec
worldConnectionsSpec = MkImageSpec
  "world_connections.png"
  800 600
  "#FFFFFF"
  [ MkText "🌍" 180 "#2563EB" (400, 250) "center"
  ]
  [ MkShape Circle (400, 300) (200, 200) "#2563EB" "#2563EB" 5  -- Globe
  , MkShape Line (400, 100) (300, 50) "#10B981" "#10B981" 4  -- Connection line 1
  , MkShape Line (600, 200) (700, 150) "#10B981" "#10B981" 4  -- Connection line 2
  , MkShape Line (600, 400) (700, 450) "#10B981" "#10B981" 4  -- Connection line 3
  , MkShape Line (400, 500) (300, 550) "#10B981" "#10B981" 4  -- Connection line 4
  , MkShape Line (200, 400) (100, 450) "#10B981" "#10B981" 4  -- Connection line 5
  , MkShape Line (200, 200) (100, 150) "#10B981" "#10B981" 4  -- Connection line 6
  , MkShape Circle (300, 50) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 1
  , MkShape Circle (700, 150) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 2
  , MkShape Circle (700, 450) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 3
  , MkShape Circle (300, 550) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 4
  , MkShape Circle (100, 450) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 5
  , MkShape Circle (100, 150) (30, 30) "#7C3AED" "#7C3AED" 0  -- Person 6
  ]
  "지구 중심, 6방향으로 연결선, 끝에 사람 아이콘"

||| Bright future with expansion possibilities
export
brightFutureSpec : ImageSpec
brightFutureSpec = MkImageSpec
  "bright_future.png"
  800 600
  "#FFF9E6"
  [ MkText "미래의 가능성" 48 "#2563EB" (400, 50) "center"
  , MkText "🏠 스마트홈" 36 "#111827" (200, 200) "center"
  , MkText "🚗 자동차" 36 "#111827" (600, 200) "center"
  , MkText "📺 가전제품" 36 "#111827" (200, 400) "center"
  , MkText "🤖 로봇" 36 "#111827" (600, 400) "center"
  ]
  [ MkShape RoundedRect (100, 150) (200, 120) "#E6F3FF" "#2563EB" 2
  , MkShape RoundedRect (500, 150) (200, 120) "#E6F3FF" "#2563EB" 2
  , MkShape RoundedRect (100, 350) (200, 120) "#E6F3FF" "#2563EB" 2
  , MkShape RoundedRect (500, 350) (200, 120) "#E6F3FF" "#2563EB" 2
  ]
  "밝은 배경, 4가지 확장 가능성: 스마트홈, 자동차, 가전, 로봇"

--------------------------------------------------------------------------------
-- Slide 10: Thank You
--------------------------------------------------------------------------------

||| GitHub QR code placeholder
export
qrCodeSpec : ImageSpec
qrCodeSpec = MkImageSpec
  "qr_code.png"
  300 300
  "#FFFFFF"
  [ MkText "GitHub" 28 "#111827" (150, 260) "center"
  ]
  [ MkShape Rectangle (50, 50) (200, 200) "#111827" "#111827" 0  -- QR placeholder
  ]
  "QR 코드 placeholder (검은색 사각형), 하단에 'GitHub' 텍스트"

||| Final logo
export
finalLogoSpec : ImageSpec
finalLogoSpec = MkImageSpec
  "logo_final.png"
  400 300
  "transparent"
  [ MkText "SoundToAct" 48 "#2563EB" (200, 150) "center"
  ]
  []
  "최종 로고, 파란색 텍스트"

--------------------------------------------------------------------------------
-- Complete List of All Images
--------------------------------------------------------------------------------

export
allImageSpecs : List ImageSpec
allImageSpecs =
  [ waveformSpec
  , microphoneSpec
  , morningIllustrationSpec
  , complexProcessSpec
  , questionMarkSpec
  , speechBubbleSpec
  , lightBulbSpec
  , logoSpec
  , demoPlaceholderSpec
  , threeStepsSpec
  , liveDemoSpec
  , beforeAfterSpec
  , inclusiveTechSpec
  , worldConnectionsSpec
  , brightFutureSpec
  , qrCodeSpec
  , finalLogoSpec
  ]

||| Total number of images
export
totalImages : Nat
totalImages = length allImageSpecs
