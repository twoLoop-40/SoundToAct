||| Image Generation Specification
|||
||| Formal specification for generating images that match visual descriptions
||| in the presentation. Each image must accurately represent its description.

module ImageGeneration

import Data.String
import Data.List

%default total

--------------------------------------------------------------------------------
-- Image Source Types
--------------------------------------------------------------------------------

||| Where to obtain the image
public export
data ImageSource
  = GenerateWithCode String  -- Generate using PIL/Python with given description
  | SearchWeb String         -- Search web with given query
  | UseExisting String       -- Use existing image file

||| Image generation specification
public export
record ImageGenSpec where
  constructor MkImageGenSpec
  visualDescription : String       -- Original visual description from Presentation.idr
  imageFileName : String            -- Output filename (e.g., "step1_listen.png")
  source : ImageSource              -- How to obtain the image
  width : Nat                       -- Width in pixels
  height : Nat                      -- Height in pixels
  backgroundColor : String          -- Hex color
  detailedSpec : String            -- Detailed description of what image should contain

--------------------------------------------------------------------------------
-- Image Generation Specifications for All Visuals
--------------------------------------------------------------------------------

||| Slide 1 Image 1: Waveform animation
export
waveformSpec : ImageGenSpec
waveformSpec = MkImageGenSpec
  "음성 웨이브폼 애니메이션"
  "waveform_animation.png"
  (GenerateWithCode "Animated sound waveform with multiple sine waves in blue/purple gradient")
  1200 300
  "#FFFFFF"
  "여러 개의 사인파가 겹쳐진 음성 웨이브폼. 파란색(#2563EB)에서 보라색(#7C3AED)으로 그라데이션. 진폭이 다른 3-4개의 파동이 겹쳐진 모습."

||| Slide 1 Image 2: Large microphone icon
export
microphoneLargeSpec : ImageGenSpec
microphoneLargeSpec = MkImageGenSpec
  "마이크 아이콘 (큼직하게)"
  "microphone_large.png"
  (GenerateWithCode "Large, simple microphone icon in blue")
  400 400
  "#FFFFFF"
  "큼직한 마이크 아이콘. 클래식 스튜디오 마이크 모양. 파란색(#2563EB). 심플하고 현대적인 디자인. 스탠드 포함."

||| Slide 2 Image 1: Student waking up
export
studentWakingSpec : ImageGenSpec
studentWakingSpec = MkImageGenSpec
  "만화 스타일 일러스트: 침대에서 일어나는 학생"
  "student_waking_up.png"
  (GenerateWithCode "Cartoon style illustration of student waking up in bed, looking tired")
  800 500
  "#FFF7ED"
  "만화 스타일. 침대에서 막 일어나는 고등학생. 머리가 헝클어진 모습. 피곤한 표정. 침대, 베개, 이불 포함. 따뜻한 오렌지 톤 배경."

||| Slide 2 Image 2: Complex process flow
export
complexProcessSpec : ImageGenSpec
complexProcessSpec = MkImageGenSpec
  "복잡한 과정 플로우: 폰 찾기 → 잠금 해제 → 연락처 앱 → 검색 → 터치"
  "complex_process_flow.png"
  (GenerateWithCode "Flow diagram with 5 steps showing phone operation complexity")
  1000 300
  "#FEF2F2"
  "5단계 프로세스 다이어그램. 각 단계를 직사각형으로 표시하고 화살표로 연결. 1) 폰 찾기 (폰 아이콘) 2) 잠금 해제 (자물쇠 아이콘) 3) 연락처 앱 (사람 아이콘) 4) 검색 (돋보기) 5) 터치 (손가락). 빨간색 계열(#DC2626). 복잡함을 강조."

