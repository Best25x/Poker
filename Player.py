import itertools

from Evaluator import *


class Player:

    def __init__(self, wealth, name):
        self.wealth = wealth
        self.name = name

        self.hand = []
        self.best_hand = []
        self.in_pot = 0
        self.is_folded = False

    def print_hand(self):
        for card in self.hand:
            card.print_card()
            print(" ", end='')
        print()

    def make_move(self, pid, top_bet):
        while True:
            try:
                move = int(
                    input(f"(P{pid}) {self.name}, make a move. (1=bet/raise, 2=check/call, 3=fold, 4=view cards): "))
            except ValueError:
                print("That's not an integer. ", end="")
            else:
                if move == 1:
                    while True:
                        try:
                            bet = int(input("How much do you want to bet/raise? "))
                        except ValueError:
                            print("That's not an integer. ", end="")
                        else:
                            break
                    amount = top_bet - self.in_pot + bet
                    self.wealth -= amount
                    self.in_pot += amount
                    break

                elif move == 2:
                    amount = top_bet - self.in_pot
                    self.wealth -= amount
                    self.in_pot += amount
                    break

                elif move == 3:
                    self.is_folded = True
                    break

                elif move == 4:
                    self.print_hand()

        return move

    def get_best_hand(self, flop):
        combos = []
        loc_flop = []
        for card in flop:
            loc_flop.append(card)
        loc_flop.append(self.hand[0])
        loc_flop.append(self.hand[1])
        for card in loc_flop:
            card.print_card()
        print()

        for card in loc_flop:
            try:
                card.value = int(card.value)
            except:
                card.value = face_cards[card.value]

        val = 0
        combos = list(itertools.combinations(loc_flop, 5))

        for combo in combos:
            eval = Evaluator.eval_hand(combo)
            if eval > val:
                val = eval

        self.best_hand = val