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
    
class ReverseEvent(GameEvent):
    
    def eventOccured(self, gameState) -> bool:
        return gameState.deck.topCard.value == REVERSE;
    
    def modifyGameState(self, gameState):
        gameState.orderReversed = not(gameState.orderReversed);
        
class UnoCalledEvent(GameEvent):
    
    def eventOccured(self, gameState) -> bool:
        return gameState.lastPlayerAction[gameState.whoseTurn].actionName == 'uno'
    
    """
        Allow the active player to perform an action after calling UNO. 
    """
    def modifyGameState(self, gameState):
        player = gameState.players[gameState.whoseTurn];
        action = player.forceAction(gameState, self.getActions(gameState));
        
        if action.actionName == 'place':
            player.cardsInHand.remove(action.card);
            gameState.deck.placeCard(action.card);
            gameState.lastPlayerAction[gameState.whoseTurn] = action;  
            gameState.lastPlayerAction[player.id] = action;
        else :
            print("You must place down a card!");
            
                 
            
    #Get normal actions, excluding DRAW or UNO. 
    def getActions(self, gameState):
        playerActions = gameState.getLegalActions(gameState.whoseTurn);
        return [action for action in playerActions if action.actionName != "Uno" or action.actionName != "Draw"]
        
        