from utils.game_map_class import GameMap
from utils.game_team_class import GameTeam
from utils.strategy_class import Strategy, RandomStrategy, RuleOfThumbStrategy
from utils.map_setup_functions import setGameBoardRandom, initializeFullRiskMap
from utils.heuristics import BST_Heuristic

import networkx as nx
import matplotlib.pyplot as plt

import math
import copy

def monteCarloTreeSearch(state, num_sims, depth, discount):
    N = defaultdict(int)
    Q = defaultdict(float)
    for i in range(num_sims):
        attacking_team = state.getTeam(attacking_territory)
        defending_team = state.getTeam(defending_territory)
        simulate(attacking_team, defending_team, state, depth, N, Q, discount)
    return list(Q.keys())[list(Q.values()).index(max(list(Q.values())))][1] # returns action with highest Q value

def getActions(state): # replace with getPossibleAttacks
    return actions

def getValue(state, my_team, opponent):
    BST_my_team_sum = sum(list(BST_Heuristic(my_team, state).values()))
    BST_opponent_sum = sum(list(BST_Heuristic(opponent, state).values()))
    return 100 * BST_opponent_sum / (BST_my_team_sum + BST_opponent_sum)

# issue: state are not going to be re-explored bc of the nondeterminism of
def simulate(my_team, opponent, state, depth, N, Q, discount):
    if depth <= 0: # return current state value estimate
        return getValue(state, my_team, opponent)
    if (state, getActions(state)[0]) not in N: # I think this covers all cases (unexplored, set state action pairs)
        for action in getActions(state):
            N[(state, action)] = 0
            Q[(state, action)] = 0
        return getValue(state, my_team, opponent)
    action = explore(state, N, Q)
    succ = generate_succ_state(state, action)
    reward = getValue(succ, my_team, opponent) - getValue(state, my_team, opponent)
    q = reward + discount * simulate(my_team, opponent, succ, depth - 1, N, Q, discount)
    N[(state, action)] += 1
    Q[(state, action)] += (q - Q[(state, action)]) / N[(state, action)]

def UCB1(state, action, N, Q, c):
    if N[(state, action)] == 0: # if unexplored
        return 10**100
    else: # standard UCB1 exploration heuristic
        Ns = sum(N[(state, a)] for a in getActions(state))
        return Q[(state, action)] + c * ((math.log(Ns) / N[(state, action)])**0.5)

def explore(state, N, Q):
    UCB1s = []
    for action in getActions(state):
        UCBs.append(UCB1(state, action, Q, N, 2**0.5)) # can change c here
    return UCB1s.index(max(UCB1s))

def generate_succ_state(state, action):
    return state