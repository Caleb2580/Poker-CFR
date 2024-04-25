from itertools import combinations
from collections import Counter
from random import shuffle, choice
from math import factorial
from poker_calc import calculate_best_hand
from poker_calc import calculate_possible_hands
import time
from math import comb
from time import sleep
# from tester import test


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


class MySet:
    def __init__(self, combos=None):
        if combos is None:
            combos = []
        else:
            pass
        self.combos = []
        self.singles = []
        self.append(combos)

    def append(self, combos):
        if not isinstance(combos, list):
            combos = [combos]
        for combo in combos:
            if len(combo) == 1 and combo[0] not in self.singles:
                self.singles.append(combo[0])
        for combo in combos:
            if len(combo) == 2:
                exists = False
                for my_combo in self.combos:
                    if (combo[0] == my_combo[0] and combo[1] == my_combo[1]) or (combo[0] == my_combo[1] and combo[1] == my_combo[0]):
                        exists = True
                        break
                for single in self.singles:
                    if single in combo:
                        exists = True
                        break
                if not exists:
                    self.combos.append(combo)

    def get(self):
        return [[single] for single in self.singles] + self.combos

    def __str__(self):
        return str([[single] for single in self.singles] + self.combos)


def get_exc_deck(deck, rank, exc_suit):
    pass


def find_card(rank, suit, deck):
    if convert_numeric_to_rank(rank) + suit in deck:
        return True
    return False


def odds_ranks(deck, rank_combos, dl=-1, exc_suit=None):
    if dl != -1:
        deck_len = dl
    else:
        deck_len = len(deck)
    rank_combos = MySet(rank_combos).get()
    deck_ranks = dict(Counter([convert_rank_to_numeric(rank) for rank, _ in deck]))
    deck_suits = dict(Counter([_ for rank, _ in deck]))
    singles = [s for s in rank_combos if len(s) == 1]
    doubles = [d for d in rank_combos if len(d) == 2]
    rank_amt = 0
    for rank in singles:
        if rank[0] in deck_ranks and deck_ranks[rank[0]] > 0:
            rank_amt += concept_of_combo_calculator(deck_len, 2) - concept_of_combo_calculator(deck_len - deck_ranks[rank[0]], 2)  # deck_ranks[hand[0]] * (deck_len - deck_ranks[hand[0]])
            if exc_suit is not None and find_card(rank[0], exc_suit, deck):
                rank_amt -= deck_suits[exc_suit] - 1
            deck_len -= deck_ranks[rank[0]]
            deck_ranks[rank[0]] = 0
    for cards in doubles:
        if cards[0] == cards[1] and cards[0] in deck_ranks:
            if deck_ranks[cards[0]] > 2:
                rank_amt += concept_of_combo_calculator(deck_ranks[cards[0]], 2)
        else:
            if cards[0] in deck_ranks and deck_ranks[cards[0]] > 0 and cards[1] in deck_ranks and deck_ranks[cards[1]] > 0:
                rank_amt += deck_ranks[cards[0]] * deck_ranks[cards[1]]
        if exc_suit is not None and find_card(cards[0], exc_suit, deck) and find_card(cards[1], exc_suit, deck):
            rank_amt -= 1
    
    return rank_amt


