from utils.game_team_class import GameTeam
import random

class Strategy:
    '''
    Initializes a game player using the following inputs:
                team_name: type str --> name of team 
                game_team: type GameTeam --> initializez through call to GameTeam()
                risk_map: type GameMap --> initialized through call to GameMap()
                strategy_type: type str --> name of desired strategy

           This results in the following member attributes:
               name: name of team
               team: GameTeam
               risk_map: GameMap
               strategy: Strategy
                 
    '''
    
    def __init__(self, game_team):
        self.game_team = game_team 
        
    def getTeamName(self):
        '''
        Return team name for given strategy 
        '''
        return self.game_team.getName()
    
    def getGameTeam(self):
        '''
        Return the team the given strategy will return for.
        '''
        return self.game_team
    
    def getPossibleAttacks(self):
        '''
        Get all of the possible attacks for your team at a given map state.
        This same function is in GameTeam as well (will probably want to delete
        one at some point)
        
        Outputs: 
        - possibleAttacks: Dict
                    Keys --> Possible attacking country names (strings)
                    Values --> Possible target country names (strings)
        '''
        possibleAttacks = {}
        for territory in self.game_team.getTerritories():
            if self.game_team.getRiskMap().getTroops(territory) == 1:
                continue
            neighbors = self.game_team.getRiskMap().getNeighbors(territory)
            attacksFromTerritory = []
            for neighbor in neighbors:
                if self.game_team.getRiskMap().getTeam(neighbor).getName() != self.game_team.getName():
                    attacksFromTerritory.append(neighbor)
            if len(attacksFromTerritory) > 0:
                possibleAttacks[territory] = attacksFromTerritory
        return possibleAttacks 

    def getNextMove(self):
        '''
        Get the next move for a given strategy
        Outputs:
        next_move --> strings in a tuple of (attacking_country, defending_country)
        '''
        raise Exception('Use subclass of strategy for getting next move')
    
    def addTroopsTurn(self, num_troops):
        '''
        Adds troops according to your policy's strategy!
        Inputs:
        num_troops --> Number of troops you have available to you to add
        '''
        raise Exception('Use subclass of strategy for adding toops')
    
    def playTurn():
        '''
        Play out a turn according to your strategy
        '''
        raise Exception('Use subclass of strategy for playing turn')
        
    


class RandomStrategy(Strategy):
    '''
    This strategy picks moves and adds troops at random! It's as simple as that :) 
    '''
    def __init__(self, game_team):
        super().__init__(game_team)
       
    def getNextMove(self):
        possibleAttacks = self.getPossibleAttacks()
        if len(possibleAttacks) == 0:
            return None
        attackingTerritoryPossibleAttacks = random.choice(list(possibleAttacks.items()))
        print(attackingTerritoryPossibleAttacks)
        return (attackingTerritoryPossibleAttacks[0], random.choice(attackingTerritoryPossibleAttacks[1]))
    
    def addTroopsTurn(self, num_troops):
        for _ in range(num_troops):
            territory = random.choice(self.game_team.getTerritories())
            self.game_team.addTroops(territory, 1)
            print("Adding {num_troops} to {territory}!".format(num_troops = 1, territory = territory))
    def playTurn(self):
        self.addTroopsTurn(max(3, len(self.game_team.getTerritories()) // 3))
        
        nextMove = self.getNextMove()
        possibleAttacks = self.game_team.getPossibleAttacks()
        i = 0
        while nextMove != None and i <= len(possibleAttacks)/2:
            self.game_team.makeMove(nextMove)
            nextMove = self.getNextMove()
            i += 1
            
class RuleOfThumbStrategy(Strategy):
    '''
    This strategy picks the moves in which you have more troops than the opponent
    '''
    def __init__(self, game_team):
        super().__init__(game_team)
       
    def getNextMove(self):
        possibleAttacks = list(self.getPossibleAttacks().items())
        if len(possibleAttacks) == 0:
            return None
        random.shuffle(possibleAttacks)
        best_diff = -float('inf')
        for territoryAttacks in possibleAttacks:
            attacker = territoryAttacks[0]
            random.shuffle(territoryAttacks[1])
            for defender in territoryAttacks[1]:
                attacker_name = attacker
                defender_name = defender
                troop_diff = self.game_team.getRiskMap().getTroops(attacker_name) - self.game_team.getRiskMap().getTroops(defender_name)
                if troop_diff > best_diff:
                    best_attack = attacker_name
                    best_defense = defender_name
                    best_diff = troop_diff
        if best_diff <= 0:
            return None
        return (best_attack, best_defense)

    
    def addTroopsTurn(self, num_troops):
        possibleAttacks = self.getPossibleAttacks()
        neighborDict = {key: len(value) for key, value in possibleAttacks.items()}
        most_neighbors = list({k: v for k, v in sorted(neighborDict.items(), key=lambda item: item[1], reverse = True)}.items())
        
        if len(possibleAttacks) == 0:
            territories = self.game_team.getTerritories()
            territories_to_neighbors_dict = {}
            for territory in territories:
                n = 0
                for neighbor in self.game_team.getRiskMap().getNeighbors(territory):
                    if self.game_team.getRiskMap().getTeam(neighbor).getName() != self.getTeamName():
                        n += 1
                territories_to_neighbors_dict[territory] = n         
            territory = list({k: v for k, v in sorted(territories_to_neighbors_dict.items(), key=lambda item: item[1], reverse = True)}.items())
            territory = territory[0]
            print("Adding {num_troops} to {territory}!".format(num_troops = num_troops, territory = territory[0]))           
            self.game_team.addTroops(territory[0], num_troops)
            return
        else:
            territory = most_neighbors[0]
            print("Adding {num_troops} to {territory}!".format(num_troops = num_troops, territory = territory[0]))
            self.game_team.addTroops(territory[0], num_troops)
            return

            
    def playTurn(self):
        self.addTroopsTurn(max(3, len(self.game_team.getTerritories()) // 3)) # Default for RISK
        
        nextMove = self.getNextMove()
        possibleAttacks = self.game_team.getPossibleAttacks()
        i = 0

        while nextMove != None:
            self.game_team.makeMove(nextMove)
            nextMove = self.getNextMove()
            i += 1
            
            
        
        