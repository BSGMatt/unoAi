'''
    This script is runs a set number of uno games and tracks the winrates of each player. 
'''
import uno
import time

def runGames():
    
    sys = uno.sys;
    args = sys.argv;
    numCards = 7;
    numPlayers = 2;
    numHumans = 1;
    deckType = 0;
    gameMode = "random";
    numGames = 1;
    
    for i in range(len(args)):
        if (args[i] == '--numGames'):
            if (i + 1 >= len(args)):
                print("Need to specify --numGames! (i.e, --numCards 10)");
                sys.exit();
            else:
                numGames = int(args[i + 1]);
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
        if (args[i] == '--numHumans'):
            if (i + 1 >= len(args)):
                print("Need to specify --numHumans! (i.e, --numHumans 2)");
                sys.exit();
            else:
                numHumans = int(args[i + 1]);
        if (args[i] == '--gameMode'):
            if (i + 1 >= len(args)):
                print("Need to specify --gameMode! (i.e, --gameMode random or --gameMode reflex)");
                sys.exit();
            else:
                gameMode = str(args[i+1])
        if (args[i] == '--agentList'):
            if (i + 1 >= len(args)):
                print("Need to specify --gameMode! (i.e, --gameMode random or --gameMode reflex)");
                sys.exit();
            else:
                gameMode = str(args[i+1])
                 
    gameLog = {};

    for i in range(numPlayers):
        gameLog[i] = 0;

    runStartTime = time.time()

    for i in range(numGames):
        gameState = uno.GameState(numCardsAtStart=numCards, numPlayers=numPlayers, deckOptions=deckType, gameMode=gameMode, numHumanAgents=numHumans);
        gameLog[uno.runGame(gameState).id] += 1 / numGames;
        
    for id in list(gameLog.keys()):
        print("Winrate for Player", id, "was: ", gameLog[id]);
        
    endTime = time.time() - runStartTime;
    print("Game(s) completed in ", endTime, "seconds.");


runGames();