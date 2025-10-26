module Specs.Actions

import Data.List
import Data.Maybe
import Specs.Types
import Specs.Errors

%default total

--------------------------------------------------------------------------------
-- Action Handler Type
--------------------------------------------------------------------------------

||| Action handler function type
||| Handlers must be total and always return a result
public export
ActionHandler : Type
ActionHandler = ActionParams -> ActionResult

||| Default implementations for built-in actions
export
callAction : ActionHandler
callAction params =
  let contact = fromMaybe "엄마" (lookup "contact" params)
      number = fromMaybe "" (lookup "number" params)
      msg = contact ++ "에게 전화를 걸었습니다."
  in MkActionResult "success" callActionType msg

export
musicAction : ActionHandler
musicAction params =
  let song = fromMaybe "음악" (lookup "song" params)
      msg = song ++ "을 재생했습니다."
  in MkActionResult "success" musicActionType msg

export
lightsAction : ActionHandler
lightsAction params =
  let state = fromMaybe "off" (lookup "state" params)
      room = fromMaybe "전체" (lookup "room" params)
      stateText = if state == "on" then "켰습니다" else "껐습니다"
      msg = room ++ " 불을 " ++ stateText
  in MkActionResult "success" lightsActionType msg

--------------------------------------------------------------------------------
-- Action Registry
--------------------------------------------------------------------------------

||| Registry mapping action types to handlers
public export
record ActionRegistry where
  constructor MkActionRegistry
  handlers : List (ActionType, ActionHandler)

||| Get handler for a given action type
export
getHandler : ActionRegistry -> ActionType -> Maybe ActionHandler
getHandler (MkActionRegistry handlers) actionType =
  lookup actionType handlers

||| Default action registry with built-in actions
export
defaultRegistry : ActionRegistry
defaultRegistry = MkActionRegistry
  [ (callActionType, callAction)
  , (musicActionType, musicAction)
  , (lightsActionType, lightsAction)
  ]

||| Register a new action handler
export
registerAction : ActionRegistry -> ActionType -> ActionHandler -> ActionRegistry
registerAction (MkActionRegistry handlers) actionType handler =
  MkActionRegistry ((actionType, handler) :: handlers)

||| Create an action result from registry (with error handling)
export
createAction : ActionRegistry ->
               ActionType ->
               ActionParams ->
               VoiceResult ActionResult
createAction registry actionType params =
  case getHandler registry actionType of
    Nothing => Left (UnknownActionType actionType)
    Just handler => Right (handler params)

--------------------------------------------------------------------------------
-- Properties
--------------------------------------------------------------------------------

||| Proof that action execution is total
||| All handlers must return a result (enforced by type system)
export
actionHandlerTotal : (handler : ActionHandler) ->
                     (params : ActionParams) ->
                     (result : ActionResult ** result = handler params)
actionHandlerTotal handler params = (handler params ** Refl)
