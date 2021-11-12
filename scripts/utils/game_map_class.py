import networkx as nx

class GameMap:
    def __init__(self, blocks, edges):
        '''Initializes a game map using the following inputs:
                blocks: a dict that maps from a block name string (such as North America) to a tuple of (the color
                        assigned to that block, a list of block member strings (such as USA)
                edges: a list of tuples of block member strings that are to be connected

           This results in the following member attributes:
               blocks: as described above
               graph: an undirected graph with the following characteristics:
                    nodes: as per nx.Graph
                    Each node has the following attributes:
                        block: a string describing which block the node belongs to
                        team: a string describing which team occupies it. None if no team occupies it
                        num_troops: the number of troops that occupy it
                    edges: as per nx.Graph'''
        self.blocks = blocks
        self.graph = nx.Graph()
        for b in blocks.keys():
            for node in blocks[b][1]:
                self.graph.add_node(node,block=b,team=None,num_troops=0)
                self.graph.nodes[node]['neighbors'] = []

        for edge in edges:
            self.graph.add_edge(edge[0],edge[1])
            self.graph.nodes[edge[0]]['neighbors'].append(edge[1])
            self.graph.nodes[edge[1]]['neighbors'].append(edge[0])

    def setTeam(self,node,team):
        self.graph.nodes[node]['team'] = team
    
    def getTeam(self, node):
        return self.graph.nodes[node]['team']

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
    
    
            
            
            
            
            
            
        
            