||| Slide 2 Image 3: Clock showing 2 minutes
export
clockTwoMinutesSpec : ImageGenSpec
clockTwoMinutesSpec = MkImageGenSpec
  "시계 아이콘: '2분 소요'"
  "clock_two_minutes.png"
  (GenerateWithCode "Clock icon showing 2 minutes with text '2분 소요'")
  400 400
  "#FFFFFF"
  "시계 아이콘. 빨간색(#DC2626). 시침과 분침이 2분을 가리킴. 아래에 큰 텍스트로 '2분 소요' 표시. 경고를 주는 느낌."

||| Slide 3 Image 1: Large question mark
export
questionMarkLargeSpec : ImageGenSpec
questionMarkLargeSpec = MkImageGenSpec
  "큰 물음표 아이콘"
  "question_mark_large.png"
  (GenerateWithCode "Very large blue question mark icon with glow effect")
  600 600
  "#FFFFFF"
  "거대한 물음표(?). 파란색(#2563EB). 약간의 그림자와 빛나는 효과. 호기심을 자극하는 느낌."

||| Slide 3 Image 2: Speech bubble with 'mom'
export
speechBubbleMomSpec : ImageGenSpec
speechBubbleMomSpec = MkImageGenSpec
  "말풍선 안에 '엄마'"
  "speech_bubble_mom.png"
  (GenerateWithCode "Speech bubble containing the Korean word '엄마' (mom)")
  600 400
  "#FFFFFF"
  "말풍선. 둥근 모서리. 파란색(#2563EB) 테두리. 연한 파란색(#EFF6FF) 배경. 안에 큰 글씨로 '엄마' 표시. 말풍선 꼬리 포함."

||| Slide 3 Image 3: Light bulb with sparkles
export
lightBulbIdeaSpec : ImageGenSpec
lightBulbIdeaSpec = MkImageGenSpec
  "빛나는 효과 (반짝이는 전구)"
  "light_bulb_sparkle.png"
  (GenerateWithCode "Light bulb with bright sparkle effects representing an idea")
  600 600
  "#FFFFFF"
  "전구. 노란색(#FEF3C7) 빛. 주변에 반짝이는 별(sparkles) 효과. 아이디어를 나타내는 느낌. 금색(#F59E0B) 강조."

||| Slide 4 Image 1: Project logo (large)
export
projectLogoLargeSpec : ImageGenSpec
projectLogoLargeSpec = MkImageGenSpec
  "프로젝트 로고 (크게)"
  "soundtoact_logo_large.png"
  (GenerateWithCode "SoundToAct logo - large version with sound wave and action arrow")
  800 300
  "#FFFFFF"
  "SoundToAct 로고. 큰 크기. 왼쪽: 소리 아이콘(음파). 가운데: 화살표. 오른쪽: 액션 아이콘(번개). 파란색(#2563EB)과 초록색(#10B981) 그라데이션. 아래에 'SoundToAct' 텍스트."

||| Slide 4 Image 2: Demo video placeholder
export
demoVideoPlaceholderSpec : ImageGenSpec
demoVideoPlaceholderSpec = MkImageGenSpec
  "10초 데모 영상: '엄마' → 전화 걸림"
  "demo_video_placeholder.png"
  (GenerateWithCode "Video placeholder showing '엄마' → phone call icon")
  1000 600
  "#F3F4F6"
  "데모 영상 플레이스홀더. 회색 배경. 가운데에 큰 재생 버튼. 위에 말풍선 '엄마'. 화살표. 전화 아이콘. 10초 표시."

||| Slide 4 Image 3: Before/After comparison
export
beforeAfterComparisonSpec : ImageGenSpec
beforeAfterComparisonSpec = MkImageGenSpec
  "Before/After 비교 이미지"
  "before_after_comparison.png"
  (GenerateWithCode "Before/After side-by-side comparison image")
  1200 600
  "#FFFFFF"
  "좌우 2분할. 왼쪽(Before): 빨간 배경(#FEE2E2), 복잡한 5단계, '2분'. 오른쪽(After): 초록 배경(#D1FAE5), 간단한 1단계, '2초'. 가운데 세로 구분선."

