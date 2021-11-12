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
            for neighbor in neighbors:
                if self.game_team.getRiskMap().getTeam(neighbor) != self.game_team.getName():
                    possibleAttacks[territory] = neighbor
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
        
    def playTurn(self):
        self.addTroopsTurn(3) # Default for RISK
        
        nextMove = self.getNextMove()
        possibleAttacks = self.game_team.getPossibleAttacks()
        i = 0
        while nextMove != None and i <= len(possibleAttacks)/2:
            self.game_team.makeMove(nextMove)
            nextMove = self.getNextMove()
            i += 1


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
        return random.choice(list(possibleAttacks.items()))
    
    def addTroopsTurn(self, num_troops):
        for _ in range(num_troops):
            territory = random.choice(self.game_team.getTerritories())
            self.game_team.addTroops(territory, 1)
            
        
        