def odds_better(cards, board, deck):
    total_combos_amt = concept_of_combo_calculator(len(deck), 2)
    double_check = [1, 2, 3, 4, 8]
    rank_odds_func_key = {
        10: odds_of_royal_flush,  # 'Royal flush',
        9: odds_of_straight_flush,  # 'Straight flush',
        8: odds_of_4kind,  # 'Four of a kind',
        7: odds_of_full_house,  # 'Full house',
        5: odds_of_straight,  # 'Straight',
        4: odds_of_3kind,  # 'Three of a kind',
        3: odds_of_2pair,  # 'Two pair',
        2: odds_of_pair,  # 'One pair',
        1: odds_of_high_card,  # 'High card'
    }
    suit_odds_func_key = {
        6: odds_of_flush,  # 'Flush',
    }
    best_hand_cards, best_hand_rank, best_hand_rank_name, best_hand_high_card = calculate_best_hand(cards + board)
    rank_combos_that_win = MySet()
    suit_wins = 0
    rank_combos_that_tie = MySet()
    all_tie = False
    maybe_ties = []
    exc_suit = None

    # NOTE FOR TOMORROW
    # NEED TO CHANGE FLUSH SO THAT IT WORKS WITH SUITS COMBOS THAT WILL WIN
    wins = []
    ties = []


    d_len = len(deck)

    # keep_going = True
    # if best_hand_rank <= 10:  # Royale Flush
    #     flush_suits = odds_of_flush(board)
    #     if flush_suits is not None:
    #         pass
    # print('==========')
    if best_hand_rank <= 9:  # Straight Flush
        flush_suits = odds_of_flush(board)
        if flush_suits is not None:
            if flush_suits == 100:
                board_flush_suit = board[0][1]
                exc_suit = board_flush_suit
                suit_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in deck if _ == board_flush_suit])
                suited_board = [c for c in board if c[1] == board_flush_suit]
                straight_hands = odds_of_straight(suited_board, deck)[0]
                player_max = sorted([convert_rank_to_numeric(rank) for rank, _ in cards if _ == board_flush_suit])
                player_max_card = 0
                player_cards_sorted = sorted([convert_rank_to_numeric(rank) for rank, _ in suited_board] + player_max)
                pcs_len = len(player_cards_sorted)
                if best_hand_rank == 9 and len(player_max) > 0:
                    if str(player_max[-1]) + exc_suit in best_hand_cards:
                        player_max = best_hand_high_card
                    else:
                        player_max = convert_rank_to_numeric(suited_board[0][0])
                        all_tie = True
                else:
                    player_max = 0
            else:
                exc_suit = flush_suits[0]
                suit_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in deck if _ == flush_suits[0]])
                suited_board = [c for c in board if c[1] == flush_suits[0]]
                straight_hands = odds_of_straight(suited_board, deck)[0]
                player_max = [convert_rank_to_numeric(rank) for rank, _ in cards if _ == flush_suits[0]]
                player_max_card = 0
                player_cards_sorted = sorted([convert_rank_to_numeric(rank) for rank, _ in suited_board] + player_max)
                pcs_len = len(player_cards_sorted)
                if best_hand_rank == 9 and len(player_max) > 0:
                    if str(player_max[-1]) + exc_suit in best_hand_cards:
                        player_max = best_hand_high_card
                    else:
                        player_max = convert_rank_to_numeric(suited_board[0][0])
                        all_tie = True
                else:
                    player_max = 0

            for h in straight_hands:
                if len(h) == 1 and h[0] in suit_ranks:
                    comb_h_board = [convert_rank_to_numeric(rank) for rank, _ in suited_board] + h
                    new_combo_h_board = []
                    for r in comb_h_board:
                        if  r == 14 and 2 in comb_h_board and 3 in comb_h_board and 4 in comb_h_board and 5 in comb_h_board:
                            new_combo_h_board.append(1)
                        else:
                            new_combo_h_board.append(r)
                    new_combo_h_board = sorted(new_combo_h_board)
                    final = []
                    for ind in range(len(new_combo_h_board)-4):
                        if new_combo_h_board[ind+4] - new_combo_h_board[ind] == 4:
                            final = new_combo_h_board[ind:ind+5]
                    if final[-1] > player_max:
                        suit_wins += d_len -1
                        d_len -= 1
                        deck.remove(convert_numeric_to_rank(h[0]) + exc_suit)
                elif len(h) == 2 and h[0] in suit_ranks and h[1] in suit_ranks:
                    comb_h_board = [convert_rank_to_numeric(rank) for rank, _ in suited_board] + h
                    new_combo_h_board = []
                    for r in comb_h_board:
                        if  r == 14 and 2 in comb_h_board and 3 in comb_h_board and 4 in comb_h_board and 5 in comb_h_board:
                            new_combo_h_board.append(1)
                        else:
                            new_combo_h_board.append(r)
                    new_combo_h_board = sorted(new_combo_h_board)
                    final = []
                    for ind in range(len(new_combo_h_board)-4):
                        if new_combo_h_board[ind+4] - new_combo_h_board[ind] == 4:
                            final = new_combo_h_board[ind:ind+5]
                    if final[-1] > player_max:
                        suit_wins += 1
    # print('==========')
    if best_hand_rank <= 6:  # Flush
        flush_suits = odds_of_flush(board)
        if flush_suits is not None:
            if flush_suits == 100:
                board_flush_suit = board[0][1]
                exc_suit = board_flush_suit
                board_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in board])
                player_max = sorted([convert_rank_to_numeric(rank) for rank, _ in cards if _ == board_flush_suit])
                if len(player_max) > 0:
                    if player_max[-1] > board_ranks[0]:
                        player_max = player_max[-1]
                    else:
                        player_max = board_ranks[0]
                        all_tie = True
                else:
                    player_max = 0
                suit_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in deck if _ == board_flush_suit and convert_rank_to_numeric(rank) > player_max])
                for ind in range(len(suit_ranks)):
                    suit_wins += d_len - 1
                    d_len -= 1
                    deck.remove(convert_numeric_to_rank(suit_ranks[ind]) + board_flush_suit)
                # all_tie = True
            elif len(flush_suits) > 0:
                exc_suit = flush_suits[0]
                player_max = [convert_rank_to_numeric(rank) for rank, _ in cards if _ == flush_suits[0]]
                if len(player_max) > 0:
                    if flush_suits[1] <= len(player_max):
                        player_max = sorted(player_max)[-1]
                    else:
                        player_max = 0
                else:
                    player_max = 0
                suit_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in deck if _ == flush_suits[0]])
                if flush_suits[1] == 1:
                    for ind in range(len(suit_ranks)):
                        if suit_ranks[ind] > player_max:
                            suit_wins += d_len - 1
                            d_len -= 1
                            deck.remove(convert_numeric_to_rank(suit_ranks[ind]) + flush_suits[0])
                elif flush_suits[1] == 2:
                    exc_suit = flush_suits[0]
                    for ind in range(len(suit_ranks)):
                        for ind2 in range(ind+1, len(suit_ranks)):
                            if suit_ranks[ind2] > player_max:
                                suit_wins += 1
                        # print(convert_numeric_to_rank(suit_ranks[ind]) + flush_suits[0])


    if best_hand_rank >= 1:
        for rank_func_ind in range(best_hand_rank, 11):
            if rank_func_ind in rank_odds_func_key:
                if rank_func_ind == best_hand_rank:  # If it's the best rank
                    best_hand_board = calculate_best_hand(board)
                    do_continue = True
                    if rank_func_ind == 3:
                        if cards[0][0] == cards[1][0]:
                            board_rank_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in board])
                            board_low_double = sorted([rank for rank in board_rank_counter if board_rank_counter[rank] == 2])[0]
                            if convert_rank_to_numeric(cards[0][0]) > board_low_double:
                                do_continue = False
                            else:
                                all_tie = True
                    if do_continue and rank_func_ind in double_check and best_hand_rank == best_hand_board[1] and best_hand_high_card == best_hand_board[3]:
                        wins, ties, ext_tie = odds_of_high_card_same(cards, board, deck)
                        if rank_func_ind <= 2:
                            for ind in range(2, 15):
                                wins.append([ind, ind])
                        elif rank_func_ind == 3:
                            low_pair_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in best_hand_cards])
                            if not all_tie:
                                board_low_d = min([rank for rank in low_pair_counter if low_pair_counter[rank] == 2])
                            else:
                                board_rank_c = Counter([convert_rank_to_numeric(rank) for rank, _ in board])
                                board_low_d = sorted([rank for rank in board_rank_c if board_rank_c[rank] == 2])[0]
                            for ind in range(board_low_d, 15):
                                wins.append([ind, ind])
                        elif rank_func_ind == 4:
                            my_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in best_hand_cards])
                            possys = [rank for rank in my_counter if my_counter[rank] <= 2]
                            for poss in possys:
                                if poss > best_hand_high_card:
                                    wins.append([poss, poss])
                        if ext_tie:
                            all_tie = True
                    else:
                        if rank_func_ind == 7:
                            low_high_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in best_hand_cards])
                            low, high = 0, 0
                            for c in low_high_counter:
                                if low_high_counter[c] == 3:
                                    high = c
                                else:
                                    low = c
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, high, low)
                        elif rank_func_ind == 1:
                            sorted_cards = sorted([convert_rank_to_numeric(rank) for rank, _ in cards])
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, sorted_cards[1], sorted_cards[0])
                        elif rank_func_ind == 4:
                            board_ranks = [convert_rank_to_numeric(rank) for rank, _ in board]
                            cards_ranks = [convert_rank_to_numeric(rank) for rank, _ in cards]
                            to_use = 0
                            for rank in cards_ranks:
                                if rank not in board_ranks:
                                    to_use = rank
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, best_hand_high_card, to_use)
                        elif rank_func_ind == 2:
                            combined_cards_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in cards + board])
                            high_card_arr = sorted([rank for rank in combined_cards_counter if combined_cards_counter[rank] == 1])  # [1]
                            player_high_card = [convert_rank_to_numeric(rank) for rank, _ in cards if convert_rank_to_numeric(rank) in high_card_arr]
                            if len(player_high_card) > 0:
                                player_high_card = player_high_card[0]
                            else:
                                # player_high_card = 0
                                player_high_card = convert_rank_to_numeric(cards[0][0])
                            high_card = max(player_high_card, high_card_arr[1])
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, best_hand_high_card, high_card)
                        elif rank_func_ind == 3:
                            combined_cards_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in cards + board])
                            low, high = tuple(sorted([rank for rank in combined_cards_counter if combined_cards_counter[rank] == 2])[-2:])
                            high_card = [h for h in combined_cards_counter if combined_cards_counter[h] == 1][0]
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, high, low, high_card)
                        else:
                            wins, ties = rank_odds_func_key[rank_func_ind](board, deck, best_hand_high_card)
                else:
                    wins, ties = rank_odds_func_key[rank_func_ind](board, deck)
                if wins == 100.0:
                    return [0, 100.0, 0]
                elif ties == 100.0:
                    all_tie = True
                else:
                    for t in maybe_ties:
                        found = False
                        for w in wins:
                            sorted_t = sorted(t)
                            sorted_w = sorted(w)
                            if t[0] == w[0] and t[1] == w[1]:
                                found = True
                                break
                        if not found:
                            ties.append(t)
                    rank_combos_that_win.append(wins)
                    rank_combos_that_tie.append(ties)

    if best_hand_rank not in [6, 9, 10]:
        rank_combos_that_tie.append([[convert_rank_to_numeric(cards[0][0]), convert_rank_to_numeric(cards[1][0])]])
    # print('pre-tie', rank_combos_that_tie.get())
    new_ties = []
    for combo in rank_combos_that_tie.get():
        if len(combo) == 1:
            if len(rank_combos_that_win.get()) > 0:
                exists = False
                # exclude = {'singles': [], 'doubles': []}
                exclude = []
                for win_combo in rank_combos_that_win.get():
                    if len(win_combo) == 1:
                        if combo[0] == win_combo[0]:
                            exists = True
                            break
                        else:
                            exclude.append(win_combo)
                    if len(win_combo) == 2:
                        if combo[0] in win_combo:
                            exclude.append(win_combo)
                if not exists:
                    if len(exclude) == 0:
                        new_ties.append(combo)
                    else:
                        exclude = MySet(exclude).get()
                        singles = [single[0] for single in exclude if len(single) == 1]
                        doubles = [double for double in exclude if len(double) == 2]
                        for exc_combo in exclude:
                            if len(exc_combo) == 1:
                                doubles_including = []
                                for d in doubles:
                                    if combo[0] in d:
                                        doubles_including_ind = d.index(combo[0])
                                        if doubles_including_ind == 0:
                                            doubles_including.append(d[1])
                                        else:
                                            doubles_including.append(d[0])
                                for ind in range(2, 15):
                                    if ind not in singles and ind not in doubles_including:
                                        new_ties.append([combo[0], ind])
                            else:
                                if combo[0] in exc_combo:
                                    not_inc = [n for n in exc_combo if n != combo[0]]
                                    if len(not_inc) > 0:
                                        not_inc = not_inc[0]
                                        for ind in range(2, 15):
                                            if ind != not_inc:
                                                new_ties.append([combo[0], ind])
                                else:
                                    new_ties.append(combo)
            else:
                new_ties.append(combo)
        elif len(combo) == 2:
            if len(rank_combos_that_win.get()) > 0:
                exists = False
                for win_combo in rank_combos_that_win.get():
                    if len(win_combo) == 1:
                        if win_combo[0] in combo:
                            exists = True
                            break
                    elif len(win_combo) == 2:
                        if max(win_combo) == max(combo) and min(win_combo) == min(combo):
                            exists = True
                            break
                if not exists:
                    new_ties.append(combo)
            else:
                new_ties.append(combo)
        else:
            new_ties.append(combo)

    rank_combos_that_win = MySet(rank_combos_that_win.get())
    rank_combos_that_tie = MySet(new_ties)

    # print('win', rank_combos_that_win.get())
    # print('tie', rank_combos_that_tie.get())
    # print(rank_combos_that_win)
    # print('win:', rank_combos_that_win.get())
    # print('tie:', rank_combos_that_tie.get())
    rank_loss_odds = ((odds_ranks(deck, rank_combos_that_win.get(), d_len, exc_suit) + suit_wins) / total_combos_amt) * 100
    if all_tie:
        rank_tie_odds = 100.0 - rank_loss_odds
    else:
        rank_tie_odds = (odds_ranks(deck, rank_combos_that_tie.get(), d_len) / total_combos_amt) * 100
    rank_odds = [100 - (rank_loss_odds + rank_tie_odds), rank_loss_odds, rank_tie_odds]

    # print(rank_odds)

    return rank_odds

    # print('Loss:', rank_loss_odds)

    # RETURN 3 values, WIN%, LOSE%, TIE%


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


