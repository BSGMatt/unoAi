from carddeck import *
from player import Player, PlayerAction

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
        self.eventComplete = False
        pass
    
    def eventOccured(self, gameState) -> bool:
        pass
    
    def modifyGameState(self, gameState):
        pass
    
    def getActions(self, gameState):
        return []
    
class SkipEvent(GameEvent):
    
    def eventOccured(self, gameState) -> bool:
        print("TopCard Value:", gameState.deck.topCard.value);
        return gameState.deck.topCard.value == SKIP;
    
    def modifyGameState(self, gameState):
        gameState.nextPlayer(0);
        print("SkipEvent - Next player will be", gameState.whoseTurn);
        self.eventComplete = True;
        
    def getActions(self, gameState):
        return []
        
class WildEvent(GameEvent):
    
    def __init__(self):
        super().__init__();
        self.enforced = True
    
    def eventOccured(self, gameState) -> bool:
        return gameState.deck.topCard.color == WILD_COLOR;
    
    def modifyGameState(self, gameState):
        player = gameState.players[gameState.whoseTurn];
        playerAction = player.forceAction(gameState, self.getActions(gameState));
        if (playerAction.actionName == 'Red'):
            gameState.deck.topCard.color = RED;
        elif (playerAction.actionName == 'Blue'):
            gameState.deck.topCard.color = BLUE;
        elif (playerAction.actionName == 'Green'):
            gameState.deck.topCard.color = GREEN;
        elif (playerAction.actionName == 'Yellow'):
            gameState.deck.topCard.color = YELLOW;
        else:
            print("Invalid color choice receieved! Picking Random Color.")
            gameState.deck.topCard.color = random.choice([RED, BLUE, GREEN, YELLOW]);
            
        self.eventComplete = True;
        
    def getActions(self, gameState):
        return [PlayerAction('Red', None), PlayerAction('Blue', None), PlayerAction('Green', None), PlayerAction('Yellow', None)]