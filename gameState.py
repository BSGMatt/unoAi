
from carddeck import *
from player import *
from agents import *
from gameevent import *
from actions import PlayerActionNames

#List Deck options
STANDARD_DECK = 0;
WILDS_ONLY_DECK = 1;
SKIPS_ONLY_DECK = 2;
REVERSES_ONLY_DECK = 3;
DRAW_2_ONLY_DECK = 4;

class GameState:
    
    def __init__(self, numPlayers=2, houseRules=[], numCardsAtStart=7, deckOptions=0, gameMode="random"):
        
        if (deckOptions == WILDS_ONLY_DECK):
            self.deck = CardDeck(standardDeck=False, wilds=True);
        elif (deckOptions == SKIPS_ONLY_DECK):
            self.deck = CardDeck(standardDeck=False, reversesOnly=True);
        elif (deckOptions == REVERSES_ONLY_DECK):
            self.deck = CardDeck(standardDeck=False, skipsOnly=True);
        elif (deckOptions == DRAW_2_ONLY_DECK):
            self.deck = CardDeck(standardDeck=False, draw2s=True);
        else:
            self.deck = CardDeck();
        
        #The id of the player whose turn it is. 
        self.whoseTurn = 0;
        
        #Whether the turn order is reversed. 
        self.orderReversed = False;
        
        #List of all players in the game. 
        self.players = [Player(0, HumanAgent())]
        for i in range(1, numPlayers):
            if gameMode == "random":
                print(True)
                self.players.append(Player(i, RandomAgent()))
            elif gameMode == "reflex":
                self.players.append(Player(i, ReflexAgent()))
        
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
        #standardEvents  = [UnoCalledEvent(), DrawCardEvent(), PlaceCardEvent(), SkipEvent(), WildEvent()]
        standardEvents = [UnoCalledEvent(0), DrawCardEvent(1), PlaceCardEvent(2), SkipEvent(3), ReverseEvent(4), Draw2Event(5), Draw4Event(6), WildEvent(7)]
        houseRules = [];
        
        self.gameEvents = standardEvents + houseRules;
        self.lose = False
        self.win = False
        
    def getLegalActions(self, playerID: int) -> list[PlayerAction]:
        
        ret = [];
        
        if (playerID == self.whoseTurn):
            ret.append(PlayerAction(PlayerActionNames.DRAW, None));
            
            #Run through each of player's card to see there's any match. 
            for card in self.players[playerID].cardsInHand:
                if (self.deck.topCard.isMatch(card)):
                    ret.append(PlayerAction(PlayerActionNames.PLACE, card));
            
            #Check if a player is on their second to last card. 
            if (len(self.players[playerID].cardsInHand) == 2):
                cards = self.players[playerID].cardsInHand
                #Check if the last any of last two cards are a match. 
                if (self.deck.topCard.isMatch(cards[0]) or self.deck.topCard.isMatch(cards[1])):
                    ret.append(PlayerAction(PlayerActionNames.UNO, None));
                    
        else:
            #Check if other players are going to call UNO.  
            for player in self.players:
                if (player.id != playerID and self.playerisReadyToCallUNO(player.id)):
                    ret.append(PlayerAction(PlayerActionNames.UNO, None));
                    break; #Only need one uno action. 
        
        #If there is no possible actions a player can take, then return the 'None' Action.        
        if (len(ret) == 0):
            ret = [PlayerAction(PlayerActionNames.NONE, None)];
                
        return ret;
    
    def playerisReadyToCallUNO(self, playerID):
        #Check if a player is on their second to last card. 
        if (len(self.players[playerID].cardsInHand) == 2):
            cards = self.players[playerID].cardsInHand
            #Check if the last any of last two cards are a match. 
            if (self.deck.topCard.isMatch(cards[0]) or self.deck.topCard.isMatch(cards[1])):
                return True;
        return False;
    
    """
        Moves to the next player in the turn order. 
        skips - How many players to skip. 
    """
    def nextPlayer(self, skips=0):
        if (self.orderReversed):
            self.whoseTurn = (self.whoseTurn - 1 - skips) % len(self.players);
        else:
            self.whoseTurn = (self.whoseTurn + 1 + skips) % len(self.players);
    
    """
        Gets the ID of the next player in the turn order.
        skips - How many players to skip. 
    """      
    def getNextPlayer(self):
        
        if (self.orderReversed):
            return (self.whoseTurn - 1) % len(self.players);
        else:
            return (self.whoseTurn + 1) % len(self.players);
            
    
            
    def cancelFutureEvents(self, startEvent: GameEvent):
        
        for event in self.gameEvents:
            if (event.order > startEvent.order):
                event.ignore = True;
                
    def cancelEvent(self, eventName: str):
        for event in self.gameEvents:
            if (event.name == eventName):
                event.ignore = True;
                
    def getEvent(self, eventName: str) -> GameEvent:
        for event in self.gameEvents:
            if (event.name == eventName):
                return event;
            
    #Check if any players' hands are empty. 
    def isTerminalState(self) -> bool:
        
        for player in self.players:
            if (len(player.cardsInHand) == 0):
                return True;

        return False;
        