def concept_of_combo_calculator(a, b):
    # print(a, b)
    try:
        return factorial(a) / (factorial(b) * factorial(a - b))
    except ValueError:
        return 0


def is_straight(cards):
    cards = sorted(cards)
    for c in range(0, len(cards)-1):
        if cards[c] + 1 != cards[c+1]:
            return False
    return True


def odds_of_royal_flush(board, deck, to_beat=0):
    return [], []


def odds_of_straight_flush(board, deck, to_beat=0):
    return [], []


def odds_of_4kind(board, deck, to_beat=0):
    ranks = Counter(convert_rank_to_numeric(rank) for rank, _ in board)
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    ranks_1 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 1]
    ranks_2 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 2]
    ranks_3 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 3]
    ranks_4 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 4]
    combos_of_hands = []
    combos_of_ties = []
    if len(ranks_4) > 0:
        if ranks_4[0] > to_beat:
            return 100.0, 0.0
        elif ranks_4[0] == to_beat:
            return 0.0, 100.0
    if len(ranks_3) > 0 and ranks_3[0] in deck_ranks and deck_ranks[ranks_3[0]] > 0:
        if ranks_3[0] > to_beat:
            combos_of_hands.append([ranks_3[0]])
        elif ranks_3[0] == to_beat:
            combos_of_ties.append([ranks_3[0]])
    if len(ranks_2) > 0:
        for rank2 in ranks_2:
            if rank2 > to_beat:
                combos_of_hands.append([rank2, rank2])
            elif rank2 == to_beat:
                combos_of_ties.append([rank2, rank2])

    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()


