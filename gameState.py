
from carddeck import *
from player import *
from agents import *
from gameevent import *

class GameState:
    
    def __init__(self, numPlayers=2, houseRules=[], numCardsAtStart=7):
        
        #Initialize the card deck. 
        self.deck = CardDeck();
        
        #The id of the player whose turn it is. 
        self.whoseTurn = 0;
        
        #Whether the turn order is reversed. 
        self.orderReversed = False;
        
        #List of all players in the game. 
        self.players = list[Player]();
        for i in range(numPlayers):
            self.players.append(Player(i, HumanAgent()));
            
        #A dictionary containing the last action each player performed.
        self.lastPlayerAction = dict();
         
        #Hand out every player cards.    
        for k in range(numCardsAtStart):
            for player in self.players:
                #print(player.id, k);
                player.cardsInHand.append(self.deck.drawCard());
                
        
        """
            Set up the game events that can occur during play.
            (Custom house rules would go here.)
        """
        standardEvents  = [SkipEvent(), WildEvent()]
        houseRules = [];
        
        
        self.gameEvents = standardEvents + houseRules;
        
        
    def getLegalActions(self, playerID: int) -> list[PlayerAction]:
        
        ret = [];
        
        if (playerID == self.whoseTurn):
            
            ret.append(PlayerAction('draw', None));
            
            #If player is about to place their 2nd to last card. 
            if (len(self.players[playerID].cardsInHand) == 2):
                ret.append(PlayerAction('uno', None));
            
            #Run through each of player's card to see there's any match. 
            for card in self.players[playerID].cardsInHand:
                if (self.deck.topCard.isMatch(card)):
                    ret.append(PlayerAction('place', card));
                
        return ret;
    
    """
        Gets the next player in the turn order. 
        skips - How many players to skip. 
    """
    def nextPlayer(self, skips=0):
        if (self.orderReversed):
            self.whoseTurn = (self.whoseTurn - 1 - skips) % len(self.players);
        else:
            self.whoseTurn = (self.whoseTurn + 1 + skips) % len(self.players);
            
    #Check if any players' hands are empty. 
    def isTerminalState(self) -> bool:
        
        for player in self.players:
            if (len(player.cardsInHand) == 0):
                return True;

        return False;
        