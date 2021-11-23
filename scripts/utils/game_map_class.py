import networkx as nx

class GameMap:
    def __init__(self, blocks, edges):
        '''Initializes a game map using the following inputs:
                blocks: a dict that maps from a block name string (such as North America) to a tuple of (the color
                        assigned to that block, a list of block member strings (such as USA)
                edges: a list of tuples of block member strings that are to be connected
                teams: a dict of team_names to GameTeams playing the game

           This results in the following member attributes:
               blocks: as described above
               teams: as described above
               graph: an undirected graph with the following characteristics:
                    nodes: as per nx.Graph
                    Each node has the following attributes:
                        block: a string describing which block the node belongs to
                        team: a string describing which team occupies it. None if no team occupies it
                        num_troops: the number of troops that occupy it
                    edges: as per nx.Graph
               team_color_map: keeps an array of which team owns which node'''
        self.blocks = blocks
        self.graph = nx.Graph()
        self.teams = teams
        for b in blocks.keys():
            for node in blocks[b][1]:
                self.graph.add_node(node,block=b,team=None,num_troops=0)
                self.graph.nodes[node]['neighbors'] = []

        for edge in edges:
            self.graph.add_edge(edge[0],edge[1])
            self.graph.nodes[edge[0]]['neighbors'].append(edge[1])
            self.graph.nodes[edge[1]]['neighbors'].append(edge[0])

    def increment_turn_stage(self):
        if self.curr_stage == "add_troops":
            self.curr_stage = "attack"
        else:
            self.curr_stage = "add_troops"
            self.curr_team_i += 1
            if self.curr_team_i >= len(self.teams):
                self.curr_team_i = 0

    def setTeam(self,node,team_name):
        """Takes in string for TEAM NAME (not GameTeam itself)"""
        if team_name not in self.teams:
            raise Exception("That team name is not corresponded to any team in this GameMap")
        self.graph.nodes[node]['team'] = team_name

    def getTeam(self, node):
        team_name = self.graph.nodes[node]['team']
        return self.teams[team_name]

    def setNumTroops(self,node,new_num):
        self.graph.nodes[node]['num_troops'] = new_num

    def getTroops(self, node):
        return self.graph.nodes[node]['num_troops']

    def addTroops(self,node,num_add_troops):
        self.graph.nodes[node]['num_troops'] += num_add_troops

    def zeroTroops(self,node,new_num):
        self.graph.nodes[node]['num_troops'] = 0

    def getTerritories(self):
        territories_by_continent = [v[1] for v in self.blocks.values()]
        country_list = [country for continent in territories_by_continent for country in continent]
        return country_list

    def getNeighbors(self, node):
        return self.graph.nodes[node]['neighbors']

    def getTeamColorMap(self):
        territories = self.getTerritories()
        color_map = []
        for territory in territories:
            if self.getTeam(territory).getName() == 'red':
                color_map.append('red')
            elif self.getTeam(territory).getName() == 'blue':
                color_map.append('blue')
            else:
                color_map.append('green')
        return color_map
