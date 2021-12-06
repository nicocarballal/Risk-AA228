from utils.game_map_class import GameMap
from utils.game_team_class import GameTeam
from utils.map_setup_functions import setGameBoardRandom, initializeFullRiskMap
from utils.heuristics import BST_Heuristic, EdgeWin

import networkx as nx
import matplotlib.pyplot as plt

import copy
import math
import random
from collections import defaultdict

def monteCarloTreeSearch(risk_map, team_name, action_type, rollout_strategy, c, depth, discount, num_sims):
    N = defaultdict(int)
    Q = defaultdict(float)
    for i in range(num_sims):
        simulate(risk_map, team_name, action_type, rollout_strategy, N, Q, c, depth, discount)
    actions = getActions(risk_map, team_name, action_type)
    if len(actions) != 0:
        best_action = actions[0]
        for action in getActions(risk_map, team_name, action_type):
            if Q[(risk_map, action)] > Q[(risk_map, best_action)]:
                best_action = action
        return best_action
    else:
        return None

def getValue(risk_map, team_name):
    '''
    Uses EdgeWin approximate evaulation function for now, can also replace with rollout?
    '''
    return 100 * EdgeWin(risk_map.teams[team_name], risk_map)
    # return rollout(risk_map, team_name, action_type, rollout_strategy)

def getActions(risk_map, team_name, action_type):
    if action_type == 'add':
        return risk_map.teams[team_name].getTerritories()
    elif action_type == 'attack': 
        actions = []
        for attacker in risk_map.teams[team_name].getPossibleAttacks(): 
            for defender in risk_map.teams[team_name].getPossibleAttacks()[attacker]:
                actions.append((attacker, defender))
        actions.append(None)
        return actions
    else:
        raise Exception('Not a valid action_type')

# identical to the one in lookahead_rollouts_attack
def compute_succ_state_prob(prob,num_attackers,num_defenders,succ_state_probs):
    """This recursive function run to completion is meant to take prob = 1 and a number of attackers
    and defenders for a battle and update the succ_state_probs dictionary with the possible outcomes mapped
    to their respective probabilities."""
    if num_attackers == 0 or num_attackers == 1 or num_defenders == 0:
        if (num_attackers,num_defenders) in succ_state_probs:
            succ_state_probs[(num_attackers,num_defenders)] += prob
        else:
            succ_state_probs[(num_attackers,num_defenders)] = prob
    if num_attackers == 2 and num_defenders == 1:
        compute_succ_state_prob(prob*5/12,num_attackers, num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*7/12,num_attackers - 1, num_defenders,succ_state_probs)
    if num_attackers == 3 and num_defenders == 1:
        compute_succ_state_prob(prob*125/216,num_attackers,num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*91/216,num_attackers - 1,num_defenders,succ_state_probs)
    if num_attackers > 3 and num_defenders == 1:
        compute_succ_state_prob(prob*95/144,num_attackers, num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*49/144,num_attackers - 1, num_defenders,succ_state_probs)
    if num_attackers == 2 and num_defenders > 1:
        compute_succ_state_prob(prob*55/216,num_attackers, num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*161/216,num_attackers - 1, num_defenders,succ_state_probs)
    if num_attackers == 3 and num_defenders > 1:
        compute_succ_state_prob(prob*295/1296,num_attackers, num_defenders - 2,succ_state_probs)
        compute_succ_state_prob(prob*35/108,num_attackers - 1, num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*581/1296,num_attackers - 2, num_defenders,succ_state_probs)
    if num_attackers > 3 and num_defenders > 1:
        compute_succ_state_prob(prob*1445/3888,num_attackers, num_defenders - 2,succ_state_probs)
        compute_succ_state_prob(prob*2611/7776,num_attackers - 1, num_defenders - 1,succ_state_probs)
        compute_succ_state_prob(prob*2275/7776,num_attackers - 2, num_defenders,succ_state_probs)        

def rollout(risk_map, team_name, action_type, rollout_strategy):
    copy_map = copy.deepcopy(risk_map)
    team = copy_map.teams[team_name]
    for name in copy_map.teams:
        if name != team_name:
            opponent = copy_map.teams[name]
    team.setStrategy(rollout_strategy)
    opponent.setStrategy(rollout_strategy)
    if action_type == 'add':
        while team.hasTeamWon() == False and opponent.hasTeamWon() == False:
            team.playTurn()
            if team.hasTeamWon() == True:
                break
            opponent.playTurn()
    elif action_type == 'attack':
        team.playAttacks()
        while team.hasTeamWon() == False and opponent.hasTeamWon() == False:
            opponent.playTurn()
            if opponent.hasTeamWon() == True:
                break
            team.playTurn()
    else:
        raise Exception('not a valid action_type')
    if team.hasTeamWon():
        return 1
    else:
        return 0
        
