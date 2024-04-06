from gameState import GameState
from carddeck import *
from player import PlayerAction

"""
    Some cards can cause events that can change the state of the 
    game significantly. This file contains specific events the game will check each time player performs
    an action. 
"""

"""
    Abstract class to describe such an event. 
"""
class GameEvent:
    
    """
        enforced - Whether the player must perform one of the actions
        provided. 
    """
    
    def __init__(self):
        self.enforced = False
        pass
    
    def eventOccured(self, gameState: GameState) -> bool:
        pass
    
    def modifyGameState(self, gameState: GameState):
        pass
    
    def getActions(self, gameState: GameState):
        return []
    
class SkipEvent(GameEvent):
    
    def eventOccured(self, gameState: GameState) -> bool:
        return gameState.deck.topCard.value == SKIP;
    
    def modifyGameState(self, gameState: GameState):
        gameState.nextPlayer(0);
        
    def getActions(self, gameState: GameState):
        return []
        
class PickColorEvent(GameEvent):
    
    def __init__(self):
        self.enforced = True
        pass
    
    def eventOccured(self, gameState: GameState) -> bool:
        return gameState.deck.topCard.color == WILD_COLOR;
    
    def modifyGameState(self, gameState: GameState):
        gameState.nextPlayer(-1);
        
    def getActions(self, gameState: GameState):
        return 