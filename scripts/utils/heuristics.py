

def BST_Heuristic(team, risk_map):
    '''
    Calculates the Border Security Threat of all of the countries owned by a team. The BST is the amount of troops in neighboring
    countries (not your team) divided by the amount of troops in your country. The paper, https://project.dke.maastrichtuniversity.nl/games/files/bsc/Hahn_Bsc-paper.pdf, describes the concept of BST in more detail

    Input:
        team: type GameTeam
        risk_map: type GameMap

    Output:
        BST_dict: type dictionary { keys --> names of territories; values --> BST ratings}
    '''

    BST_dict = {}
    for territory in team.getTerritories():
        BST = 0
        neighbors = risk_map.getNeighbors(territory)
        for neighbor in neighbors:
            if risk_map.getTeam(neighbor).getName() != team.getName():
                BST += risk_map.getTroops(neighbor)
        BST_dict[territory] = BST/risk_map.getTroops(territory)
    return BST_dict

def BSR_Heuristic(team, risk_map, opponent = None):
    '''
    Returns normalized version of the Border Securty Threat

    Input:
        team: type GameTeam
        risk_map: type GameMap

    Output:
        BSR_dict: type dictionary { keys --> names of territories; values --> BSR ratings}
    '''
    if opponent is None:
        return 100
        
    BSR_dict = BST_Heuristic(team, risk_map)
    BSR_opp_dict = BST_Heuristic(opponent, risk_map)
    factor=1.0/sum(BSR_dict.values())
    factor2=1.0/sum(BSR_opp_dict.values())
    for country in BSR_dict:
        BSR_dict[country] = BSR_dict[country]*factor
    for country in BSR_opp_dict:
        BSR_opp_dict[country] = BSR_opp_dict[country]*factor2
    BST_my_team_sum = sum(list(BSR_dict.values()))
    BST_opponent_sum = sum(list(BSR_opp_dict.values()))
    r = 100*BST_opponent_sum/(BST_my_team_sum+BST_opponent_sum)
    return r

def Countries_Heuristic(team, risk_map):
    return len(team.getTerritories())

def Troops_Heuritic(team, risk_map):
    return self.team.getTroops()
def EdgeWin(team, game_map, opponent = None):
    """This function takes a game map (i.e. a state) and returns
    the % equity they have in the game

    This one just calculates proportion of edges it would win"""

    edge_win_dict = {}
    for team_name in game_map.teams:
        edge_win_dict[team_name] = 0

    total = 0
    for e in game_map.graph.edges():
        nodeA = game_map.graph.nodes[e[0]]
        nodeB = game_map.graph.nodes[e[1]]
        if nodeA['team'] or nodeB['team']:
            total += 1
            if nodeA['team'] == nodeB['team']:
                edge_win_dict[nodeA['team']] += 1
            elif nodeA['team'] == None or nodeA['num_troops'] < nodeB['num_troops']:
                edge_win_dict[nodeB['team']] += 1
            elif nodeB['team'] == None or nodeB['num_troops'] < nodeA['num_troops']:
                edge_win_dict[nodeA['team']] += 1
            else:
                total -= 1

    if total == 0:
        equity = .5
    else:
        equity = edge_win_dict[team.getName()]/total

    return equity