# 2
def odds_of_full_house(board, deck, to_beat=0, to_beat2=0):
    ranks = Counter(convert_rank_to_numeric(rank) for rank, _ in board)
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    ranks_1 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 1]
    ranks_2 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 2]
    ranks_3 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] >= 3]
    combos_of_hands = []
    combos_of_ties = []

    if len(ranks_3) > 0 and len(ranks_2) > 0:
        return 100.0, 0.0

    # 3 on board and (pocket pairs, 1 on board and matching in hand)
    if len(ranks_3) > 0:
        for rank in ranks_3:
            if rank > to_beat:
                if len(ranks_2) > 0:
                    if ranks_2[0] > to_beat2:
                        return 100.0, 0.0
                for rank1 in ranks_1:
                    combos_of_hands.append([rank1])
                for deck_rank in deck_ranks:
                    if deck_rank != rank:
                        combos_of_hands.append([deck_rank, deck_rank])
            elif rank == to_beat:
                if len(ranks_2) > 0:
                    if ranks_2[0] > to_beat2:
                        return 100.0, 0.0
                    elif ranks_2[0] == to_beat2:
                        return 0.0, 100.0
                for rank1 in ranks_1:
                    if rank1 > to_beat2:
                        combos_of_hands.append([rank1])
                    elif rank1 == to_beat2:
                        if rank1 > to_beat:
                            combos_of_hands.append([rank1, rank1])
                        for deck_rank in deck_ranks:
                            if deck_rank in ranks_1 and deck_rank not in ranks_3:
                                if deck_rank <= to_beat2:
                                    combos_of_ties.append([rank1])
                            else:
                                combos_of_ties.append([rank1])
                for deck_rank in deck_ranks:
                    if deck_rank > to_beat2:
                        combos_of_hands.append([deck_rank, deck_rank])
    if len(ranks_2) > 0:  # If no 3s on the table
        # If they have one card that matches the pair and one that matches a single card
        for rank in ranks_2:
            if rank > to_beat:
                for rank2 in ranks_2:
                    if rank != rank2:
                        combos_of_hands.append([rank])
                for rank1 in ranks_1:
                    combos_of_hands.append([rank, rank1])
            elif rank == to_beat:
                for rank2 in ranks_2:
                    if rank2 != rank and rank2 == to_beat2:
                        combos_of_ties.append([rank])
                for rank1 in ranks_1:
                    if rank1 > to_beat2:
                        combos_of_hands.append([rank, rank1])
                    if rank1 == to_beat2:
                        combos_of_ties.append([rank, rank1])

    if len(ranks_1) > 0:
        for rank in ranks_1:
            for rank2 in ranks_2:
                if rank > to_beat:
                    combos_of_hands.append([rank, rank])


    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()
    # return (amt_of_hands / concept_of_combo_calculator(len(deck), 2)) * 100


