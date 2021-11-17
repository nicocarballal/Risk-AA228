

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
            if risk_map.getTeam(neighbor) != team.getName():
                BST += risk_map.getTroops(neighbor)
        BST_dict[territory] = BST_dict/risk_map.getTroops(territory)
    return BST_dict

def BSR_Heuristic(team, risk_map):
    '''
    Returns normalized version of the Border Securty Threat

    Input:
        team: type GameTeam
        risk_map: type GameMap

    Output:
        BSR_dict: type dictionary { keys --> names of territories; values --> BSR ratings}
    '''
    BSR_dict = BST_Heuristic(team, risk_map)
    factor=1.0/sum(BSR_dict.itervalues())
    for country in BSR_dict:
        BSR_dict[country] = BSR_dict[country]*factor
    return BSR_dict
