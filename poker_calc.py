import itertools
from itertools import combinations
from collections import Counter
import random
from random import shuffle, choice
import time


full_counter = 0
full_counter_hands = []


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


def convert_ln(cards):
    cards = cards.replace(' ', '')
    key = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
        's': 0,
        'h': 1,
        'd': 2,
        'c': 3,
    }
    n_cards = []
    for i in range(0, len(cards)-1, 2):
        n_cards.append([key[cards[i]], key[cards[i+1]]])
    return n_cards


def convert_nl(cards):
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
    new_cards = ''
    for card in cards:
        new_cards += key_nums[card[0]] + key_suits[card[1]] + ' '
    return new_cards


def calculate_best_hand(cards):
    if len(cards) >= 5:
        hand_combinations = list(combinations(cards, 5))  # Generate all possible combinations of 5 cards
    else:
        hand_combinations = [cards + []]

    # Dictionary to map hand ranks to names
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

    best_hand = None
    best_rank = -1
    highest_card = -1

    for hand in hand_combinations:
        rank, high_card = evaluate_hand(hand)
        if rank > best_rank:
            best_rank = rank
            best_hand = hand
            highest_card = high_card
        elif rank == best_rank and high_card > highest_card:
            best_hand = hand
            highest_card = high_card

    return best_hand, best_rank, hand_rank_key[best_rank], highest_card


def convert_rank_to_numeric(rank):
    # Map face cards to numeric values
    rank_mapping = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
    if rank in rank_mapping:
        return rank_mapping[rank]
    else:
        return int(rank)


def evaluate_hand(hand):
    # Count the occurrences of each rank and suit
    rank_counts = Counter(convert_rank_to_numeric(rank) for rank, _ in hand)
    suit_counts = Counter(suit for _, suit in hand)

    if len(hand) > 3:
        is_flush = len(suit_counts) == 1  # All cards have the same suit

        # Check for straight
        sorted_ranks = sorted(rank_counts.keys(), reverse=True)
        is_straight = len(sorted_ranks) == 5 and (sorted_ranks[0] - sorted_ranks[-1] == 4 or sorted_ranks == [14, 5, 4, 3, 2])

        if is_straight:
            if sorted_ranks[0] == 14 and sorted_ranks[1] == 5:
                sorted_ranks[0] = 1
                sorted_ranks = sorted(sorted_ranks, reverse=True)

        # Check for royal flush
        if is_flush and is_straight and sorted_ranks[0] == 14:
            return 10, get_highest_card(hand)

        # Check for straight flush
        if is_flush and is_straight:
            if sorted_ranks[0] == 14 and sorted_ranks[1] == 5:
                return 5, 5
            return 9, sorted_ranks[0]
            # return 9, get_highest_card(hand)

        # Check for four of a kind
        if 4 in rank_counts.values():
            return 8, get_highest_card_four_of_a_kind(rank_counts)

        # Check for full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            high = 0
            for key in rank_counts:
                if rank_counts[key] == 3:
                    high = key
            return 7, high

        # Check for flush
        if is_flush:
            return 6, get_highest_card(hand)

        # Check for straight
        if is_straight:
            if sorted_ranks[0] == 14 and sorted_ranks[1] == 5:
                return 5, 5
            return 5, get_highest_card(hand)

    # Check for three of a kind
    if 3 in rank_counts.values():
        return 4, get_highest_card_three_of_a_kind(rank_counts)

    # Check for two pair
    if list(rank_counts.values()).count(2) == 2:
        return 3, get_highest_card_two_pair(rank_counts)

    # Check for one pair
    if 2 in rank_counts.values():
        return 2, get_highest_card_one_pair(rank_counts)

    # High card
    return 1, get_highest_card(hand)


def get_highest_card(hand):
    return max(convert_rank_to_numeric(rank) for rank, _ in hand)


def get_highest_card_four_of_a_kind(rank_counts):
    return max(convert_rank_to_numeric(rank) for rank, count in rank_counts.items() if count == 4)