def simulate(risk_map, team_name, action_type, rollout_strategy, N, Q, c, depth, discount): 
    '''
    N, Q are dictionaries from (s, a) to N(s, a) and Q(s, a) respectively
    '''
    for name in risk_map.teams:
        if name != team_name:
            opponent = risk_map.teams[name]
    if risk_map.teams[team_name].hasTeamWon():
        return 1000 # not sure about this value
    if opponent.hasTeamWon():
        return -1000 # not sure about this value
    if depth <= 0:
        return getValue(risk_map, team_name) # or can use rollout?
    if (risk_map, getActions(risk_map, team_name, action_type)[0]) not in N: 
        for action in getActions(risk_map, team_name, action_type):
            N[(risk_map, action)] = 0
            Q[(risk_map, action)] = 0
        return getValue(risk_map, team_name) # or can use rollout
    action = explore(risk_map, team_name, action_type, N, Q, c)
    succ_map = generate_succ(risk_map, team_name, action, action_type)
    reward = 0
    reward = getValue(succ_map, team_name) - getValue(risk_map, team_name) # would change to smth related to soldiers, too dependent on the edgeWin heuristic currently
    if action == None:
        q = reward + discount * simulate(succ_map, team_name, 'add', rollout_strategy, N, Q, c, depth - 1, discount)
    else:
        q = reward + discount * simulate(succ_map, team_name, 'attack', rollout_strategy, N, Q, c, depth - 1, discount)
    N[(risk_map, action)] += 1
    Q[(risk_map, action)] += (q - Q[(risk_map, action)]) / N[(risk_map, action)]
    return q
    
def generate_succ(risk_map, team_name, action, action_type): 
    succ_map = copy.deepcopy(risk_map)
    if action_type == 'add':
        num_troops = max(3, len(succ_map.teams[team_name].getTerritories()) // 3 + getContinentBonus(risk_map, team_name))
        succ_map.teams[team_name].addTroops(action, num_troops)
    elif action_type == 'attack': 
        if action != None:
            probs = {}
            compute_succ_state_prob(1, succ_map.getTroops(action[0]), succ_map.getTroops(action[1]), probs)
            rand_val = random.random()
            total = 0
            for succ, prob in probs.items():
                if rand_val <= total:
                    succ_num_attackers, succ_num_defenders = succ
                    succ_map.setNumTroops(action[0], succ_num_attackers)
                    succ_map.setNumTroops(action[1], succ_num_defenders)
                    defending_team = succ_map.getTeam(action[1])
                    if succ_num_defenders == 0:
                        succ_map.setTeam(action[1], team_name)
                        succ_map.teams[team_name].addTerritory(action[1])
                        defending_team.removeTerritory(action[1])
                        succ_map.teams[team_name].moveTroops(action[0], action[1], succ_num_attackers - 1)
        else: # check this
            for name in succ_map.teams:
                if name != team_name:
                    opponent = succ_map.teams[name]
            opponent.playTurn() # issue - None will always be associated with low value, since it transitions to the opponent, needs the depth to see the impact of the opposing turn
    else:
        raise Exception('not a valid action_type')
    return succ_map
                                
def UCB1(risk_map, action, team_name, action_type, N, Q, c):
    '''
    Calculates and returns UCB1 exploration heuristic, pick c to be on the order of the range of reward
    '''
    if N[(risk_map, action)] == 0: 
        return 10**100
    else:
        Ns = sum(N[(risk_map, a)] for a in getActions(risk_map, team_name, action_type))
        return Q[(risk_map, action)] + c * ((math.log(Ns) / N[(risk_map, action)])**0.5)
    
def explore(risk_map, team_name, action_type, N, Q, c):
    '''
    Returns action to explore from the current state using the UCB1 exploration heuristic
    '''
    UCB1s = []
    actions = getActions(risk_map, team_name, action_type)
    for action in actions: # I assume this iterates in order
        UCB1s.append(UCB1(risk_map, action, team_name, action_type, N, Q, c))
    return actions[UCB1s.index(max(UCB1s))]

def getContinentBonus(risk_map, team_name):
        NA = ['Alaska', 'North West Territory', 'Greenland', 'Alberta', 'Ontario', 'Quebec', 'Western United States', 'Eastern United States', 'Central America']
        SA = ['Venezuela', 'Brazil', 'Peru', 'Argentina']
        AF = ['North Africa', 'Egypt', 'Congo', 'East Africa', 'South Africa', 'Madagascar']
        EU = ['Great Britain', 'Iceland', 'Scandinavia', 'Ukraine', 'Northern Europe', 'Western Europe', 'Southern Europe']
        AS = ['Middle East', 'India', 'China', 'Siam', 'Afghanistan', 'Ural', 'Siberia', 'Yakutsk', 'Kamchatka', 'Mongolia', 'Japan', 'Irkutsk']
        AU = ['Indonesia', 'New Guinea', 'Western Australia', 'Eastern Australia']
        continents = [NA, SA, AF, EU, AS, AU] 
        continent_bonuses = [5, 2, 3, 5, 7, 2]
        total_bonus = 0
        for continent, bonus in zip(continents, continent_bonuses): 
            if all([country in risk_map.teams[team_name].getTerritories() for country in continent]):
                total_bonus += bonus
        return total_bonus
                     
    
    