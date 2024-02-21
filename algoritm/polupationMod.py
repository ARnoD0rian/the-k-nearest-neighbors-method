import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import queue as q
import random
import copy

NUM_INDIVID = 200

class Algoritm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        self._result = nx.DiGraph()
        
    def init_graph(self, vertex_num: int, edges: list[dict]):
        self._graph.add_nodes_from([(x+1) for x in range(NUM_INDIVID)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight = edge["weight"])
            
    def search_gamiltonov_cycle(self) -> list[dict]:
        individs = [Individ(self._graph) for _ in range(len(list(self._graph.nodes)))]
        for i in range(len(individs)): individs[i].algoritm()
        best_individ = min(individs, key= lambda ind: ind.way_long)
        return best_individ.way
            
class Individ:
    def __init__(self, graph: nx.DiGraph) -> None:
        self._graph = graph
        self._visited = dict.fromkeys(graph.nodes, False)
        self._way_node = list()
        self._way_long = 0
        self._way = list()
        
    @property
    def visited(self):
        return self._visited
    
    @property
    def way_node(self):
        return self._way_node
    
    @property
    def way_long(self):
        return self._way_long
    
    @property
    def way(self):
        return self._way
    
    def algoritm(self):
        lifo = q.LifoQueue()
        lifo.put(1)
        while not lifo.empty():
            min_weight_edge = {"from": None, "to": None, "weight": float('inf')}
            vertex = lifo.get()
            if self._visited[vertex]: continue
            else: self._visited[vertex] = True

            neighbors = []
            rand_coefficient = []
            for neighbor in self._graph.neighbors(vertex):
                if not self._visited[neighbor]:
                    neighbors.append((neighbor, self._graph[vertex][neighbor]["weight"]))
                    rand_coefficient.append(1 / neighbors[-1][1])
                    
            if len(neighbors) > 0:
                new_vertex = random.choices(neighbors, rand_coefficient)[0]
                min_weight_edge = {"from": vertex, "to": new_vertex[0], "weight": new_vertex[1]}
                self._way_long += new_vertex[1]
                
            if min_weight_edge["weight"] == float('inf'):

                if all([self._visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):
                    self._way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})
                    self._way_long += self._graph[vertex][1]["weight"]

                return 

            self._way.append(min_weight_edge)
            lifo.put(self._way[-1]["to"])
    
        return    
                
            
            