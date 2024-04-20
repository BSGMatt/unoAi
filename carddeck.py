import random

RED = 0;
BLUE = 1;
GREEN = 2;
YELLOW = 3;
WILD_COLOR = 4;

COLORS = [RED, BLUE, GREEN, YELLOW, WILD_COLOR]
COLORNAMES = ["RED", "BLUE", "GREEN", "YELLOW", "WILD"]


SKIP = 10;
REVERSE = 11;
DRAW_2 = 12;
DRAW_4 = 13;
WILD_ACTION = 14;

ACTIONS = [SKIP, REVERSE, DRAW_2, DRAW_4, WILD_ACTION]
ACTIONNAMES = ["SKIP", "REVERSE", "+2", "+4", "WILD"]

#Create a lookup to store the card names. 
cardName = dict();
for c in COLORS:
    for v in range(10):
        cardName[(c, v)] = str.format("{0} {1}", COLORNAMES[c], v);
    for v in range (3):
        cardName[(c, v + 10)] = str.format("{0} {1}", COLORNAMES[c], ACTIONNAMES[v]);
    cardName[(c, WILD_ACTION)] = str.format("WILD CARD ({0})", COLORNAMES[c]);
    cardName[(c, DRAW_4)] = str.format("DRAW +4 ({0})", COLORNAMES[c]);
cardName[(WILD_COLOR, WILD_ACTION)] = "WILD CARD";
cardName[(WILD_COLOR, DRAW_4)] = "WILD +4";



class Card:
    
    def __init__(self, color: int, value: int):
        self.color = color;
        self.value = value;
        
    def isMatch(self, cardOnTop):
        return cardOnTop.color >= WILD_COLOR or self.color == cardOnTop.color or self.value == cardOnTop.value;
    
    def __str__(self) -> str:
        return cardName[(self.color, self.value)];
    
    def __repr__(self) -> str:
        return self.__str__();
        

class CardDeck:
    
    def __init__(self, wilds=True):
        print("CardDeck", wilds);
        if (CARDS == []): self.buildCards(wilds);
        self.drawPile = shuffle(CARDS);
        self.discardPile = list[Card]();
        self.topCard = self.drawPile.pop();
        
        #Pick a random color if the card is a wild or wild +4. 
        if (self.topCard.color == WILD_COLOR):
            self.topCard.color = random.choice(COLORS[0:-1]);
        
    def drawCard(self) -> Card:
        card = self.drawPile.pop();
        if (len(self.drawPile) == 0):
            self.drawPile = shuffle(CARDS);
            
        return card;
            
    def placeCard(self, card: Card):
        if (self.topCard.isMatch(card)):
            self.discardPile.append(self.topCard);
            self.topCard = card;
        else:
            print("ILLEGAL MOVE");
            
    def undoLastPlace(self) -> Card:
        oldTopCard = self.topCard;
        self.topCard = self.discardPile.pop();
        return oldTopCard;
        
            
    def buildCards(self, wilds=True): 
    
        print("buildCards: ", wilds);
        
        #Build all of the colored cards
        for color in COLORS[0:-1]:
            for value in range (0, 13):
                CARDS.append(Card(color, value));
                if (value > 0):
                    CARDS.append(Card(color, value));
                    
        if (wilds):
            #Wilds and Draw 4's
            CARDS.append(Card(WILD_COLOR, WILD_ACTION));
            CARDS.append(Card(WILD_COLOR, WILD_ACTION));
            CARDS.append(Card(WILD_COLOR, WILD_ACTION));
            CARDS.append(Card(WILD_COLOR, WILD_ACTION));
            CARDS.append(Card(WILD_COLOR, DRAW_4));
            CARDS.append(Card(WILD_COLOR, DRAW_4));
            CARDS.append(Card(WILD_COLOR, DRAW_4));
            CARDS.append(Card(WILD_COLOR, DRAW_4));
        
    
def shuffle(cards: list) -> list:
    
    ret = [];
    cards = list(cards);
    
    while (len(cards) > 0):
        rand = random.randrange(0, len(cards));
        ret.append(cards.pop(rand));
    return ret;
    
    
#List all of the cards in an UNO deck. 
CARDS = [];


#Builds the card deck based on this 
#image: https://en.wikipedia.org/wiki/Uno_(card_game)#/media/File:UNO_cards_deck.svg


    
    #print("CARDS,", CARDS)
            


    