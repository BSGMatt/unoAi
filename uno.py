
from gameState import GameState
from actions import PlayerActionNames as Actions
from player import *
import sys

"""
DRAW = "draw"
PLACE = "place"
UNO = "uno"
NONE = "none"
""" 

def main():
    
    print("Welcome to UNO AI Version 0.0!");
    
    #Process command line args. 
    
    args = sys.argv;
    numCards = 7;
    numPlayers = 2;
    deckType = 0;
    
    for i in range(len(args)):
        if (args[i] == '--numCards'):
            if (i + 1 >= len(args)):
                print("Need to specify --numCards! (i.e, --numCards 7)");
                sys.exit();
            else:
                numCards = int(args[i + 1]);
        elif (args[i] == '--deckType'):
            if (i + 1 >= len(args)):
                print("Need to specify --wilds! (i.e, --wilds 0)");
                sys.exit();
            else:
                """
                    0 for standard deck
                    1 for wilds and wild +4's only
                    2 for skips only
                    3 for reverses only
                    4 for draw 2's only
                """
                deckType = int(args[i + 1]);
        if (args[i] == '--numPlayers'):
            if (i + 1 >= len(args)):
                print("Need to specify --numPlayers! (i.e, --numPlayers 4)");
                sys.exit();
            else:
                numPlayers = int(args[i + 1]);
            
    
    gameState = GameState(numCardsAtStart=numCards, numPlayers=numPlayers, deckOptions=deckType);
    
    while (not(gameState.isTerminalState())):
        
        """
            To make make events like calling "UNO" or "Jump-In's" easier, I plan to implement
            multhreading down the line. For now, we're using a psuedo-multithreading approach where
            each player can have a set of actions they can take wether it's their turn or not, just with 
            a predefined order. 
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
            print("Player", player.id,"'s Hand:", player.cardsInHand);
            
            action = player.makeAction(gameState);
            gameState.lastPlayerAction[player.id] = action;
            

        #Handle any events that have been triggered due to player actions.
        for event in gameState.gameEvents:
            if (not(event.ignore) and event.eventOccured(gameState)):
                print ("A", event.name, "has occured!");
                event.modifyGameState(gameState);
            event.ignore = False;
                

        gameState.nextPlayer();
        print("Next player will be:", gameState.whoseTurn);
                    
    logResults(gameState);                
    
    print("Thanks for playing!");
    
def logResults(gameState: GameState):
    
    for player in gameState.players:
        if (len(player.cardsInHand) == 0):
            print("Player %d wins!" % (player.id))
        else:
            print("Player %d had %d cards left!" % (player.id, len(player.cardsInHand)))

if __name__ == "__main__":
    main();