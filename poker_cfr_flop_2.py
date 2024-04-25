import numpy as np
import json
# import poker_calc
# import oth
from random import choice, shuffle
from per_calc import get_odds
import time
from poker_calc import compare_hands
import os

# KEY
# perc | (#players) | (Bet History)


# POSITION
# 0: Dealer, 1: Small Blind, 2: Big Blind

# Raise key
# 1 == 1BB, 2 == 2BB, 3 == 3BB, 4 == 4BB, 5 == 5BB, A == All in


class Poker:
    def __init__(self):
        self.deck = self.get_deck()
        self.player_hands = [[], []]
        self.player_odds_pre_flop = ['', '']
        self.player_odds_flop = []
        self.player_odds_turn = []
        self.player_odds_river = []
        self.player_odds_flop_class = []
        self.player_odds_turn_class = []
        self.player_odds_river_class = []
        self.num_players = 2
        self.winners = []
        self.broll = 300
        self.big_blind = 20
        self.small_blind = 10
        self.bet_key = ['1', '2', '3', '4', '5', 'A']

        for _ in range(self.num_players):
            self.player_odds_flop.append((-1, -1))
            self.player_odds_flop_class.append((-1, -1))
            # self.player_odds_flop.append([(-1, -1), (-1, -1)])
            # self.player_odds_flop_class.append([(-1, -1), (-1, -1)])
            # self.player_odds_turn.append([(-1, -1), (-1, -1)])
            # self.player_odds_turn_class.append([(-1, -1), (-1, -1)])
            # self.player_odds_river.append([(-1, -1), (-1, -1)])
            # self.player_odds_river_class.append([(-1, -1), (-1, -1)])
    
    def get_deck(self):
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

    def make_deck(self, cards, board):
        deck = self.get_deck()
        for card in cards + board:
            deck.remove(card)
        return deck
    
    def convert_rank_to_numeric(self, rank):
        rank_mapping = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        if rank in rank_mapping:
            return rank_mapping[rank]
        else:
            return int(rank)

    def convert_numeric_to_rank(self, rank):
        rank_mapping = {14: 'A', 13: 'K', 12: 'Q', 11: 'J', 10: 'T'}
        if rank in rank_mapping:
            return rank_mapping[rank]
        else:
            return str(rank)

    # DONE
    def classify_tie_odds(self, odds):
        if odds > 5:
            if odds > 10:
                if odds > 30:
                    if odds > 60:
                        if odds > 90:
                            return 5
                        return 4
                    return 3
                return 2
            return 1
        return 0

    # DONE
    def classify_odds(self, odds):  # 0-10 == 0     10-30 == 1     30-50 == 2     50-70 == 3      70-90 == 4      90-100 == 5
        # if odds > 10:
        #     if odds > 30:
        #         if odds > 50:
        #             if odds > 70:
        #                 if odds > 90:
        #                     return 5
        #                 return 4
        #             return 3
        #         return 2
        #     return 1
        # return 0
        return int(round(odds / 20, 0))

    # DONE
    def get_active_player(self, round_history):  # 0c,1c,2x/1r,2f,0c/
        players_involved = [1, 0]
        if round_history == '':
            return players_involved[0]
        temp_history = round_history + ''
        if round_history == '':
            return 0
        while temp_history.find('f') != -1:
            temp_history_f = temp_history.find('f')
            players_involved.remove(int(temp_history[temp_history_f-1:][:1]))
            temp_history = temp_history[temp_history_f+1:]
        
        if len(players_involved) == 1:
            return players_involved[0]

        last_round = round_history.split(',')
        for m in last_round:
            if m != '':
                if int(m[0]) not in players_involved:
                    last_round.remove(m)
        
        if len(last_round) > 1:
            last_player = int(last_round[-2][0])
        else:
            if last_round[0] == '':
                last_player = players_involved[-1]
            else:
                last_player = int(last_round[-1][0])
        for m in last_round:
            if m != '':
                pass
            else:
                lpi = players_involved.index(last_player)
                if lpi < len(players_involved)-1:
                    return players_involved[lpi+1]
                else:
                    return players_involved[0]
        print(round_history, last_round)

    # DONE
    def classify_bet(self, bet, broll=300):
        bet_key = {10: '0', 20: '1', 40: '2', 60: '3', 80: '4', 100: '5', 300: 'A'}
        return bet_key[bet]

    # DONE
    def unclassify_bet(self, bet, broll=300):
        bet_key = {'0': self.small_blind, '1': self.big_blind, '2': self.big_blind*2, '3': self.big_blind*3, '4': self.big_blind*4, '5': self.big_blind*5, 'A': broll}
        # bet_key = {'1': 20, '2': 40, '3': 60, '4': 80, '5': 100, 'A': 300}
        return bet_key[bet]

    # DONE
    def is_next_round(self, round_history):
        players_involved = [1, 0]
        temp_history = round_history + ''
        while temp_history.find('f') != -1:
            temp_history_f = temp_history.find('f')
            players_involved.remove(int(temp_history[temp_history_f-1:][:1]))
            temp_history = temp_history[temp_history_f+1:]
        
        if len(players_involved) <= 1:
            return True

        last_round = round_history.split(',')
        for m in last_round:
            if m != '' and int(m[0]) not in players_involved:
                last_round.remove(m)

        player_bets = self.get_all_bets(round_history)
        player_bets = {p: player_bets[p] for p in player_bets if p in players_involved}
        max_bet = max(player_bets.values())
        
        if len(last_round) - (1 if last_round[-1] == '' else 0) >= len(players_involved):
            for p in player_bets:
                if player_bets[p] != max_bet:
                    return False
            return True
        return False
    
    # DONE
    def get_player_bet(self, round_history, player):
        return self.get_all_bets(round_history)[player]

    # DONE
    def get_all_bets(self, round_history):
        player_bets = {0: 0, 1: 0}
        for m in round_history.split(','):
            if m != '':
                # print(m, max(list(player_bets.values())))
                if m[1] == 'x':
                    player_bets[int(m[0])] = max(list(player_bets.values()))
                elif m[1] != 'f':
                    if m[1] == 'A':
                        player_bets[int(m[0])] = self.broll
                    else:
                        player_bets[int(m[0])] = max(list(player_bets.values())) + (self.unclassify_bet(m[1]) if m[1] != 'x' else 0)

        return player_bets

    # DONE
    def get_pot(self, round_history):
        return sum(list(self.get_all_bets(round_history).values()))
    
    # DONE
    def get_valid_actions(self, round_history, current_player, previous_bet=0):
        br = self.broll - previous_bet
        br -= self.get_all_bets(round_history)[current_player]

        bet = -1
        player_bet_count = self.get_all_bets(round_history)

        for m in round_history.split(','):
            if m != '':
                if m[1] not in ['f', 'x']:
                    # player_bet_count[int(m[0])] += 1
                    if m[1] == 'A':
                        bet = 6
                        if int(m[0]) == current_player:
                            return []
                    elif int(m[1]) > bet:
                        bet = int(m[1])

        acts = ['f', 'x']
        if bet == 6:
            return acts
        
        if bet == -1:
            acts = ['x']
            bet = 1
        elif bet == 0:
            bet = 1
        
        if player_bet_count[current_player] < 2 and br > self.unclassify_bet(str(bet)):
            for ind in range(bet, 6):
                if br - self.unclassify_bet(str(ind)) > 0:
                    acts.append(str(ind))
        acts.append('A')
        return acts

    # DONE
    def get_players_involved(self, round_history):
        players_involved = [1, 0]
        if round_history == '':
            return players_involved
        temp_history = round_history + ''
        while temp_history.find('f') != -1:
            temp_history_f = temp_history.find('f')
            players_involved.remove(int(temp_history[temp_history_f-1:][:1]))
            temp_history = temp_history[temp_history_f+1:]
        return players_involved

    def get_winners(self, players_involved):
        winners = []
        for ws in self.winners:
            new_ws = []
            for w in ws:
                if w in players_involved:
                    new_ws.append(w)
            if len(new_ws) > 0:
                winners.append(new_ws)
        
        return winners[-1]

    # MAYBE DONE
    def is_call(self, round_history):
        current_player = self.get_active_player(round_history)
        current_bets = self.get_all_bets
        if current_bets[current_player] == max(current_bets.values()):
            return False
        else:
            return True

    def get_info_set(self, i_map, history, current_round, current_player):
        new_key = ''
        if current_round == 0:  # Pre-flop
            new_key = self.player_odds_pre_flop[current_player]
        elif current_round == 1:  # Flop
            new_key = self.player_odds_flop_class[current_player]
        elif current_round == 2:  # Turn
            new_key = self.player_odds_turn_class[current_player]
        elif current_round == 3:  # River
            new_key = self.player_odds_river_class[current_player]
        new_key = str(new_key)
        new_key += f' | {self.num_players} | {history}'

        if new_key in i_map:
            return i_map[new_key]

        valid_actions = self.get_valid_actions(history, current_player, current_round)

        n_actions = len(valid_actions)
        info_set = InformationSet(new_key, n_actions)
        i_map[new_key] = info_set

        return i_map[new_key]

    def cfr(self, i_map, history="", pr_1=1, pr_2=1):
        if history == "":  # odds | (#players) | (Bet History)
            self.__init__()
            self.deck = self.get_deck()
            shuffle(self.deck)
            self.player_hands = [ self.deck[0:2] , self.deck[2: 4], self.deck[4: 6]]
            for ind in range(self.num_players):
                if self.convert_rank_to_numeric(self.player_hands[ind][0][0]) > self.convert_rank_to_numeric(self.player_hands[ind][1][0]):
                    hand = self.player_hands[ind][0][0] + self.player_hands[ind][1][0]  + ('s' if self.player_hands[ind][0][1] == self.player_hands[ind][1][1] else '')
                else:
                    hand = self.player_hands[ind][1][0] + self.player_hands[ind][0][0]  + ('s' if self.player_hands[ind][0][1] == self.player_hands[ind][1][1] else '')
                self.player_odds_pre_flop[ind] = hand

                # All odds
                flop_odds = get_odds(self.player_hands[ind], self.deck[-5:-2], self.make_deck(self.player_hands[ind], self.deck[-5:-2]))

                # Flop odds
                self.player_odds_flop[ind] = flop_odds
                self.player_odds_flop_class[ind] = (self.classify_odds(flop_odds[0]), self.classify_tie_odds(flop_odds[1]))
            
            board = self.deck[-5:]
            d_vs_s = compare_hands(self.player_hands[0], self.player_hands[1], board)

            if d_vs_s == 1:
                self.winners = [[1], [0]]
            elif d_vs_s == 0:
                self.winners = [[1, 0]]
            else:
                self.winners = [[0], [1]]
            
            # history = f'1{self.classify_bet(self.small_blind)},2{self.classify_bet(self.big_blind)},'
            history = ''
        # print()
        # print(history)
        # print(pres)
        # if max(pres) > 600 or max(pres) < -300:
        #     exit()
        current_player = self.get_active_player(history)
        current_round = 1
        players_involved = self.get_players_involved(history)

        if self.is_next_round(history):
            winners = self.get_winners(players_involved)

            res = []

            for player_ind in range(2):
                player_bet = self.get_player_bet(history, player_ind)
                if len(players_involved) == 1 and player_ind in players_involved:
                    res.append(self.get_pot(history) - player_bet)
                elif player_ind in winners:
                    res.append((self.get_pot(history) / len(winners)) - player_bet)
                else:
                    res.append(-1 * player_bet)

            return res

        info_set = self.get_info_set(i_map, history, current_round, current_player)

        strategy = info_set.strategy

        if current_player == 0:
            info_set.reach_pr += pr_1
        elif current_player == 1:
            info_set.reach_pr += pr_2
        
        val_act = self.get_valid_actions(history, current_player, current_round)
        action_utils = np.array([[0, 0] for act in val_act])

        for ind, action in enumerate(val_act):
            next_history = history + str(current_player) + action + ','
            if current_player == 0:
                amt = self.cfr(i_map, next_history, pr_1 * strategy[ind], pr_2)
            elif current_player == 1:
                amt = self.cfr(i_map, next_history, pr_1, pr_2 * strategy[ind])

            action_utils[ind] = amt  # utility of current player equals - utility of player corresponding to next history

        pres = [0, 0]

        new_action_utils = [act[current_player] for act in action_utils]

        for ind, act in enumerate(action_utils):
            act = act * strategy[ind]
            for p in range(len(act)):
                pres[p] += act[p]

        util = pres[current_player]  # expected value: sum of outcome for each action times the probability that said action is chosen
        regrets = new_action_utils - util  # entry a stores the difference between the value of always choosing action a and the expected value for given strategy

        if current_player == 0:
            info_set.regret_sum += pr_2 * regrets
        elif current_player == 1:
            info_set.regret_sum += pr_1 * regrets

        # if history == '1A,2x,' or history == '1A,':
        #     print()
        #     print(history)
        #     print(pres)
        #     print('self.winners:', self.winners)
        #     print('WINNERS:', self.get_winners(players_involved))
        #     print(current_player, history, new_action_utils, regrets)

        return pres


