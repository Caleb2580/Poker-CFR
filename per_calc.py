import oth
import sys
import time


hand_rank_key = {
        10: 'Royal flush',
        9: 'Straight flush',
        8: 'Four of a kind',
        7: 'Full house',
        6: 'Flush',
        5: 'Straight',
        4: 'Three of a kind',
        3: 'Two pair',
        2: 'One pair',
        1: 'High card'
    }


def get_deck():
    key_nums = {
        14: 'A',
        13: 'K',
        12: 'Q',
        11: 'J',
        10: 'T',
        9: '9',
        8: '8',
        7: '7',
        6: '6',
        5: '5',
        4: '4',
        3: '3',
        2: '2',
    }
    key_suits = {
        0: 's',
        1: 'h',
        2: 'd',
        3: 'c',
    }
    deck = []
    for n in key_nums:
        for s in key_suits:
            deck.append(key_nums[n]+key_suits[s])
    return deck


def make_deck(cards, board):
    deck = get_deck()
    for card in cards + board:
        deck.remove(card)
    return deck



def convert_rank_to_numeric(rank):
    rank_mapping = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    if rank in rank_mapping:
        return rank_mapping[rank]
    else:
        return int(rank)


def convert_numeric_to_rank(rank):
    rank_mapping = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
    if rank in rank_mapping:
        return rank_mapping[rank]
    else:
        return str(rank)


def get_percentages(cards, board, deck):
    percentage_odds = oth.odds_better(cards, board, deck)
    return percentage_odds[0], percentage_odds[2]


def get_percentages_pre_flop(cards):
    pf_hands = open('pf_rankings.txt', 'r').read().splitlines()

    # pre_flop_hands = ['AA', 'KK', 'QQ', 'JJ', 'AKs', 'AQs', 'TT', 'AK', 'AJs', 'KQs', '99', 'ATs', 'AQ', 'KJs', '88', 'KTs', 'QJs', 'A9s', 'AJ', 'QTs', 'KQ', '77', 'JTs', 'A8s', 'K9s', 'AT', 'A5s', 'A7s', 'KJ', '66', 'T9s', 'A4s', 'Q9s', 'J9s', 'QJ', 'A6s', '55', 'A3s', 'K8s', 'KT', '98s', 'T8s', 'K7s', 'A2s', '87s', 'QT', 'Q8s', '44', 'A9', 'J8s', '76s', 'JT']
    # rankings_dict = {0: ['AA', 'KK', 'QQ', 'JJ', 'AKs'], 1: ['AQs', 'TT', 'AK', 'AJs', 'KQs', '99'], 2: ['ATs', 'AQ', 'KJs', '88', 'KTs', 'QJs'], 3: ['A9s', 'AJ', 'QTs', 'KQ', '77', 'JTs'], 4: ['A8s', 'K9s', 'AT', 'A5s', 'A7s'], 5: ['KJ', '66', 'T9s', 'A4s', 'Q9s'], 6: ['J9s', 'QJ', 'A6s', '55', 'A3s', 'K8s', 'KT'], 7: ['98s', 'T8s', 'K7s', 'A2s'], 8: ['87s', 'QT', 'Q8s', '44', 'A9', 'J8s', '76s', 'JT']}
    # rankings_dict = {'AA,KK,QQ,JJ,AKs,': 0, 'AQs,TT,AK,AJs,KQs,99,': 1, 'ATs,AQ,KJs,88,KTs,QJs,': 2, 'A9s,AJ,QTs,KQ,77,JTs,': 3, 'A8s,K9s,AT,A5s,A7s,': 4, 'KJ,66,T9s,A4s,Q9s,': 5, 'J9s,QJ,A6s,55,A3s,K8s,KT,': 6, '98s,T8s,K7s,A2s,': 7, '87s,QT,Q8s,44,A9,J8s,76s,JT,': 8}

    pre_flop_hands = ['72', '82', '83', '92', '93', '94', '62', 'T2', '73', 'T3', '32', 'T4', 'T5', '84', 'J2', '42', 'J3', 'J4', '52', '95', 'J5', '63', 'J6', 'Q2', '74', 'Q3', 'Q4', '43', 'Q5', 'T6', '85', '53', 'Q6', '64', 'K2', '96', 'K3', 'K4', 'Q7', '75', 'J7', 'K5', '54', '86', 'K6', 'T7', '65', 'K7', '76', '72s', '97', '82s', 'A2', '83s', 'Q8', '87', 'A6', 'K8', '92s', '62s', 'A3', 'J8', '93s', '94s', '32s', 'A4', '73s', 'A7', 'A5', 'T8', '98', 'T2s', '42s', 'T3s', 'T4s', '84s', 'T5s', '52s', 'A8', '63s', 'J2s', '95s', 'J3s', 'J4s', '74s', '43s', 'Q9', 'J5s', 'K9', 'J9', 'J6s', '85s', '53s', 'A9', 'Q2s', 'T6s', 'T9', 'Q3s', 'Q4s', '64s', 'Q5s', '96s', '75s', 'Q6s', '54s', 'J7s', '65s', '86s', 'K7s', 'K2s', 'K3s', 'K4s', 'T7s', '76s', 'K5s', '97s', 'K6s', '22', '33', '44', 'QT', '87s', 'JT', '55', 'KT', 'K7s', 'Q8s', 'AT', 'J8s', '98s', 'A2s', 'T8s', 'K8s', '66', 'QJ', 'A6s', 'A3s', 'A4s', 'KJ', 'A7s', '77', 'A5s', 'AJ', 'J9s', 'Q9s', 'A8s', 'T9s', 'K9s', '88', 'KQ', 'A9s', 'AQ', '99', 'JTs', 'QTs', 'KTs', 'QJs', 'ATs', 'AK', 'TT', 'KJs', 'AJs', 'KQs', 'AQs', 'JJ', 'AKs', 'QQ', 'KK', 'AA']
    
    hand = cards[0][0] + cards[1][0]  + ('s' if cards[0][1] == cards[1][1] else '')

    #     if hand + ',' in key:
    #         return rankings_dict[key]
    
    # return 9

    return pre_flop_hands.index(hand) / len(pre_flop_hands)

