module Specs.Recognition

%default total

--------------------------------------------------------------------------------
-- Voice Recognition Types
--------------------------------------------------------------------------------

||| Recognition engines available (with fallback order)
public export
data RecognitionEngine
  = WhisperKorean
  | GoogleKorean
  | GoogleEnglish

export
Show RecognitionEngine where
  show WhisperKorean = "Whisper (Korean)"
  show GoogleKorean = "Google Speech (ko-KR)"
  show GoogleEnglish = "Google Speech (English)"

||| Voice recognition result with engine information
public export
data RecognitionResult : Type where
  ||| Successful recognition with engine used and text
  Recognized : RecognitionEngine -> String -> RecognitionResult
  ||| No speech detected or timeout
  NotRecognized : RecognitionResult
  ||| Recognition service error
  RecognitionError : String -> RecognitionResult

export
Show RecognitionResult where
  show (Recognized engine text) = "Recognized[\{show engine}]: \{text}"
  show NotRecognized = "NotRecognized"
  show (RecognitionError err) = "RecognitionError: \{err}"

||| Recognizer configuration for voice capture
public export
record RecognizerConfig where
  constructor MkRecognizerConfig
  ||| Energy threshold for voice detection (50 = very sensitive)
  energyThreshold : Nat
  ||| Pause threshold in seconds before phrase is complete
  pauseThreshold : Double
  ||| Sample rate in Hz (48000 = high quality)
  sampleRate : Nat
  ||| Whether to dynamically adjust energy threshold
  dynamicEnergyThreshold : Bool

||| Default recognizer configuration (optimized for quiet environments)
export
defaultRecognizerConfig : RecognizerConfig
defaultRecognizerConfig = MkRecognizerConfig 50 0.8 48000 False

||| Microphone state
public export
data MicrophoneState
  = NotInitialized
  | Initialized RecognizerConfig

export
Show MicrophoneState where
  show NotInitialized = "Microphone not initialized"
  show (Initialized cfg) = "Microphone initialized (threshold=\{show cfg.energyThreshold})"
