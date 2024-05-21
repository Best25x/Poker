# oh boy here we go
import numpy as np



#   card & deck generation
values = list(range(2, 15))
suits = ['C', 'D', 'H', 'S']

face_cards = {
    10: 'T',
    11: 'J',
    12: 'Q',
    13: 'K',
    14: 'A',
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}
class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def print_card(self):
        print(f"{self.value}{self.suit}")

class Deck:

    def __init__(self):
        self.deck = []
        self.generate_deck(values, suits)
        self.shuffle_deck()

    def generate_deck(self, vals, sui):
        for value in vals:
            for suit in sui:
                if value in face_cards:
                    real_value = face_cards[value]
                else:
                    real_value = value
                self.deck.append(Card(real_value, suit))

    def shuffle_deck(self):
        np.random.shuffle(self.deck)

    def draw_card(self, card=None):
        if card is type(Card): #for manually setting drawn cards
            drawn_card = card
        else:
            drawn_card = self.deck[0]
            self.deck.pop(0)
        return drawn_card


    def print_deck(self):
        for card in self.deck:
            card.print_card()


class Evaluator:

    @staticmethod
    def hand_dist(cards):
        dist = {i: 0 for i in range(1, 15)} #accounting for both ace representations
        for card in cards:
            dist[card.value] += 1
        dist[1] = dist[14] #an ace can be a low ace in a a2345 straight and a high ace in a tjqka straight - two representations
        return dist

    @staticmethod
    def high_card(cards):
        dist = Evaluator.hand_dist(cards)
        return max([val for val, count in dist.items() if count == 1])


    @staticmethod
    def flush_high_card(cards): #jank as hell but it works i think :)
        for card in cards:
            if cards[0].suit != card.suit:
                return None
        return max([card.value for card in cards])

    @staticmethod
    def straight_high_card(cards):
        dist = Evaluator.hand_dist(cards)
        for i in range(1,11): #low ace to 10 minimum straight values
            if all([dist[i+k] == 1 for k in range(5)]):
                return i+4
        return None

    @staticmethod
    def card_count(cards, num_of_a_kind, exclude=None):
        dist = Evaluator.hand_dist(cards)
        for i in range(2,15):
            if i == exclude:
                continue
            if dist[i] == num_of_a_kind:
                return i
        return None

    @staticmethod
    def eval_hand(cards): #straight+royal flush = 8+highcard; 4kind = 7+value; fullhouse = 6+high3kind+high2kind; flush = 5+value; straight = 4+highcard; 3kind = 3+value; twopair = 2+value+value; pair = 1+value; high = 0+value
        #returns XYYZZ; X=hand id YY = high card if applicable ZZ = secondary high card if applicable (full house, two pair)

        if Evaluator.straight_high_card(cards) is not None and Evaluator.flush_high_card(cards):
            #straight flush
            return int("8{:02d}00".format(Evaluator.straight_high_card(cards)))
        if Evaluator.card_count(cards, 4) is not None:
            #four of a kind
            return int("7{:02d}00".format(Evaluator.card_count(cards, 4)))
        if Evaluator.card_count(cards, 3) is not None and Evaluator.card_count(cards, 2) is not None:
            #full house
            return int("6{:02d}{:02d}".format(Evaluator.card_count(cards, 3), Evaluator.card_count(cards, 2)))
        if Evaluator.flush_high_card(cards):
            #flush
            return int("5{:02d}00".format(Evaluator.flush_high_card(cards)))
        if Evaluator.straight_high_card(cards) is not None:
            #straight
            return int("4{:02d}00".format(Evaluator.straight_high_card(cards)))
        if Evaluator.card_count(cards, 3) is not None:
            #three of a kind
            return int("3{:02d}00".format(Evaluator.card_count(cards, 3)))
        pair1 = Evaluator.card_count(cards,2)
        if pair1 is not None:
            if Evaluator.card_count(cards, 2, exclude=pair1) is not None:
                #two pair
                return int("2{:02d}{:02d}".format(Evaluator.card_count(cards,2,exclude=pair1),Evaluator.card_count(cards,2)))
            return int("1{:02d}00".format(Evaluator.card_count(cards,2)))
        return int("{:02d}00".format(Evaluator.high_card(cards)))







#players


class Player:

    def __init__(self, wealth, name):
        self.wealth = wealth
        self.name = name

        self.hand = []
        self.in_pot = 0
        self.is_folded = False


    def print_hand(self):
        for card in self.hand:
            card.print_card()

    def make_move(self, previous_bet):
        um = True
        while um:
            try:
                move = int(input("Make a move: (1=bet, 2=check/call, 3=fold): "))
            except ValueError:
                print("That's not an integer. ", end="")
            else:
                um = False


        if move == 1:
            uhh = True
            while uhh:
                try:
                    bet = int(input("How much do you want to bet/raise? "))
                except ValueError:
                    print("That's not an integer. ", end="")
                else:
                    uhh = False
            self.wealth -= bet
            self.in_pot += bet

        elif move == 2:
            amount = previous_bet - self.in_pot
            self.wealth -= amount
            self.in_pot += amount

        elif move == 3:
            self.is_folded = True

class AI_Player:

    def __init__(self, wealth, name):
        self.wealth = wealth
        self.name = name

        self.hand = []
        self.in_pot = 0
        self.is_folded = False



# GAME
class Game:
    small_blind = 5
    big_blind = 10

    def __init__(self, player_count, start_wealth):
        self.player_count = player_count
        self.start_wealth = start_wealth

        self.deck = Deck()
        self.pot = 0
        self.flop = []
        self.players = {}
        self.round = 2

    def main(self):
        self.make_players()

        dealer_id = ((self.round-1) % self.player_count) + 1 #NO 0th PLAYER
        small_blind_id = (dealer_id % self.player_count) + 1 #NO 0th PLAYER
        big_blind_id = (small_blind_id % self.player_count) + 1 #NO 0th PLAYER
        new_line()
        print(f"{self.players[dealer_id].name} is dealing.\n{self.players[small_blind_id].name} has to pay small blind ({Game.small_blind}).\n{self.players[big_blind_id].name} has to pay big blind ({Game.big_blind}).")

        self.get_blind()



        # if self.players[small_blind_id].wealth >= Game.small_blind:
        #     self.players[small_blind_id] -= Game.small_blind
        #     self.pot += Game.small_blind
        # else:
        #     ... #small has to fold and shifts over one
        #
        # if self.players[big_blind_id].wealth >= Game.big_blind:
        #     self.players[big_blind_id].wealth -= Game.big_blind
        #     self.pot += Game.big_blind
        # else:
        #     ... #big has to fold and shifts over one

        #request small and big blind

    def make_players(self):
        for i in range(1,self.player_count+1): #FIRST PLAYER IS PLAYER 1 NOT 0
            name = input(f"What is Player {i}'s name? (Type 'AI' for AI player): ")
            if name == "AI":
                self.players[i] = AI_Player()
            else:
                self.players[i] = Player(self.start_wealth, name)

    def get_blind(self):
        ...

def new_line():
    print("--------------------------------------")


game = Game(5, 100) #player_count has to be >= 3
game.main()




#   TEST CASES FOR PROGRAMMING AGH
# hands = {
#     1:[Card(14,'C'),Card(7,'D'),Card(2,'S'),Card(7,'S'),Card(7,'H')]
# }
#
# for id, hand in hands.items():
#     print(f"{id} : {Evaluator.eval_hand(hand)}")