# Done
def odds_of_straight(board, deck, to_beat=0):
    ranks = [convert_rank_to_numeric(rank) for rank, _ in board]
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    for rank in ranks.copy():
        if rank == 14:
            ranks.append(1)
    ranks = sorted(list(set(ranks)))

    cards_for_straight = []
    cards_for_tie = []
    for ind in range(0, 1):
        straight_arr = [num for num in range(to_beat-4, to_beat+1)]
        straight_non = []
        counter = 0
        for straight_ind in straight_arr:
            if straight_ind in ranks:
                counter += 1
            else:
                straight_non.append(straight_ind)
            if counter >= 3 and max(straight_arr) == to_beat:
                for ind in range(len(straight_non)):
                    if straight_non[ind] == 1:
                        straight_non[ind] = 14
                cards_for_tie.append(straight_non)
    for ind in range(to_beat-3, 15-4):
        straight_arr = [num for num in range(ind, ind+5)]
        straight_non = []
        counter = 0
        for straight_ind in straight_arr:
            if straight_ind in ranks:
                counter += 1
            else:
                straight_non.append(straight_ind)
            if counter == 3:
                for ind in range(len(straight_non)):
                    if straight_non[ind] == 1:
                        straight_non[ind] = 14
                cards_for_straight.append(straight_non)
    return MySet(cards_for_straight).get(), MySet(cards_for_tie).get()


