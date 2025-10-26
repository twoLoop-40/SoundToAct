module Specs.Errors

import Specs.Types

%default total

--------------------------------------------------------------------------------
-- Error Types
--------------------------------------------------------------------------------

||| Errors that can occur in the voice system
public export
data VoiceError
  = MicrophoneNotInitialized
  | AudioCaptureError String
  | RecognitionServiceError String
  | UnknownActionType ActionType
  | InvalidKeyword String

export
Show VoiceError where
  show MicrophoneNotInitialized = "Microphone not initialized. Call initialize() first."
  show (AudioCaptureError msg) = "Audio capture failed: \{msg}"
  show (RecognitionServiceError msg) = "Recognition service error: \{msg}"
  show (UnknownActionType at) = "Unknown action type: \{at}"
  show (InvalidKeyword kw) = "Invalid keyword: \{kw}"

||| Result type for operations that can fail
public export
VoiceResult : Type -> Type
VoiceResult a = Either VoiceError a
