module Specs.VoiceListener

import Data.List
import Data.Maybe
import Specs.Types
import Specs.Recognition
import Specs.Errors
import Specs.Actions
import Specs.Keywords

%default total

--------------------------------------------------------------------------------
-- Voice Listener
--------------------------------------------------------------------------------

||| Voice listener state
||| Corresponds to Python's VoiceListener class
public export
record VoiceListener where
  constructor MkVoiceListener
  ||| Whether currently in continuous listening mode
  isListening : Bool
  ||| Microphone initialization state
  microphoneState : MicrophoneState
  ||| Recognizer configuration
  recognizerConfig : RecognizerConfig
  ||| Keyword-action mappings
  mappings : KeywordMappings
  ||| Action registry
  registry : ActionRegistry

||| Initialize voice listener with default configuration
export
initListener : VoiceListener
initListener = MkVoiceListener False NotInitialized defaultRecognizerConfig [] defaultRegistry

||| Initialize microphone with given configuration
export
initializeMicrophone : VoiceListener -> RecognizerConfig -> VoiceListener
initializeMicrophone listener config =
  { microphoneState := Initialized config
  , recognizerConfig := config
  } listener

||| Register a keyword-action mapping
export
registerKeyword : VoiceListener ->
                  Keyword ->
                  ActionType ->
                  ActionParams ->
                  VoiceListener
registerKeyword listener keyword actionType params =
  let ka = MkKeywordAction keyword actionType params
      newMappings = addMapping listener.mappings ka
  in { mappings := newMappings } listener

||| Unregister a keyword
export
unregisterKeyword : VoiceListener -> Keyword -> VoiceListener
unregisterKeyword listener keyword =
  { mappings := removeMapping listener.mappings keyword } listener

||| Get all registered keywords
export
getKeywords : VoiceListener -> List Keyword
getKeywords listener = map keyword listener.mappings

||| Find all matching keywords in recognized text
export
findMatchingKeywords : VoiceListener -> String -> List KeywordAction
findMatchingKeywords listener text =
  filter (\ka => containsKeyword ka.keyword text) listener.mappings

||| Execute actions for matched keywords
||| Returns list of (keyword, result or error)
export
executeMatched : VoiceListener ->
                 List KeywordAction ->
                 List (Keyword, VoiceResult ActionResult)
executeMatched listener [] = []
executeMatched listener (ka :: kas) =
  let result = createAction listener.registry ka.actionType ka.actionParams
  in (ka.keyword, result) :: executeMatched listener kas

||| Process recognition result and trigger actions
export
processRecognition : VoiceListener ->
                     RecognitionResult ->
                     List (Keyword, VoiceResult ActionResult)
processRecognition listener NotRecognized = []
processRecognition listener (RecognitionError _) = []
processRecognition listener (Recognized _ text) =
  let matched = findMatchingKeywords listener text
  in executeMatched listener matched

||| Listen once with timeout and phrase limit
||| Note: Actual microphone I/O is side-effectful and not represented here
||| This is the logical specification of the operation
export
listenOnceSpec : VoiceListener ->
                 (timeout : Nat) ->
                 (phraseTimeLimit : Nat) ->
                 VoiceResult RecognitionResult
listenOnceSpec listener timeout phraseTimeLimit =
  case listener.microphoneState of
    NotInitialized => Left MicrophoneNotInitialized
    Initialized _ => Right NotRecognized  -- Placeholder for actual I/O

--------------------------------------------------------------------------------
-- Example Usage
--------------------------------------------------------------------------------

namespace Examples

  ||| Example: Register "엄마" keyword for calling mom
  export
  exampleRegisterCall : VoiceListener
  exampleRegisterCall =
    case toKeyword "엄마" of
      Nothing => initListener
      Just kw => registerKeyword initListener kw callActionType
                   [("contact", "엄마"), ("number", "01012345678")]

  ||| Example: Process recognized text containing "엄마"
  export
  exampleProcess : List (Keyword, VoiceResult ActionResult)
  exampleProcess = processRecognition exampleRegisterCall (Recognized WhisperKorean "엄마")

  ||| Example: Multiple keywords
  export
  exampleMultiple : VoiceListener
  exampleMultiple =
    let l1 = case toKeyword "엄마" of
               Nothing => initListener
               Just kw => registerKeyword initListener kw callActionType
                           [("contact", "엄마")]
        l2 = case toKeyword "음악" of
               Nothing => l1
               Just kw => registerKeyword l1 kw musicActionType
                           [("song", "좋아하는 노래")]
    in l2

  ||| Example: Process text with multiple keywords
  export
  exampleMultipleProcess : List (Keyword, VoiceResult ActionResult)
  exampleMultipleProcess =
    processRecognition exampleMultiple (Recognized GoogleKorean "엄마 음악")

  ||| Example: Custom action type
  export
  exampleCustomAction : ActionHandler
  exampleCustomAction params =
    let name = fromMaybe "사용자" (lookup "name" params)
    in MkActionResult "success" "custom_greeting" ("안녕하세요 " ++ name ++ "님")

  ||| Example: Register custom action
  export
  exampleWithCustom : ActionRegistry
  exampleWithCustom = registerAction defaultRegistry "custom_greeting" exampleCustomAction
