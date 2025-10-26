||| SoundToAct Formal Specification
|||
||| This is the main module that re-exports all components of the SoundToAct system.
|||
||| Module Organization:
||| - Specs.Types: Basic types (ActionType, Keyword, ActionResult)
||| - Specs.Recognition: Voice recognition types (RecognitionEngine, RecognizerConfig)
||| - Specs.Errors: Error handling (VoiceError, VoiceResult)
||| - Specs.Actions: Action handlers and registry
||| - Specs.Keywords: Keyword-action mappings
||| - Specs.VoiceListener: Main voice listener logic
||| - Specs.API: API request/response types
module Specs.SoundToAct

-- Re-export all public types and functions
import public Specs.Types
import public Specs.Recognition
import public Specs.Errors
import public Specs.Actions
import public Specs.Keywords
import public Specs.VoiceListener
import public Specs.API

%default total

--------------------------------------------------------------------------------
-- Documentation
--------------------------------------------------------------------------------

{-
SoundToAct Type Specification
==============================

This formal specification describes the core logic of the SoundToAct
voice-triggered automation system.

Key Components:
---------------

1. Types (Specs.Types)
   - ActionType: Extensible String-based action types
   - Keyword: Case-insensitive keyword type
   - ActionResult: Result of action execution
   - ActionParams: Key-value parameter list

2. Recognition (Specs.Recognition)
   - RecognitionEngine: Whisper -> Google Korean -> Google English (fallback chain)
   - RecognitionResult: Success/failure with engine tracking
   - RecognizerConfig: Microphone configuration (energy threshold, sample rate, etc.)
   - MicrophoneState: Initialization tracking

3. Errors (Specs.Errors)
   - VoiceError: Explicit error types (no exceptions)
   - VoiceResult: Either VoiceError a (type-safe error handling)

4. Actions (Specs.Actions)
   - ActionHandler: Total functions (ActionParams -> ActionResult)
   - ActionRegistry: Type-safe handler lookup
   - Built-in actions: call, music, lights
   - Extensible: Custom actions supported

5. Keywords (Specs.Keywords)
   - KeywordAction: Maps keyword to action type and params
   - KeywordMappings: List-based storage (vs Python's Dict)
   - Case-insensitive substring matching

6. VoiceListener (Specs.VoiceListener)
   - Main state container
   - Keyword registration/unregistration
   - Recognition result processing
   - Action execution coordination

7. API (Specs.API)
   - REST API types matching Python Pydantic models
   - Request/response types for all endpoints

Properties Verified:
--------------------

✓ Totality: All functions terminate (enforced by %default total)
✓ Type Safety: Invalid action types handled explicitly
✓ Extensibility: Custom actions can be added
✓ Error Handling: All errors are typed (VoiceError)
✓ Case Insensitivity: Keyword matching uses toLower

Implementation Mapping:
-----------------------

Python Implementation         →  Idris2 Specification
------------------------         ---------------------
action_type: str             →  ActionType = String
Dict[str, Callable]          →  List KeywordAction
Optional[sr.Microphone]      →  MicrophoneState
sr.Recognizer properties     →  RecognizerConfig
Exceptions                   →  VoiceError / VoiceResult
Whisper->Google fallback     →  RecognitionEngine (explicit)

Usage Examples:
---------------

See Specs.VoiceListener.Examples for:
- exampleRegisterCall: Register a keyword
- exampleProcess: Process recognized text
- exampleMultiple: Multiple keyword handling
- exampleCustomAction: Adding custom actions

For detailed documentation on each module, see the respective .idr files.
-}
