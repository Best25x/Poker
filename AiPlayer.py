import itertools

from Evaluator import *


class AiPlayer:

    def __init__(self, wealth, name):
        self.wealth = wealth
        self.name = name

        self.hand = []
        self.best_hand = []
        self.in_pot = 0
        self.is_folded = False


    def make_move(self, pid, top_bet):
        move = str(self.get_move(pid, top_bet))

        if move[0] == '1':
            amount = top_bet - self.in_pot + sum([int(move[i+1]) for i in range(len(move)-1)])
            self.wealth -= amount
            self.in_pot += amount
        elif move[0] == '2':
            amount = top_bet - self.in_pot
            self.wealth -= amount
            self.in_pot += amount
        elif move[0] == '3':
            self.is_folded = True

        return int(str(move)[0])

    def get_move(self, pid, top_bet):

        # HAHAHA OH NO

        #temporary
        val = 0
        for card in self.hand:
            card_value = card.value
            if card.value in face_cards:
                card_value = face_cards[card.value]
            val += card_value

        if val <= 8:
            return 3
        elif 8 < val <= 20:
            return 2
        elif 20 < val <= 24:
            return 15 #bet, 5
        else:
            return 110 #bet, 10

    def get_best_hand(self, flop):
        loc_flop = flop
        loc_flop.append(self.hand[0])
        loc_flop.append(self.hand[1])

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
