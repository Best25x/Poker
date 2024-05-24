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
            #at least one pair
            if Evaluator.card_count(cards, 2, exclude=pair1) is not None:
                #two pair
                return int("2{:02d}{:02d}".format(Evaluator.card_count(cards,2,exclude=pair1),Evaluator.card_count(cards,2)))
            return int("1{:02d}00".format(Evaluator.card_count(cards,2)))
        #nothing but high card
        return int("{:02d}00".format(Evaluator.high_card(cards)))
