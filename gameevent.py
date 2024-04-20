from carddeck import *
from player import Player, PlayerAction
from actions import PlayerActionNames as pan

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
    
    def __init__(self, order):
        self.order = order;
        self.enforced = False
        self.eventComplete = False
        self.name = "Generic Event"
        self.ignore = False
        pass
    
    def eventOccured(self, gameState) -> bool:
        pass
    
    def modifyGameState(self, gameState):
        pass
    
    def getActions(self, gameState):
        return []
    
class DrawCardEvent(GameEvent):
    
    def __init__(self, order):
        super().__init__(order)
        self.name = "Draw Card Event"
        
    def eventOccured(self, gameState) -> bool:
        #print(gameState.lastPlayerAction[gameState.whoseTurn]);
        return gameState.lastPlayerAction[gameState.whoseTurn].actionName == pan.DRAW;
    
    def modifyGameState(self, gameState):
        newCard = gameState.deck.drawCard();
        gameState.players[gameState.whoseTurn].cardsInHand.append(newCard);
        
class PlaceCardEvent(GameEvent):
    
    def __init__(self, order):
        super().__init__(order)
        self.name = "Place Card Event"
        
    def eventOccured(self, gameState) -> bool:
        print("Action", gameState.lastPlayerAction[gameState.whoseTurn]);
        return gameState.lastPlayerAction[gameState.whoseTurn].actionName == pan.PLACE;
    
    def modifyGameState(self, gameState):
        player = gameState.players[gameState.whoseTurn];
        print("Player", gameState.whoseTurn, "'s deck", player.cardsInHand);
        player.cardsInHand.remove(gameState.lastPlayerAction[player.id].card);
        gameState.deck.placeCard(gameState.lastPlayerAction[player.id].card);
    
class SkipEvent(GameEvent):
    
    def __init__(self, order):
        super().__init__(order)
        self.name = "Skip Event"
    
    def eventOccured(self, gameState) -> bool:
        print("TopCard Value:", gameState.deck.topCard.value);
        return gameState.lastPlayerAction[gameState.whoseTurn].card.value == SKIP;
    
    def modifyGameState(self, gameState):
        gameState.nextPlayer(0);
        print("SkipEvent - Next player will be", gameState.whoseTurn);
        self.eventComplete = True;
        
class WildEvent(GameEvent):
    
    def __init__(self, order):
        super().__init__(order);
        self.enforced = True
        self.name = "Wild Event"
    
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
    
    def __init__(self, order):
        super().__init__(order)
        self.name = "Reverse Event"
    
    def eventOccured(self, gameState) -> bool:
        return gameState.deck.topCard.value == REVERSE;
    
    def modifyGameState(self, gameState):
        gameState.orderReversed = not(gameState.orderReversed);
        

class UnoCalledEvent(GameEvent):
    
    def __init__(self, order):
        super().__init__(order);
        self.playerWhoCalledId = -1
        self.name = "Uno Called Event"
    
    def eventOccured(self, gameState) -> bool:
        
        for player in gameState.players:
            if (gameState.lastPlayerAction[player.id].actionName == pan.UNO):
                self.playerWhoCalledId = player.id
                return True;
        
        return False;
    
    """
        If the player who called UNO was the current player:
        
    """
    def modifyGameState(self, gameState):
        
        print("")
        print("Player", self.playerWhoCalledId,"called UNO!")
        print("")
        
        currentPlayer = gameState.players[gameState.whoseTurn];
        
        #Uno was called by current player. Let them place a card. 
        if (self.playerWhoCalledId == currentPlayer.id):
            action = currentPlayer.forceAction(gameState, self.getActions(gameState));
            if action.actionName == pan.PLACE:
                gameState.lastPlayerAction[currentPlayer.id] = action;  
            else :
                print("You must place down a card!");  
             
        elif (self.playerWhoCalledId != -1):
            #Someone else called uno before current player. Current player must draw 2 cards.
            newCard = gameState.deck.drawCard();
            currentPlayer.cardsInHand.append(newCard);
            newCard = gameState.deck.drawCard();
            currentPlayer.cardsInHand.append(newCard); 
            
            #Prevent any events from occuring after uno has been called. 
            gameState.cancelFutureEvents(self);
            
    #Get normal actions, excluding DRAW or UNO. 
    def getActions(self, gameState):
        playerActions = gameState.getLegalActions(gameState.whoseTurn);
        return [action for action in playerActions if action.actionName == pan.PLACE]
        
        