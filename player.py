from agents import Agent
from playeraction import PlayerAction

class Player:
    
    """
        id: The ID number of this player. 
        agent: The agent that controls this player's actions. 
        cardsInHand: A list containing the cards in the player's hand. 
    """
    
    def __init__(self, id: int, agent: Agent):
        self.agent = agent;
        self.id = id;
        self.cardsInHand = [];
        
    def makeAction(self, gameState) -> PlayerAction:
        return self.agent.getAction(self.id, gameState);
    
    
    """
        Force the player to pick between the given actions. 
    """
    
    def forceAction(self, gameState, action: list[PlayerAction]) -> PlayerAction:
        return self.agent.forceAction(self.id, gameState);