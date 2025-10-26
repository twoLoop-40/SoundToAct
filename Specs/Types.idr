module Specs.Types

import Data.String

%default total

--------------------------------------------------------------------------------
-- Basic Types
--------------------------------------------------------------------------------

||| Action types - extensible via String to allow custom actions
||| Built-in types: "call", "music", "lights"
public export
ActionType : Type
ActionType = String

||| Standard action types
public export
callActionType : ActionType
callActionType = "call"

public export
musicActionType : ActionType
musicActionType = "music"

public export
lightsActionType : ActionType
lightsActionType = "lights"

||| Action parameters as key-value pairs
public export
ActionParams : Type
ActionParams = List (String, String)

||| Result of action execution
public export
record ActionResult where
  constructor MkActionResult
  status : String
  actionType : ActionType
  message : String

export
Show ActionResult where
  show r = "ActionResult(status=\{r.status}, type=\{r.actionType}, message=\{r.message})"

||| Non-empty keyword type (runtime check)
public export
record Keyword where
  constructor MkKeyword
  text : String

export
Eq Keyword where
  (MkKeyword t1) == (MkKeyword t2) = toLower t1 == toLower t2

export
Show Keyword where
  show (MkKeyword t) = t

||| Convert string to keyword if non-empty
export
toKeyword : (s : String) -> Maybe Keyword
toKeyword "" = Nothing
toKeyword s = Just (MkKeyword s)