def odds_of_flush(board):  # s s s
    # rank_counts = Counter(convert_rank_to_numeric(rank) for rank, _ in hand)
    suits = Counter(suit for _, suit in board)
    suits_flush = {}
    for s in suits:
        if suits[s] == 3:
            return (s, 2)
            # return concept_of_combo_calculator(deck_suits[s], 2) / concept_of_combo_calculator(len(deck), 2) * 100
        elif suits[s] == 4:
            return (s, 1)
            # return ((deck_suits[s] * (len(deck)-deck_suits[s])) + concept_of_combo_calculator(deck_suits[s], 2)) / concept_of_combo_calculator(len(deck), 2) * 100
        elif suits[s] == 5:
            return 100.0
    return None


# Done
def odds_of_3kind(board, deck, to_beat=0, h_card=0):
    board_ranks = [convert_rank_to_numeric(rank) for rank, _ in board]
    ranks = Counter(board_ranks)
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    ranks_1 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 1]
    ranks_2 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 2]
    ranks_3 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] >= 3]
    combos_of_hands = []
    combos_of_ties = []

    tied = False
    if len(ranks_3) > 0:
        if ranks_3[0] > to_beat:
            return 100.0, 0.0
        elif ranks_3[0] == to_beat:
            return 0.0, 100.0
    for rank in ranks_2:
        if rank > to_beat:
            combos_of_hands.append([rank])
        elif rank == to_beat:
            new_board_ranks = board_ranks + []
            new_board_ranks.remove(rank)
            new_board_ranks.remove(rank)
            board_rank_counter = Counter(new_board_ranks)
            high_board_rank = sorted([rank for rank in board_rank_counter if board_rank_counter[rank] == 1])[-2]
            max_c = max(high_board_rank, h_card)
            if max_c == h_card:
                for ind in range(2, 15):
                    if ind == max_c:
                        combos_of_ties.append([rank, ind])
                    elif ind > max_c:
                        combos_of_hands.append([rank, ind])
            else:
                for ind in range(2, 15):
                    if ind < max_c:
                        combos_of_ties.append([rank, ind])
                    elif ind > max_c:
                        combos_of_hands.append([rank, ind])
    for rank in ranks_1:
        if deck_ranks[rank] >= 2:
            if rank > to_beat:
                combos_of_hands.append([rank, rank])
            elif rank == to_beat:
                combos_of_ties.append([rank, rank])
    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()