class InformationSet:
    def __init__(self, key, n_actions):
        self.key = key
        self.n_actions = n_actions
        self.regret_sum = np.zeros(self.n_actions)
        self.strategy_sum = np.zeros(self.n_actions)
        self.strategy = np.repeat(1/self.n_actions, self.n_actions)
        self.reach_pr = 0
        self.reach_pr_sum = 0
    
    def update_strategy(self):
        self.strategy_sum += self.reach_pr * self.strategy
        self.reach_pr_sum += self.reach_pr
        self.strategy = self.get_strategy()
        self.reach_pr = 0
    
    def get_strategy(self):
        strategy = self.to_nonnegative(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy /= total
            return strategy
        return np.repeat(1/self.n_actions, self.n_actions)
    
    def get_average_strategy(self):
        strategy = self.strategy_sum
        total = sum(strategy)
        if total > 0:
            strategy /= total
            return strategy
        return np.repeat(1/self.n_actions, self.n_actions)

    def __str__(self):
        strategies = ['{:03.2f}'.format(x)
                        for x in self.get_average_strategy()]
        return '{} {}'.format(self.key.ljust(6), strategies) + ' ' + str(self.reach_pr_sum)

    def to_nonnegative(self, val):
        return np.where(val > 0, val, 0)


def map_to_string(mp):
    final_str = ''
    for key in mp:
        final_str += key + ' ` ' + str(mp[key].get_strategy()) + ' ` ' + str(mp[key].regret_sum) + '\n'
    return final_str

def write_map(mp):
    final_str = ''
    for key in mp:
        final_str += key + ' ` ' + str(mp[key].get_strategy()) + ' ` ' + str(mp[key].regret_sum) + '\n'
    cur = -1
    folder_num = -1
    nash_path = 'flop_2_nashes_new/'
    for f in os.listdir(nash_path):
        if int(f) > folder_num:
            folder_num = int(f)
    print(folder_num+1)
    os.mkdir(f'{nash_path}{folder_num+1}/')
    for f in os.listdir(f'{nash_path}{folder_num+1}/'):
        num = int(f[f.find('_')+1:f.find('.')])
        if num > cur:
            cur = num
    open(f'{nash_path}{folder_num+1}/2playerflop_{cur+1}.txt', 'w+').write(final_str)


def main(n_iterations=1):
    poker = Poker()
    i_map = {}
    # print(poker.get_valid_actions('1x,2x,01,1x,21,0x,14,2x,05,', 1))  # 1x,2x,01,1x,21,0x,14,2x,05,15,2A,0f,1x,
    # exit()
    # print( poker.get_active_player(hist) )  # 11,2x,0f,
    # print('---')
    # print( poker.history_to_readable(hist) )
    tm = time.time()
    egv = 0
    for _ in range(1, n_iterations+1):
        print('I_MAP length:', len(i_map))
        print('Iteration:', _)
        if _ % 5 == 0:  # if _ % 50 == 0:
            if _ != 0:
                print('UPDATED')
                write_map(i_map)
        this_egv = sum(poker.cfr(i_map))
        egv += this_egv
        print('EGV:', egv, 'This EGV:', this_egv)
        print('Post:', time.time() - tm)
        for key in i_map:
            i_map[key].update_strategy()
        print('POST:', time.time() - tm)
    # print(map_to_string(i_map))
    write_map(i_map)
    print('Expected Game Value:', egv)
    print('Total Iterations:', n_iterations)
    print('Total Time:', time.time() - tm)


def test(cards, board):
    poker = Poker()
    flop_odds = get_odds(cards, board, poker.make_deck(cards, board))
    print(poker.classify_odds(flop_odds[0]), poker.classify_tie_odds(flop_odds[1]))


if __name__ == '__main__':
    main(5000)

    
    # my_cards, my_board = [ '9s', 'Js' ], [ '6h', 'Kh', 'Jd' ]
    # test(my_cards, my_board)


































