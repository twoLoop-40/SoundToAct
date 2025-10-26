module Specs.API

import Data.Maybe
import Specs.Types

%default total

--------------------------------------------------------------------------------
-- API Types (matching Python Pydantic models)
--------------------------------------------------------------------------------

||| Request to register a keyword (POST /keywords)
public export
record KeywordCreateRequest where
  constructor MkKeywordCreateRequest
  keyword : String
  actionType : ActionType  -- Extensible String
  actionParams : Maybe ActionParams

||| Response after registering keyword
public export
record KeywordResponse where
  constructor MkKeywordResponse
  keyword : Keyword
  actionType : ActionType
  actionParams : Maybe ActionParams
  isActive : Bool

||| Request for listening (POST /listen)
public export
record ListenRequest where
  constructor MkListenRequest
  timeout : Nat
  phraseTimeLimit : Nat

||| Response after listening
public export
record ListenResponse where
  constructor MkListenResponse
  recognizedText : String
  triggeredKeywords : List Keyword
  actionMessages : List String
  success : Bool

||| Status response (GET /status)
public export
record StatusResponse where
  constructor MkStatusResponse
  isListening : Bool
  registeredKeywords : List Keyword
  message : String
