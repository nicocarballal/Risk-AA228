from utils.game_map_class import GameMap
from utils.game_team_class import GameTeam
#from utils.strategy_class import Strategy, RandomStrategy, RuleOfThumbStrategy
from utils.map_setup_functions import setGameBoardRandom, initializeFullRiskMap
from utils.heuristics import BST_Heuristic, EdgeWin

import networkx as nx
import matplotlib.pyplot as plt

import copy

def rollout_lookahead(team,riskMap,d,discount):
    '''Returns the best action according to lookahead with rollouts'''
    return greedy(team,riskMap,d,discount)[0]

def greedy(team,riskMap,d,discount):
    '''Greedily looks through all possible actions and determines the value of each from the current state
    using lookahead with rollouts. Returns action with maximum value and the value itself'''
    possible_attackers = team.getPossibleAttacks()
    print(possible_attackers)
    lookahead_list = []
    for attacker in possible_attackers:
        for defender in possible_attackers[attacker]:
            action = (attacker,defender)
            u = lookahead(discount,riskMap,action,d)
            lookahead_list.append((action,u))
    print(lookahead_list)
    if len(lookahead_list) == 0:
        return (None,None)
    return max(lookahead_list, key = lambda x: x[1])

def lookahead(discount,riskMap,action,d):
    ''' Computes successor states and probabilities of these successor states given the current riskMap

    Then for each of these successor states performs a rollout to get a value that that successor state and
    multiplies it by the probability of that successor state. Takes the sum of those values and multiplies it
    by the discount factor to return the value of that function.
    '''

    # Gets basic information about current state of play
    attacking_territory, defending_territory = action
    num_attackers = riskMap.getTroops(attacking_territory)
    num_defenders = riskMap.getTroops(defending_territory)

    # Computes successor states and transition probabilities
    succ_state_probs = {}
    compute_succ_state_prob(1,num_attackers,num_defenders,succ_state_probs)

    sum_successors = 0
    for succ in succ_state_probs:

        # Sets up successor state
        sp = copy.deepcopy(riskMap)
        # Doing a deepcopy of the riskMap also makes copies of the GameTeams stored within the map in riskMap.teams
        # so we don't have to make another copy
        attacking_team = sp.getTeam(attacking_territory)
        defending_team = sp.getTeam(defending_territory)
        set_up_sp(sp,succ,attacking_team,defending_team,attacking_territory,defending_territory)

        # Gets value of successor state via rollout and multiplies by the transition probability to add to sum
        prob = succ_state_probs[succ]
        sum_successors += prob*rollout(discount,sp,d,attacking_team,defending_team)

    return discount*sum_successors

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

def set_up_sp(sp,succ,attacking_team,defending_team,attacking_territory,defending_territory):
    '''Sets up a successor state'''
    succ_num_attackers, succ_num_defenders = succ

    attacking_team.setTroops(attacking_territory, succ_num_attackers)
    defending_team.setTroops(defending_territory, succ_num_defenders)

    # Do not need to consider succ_num_attackers == 1 because we've already set the number of troops to be 1 above

    if succ_num_defenders == 0:

        # Declare the territory to the attacking team!
        sp.setTeam(defending_territory, attacking_team.name)
        # Assign the territory to the attacking team
        attacking_team.addTerritory(defending_territory)
        defending_team.removeTerritory(defending_territory)

        # Move all but one remaining attacking troops to the territory
        attacking_team.moveTroops(attacking_territory, defending_territory, succ_num_attackers - 1)

def rollout(discount,sp,d,my_team,opponent):
    '''Rolls out using a stochastic policy (this is encoded in the strategy of my_team itself) against player.
    Repeats rounds of turns to depth. If my_team wins, the reward is 100. If the opponent wins, the reward is 0.
    Otherwise, at the end of the rollout, we use the BST heuristic for both teams and the reward. We see what percentage
    of BTS between the two teams is attributed to the opponent (would be good for my_team) and use that as the reward'''
    ret = 0
    end_reached = False
    for t in range(d):
        if my_team.hasTeamWon():
            r = 100
            return (discount**t)*r
        opponent.playTurn()
        if opponent.hasTeamWon():
            r = -1
            return (discount**t)*r
        my_team.playTurn()
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
