import networkx as nx

def initialize_graph(blocks, edges):
        '''Inputs:
                blocks: a dict that maps from a block name string (such as North America) to a tuple of (the color
                        assigned to that block, a list of block member strings (such as USA)
                edges: a list of tuples of block member strings that are to be connected

           Returns an undirected graph with the following characteristics:
            The graph itself has:
                nodes: as per nx.Graph
                edges: as per nx.Graph
                block_dict: stores blocks from input
            Each node has the following attributes:
                block: a string describing which block the node belongs to
                team: a string describing which team occupies it. None if no team occupies it
                num_troops: the number of troops that occupy it'''
    graph = nx.Graph(block_dict=blocks)
    for b in blocks.keys():
        for node in blocks[b][1]:
            graph.add_node(node,block=b,team=None,num_troops=0)

    for edge in edges:
        graph.add_edge(edge[0],edge[1])
    return graph


def setTeam(graph,node,team):
    graph.nodes[node]['team'] = team

def setNumTroops(graph,node,new_num):
    graph.nodes[node]['num_troops'] = newNum

def addTroops(graph,node,num_add_troops):
    graph.nodes[node]['num_troops'] += num_add_troops

def zeroTroops(graph,node,new_num):
    graph.nodes[node]['num_troops'] = 0