||| Slide 5 Image 1: Step 1 - Listen
export
step1ListenSpec : ImageGenSpec
step1ListenSpec = MkImageGenSpec
  "1단계: 듣기 - 마이크 아이콘 + 음성 웨이브"
  "step1_listen.png"
  (GenerateWithCode "Step 1: Listen - microphone icon with sound waves")
  400 400
  "#FFFFFF"
  "1단계 표시. 원 안에 숫자 '1'. 파란색(#2563EB). 아래에 마이크 아이콘. 주변에 음파 표시. '듣기' 텍스트."

||| Slide 5 Image 2: Step 2 - Understand
export
step2UnderstandSpec : ImageGenSpec
step2UnderstandSpec = MkImageGenSpec
  "2단계: 이해하기 - AI 뇌 + 키워드 매칭"
  "step2_understand.png"
  (GenerateWithCode "Step 2: Understand - brain icon with keywords")
  400 400
  "#FFFFFF"
  "2단계 표시. 원 안에 숫자 '2'. 보라색(#7C3AED). 아래에 뇌 또는 AI 아이콘. 주변에 키워드 말풍선들. '이해하기' 텍스트."

||| Slide 5 Image 3: Step 3 - Act
export
step3ActSpec : ImageGenSpec
step3ActSpec = MkImageGenSpec
  "3단계: 실행하기 - 액션 아이콘 (전화, 음악, 조명)"
  "step3_act.png"
  (GenerateWithCode "Step 3: Act - action icons (phone, music, light)")
  400 400
  "#FFFFFF"
  "3단계 표시. 원 안에 숫자 '3'. 초록색(#10B981). 아래에 3개 액션 아이콘: 전화, 음악 노트, 전구. '실행하기' 텍스트."

||| Slide 5 Image 4: 3-step flow with arrows
export
threeStepFlowSpec : ImageGenSpec
threeStepFlowSpec = MkImageGenSpec
  "화살표로 연결된 3단계 플로우"
  "three_step_flow_arrows.png"
  (GenerateWithCode "3 steps connected by arrows in a horizontal flow")
  1200 500
  "#FFFFFF"
  "가로로 배치된 3단계. 각 단계는 원 안에 숫자. 1(파랑), 2(보라), 3(초록). 굵은 화살표로 연결. 각 단계 아래 아이콘."

||| Slide 6 Image 1: Live demo video
export
liveDemoVideoSpec : ImageGenSpec
liveDemoVideoSpec = MkImageGenSpec
  "실제 사용 데모 영상 (30초)"
  "live_demo_video.png"
  (GenerateWithCode "Live demo video placeholder with LIVE indicator")
  1200 700
  "#1F2937"
  "어두운 배경. 가운데에 'LIVE' 텍스트 (빨간색 #EF4444). 'DEMO' 텍스트 (흰색). 주변에 펄스 효과. '30초' 표시."

||| Slide 6 Image 2: Demo screenshot
export
demoScreenshotSpec : ImageGenSpec
demoScreenshotSpec = MkImageGenSpec
  "데모 스크린샷 (백업)"
  "demo_screenshot_backup.png"
  (GenerateWithCode "Demo screenshot showing voice command interface")
  1000 600
  "#F3F4F6"
  "앱 화면 스크린샷 스타일. 상단: '음성 인식 중...' 텍스트. 가운데: 큰 마이크 아이콘 (애니메이션). 하단: 최근 명령어 리스트."

||| Slide 7 Image 1: Before - complex process (2 minutes)
export
before2MinutesSpec : ImageGenSpec
before2MinutesSpec = MkImageGenSpec
  "Before: 복잡한 과정 (2분)"
  "before_2_minutes.png"
  (GenerateWithCode "Before scenario: complex process taking 2 minutes")
  500 500
  "#FEE2E2"
  "빨간 배경. 'Before' 텍스트 (상단). 5개 박스가 세로로 연결 (복잡함). '2분 걸림' 텍스트 (하단, 큰 글씨)."

