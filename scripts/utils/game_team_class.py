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
            self.strategy = None
        else:
            self.strategy = strategy(self)
        self.risk_map.teams[team_name] = self

    def setStrategy(self,strategy_class):
        self.strategy = strategy_class(self)

    def getName(self):
        return self.name

    def getTerritories(self):
        return self.territories

    def addTerritory(self, territory):
        self.territories.append(territory)

    def removeTerritory(self, territory):
        self.territories.remove(territory)

    def getContinentsOwned(self):
        return self.continents_owned

    def addContinentsOwned(self, continent):
        self.continents_owned.append(continent)

    def getTroops(self):
        return self.troops

    def addTroops(self, country, troops):
        '''
        Adds a certain number of troops to a given territory on the map and adds the same number
        of troops to your team

        Inputs:
        country --> name of country to add troops to
        troops --> number of troops to add (this number can be negative if you want to subtract troops)
        '''
        if (self.risk_map.getTroops(country)+troops)<0:
            raise Exception("Resulting number of troops cannot be negative")
        self.troops += troops
        self.risk_map.addTroops(country, troops)

    def setTroops(self, country, troops):
        '''
        Set a certain number of troops for a given territory and adds the difference
        between this number and the number currently there to your teams numTroops
        '''
        if troops < 0:
            raise Exception("cannot have negative number of troops")
        self.troops += (troops - self.risk_map.getTroops(country))
        self.risk_map.setNumTroops(country,troops)

    def moveTroops(self, from_territory, to_territory, numTroops):
        if from_territory in self.getTerritories() and to_territory in self.getTerritories():
            self.addTroops(from_territory, -numTroops)
            self.addTroops(to_territory, numTroops)
        else:
            raise Exception("Only can moveTroops within your own territory, assign territories first")

    def getStrategy(self):
        '''
        Return your strategy
        Outputs:
        - Returns an instance of the strategy class according to your team
        '''
        return self.strategy


    def changeStrategy(self, StrategyClass):
        '''
        Change your teams strategy at any given time!

        Inputs:
        - StrategyClass --> Will need to pass the Strategy class like so "self.changeStrategy(RandomStrategy)
        '''
        self.strategy = StrategyClass(self)

    def getRiskMap(self):
        return self.risk_map

    def getPossibleAttacks(self):
        '''
        This same function is in Strategy Class as well (will probably want to delete
        one at some point)


        Outputs:
        - possibleAttacks: Dict
                    Keys --> Possible attacking country names (strings)
                    Values --> Possible target country names (strings)
        '''
        possibleAttacks = {}
        for territory in self.territories:
            if self.risk_map.getTroops(territory) == 1:
                continue
            neighbors = self.risk_map.getNeighbors(territory)
            attacksFromTerritory = []
            for neighbor in neighbors:
                if self.risk_map.getTeam(neighbor).getName() != self.name:
                    attacksFromTerritory.append(neighbor)
            if len(attacksFromTerritory) > 0:
                possibleAttacks[territory] = attacksFromTerritory
        return possibleAttacks

    def playAddTroops(self):
        '''
        Play out adding troops according to your strategy_type
        '''
        return self.strategy.playAddTroops()

    def playAttacks(self):
        '''
        Play out attacks according to your strategy_type
        '''
        return self.strategy.playAttacks()

    def playTurn(self):
        '''
        Play a turn according to your strategy
        '''
        return self.strategy.playTurn()

    def getNextMove(self):
        return self.strategy.getNextMove()


    def determineAndMakeMove(self):
        '''
        Make a move according to your strategy
        '''
        next_move = self.getNextMove()

        if next_move == None:
            return

        return self.simNextMove(next_move[0], next_move[1])

    def hasTeamWon(self):
        return len(self.getTerritories()) == len(self.getRiskMap().getTerritories())

    def makeMove(self, next_move):
        '''
        Make a move according to next_move

        Inputs:
        next_move --> type tuple - (str "attacking territory", str "defending territory")


        '''
        print(next_move)

        return self.simNextMove(next_move[0], next_move[1])



    def simNextMove(self, attacking_territory, defending_territory):
        '''
        Simulate the next move from the attacking territory to the defending territory

        Inputs:
        attacking_territory --> type str - name of attacking territory
        defending_territory --> type str - name of defending territory
        '''

        defending_team = self.risk_map.getTeam(defending_territory)
        print("Team {team1} declares attack on Team {team2} from {attacker} to {defender}".format(team1 = self.getName(), team2 = defending_team.getName(), attacker = attacking_territory, defender = defending_territory))

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
            self.risk_map.setTeam(defending_territory, self.name)
            # Assign the territory to the attacking team
            self.addTerritory(defending_territory)
            defending_team.removeTerritory(defending_territory)
            # Add all but one remaining attacking troops to the territory
            self.addTroops(defending_territory, attacking_troops - 1)
