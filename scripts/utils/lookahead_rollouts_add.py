from utils.game_map_class import GameMap
from utils.game_team_class import GameTeam
#from utils.strategy_class import Strategy, RandomStrategy, RuleOfThumbStrategy
from utils.map_setup_functions import setGameBoardRandom, initializeFullRiskMap
from utils.heuristics import BST_Heuristic, EdgeWin

import networkx as nx
import matplotlib.pyplot as plt

import copy

def rollout_lookahead(team,opponent,riskMap,d,discount, print_ = False):
    '''Returns the best action according to lookahead with rollouts'''
    return greedy(team,opponent,riskMap,d,discount, print_ = print_)[0]

def greedy(team,opponent,riskMap,d,discount, print_ = False):
    '''Greedily looks through all possible actions and determines the value of each from the current state
    using lookahead with rollouts. Returns action with maximum value and the value itself'''
    possible_destinations = team.getTerritories()

    if print_:
        print("Possible Destinations:", possible_destinations)
    lookahead_list = []
    for dest in possible_destinations:
        #print("Try adding 1 troop to {dest}".format(dest = dest))
        action = dest
        u = lookahead(discount,riskMap,action,d,team.name,opponent.name, print_ = print_)
        lookahead_list.append((action,u))
    if print_:
        print("Lookahead List:", lookahead_list)
    if len(lookahead_list) == 0:
        return (None,None)
    return max(lookahead_list, key = lambda x: x[1])

def lookahead(discount,riskMap,action,d,team_name,opponent_name, print_ = False):
    ''' Computes successor states and probabilities of these successor states given the current riskMap

    Then for each of these successor states performs a rollout to get a value that that successor state and
    multiplies it by the probability of that successor state. Takes the sum of those values and multiplies it
    by the discount factor to return the value of that function.
    '''
    # There's only one successor state with 100% likelihood

    # Sets up successor state
    sp = copy.deepcopy(riskMap)
    # Doing a deepcopy of the riskMap also makes copies of the GameTeams stored within the map in riskMap.teams
    # so we don't have to make another copy
    my_team = sp.teams[team_name]
    opponent = sp.teams[opponent_name]
    
    my_team.addTroops(action,1)

    sum_successors = 1*rollout(discount,sp,d,my_team,opponent, print_ = print_)

    return discount*sum_successors

def rollout(discount,sp,d,my_team,opponent, print_ = False):
    '''Rolls out using a stochastic policy (this is encoded in the strategy of my_team itself) against player.
    Repeats rounds of turns to depth. If my_team wins, the reward is 100. If the opponent wins, the reward is 0.
    Otherwise, at the end of the rollout, we use the BST heuristic for both teams and the reward. We see what percentage
    of BTS between the two teams is attributed to the opponent (would be good for my_team) and use that as the reward'''
    ret = 0
    end_reached = False
    for t in range(d):
       
        my_team.playAttacks(print_ = print_)
       
        if my_team.hasTeamWon():
            r = 100
            return (discount**t)*r
        opponent.playTurn(print_ = print_)
        if opponent.hasTeamWon():
            r = -1
            return (discount**t)*r
        my_team.playAddTroops(print_ = print_)
    if my_team.hasTeamWon():
        r = 100
        return (discount**(d-1))*r
    elif opponent.hasTeamWon():
        r = -1
        return (discount**(d-1))*r
    else:
        #print(BST_Heuristic(my_team,sp))
        #BST_my_team_sum = sum(list(BST_Heuristic(my_team,sp).values()))
        #BST_opponent_sum = sum(list(BST_Heuristic(opponent,sp).values()))
        #r = 100*BST_opponent_sum/(BST_my_team_sum+BST_opponent_sum)
        r = 100*EdgeWin(my_team,sp)
        return (discount**(d-1))*r