# Done
def odds_of_2pair(board, deck, to_beat=0, to_beat2=0, h_card=0):
    board_ranks = [convert_rank_to_numeric(rank) for rank, _ in board]
    ranks = Counter(board_ranks)
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    ranks_1 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 1]
    ranks_2 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] >= 2]
    combos_of_hands = []
    combos_of_ties = []

    # Any 2 pair with a higher high than ours or == high and higher low
    for rank in ranks_2:
        if rank > to_beat:
            for rank2 in ranks_2:
                if rank2 != rank:
                    return 100.0, 0.0
            for rank1 in ranks_1:
                combos_of_hands.append([rank1])
            for ind in range(2, 15):
                combos_of_hands.append([ind, ind])
        elif rank == to_beat:
            for rank1 in ranks_1:
                if rank1 > to_beat2:
                    combos_of_hands.append([rank1])
                elif rank1 == to_beat2:
                    new_board_ranks = board_ranks + []
                    new_board_ranks.remove(rank1)
                    board_rank_counter = Counter(new_board_ranks)
                    high_board_rank = sorted([rank for rank in board_rank_counter if board_rank_counter[rank] == 1])[-1]
                    max_c = max(high_board_rank, h_card)
                    for ind in range(2, 15):
                        if ind < max_c:
                            if max_c != h_card:
                                combos_of_ties.append([rank1, ind])
                        if ind > max_c:
                            combos_of_hands.append([rank1, ind])
            for ind in range(to_beat2+1, 15):
                combos_of_hands.append([ind, ind])
            combos_of_ties.append([to_beat2, to_beat2])
        else:
            for rank1 in ranks_1:
                if rank1 > to_beat:
                    combos_of_hands.append([rank1])
                elif rank1 == to_beat:
                    new_board_ranks = board_ranks + []
                    new_board_ranks.remove(rank1)
                    new_board_ranks.remove(rank)
                    board_rank_counter = Counter(new_board_ranks)
                    high_board_rank = sorted([rank for rank in board_rank_counter if board_rank_counter[rank] == 1])
                    if len(high_board_rank) > 0:
                        high_board_rank = high_board_rank[-1]
                    else:
                        high_board_rank = high_board_rank[-1]
                    max_c = max(high_board_rank, h_card)
                    for ind in range(2, 15):
                        if ind < max_c:
                            if max_c != h_card:
                                combos_of_ties.append([rank1, ind])
                        if ind > max_c:
                            combos_of_hands.append([rank1, ind])
    for rank in ranks_1:
        if rank > to_beat:
            for rank1 in ranks_1:
                if rank != rank1:
                    combos_of_hands.append([rank, rank1])
        elif rank == to_beat:
            for rank1 in ranks_1:
                if rank != rank1:
                    if rank1 > to_beat2:
                        combos_of_hands.append([rank, rank1])
                    elif rank1 == to_beat2:
                        combos_of_ties.append([rank, rank1])
    if to_beat > 0:
        if to_beat not in ranks_1:
            combos_of_ties.append([to_beat, to_beat])
        if len(ranks_2) > 0:
            for ind in range(to_beat+1, 15):
                combos_of_hands.append([ind, ind])
    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()


# Done
def odds_of_pair(board, deck, to_beat=0, h_card=0):
    ranks = Counter(convert_rank_to_numeric(rank) for rank, _ in board)
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    ranks_1 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] == 1]
    ranks_2 = [convert_rank_to_numeric(rank) for rank in ranks if ranks[rank] >= 2]
    combos_of_hands = []
    combos_of_ties = []

    highest_ranks_2 = -1
    for rank in ranks_2:
        if rank > highest_ranks_2:
            highest_ranks_2 = ranks_2[0]
    if highest_ranks_2 > to_beat:
        return 100.0, 0.0
    elif highest_ranks_2 == to_beat:
        return 0.0, 100.0

    for rank in ranks_1:
        if rank > to_beat:
            combos_of_hands.append([rank])
        elif rank == to_beat:
            for ind in range(2, 15):
                if ind not in ranks:
                    if h_card in ranks and ind < h_card:
                        combos_of_ties.append([rank, ind])
                    elif h_card not in ranks and ind == h_card:
                        combos_of_ties.append([rank, ind])
                    elif ind > h_card:
                        combos_of_hands.append([rank, ind])

    for rank in deck_ranks:
        if rank > to_beat:
            combos_of_hands.append([rank, rank])

    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()


# Done
def odds_of_high_card(board, deck, to_beat=0, to_beat2=0):
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    combos_of_hands = []
    combos_of_ties = []
    board_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in board])
    least_rank = 0
    if board_ranks[1] > to_beat2:
        least_rank = board_ranks[1]
    else:
        least_rank = to_beat2
    for rank in range(2, 15):
        if rank > to_beat:
            combos_of_hands.append([rank])
        elif rank == to_beat:
            if to_beat2 == least_rank:
                for rank1 in range(2, 15):
                    if rank1 > to_beat2:
                        combos_of_hands.append([rank, rank1])
                    elif rank1 == to_beat2:
                        combos_of_ties.append([rank, rank1])
            else:
                for rank1 in range(2, 15):
                    if rank1 > least_rank:
                        combos_of_hands.append([rank, rank1])
                    elif rank1 < least_rank:
                        combos_of_ties.append([rank, rank1])
    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get()


