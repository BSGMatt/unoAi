from playeraction import PlayerAction

class Agent:
    
    def getAction(self, playerID: int, gameState):
        pass
    
    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        pass
    
class HumanAgent(Agent):
    
    def getAction(self, playerID: int, gameState):
        playerActions = gameState.getLegalActions(playerID);
        
        if (len(playerActions) == 0):
            return PlayerAction('None', None);
        
        print("Here's your possible actions: ");
        
        #Print out all of the player's actions. 
        for i in range(len(playerActions)):
            print(i, playerActions[i]);
        
        choice = input("Which action?\n");
        choiceInt = int(choice);
        
        if (choiceInt < 0 or choiceInt > len(playerActions)):
            print("Invalid choice number");
            return playerActions[0];
        else:
            return playerActions[choiceInt];
        
    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        
        if (len(actions) == 0):
            return PlayerAction('None', None);
        
        print("Here's your possible actions: ");
        
        #Print out all of the player's actions. 
        for i in range(len(actions)):
            print(i, actions[i]);
        
        choice = input("Which action?\n");
        choiceInt = int(choice);
        
        if (choiceInt < 0 or choiceInt > len(actions)):
            print("Invalid choice number");
            return actions[0];
        else:
            return actions[choiceInt];