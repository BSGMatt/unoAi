from carddeck import Card

class PlayerAction:
    
    """
        action -> The action to take. 
        card -> If the action is 'Place', then the card to place is stored here. 
    """
    
    def __init__(self, action: str, card: Card | None):
        self.actionName = action;
        self.card = card;
        
    def __str__(self) -> str:
        return str.format("({0}, {1})", self.actionName, self.card);
    
    def __repr__(self) -> str:
        return self.__str__();

    def getActionName(self):
        return self.actionName

    def getCard(self):
        return self.card