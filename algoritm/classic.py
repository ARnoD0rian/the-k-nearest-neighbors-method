import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import queue as q


class Algoritm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        self._result = nx.DiGraph()
        
    def init_graph(self, vertex_num: int, edges: list[dict]):
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight = edge["weight"])
            
    def search_gamiltonov_cycle(self) -> list[dict]:
        lifo = q.LifoQueue()
        lifo.put(1)
        visited = dict.fromkeys(self._graph.nodes, False)
        way = list()
        
        while not lifo.empty():
            min_weight_edge = {"from": None, "to": None, "weight": float('inf')}
            vertex = lifo.get()
            if visited[vertex]: continue
            else: visited[vertex] = True
            
            for neighbor in self._graph.neighbors(vertex):
                weight = self._graph[vertex][neighbor]["weight"]
                if weight < min_weight_edge["weight"] and not visited[neighbor]: 
                    min_weight_edge = {"from": vertex, "to": neighbor, "weight": weight}
            if min_weight_edge["weight"] == float('inf'):
                
                if all([visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):
                    way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})
                    return way
                
                return way
                    
            way.append(min_weight_edge)
            lifo.put(way[-1]["to"])
        
        return way
            
                
                
            
            