# oh boy here we go
import random
import itertools

#CARD EVALUATOR WORKS BUT APPLICATION IS BROKEN

import numpy as np

from Player import *
from AiPlayer import *
from Evaluator import *


#   card & deck generation
values = list(range(2, 15))
suits = ['C', 'D', 'H', 'S']

class Card:

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def print_card(self):
        print(f"{self.value}{self.suit}", end='')

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



# GAME
class Game:
    small_blind = 5
    big_blind = 10

    def __init__(self, player_count, start_wealth, is_manual):
        self.player_count = player_count
        self.start_wealth = start_wealth
        self.is_manual = is_manual

        self.deck = Deck()
        self.pot = 0
        self.flop = []
        self.players = {}
        self.round = 1
        self.make_players()
        self.is_running = True
        self.is_round = True
        self.top_bet = 0

    def main(self):
        #game
        while self.is_running:

            # RESET
            for player in self.players.values():
                player.is_folded = False
                player.in_pot = 0
                player.hand = []
            self.is_round = True
            self.flop = []

            #round
            if self.is_round:


                dealer_id = ((self.round -1) % self.player_count) + 1 #NO 0th PLAYER
                small_blind_id = (dealer_id % self.player_count) + 1 #NO 0th PLAYER
                big_blind_id = (small_blind_id % self.player_count) + 1 #NO 0th PLAYER
                new_line()

                #LOOP THROUGH BLINDS AND ELIMINATE BROKE PEOPLE
                print(f"(P{dealer_id}) {self.players[dealer_id].name} is dealing.")
                while self.get_blind(Game.small_blind, self.players[small_blind_id]) == False:
                    print(f"(P{small_blind_id}) {self.players[small_blind_id].name} couldn't afford to play.")
                    small_blind_id = (small_blind_id % self.player_count) + 1#NO 0th PLAYER
                    big_blind_id = (big_blind_id % self.player_count) + 1#NO 0th PLAYER
                print(f"(P{small_blind_id}) {self.players[small_blind_id].name} pays small blind ({Game.small_blind}).")

                while self.get_blind(Game.big_blind, self.players[big_blind_id]) == False:
                    print(f"(P{big_blind_id}) {self.players[big_blind_id].name} couldn't afford to play.")
                    big_blind_id = (big_blind_id % self.player_count) + 1#NO 0th PLAYER
                print(f"(P{big_blind_id}) {self.players[big_blind_id].name} pays big blind ({Game.big_blind}).")

                new_line()

                #HAND OUT CARDS
                for player in [play for play in self.players.values() if play.is_folded is False]: #for all players that havent folded:

                    if self.is_manual and player.name == "AI":
                        card = input("What is the first card you got? ")
                        player.hand.append(self.deck.draw_card(Card(card[0], card[1])))
                        card = input("What is the second card you got? ")
                        player.hand.append(self.deck.draw_card(Card(card[0], card[1])))
                    else:
                        player.hand.append(self.deck.draw_card())
                        player.hand.append(self.deck.draw_card())


                self.update_top_bet() #top_bet now = big blind


                # Betting (pre flop)
                self.run_betting(big_blind_id)

                #checking winner
                self.check_winner()

            if self.is_round:
                #flop
                if self.is_manual:
                    for i in range(3):
                        card = input("What is the one of flop cards? ")
                        rank = card[0]
                        if card is type(int):
                            rank = int(card[0])
                        self.turn_card(Card(rank, card[1]))
                else:
                    for i in range(3):
                        self.turn_card()

                print(f"The flop has been drawn.\nThe community cards are now: ", end='')
                for card in self.flop:
                    card.print_card()
                    print(" ", end='')
                print()
                new_line()

                #bet flop
                self.run_betting(big_blind_id)

                #check_winner
                self.check_winner()

            if self.is_round:

                #turn
                if self.is_manual:
                    card = input("What is the turn card? ")
                    rank = card[0]
                    if card is type(int):
                        rank = int(card[0])
                    self.turn_card(Card(rank, card[1]))
                else:
                    self.turn_card()
                print(f"The turn has been drawn.\nThe community cards are now: ", end='')
                for card in self.flop:
                    card.print_card()
                    print(" ", end='')
                print()
                new_line()

                #bet turn
                self.run_betting(big_blind_id)

                # check_winner
                self.check_winner()

            if self.is_round:

                #river
                if self.is_manual:
                    card = input("What is the river card? ")
                    rank = card[0]
                    if card is type(int):
                        rank = int(card[0])
                    self.turn_card(Card(rank, card[1]))
                else:
                    self.turn_card()

                print(f"The flop has been drawn.\nThe community cards are now: ", end='')
                for card in self.flop:
                    card.print_card()
                    print(" ", end='')
                print()
                new_line()

                #bet river
                self.run_betting(big_blind_id)

                # check_winner
                self.check_winner()

            if self.is_round:

                scores = {}


                if self.is_manual:
                    for id in [id for id in self.players.keys() if not self.players[id].is_folded]:
                        player = self.players[id]
                        if player.name != "AI":
                            for i in range(2):
                                card = input(f"What is one of (P{id}) {player.name}'s cards? ")
                                rank = card[0]
                                if card is type(int):
                                    rank = int(card[0])
                                player.hand[i] = Card(rank, card[1])
                new_line()

                for id in [id for id in self.players.keys() if not self.players[id].is_folded]:
                    player = self.players[id]
                    player.get_best_hand(self.flop)
                    scores[id] = player.best_hand


                # COMPARE SCORES AND DETERMINE WINNER
                print(scores)






            #CHECK FOR ANOTHER ROUND
            if not self.another_round():
                print("Good bye.")
                self.is_running = False #no more game :(






    def make_players(self):
        for i in range(1,self.player_count+1): #FIRST PLAYER IS PLAYER 1 NOT 0
            #CHANGE HOW TO DETERMINE AI PLAYER
            name = input(f"What is Player {i}'s name? (Type 'AI' for an AI player): ")
            if name == "AI":
                self.players[i] = AiPlayer(self.start_wealth, name)
            else:
                self.players[i] = Player(self.start_wealth, name)

    def get_blind(self, ante, player):
        if player.wealth >= ante:
            player.wealth -= ante
            player.in_pot += ante
            return True
        else:
            player.is_folded = True
            return False

    def update_top_bet(self):
        self.top_bet = max([player.in_pot for player in self.players.values()])

    def run_betting(self, big_blind_id):
        #   everyone places a bet
        for i in range(self.player_count):
            index = ((big_blind_id + i) % self.player_count) + 1#NO 0th PLAYER
            player = self.players[index]
            if not player.is_folded:
                bet_index = player.make_move(index, self.top_bet)
                self.update_top_bet()
                print(f"{player.name} has {f'bet/raised to {self.top_bet}' if bet_index == 1 else f'checked/called {self.top_bet}' if bet_index == 2 else 'folded'}.")
                new_line()

        # anyone who has less than top_bet gets to call, fold, or raise further
        players = [player.in_pot for player in self.players.values() if player.is_folded is False]
        while not all([i == players[0] for i in players]):

            index = ((index) % self.player_count) + 1
            player = self.players[index]
            if not player.is_folded:
                bet_index = player.make_move(index, self.top_bet)
                self.update_top_bet()
                print(
                    f"{player.name} has {f'bet/raised to {self.top_bet}' if bet_index == 1 else f'checked/called {self.top_bet}' if bet_index == 2 else 'folded'}.")
                new_line()

            players = [player.in_pot for player in self.players.values() if player.is_folded is False]

        #collect bets
        for player in [play for play in self.players.values()]:
            self.pot += player.in_pot
            player.in_pot = 0

        self.top_bet = 0

    def check_winner(self):
        unfolded = [play for play in self.players.values() if not play.is_folded]
        if len(unfolded) == 1:
            #everyone but play has folded
            winner = unfolded[0]
            winner.wealth += self.pot
            self.pot = 0
            self.is_round = False

    def turn_card(self, card=None):
        if card is not None:
            self.flop.append(card) #manual input draw
        else:
            self.flop.append(self.deck.draw_card())


    def another_round(self):
        print("End of Round Results:")
        for id in self.players:
            player = self.players[id]
            print(f"{player.name} has {player.wealth} chips.")

        while True:
            try:
                play_again = int(input("Would you like to play another round? (1=yes, 2=no): "))
            except:
                print("That's not a number. ", end="")
            else:
                if play_again == 1:
                    self.round += 1
                    return True
                elif play_again == 2:
                    self.is_running = False
                    return False
                else:
                    print("That's not an option. ", end="")


def new_line():
    print("--------------------------------------")


manual_game = bool(int(input("Is this a manual input game? (0 = no, 1 = yes): ")))
print(manual_game)
game = Game(3, 100, manual_game) #player_count has to be >= 3
game.main()




#   TEST CASES FOR PROGRAMMING AGH
# hands = {
#     1:[Card(14,'C'),Card(7,'D'),Card(2,'S'),Card(7,'S'),Card(7,'H')]
# }
#
# for id, hand in hands.items():
#     print(f"{id} : {Evaluator.eval_hand(hand)}")
