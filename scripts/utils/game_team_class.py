import networkx as nx
import random
import numpy as np

class GameTeam:
    '''
    Initializes a game team using the following inputs:
                team_name: type str --> name of team 
                risk_map: type GameMap --> initialized through call to GameMap()

           This results in the following member attributes:
               name: name of team
               territories: list of names of the territories a team owns
               risk_map: the map that you are playing on
               troops: number of troops owned by a team
               continents_owned: which continents a team owns
               cards: if we implement cards, the cars that a team owns
                 
    '''
    
    def __init__(self, team_name, risk_map, strategy = None, territories = [], num_troops = 0, continents_owned = None, cards = None):
        self.name = team_name
        self.territories = territories
        self.continents_owned = continents_owned
        self.troops = num_troops
        self.cards = cards
        self.risk_map = risk_map
        if strategy == None:            
            self.strategy = Strategy(self)
        else:         
            self.strategy = strategy(self)
        
    def getName(self):
        return self.name 
    
    def getTerritories(self):
        return self.territories
    
    def addTerritory(self, territory):
        self.territories.append(territory)
        
    def getContinentsOwned(self):
        return self.continents_owned
    
    def addContinentsOwned(self, continent):
        self.continents_owned.append(continent)
          
    def getTroops(self):
        return self.troops

    def addTroops(self, block, troops):
        self.troops += troops
        self.risk_map.addTroops(block, troops)
    
    def getStrategy(self):
        return self.strategy
    
    def changeStrategy(self, strategy):
        self.strategy = strategy
        
    def getRiskMap(self):
        return self.risk_map
        
    def getPossibleAttacks(self):
        possibleAttacks = {}
        for territory in self.territories:
            if self.risk_map.getTroops(territory) == 1:
                continue
            neighbors = self.risk_map.getNeighbors(territory)
            for neighbor in neighbors:
                if self.risk_map.getTeam(neighbor) != self.name:
                    possibleAttacks[territory] = neighbor
        return possibleAttacks 
    
    def playTurn(self):
        return self.strategy.playTurn()

    def getNextMove(self):
        return self.strategy.getNextMove()
    
  
    def makeNextMove(self):
        next_move = self.getNextMove()
        print(next_move)
        
        return self.simNextMove(next_move[0], next_move[1])
        
    
    def simNextMove(self, attacking_territory, defending_territory):
        
        defending_team = self.risk_map.getTeam(defending_territory)
        
        attacking_troops = self.risk_map.getTroops(attacking_territory)
        defending_troops = self.risk_map.getTroops(defending_territory)
        
        prev_attacking_troops = attacking_troops
        prev_defending_troops = defending_troops
     
        # Play out the turn until someone wins or loses (no stopping)
        while attacking_troops != 1 and defending_troops != 0:
            attackers = min(attacking_troops - 1, 3)
            defenders = min(defending_troops, 2)
            
            attacking_dice = random.sample(range(1, 7), attackers)
            defending_dice = random.sample(range(1, 7), defenders)
            
            attacking_dice.sort(reverse = True)
            defending_dice.sort(reverse = True)
            
            min_dice = min(attackers, defenders)
            
            results = np.array(attacking_dice)[:min_dice] > np.array(defending_dice)[:min_dice]

            attacking_win = np.sum(results)
            defending_win = len(results) - attacking_win
            
            attacking_troops -= defending_win
            defending_troops -= attacking_win
            
            print("Attacking_dice: ", attacking_dice)
            print("Defending_dice: ", defending_dice)
            print(results)
            print("Attacking Troops Left: ", attacking_troops)
            print("Defending Troops Left: ", defending_troops)
        # Attacking territory will always remain with 1 troop in this setup since they will always
        # move all of their troops but 1 in this set-up or they will lose all but 1 of their troops
        self.risk_map.setNumTroops(attacking_territory, 1)
        if attacking_troops == 1:
            # Defending team is left with how many troops they lost during fighting in their territory
            defending_team.addTroops(defending_territory, -prev_defending_troops+defending_troops)
        elif defending_troops == 0:
            # Delete defending team troops from territory
            defending_team.addTroops(defending_territory, -prev_defending_troops)
            # Declare the territory to the attacking team! 
            self.risk_map.setTeam(defending_territory, self)
            # Add all but one remaining attacking troops to the territory
            self.addTroops(defending_territory, attacking_troops - 1)