# Done
def odds_of_high_card_same(cards, board, deck):
    combos_of_hands = []
    combos_of_ties = []
    deck_ranks = Counter([convert_rank_to_numeric(rank) for rank, _ in deck])
    cards_ranks = sorted([convert_rank_to_numeric(rank) for rank, _ in cards])
    board_ranks = [convert_rank_to_numeric(rank) for rank, _ in board]
    board_ranks_counter = Counter([convert_rank_to_numeric(rank) for rank, _ in cards + board])
    used = []
    non_used = []
    four_kind = False
    for c in board_ranks_counter:
        if board_ranks_counter[c] >= 2:
            if board_ranks_counter[c] == 4:
                four_kind = True
                break
            used += [c for ind in range(board_ranks_counter[c])]
        else:
            non_used.append(c)

    if four_kind:
        non_used = []
        for c in board_ranks_counter:
            if board_ranks_counter[c] != 4:
                non_used.append(c)

    if len(non_used) > 2:
        total_ranks = sorted(non_used)[2:]
    else:
        total_ranks = sorted(non_used)
    
    small_instance = True if cards_ranks[0] in total_ranks else False
    big_instance = True if cards_ranks[1] in total_ranks else False
    # print('t', total_ranks)
    
    try:
        least_board_rank = total_ranks[0]
    except:
        pass
        # print(cards, board, total_ranks)
    uses = {'none': not big_instance, 'once': (not small_instance and big_instance), 'twice': (small_instance and big_instance)}

    # for rank in board_ranks:
    #     combos_of_hands.append([rank])
    if uses['none']:
        for rank in deck_ranks:
            if rank > least_board_rank:
                combos_of_hands.append([rank])
    elif uses['once']:
        for rank in range(cards_ranks[1]+1, 15):
            combos_of_hands.append([rank])
        for ind in range(2, least_board_rank):
            combos_of_ties.append([cards_ranks[1], ind])
        for ind in range(least_board_rank+1, 15):
            combos_of_hands.append([cards_ranks[1], ind])
    elif uses['twice']:
        for ind1 in range(cards_ranks[1]+1, 15):
            combos_of_hands.append([ind1])
        for ind1 in range(cards_ranks[0]+1, 15):
            combos_of_hands.append([cards_ranks[1], ind1])
        combos_of_ties.append([cards_ranks[1], cards_ranks[0]])
        # for rank in deck_ranks:
        #     if rank > cards_ranks[1]:
        #         combos_of_hands.append([rank])
        #     elif rank == cards_ranks[1]:
        #         combos_of_hands.append([rank, rank])
        #         for rank2 in deck_ranks:
        #             if rank2 < rank:
        #                 if rank2 > cards_ranks[0]:
        #                     combos_of_hands.append([rank, rank2])
        #                 elif rank2 == cards_ranks[0]:
        #                     combos_of_ties.append([rank, rank2])

    return MySet(combos_of_hands).get(), MySet(combos_of_ties).get(), uses['none']


def main(cards = [], board = []):
    if len(cards) == 0:
        my_deck = get_deck()
        shuffle(my_deck)
        mcl = 2
        my_cards = []
        for ind in range(mcl):
            c = choice(my_deck)
            my_cards.append(c)
            my_deck.remove(c)

        mcl = 5
        my_board = []
        for ind in range(mcl):
            c = choice(my_deck)
            my_board.append(c)
            my_deck.remove(c)
    else:
        my_cards = cards + []
        my_board = board + []
        my_deck = make_deck(cards, board)

    # my_cards = ['7c', 'Jd']
    # my_board = ['Kh', '8s', 'Ac', '9s', 'Qh']
    # my_deck = make_deck(my_cards, my_board)

    print('Mine:', str(my_cards) + ', ' + str(my_board))
    # print(calculate_best_hand(my_cards + my_board))
    ods = odds_better(my_cards, my_board, my_deck)
    # print('Time:', time.time() - tm)

    return my_cards, my_board

    # test turn and river combos


if __name__ == '__main__':
    highest = None
    highest_straight = 0
    pre_time = time.time()
    for i in range(0, 1):
        if i % 1000 == 0:
            print('i', i)
        m_c, m_b = [], []
        m_c, m_b = ['2d', '2c'], ['Qs', 'Qd', '2s', 'Qh', 'Qc']
        m_c, m_b = main(m_c, m_b)
        # test(m_c, m_b)
        # if new[0] > highest_straight:
        #     highest_straight = new[0]
        #     highest = new
    print('\n\nTotal Time:', time.time() - pre_time)

    # print(highest)
    # print(highest_straight)





