def get_percentages_flop(cards, board, deck):
    total = 0.0
    total_win = 0.0
    total_tie = 0.0
    use_deck = deck + []
    while len(use_deck) > 1:
        card = use_deck[0]
        use_deck = use_deck[1:]
        for card2 in use_deck:
            new_deck = use_deck + []
            new_deck.remove(card2)
            percentage_odds = get_percentages(cards, board + [card, card2], deck)
            total_win += percentage_odds[0]
            total_tie += percentage_odds[1]
            total += 1
    return total_win / total, total_tie / total

def get_percentages_turn(cards, board, deck):
    total = 0.0
    total_win = 0.0
    total_tie = 0.0
    for card in deck:
        percentage_odds = get_percentages(cards, board + [card], deck)
        total_win += percentage_odds[0]
        total_tie += percentage_odds[1]
        total += 1
    return total_win / total, total_tie / total


def get_odds(cards, board, deck):
    if len(board) == 0:
        if convert_rank_to_numeric(cards[0][0]) < convert_rank_to_numeric(cards[1][0]):
            cards = cards[::-1]
        return get_percentages_pre_flop(cards), 0.0
    elif len(board) == 3:
        return get_percentages_flop(cards, board, deck)
    elif len(board) == 4:
        return get_percentages_turn(cards, board, deck)
    elif len(board) == 5:
        return get_percentages(cards, board, deck)


if __name__ == '__main__':
    my_cards, my_board = ['8c', '9c'], ['Qc', 'Jc', 'Tc']
    my_deck = make_deck(my_cards, my_board)
    tm = time.time()
    perc = get_odds(my_cards, my_board, my_deck)
    # perc = get_percentages(my_cards, my_board, my_deck)
    print(f'Win: {perc[0]}, Lose: {100.0 - perc[0] - perc[1]}, Tie: {perc[1]}')
    print('Total Time:', time.time() - tm)