def get_highest_card_three_of_a_kind(rank_counts):
    return max(convert_rank_to_numeric(rank) for rank, count in rank_counts.items() if count == 3)


def get_highest_card_two_pair(rank_counts):
    pairs = [convert_rank_to_numeric(rank) for rank, count in rank_counts.items() if count == 2]
    return max(pairs)


def get_highest_card_one_pair(rank_counts):
    return max(convert_rank_to_numeric(rank) for rank, count in rank_counts.items() if count == 2)


def compare_hands(hand1, hand2, board):
    hand1_best_cards, hand1_rank, hand1_rank_name, hand1_high = calculate_best_hand(hand1 + board)
    hand2_best_cards, hand2_rank, hand2_rank_name, hand2_high = calculate_best_hand(hand2 + board)
    global full_counter
    global full_counter_hands
    if hand2_rank_name == 'Full house':
        full_counter += 1
        oth_cards = []
        for card in hand2_best_cards:
            if card not in board:
                oth_cards.append(card)
        full_counter_hands.append(oth_cards)
    if hand1_rank > hand2_rank:
        return 1  # Win
    elif hand1_rank == hand2_rank:
        if hand1_high > hand2_high:
            return 1  # Win
        elif hand1_high == hand2_high:
            hand1_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in hand1_best_cards], reverse=True)
            hand2_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in hand2_best_cards], reverse=True)
            for ind in range(len(hand1_ranks)):
                if hand1_ranks[ind] > hand2_ranks[ind]:
                    return 1  # Win
                elif hand1_ranks[ind] < hand2_ranks[ind]:
                    # print(hand2)
                    return -1  # Lose
            return 0  # Tie
        else:
            # print(hand2)
            return -1  # Lose
    else:
        # print(hand2)
        return -1  # Lose


def next_card(deck, times, max_times):
    combs = []
    if times < max_times:
        # Get every combo for cur card
        for card in deck:
            print(card)
        times += 1
    return combs


def calculate_possible_hands(cards, board, deck):
    combos_of_hands = []
    for ind in range(len(deck)):
        new_deck = []
        for ind2 in range(len(deck)):
            if ind != ind2:
                new_deck.append(deck[ind2])
        for new_card in new_deck:
            combos_of_hands.append([deck[ind], new_card])
    new_combos = []
    for combo in combos_of_hands:
        dupe = False
        for new_combo in new_combos:
            if (combo[0] == new_combo[0] or combo[0] == new_combo[1]) and (combo[1] == new_combo[1] or combo[1] == new_combo[0]):
                dupe = True
                break
        if not dupe:
            new_combos.append(combo)
    return new_combos


def make_deck(cards, board):
    deck = get_deck()
    for card in cards + board:
        deck.remove(card)
    return deck


def calculate_winning_percent(cards, board):
    deck = make_deck(cards, board)
    if len(board) == 0:
        pass
    elif len(board) == 3:
        win_count = 0
        tie_count = 0
        loss_count = 0
        total_count = 0
        possible_hands = calculate_possible_hands(cards, board, deck)
        for opp_hand_possibility_ind in range(0, len(possible_hands)):
            for board_possibility_ind in range(0, len(possible_hands)):
                if opp_hand_possibility_ind != board_possibility_ind:
                    winner = compare_hands(cards, possible_hands[opp_hand_possibility_ind], board + possible_hands[board_possibility_ind])
                    if winner == -1:
                        loss_count += 1
                    elif winner == 1:
                        win_count += 1
                    else:
                        tie_count += 1
                    total_count += 1
        print(f'Win: {round(win_count / total_count, 2)}%')
        print(f'Lose: {round(loss_count / total_count, 2)}%')
        print(f'Tie: {round(tie_count / total_count, 2)}%')
    elif len(board) == 4:
        pass
    elif len(board) == 5:
        win_count = 0
        tie_count = 0
        loss_count = 0
        total_count = 0
        possible_hands = calculate_possible_hands(cards, board, deck)
        for opp_hand_possibility_ind in range(0, len(possible_hands)):
            winner = compare_hands(cards, possible_hands[opp_hand_possibility_ind], board)
            if winner == -1:
                loss_count += 1
            elif winner == 1:
                win_count += 1
            else:
                tie_count += 1
            total_count += 1
        print(f'Win: {round(win_count / total_count, 5)}%')
        print(f'Lose: {round(loss_count / total_count, 5)}%')
        print(f'Tie: {round(tie_count / total_count, 5)}%')