||| Slide 7 Image 2: After - simple voice command (2 seconds)
export
after2SecondsSpec : ImageGenSpec
after2SecondsSpec = MkImageGenSpec
  "After: 말 한마디 (2초)"
  "after_2_seconds.png"
  (GenerateWithCode "After scenario: simple voice command taking 2 seconds")
  500 500
  "#D1FAE5"
  "초록 배경. 'After' 텍스트 (상단). 말풍선 1개 (간단함). '2초!' 텍스트 (하단, 큰 글씨)."

||| Slide 7 Image 3: 60x faster number
export
sixtyTimesFasterSpec : ImageGenSpec
sixtyTimesFasterSpec = MkImageGenSpec
  "숫자 강조: 60배 빨라짐"
  "sixty_times_faster.png"
  (GenerateWithCode "Large '60x' number emphasizing speed improvement")
  600 400
  "#FFFFFF"
  "거대한 '60×' 숫자. 초록색(#10B981). 굵은 폰트. 주변에 속도선(speed lines). 아래에 '빨라짐!' 텍스트."

||| Slide 7 Image 4: 30 minutes saved per day
export
thirtyMinutesSavedSpec : ImageGenSpec
thirtyMinutesSavedSpec = MkImageGenSpec
  "하루 30분 절약"
  "thirty_minutes_saved.png"
  (GenerateWithCode "Clock icon showing 30 minutes saved daily")
  600 400
  "#FFFFFF"
  "시계 아이콘. 초록색(#10B981). 숫자 '30분' 강조. 아래에 '하루 절약' 텍스트. 긍정적인 느낌."

||| Slide 8 Image 1: Elderly scenario
export
elderlyScenarioSpec : ImageGenSpec
elderlyScenarioSpec = MkImageGenSpec
  "시나리오 1: 어르신 - 큰 글씨 필요없이"
  "elderly_scenario.png"
  (GenerateWithCode "Elderly person using voice control without needing large text")
  400 400
  "#FFFFFF"
  "어르신 캐릭터. 심플한 스타일. 말풍선으로 명령. 폰/기기 없이. 파란색(#3B82F6). '큰 글씨 필요없이' 텍스트."

||| Slide 8 Image 2: Worker scenario
export
workerScenarioSpec : ImageGenSpec
workerScenarioSpec = MkImageGenSpec
  "시나리오 2: 바쁜 직장인 - 운전 중에도"
  "worker_scenario.png"
  (GenerateWithCode "Busy worker using voice control while driving")
  400 400
  "#FFFFFF"
  "직장인 캐릭터. 운전 중. 핸들을 잡고 있음. 말풍선으로 명령. 파란색(#3B82F6). '운전 중에도' 텍스트."

||| Slide 8 Image 3: Disability scenario
export
disabilityScenarioSpec : ImageGenSpec
disabilityScenarioSpec = MkImageGenSpec
  "시나리오 3: 장애인 - 손 사용 불편해도"
  "disability_scenario.png"
  (GenerateWithCode "Person with disability using voice control without hands")
  400 400
  "#FFFFFF"
  "장애인 캐릭터. 손을 사용하지 않음. 말풍선으로 명령. 파란색(#3B82F6). '손 사용 불편해도' 텍스트."

||| Slide 8 Image 4: Technology for everyone
export
inclusiveTechSpec : ImageGenSpec
inclusiveTechSpec = MkImageGenSpec
  "모두를 위한 기술"
  "inclusive_technology.png"
  (GenerateWithCode "Inclusive technology concept with diverse people")
  1200 500
  "#FFFFFF"
  "상단: '모두를 위한 기술' 텍스트 (초록색 #10B981). 3명의 사람 실루엣 (어르신, 직장인, 장애인). 평등함을 표현."

