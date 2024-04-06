
from gameState import GameState
from player import *

DRAW = "draw"
PLACE = "place"
UNO = "UNO"
NONE = "NONE"
    

def main():
    
    print("Welcome to UNO AI Version 0.0!");
    
    gameState = GameState();
    
    while (not(gameState.isTerminalState())):
        
        """
            To make implementing rules like Calling "Uno" or Jump-In's easier, 
            player's perform actions in a more "asynchronous" manner. Players 
            can perform actions regardless of whose turn it is. 
        """
        
        for player in gameState.players:
            
            print("\n");
            print("Player", player.id);
            print("\n");
            
            print("Top Card is a", gameState.deck.topCard);
            print("Your Hand:", player.cardsInHand);
            
            action = player.makeAction(gameState);
            
            if action.actionName == PLACE:
                player.cardsInHand.remove(action.card);
                gameState.deck.placeCard(action.card);
            elif action.actionName == DRAW:
                newCard = gameState.deck.drawCard();
                player.cardsInHand.append(newCard);
            elif action.actionName == UNO:
                #If the active player is calling UNO
                if (gameState.whoseTurn == player.id):
                    newCard = gameState.deck.drawCard();
                    player.cardsInHand.append(newCard);
                else:
                    newCard = gameState.deck.drawCard();
                    gameState.players[gameState.whoseTurn].cardsInHand.append(newCard);
                    
        gameState.nextPlayer();
                    
    print("Thanks for playing!");
    
    
    
    



if __name__ == "__main__":
    main();