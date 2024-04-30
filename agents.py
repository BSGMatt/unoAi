from playeraction import PlayerAction
import random
from collections import Counter


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
            if action.actionName == "uno":
                # Call UNO if it's a legal option
                return action
            elif action.actionName == "place":
                # Prioritize playing cards if possible
                bestAction = action

        return bestAction
        # If no preferable action is found, draw a card if possible
        for action in playerActions:
            if action.actionName == "draw":
                return action

        return bestAction

    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        if len(actions) == 0:
            return PlayerAction("None", None)

        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(actions)):
            print(i, actions[i])

        return random.choice(actions)




class ReflexAgent2(Agent):
    def getAction(self, playerID: int, gameState, opponentCardLen):
        playerActions = gameState.getLegalActions(playerID)

        if len(playerActions) == 1:
            return playerActions[0]

        bestAction = None
        for action in playerActions:
            if action.actionName == "uno":
                # Call UNO if it's a legal option
                return action
        print("Length of pa")
        print(len(playerActions))
        bestAction = playerActions[self.evaluate(playerActions, opponentCardLen)]
        print("Best Action")
        print(bestAction)

        return bestAction

        # # If no preferable action is found, draw a card if possible
        # for action in playerActions:
        #     if action.actionName == "draw":
        #         return action
    

    def evaluate(self, actions, opponentLen):
        """
        1) if opponent is has/is ready to call uno (has 4 or fewer cards left), use wild draw 4, draw 2, or reverse, skip, or random color/number card
        2) never play wild cards unless they are absolutely necessary (no cards match the top card) or use as final cards
        3) playing big numbers 
        4) prioritize playing duplicate numbers  
        """                

        print("Actions")
        print(type(actions[0]))

        # counter = float("-inf")
        # num = 0
        # for i in range(0, len(actions)):
        #     actionFrequency = actions.count(i)
        #     print("Action Frequency")
        #     print(actionFrequency)
        #     if(actionFrequency > counter):
        #         counter = actionFrequency
        #         num = i
        # print("Num")
        # print(num)
        # return num
        # return max(set(actions.card.value), key = actions.count)

        duplicate = -1
        wild = -1
        wild4 = -1
        draw2 = -1
        skip = -1
        reverse = -1


        #print(counts)
        if opponentLen > len(actions):
            aList = []
            for action in actions:
                aList.append(action.toString())

            print(aList)
            counts = Counter(aList)
            most_common_element = max(counts, key=counts.get)
            most_common_index = 0
            if counts[most_common_element] == 1:
                most_common_index = aList.index(most_common_element)
                most_common_index += 1
            i = most_common_index
            duplicate = i
            return duplicate

        for i, action in enumerate(actions): 
            if action.getActionName() == "+4" and action.getCard() == "WILD":
                wild4 = i
            elif action.getActionName() == "CARD" and action.getCard() == "WILD":
                wild = i
            elif action.getActionName() == "2" and action.getCard() == "DRAW":
                draw2 = i
            elif action.getActionName() == "CARD" and action.getCard() == "REVERSE":
                reverse = i
            elif action.getActionName() == "CARD" and action.getCard() == "SKIP":
                skip = i

        largest = float("-inf")
        largestI = 0
        for i, action in enumerate(actions):
            print(action)
            if "draw" not in action.actionName:
                if action.card.value > largest and action.card.value is not None:
                    print("Value action card")
                    print(action.card.value)
                    largest = action.card.value
                    largestI = i
        print("Largest")
        print(largestI)


        if len(actions) <= 3:
            if wild != -1:
                return wild
            elif wild4 != -1:
                return wild4
            elif draw2 != -1:
                return draw2
            elif reverse != -1:
                return reverse
            elif skip != -1:
                return skip

        if opponentLen <= 4:
            if wild4 != -1:
                return wild4
            elif wild != -1:
                return wild
            elif draw2 != -1:
                return draw2
            elif reverse != -1:
                return reverse
            elif skip != -1:
                return skip



        return largestI
    

    def forceAction(self, playerID: int, gameState, actions: list[PlayerAction]):
        if len(actions) == 0:
            return PlayerAction("None", None)

        print("Here's your possible actions: ")

        # Print out all of the player's actions.
        for i in range(len(actions)):
            print(i, actions[i])

        return random.choice(actions)
