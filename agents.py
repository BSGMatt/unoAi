from playeraction import PlayerAction
import random

class Agent:

    def __init__(self):
        self.opponentCardLen = 0
    #Returns the agent's best action. 
    def getAction(self, playerID: int, gameState):
        pass

    def getAction(self, playerID: int, gameState, opponentCardLen: int):
        self.opponentCardLen = opponentCardLen
        pass

    #Make the agent select between a set of predefined options. 
    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        pass
    
    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction], opponentCardLen):
        self.opponentCardLen = opponentCardLen
        pass

class HumanAgent(Agent):
    
    def getAction(self, playerID: int, gameState):
        playerActions = gameState.getLegalActions(playerID);
        
        if (len(playerActions) == 1):
            return playerActions[0];
        
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


class RandomAgent(Agent):
    def getAction(self, playerID: int, gameState):
        playerActions = gameState.getLegalActions(playerID)

        if len(playerActions) == 1:
            return playerActions[0]

        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(playerActions)):
            print(i, playerActions[i])

        print("Which action?\n")

        return random.choice(playerActions)

    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        if len(actions) == 0:
            return PlayerAction("None", None)

        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(actions)):
            print(i, actions[i])

        return random.choice(actions)


class ReflexAgent(Agent):
    def getAction(self, playerID: int, gameState, opponentCardLen):
        playerActions = gameState.getLegalActions(playerID)

        if len(playerActions) == 1:
            return playerActions[0]

        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(playerActions)):
            print(i, playerActions[i])

        bestAction = None
        for action in playerActions:
            #print("Action 0")
            #print(action)
            if action.getActionName() == "uno":
                # Call UNO if it's a legal option
                return action
            elif action.getActionName() == "place":
                # Prioritize playing cards if possible
                bestAction = action

        # If no preferable action is found, draw a card if possible
        for action in playerActions:
            if action.getActionName() == "draw":
                return action
            else:
                print(action)

        return bestAction

    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction], opponentCardLen):
        if len(actions) == 0:
            return PlayerAction("None", None)
        #print("Opponent card length: " + opponentCardLen)
        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(actions)):
            print(i, actions[i])


        return random.choice(actions)

    def evaluate():
        return None