def calculate(cards, board):
    player_best_hand = calculate_best_hand(cards + board)
    board_best_hand = calculate_best_hand(board)
    player_high_card = 0
    if player_best_hand[2] == board_best_hand[2] and player_best_hand[3] == board_best_hand[3]:
        player_high_card = max(convert_rank_to_numeric(rank) for rank, _ in cards)
    return player_best_hand[0], player_best_hand[1], player_best_hand[2], player_best_hand[3], player_high_card



inp = '4s 8s Th'
nums = convert_ln(inp)

my_deck = get_deck()
shuffle(my_deck)
mcl = 2
my_cards = []
for i in range(mcl):
    c = choice(my_deck)
    my_cards.append(c)
    my_deck.remove(c)

mcl = 3
my_board = []
for i in range(mcl):
    c = choice(my_deck)
    my_board.append(c)
    my_deck.remove(c)

# print(my_cards, my_board)
# other_combos = calculate_possible_hands(my_cards, my_board, my_deck)

# print(other_combos)
# print(len(other_combos))


if __name__ == '__main__':
    mcl = 2
    opp_cards = []
    for i in range(mcl):
        c = choice(my_deck)
        opp_cards.append(c)
        my_deck.remove(c)

    my_cards, my_board = (['2d', '2c'], ['Qs', 'Qd', '2s', 'Qh', 'Qc'])
    my_deck = make_deck(my_cards, my_board)

    print(calculate_best_hand(my_cards + my_board))



# tm = time.time()
# calculate_winning_percent(my_cards, my_board)
# print(tm - time.time())


# Start


# poss_hands = calculate_possible_hands(my_cards, my_board, my_deck)
# new_poss = []
# counter = 0
# for hand in poss_hands:
#     broke = False
#     for card in hand:
#         if card.find('A') > -1:
#             counter += 1
#             broke = True
#             break
#     if not broke:
#         new_poss.append(hand)
# # print(len(new_poss))
# # print(new_poss)
# newest_poss = []
# for hand in new_poss:
#     broke = False
#     for card in hand:
#         if card.find('K') > -1:
#             counter += 1
#             broke = True
#             break
#     if not broke:
#         newest_poss.append(hand)
#
# print(counter)
# # exit()
#
# double_poss = []
# for hand in newest_poss:
#     broke = False
#     if sorted([convert_rank_to_numeric(rank) for rank, _ in hand]) == [7, 8]:
#         print(hand)
#         counter += 1
#         broke = True
#     if not broke:
#         double_poss.append(hand)
#
# print(counter)
# print('[][][][]')











# print(double_poss)

# print(counter)

# print('Mine:', my_cards, my_board)

# calc = calculate_best_hand(my_cards + my_board)
# calc_board = calculate_best_hand(my_board)

# print(calculate(my_cards, my_board))
# print(calc)
# print(calc_board)

# if calc[1] == calc_board[1] and calc[2] == calc_board[2]:
#     print('Board')


# my_cards = ['4c', '3c']
# opp_cards = ['3h', '4h']
# my_board = ['Ac', 'Kd', 'Jd', 'Th', '2s']

# my_board = ['3s', '3c', '3h', '5c', '6s']
# my_cards = ['4d', '7s']
# calculate_winning_percent(my_cards, my_board)

# print('Time it took: ', time.time() - tm)
#
# counter = {}
#
# print(Counter([str(hand) for hand in full_counter_hands]))
# print(full_counter)

# print(my_cards, opp_cards)
# print(my_board)
# print(compare_hands(my_cards, opp_cards, my_board))

# # Example usage
# best_hand = calculate_best_hand(my_cards + my_board)
# print("Best hand:", best_hand)

































