import networkx as nx

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
    
    def __init__(self, team_name, risk_map, territories = [], num_troops = 0, continents_owned = None, cards = None):
        self.name = team_name
        self.territories = territories
        self.continents_owned = continents_owned
        self.troops = num_troops
        self.cards = cards
        self.risk_map = risk_map
        
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
    