||| Slide 9 Image 1: Connected world
export
connectedWorldSpec : ImageGenSpec
connectedWorldSpec = MkImageGenSpec
  "지구 아이콘 + 연결된 사람들"
  "connected_world.png"
  (GenerateWithCode "Globe icon with people connected around it")
  800 600
  "#FFFFFF"
  "가운데 지구 아이콘 (파란색 #3B82F6). 주변에 8개 작은 원 (사람들). 지구와 선으로 연결. 초록색(#10B981) 연결선. 글로벌 네트워크 느낌."

||| Slide 9 Image 2: Bright future
export
brightFutureSpec : ImageGenSpec
brightFutureSpec = MkImageGenSpec
  "밝은 미래 이미지"
  "bright_future.png"
  (GenerateWithCode "Bright future illustration with rising sun")
  800 600
  "#FEF3C7"
  "떠오르는 태양. 노란색/오렌지(#F59E0B). 햇살 광선. 상단에 '밝은 미래' 텍스트. 희망적인 느낌. 따뜻한 색조."

||| Slide 9 Image 3: Expansion vision
export
expansionVisionSpec : ImageGenSpec
expansionVisionSpec = MkImageGenSpec
  "확장 가능성: 스마트홈, 자동차, 가전제품..."
  "expansion_vision.png"
  (GenerateWithCode "Expansion possibilities: smart home, car, appliances")
  800 600
  "#FFFFFF"
  "3-4개 아이콘. 1) 집 (스마트홈) 2) 자동차 3) 가전제품 (TV, 세탁기). 화살표로 연결. 확장성 표현. 보라색(#7C3AED)."

||| Slide 10 Image 1: QR code
export
qrCodeGithubSpec : ImageGenSpec
qrCodeGithubSpec = MkImageGenSpec
  "QR 코드 (GitHub)"
  "qr_code_github.png"
  (GenerateWithCode "QR code for GitHub repository")
  400 400
  "#FFFFFF"
  "QR 코드. 검은색/흰색. 전형적인 QR 패턴. 모서리에 3개 큰 사각형 마커. 아래에 'GitHub' 작은 텍스트."

||| Slide 10 Image 2: SoundToAct logo (final)
export
soundToActLogoFinalSpec : ImageGenSpec
soundToActLogoFinalSpec = MkImageGenSpec
  "SoundToAct 로고"
  "soundtoact_logo_final.png"
  (GenerateWithCode "SoundToAct logo - final version with tagline")
  800 400
  "#FFFFFF"
  "SoundToAct 로고. 파란색(#2563EB) 텍스트. 아래에 작은 태그라인 '말 한마디로 움직이는 세상' (보라색 #7C3AED). 심플하고 전문적인 느낌."

--------------------------------------------------------------------------------
-- All Image Specifications
--------------------------------------------------------------------------------

||| Complete list of all image generation specifications
export
allImageSpecs : List ImageGenSpec
allImageSpecs =
  [ waveformSpec
  , microphoneLargeSpec
  , studentWakingSpec
  , complexProcessSpec
  , clockTwoMinutesSpec
  , questionMarkLargeSpec
  , speechBubbleMomSpec
  , lightBulbIdeaSpec
  , projectLogoLargeSpec
  , demoVideoPlaceholderSpec
  , beforeAfterComparisonSpec
  , step1ListenSpec
  , step2UnderstandSpec
  , step3ActSpec
  , threeStepFlowSpec
  , liveDemoVideoSpec
  , demoScreenshotSpec
  , before2MinutesSpec
  , after2SecondsSpec
  , sixtyTimesFasterSpec
  , thirtyMinutesSavedSpec
  , elderlyScenarioSpec
  , workerScenarioSpec
  , disabilityScenarioSpec
  , inclusiveTechSpec
  , connectedWorldSpec
  , brightFutureSpec
  , expansionVisionSpec
  , qrCodeGithubSpec
  , soundToActLogoFinalSpec
  ]

||| Proof that we have 30 image specifications
export
totalImageCount : Nat
totalImageCount = 30

||| Get image spec by visual description
export
findImageSpec : String -> Maybe ImageGenSpec
findImageSpec desc = find (\spec => visualDescription spec == desc) allImageSpecs
