module Specs.Keywords

import Data.List
import Data.String
import Specs.Types

%default total

--------------------------------------------------------------------------------
-- Keyword-Action Mapping
--------------------------------------------------------------------------------

||| Mapping from keyword to action
public export
record KeywordAction where
  constructor MkKeywordAction
  keyword : Keyword
  actionType : ActionType
  actionParams : ActionParams

export
Show KeywordAction where
  show ka = "KeywordAction(\{show ka.keyword} -> \{ka.actionType})"

||| Keyword-action mappings
||| Implementation note: Python uses Dict[str, Callable], we use List for simplicity
public export
KeywordMappings : Type
KeywordMappings = List KeywordAction

||| Add a keyword-action mapping
export
addMapping : KeywordMappings -> KeywordAction -> KeywordMappings
addMapping mappings ka = ka :: mappings

||| Remove all mappings for a keyword
export
removeMapping : KeywordMappings -> Keyword -> KeywordMappings
removeMapping mappings key = filter (\ka => ka.keyword /= key) mappings

||| Get all actions for a keyword
export
getActions : KeywordMappings -> Keyword -> List KeywordAction
getActions mappings key = filter (\ka => ka.keyword == key) mappings

||| Check if keyword is registered
export
isRegistered : KeywordMappings -> Keyword -> Bool
isRegistered mappings key = not $ null (getActions mappings key)

||| Check if text contains a keyword (case-insensitive, substring match)
export
containsKeyword : Keyword -> String -> Bool
containsKeyword (MkKeyword kw) text =
  isInfixOf (toLower kw) (toLower text)
