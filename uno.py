
from gameState import GameState
from player import *

DRAW = "draw"
PLACE = "place"
UNO = "uno"
NONE = "none"
    

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
            
            if (player.id == gameState.whoseTurn):
                print("");
                print("It's Player ", player.id,"'s Turn!!", sep="");
                print("");
            else:
                print("");
                print("Player ", player.id,"'s Stats:", sep="");
                print("");
            
            print("Top Card is a", gameState.deck.topCard);
            print("Your Hand:", player.cardsInHand);
            
            action = player.makeAction(gameState);
            
            if action.actionName == PLACE:
                player.cardsInHand.remove(action.card);
                gameState.deck.placeCard(action.card);
                gameState.lastPlayerAction[player.id] = action;
            elif action.actionName == DRAW:
                newCard = gameState.deck.drawCard();
                player.cardsInHand.append(newCard);
                gameState.lastPlayerAction[player.id] = action;
            elif action.actionName == UNO:
                #If the active player is calling UNO
                if (gameState.whoseTurn == player.id):
                    newCard = gameState.deck.drawCard();
                    player.cardsInHand.append(newCard);
                    gameState.lastPlayerAction[player.id] = action;
                else:
                    newCard = gameState.deck.drawCard();
                    gameState.players[gameState.whoseTurn].cardsInHand.append(newCard);
                    gameState.lastPlayerAction[player.id] = action;

        #Handle any events that have been triggered due to player actions.
        for event in gameState.gameEvents:
            if (event.eventOccured(gameState)):
                event.modifyGameState(gameState);
                

        gameState.nextPlayer();
        print("Next player will be:", gameState.whoseTurn);
                    
    print("Thanks for playing!");

if __name__ == "__main__":
    main();