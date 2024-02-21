import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import queue as q
import random
import copy

NUM_INDIVID = 50

class Algoritm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        self._result = nx.DiGraph()
        
    def init_graph(self, vertex_num: int, edges: list[dict]):
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight = edge["weight"])
            
    def search_gamiltonov_cycle(self) -> list[dict]:
        individs = [Individ(self._graph) for _ in range(NUM_INDIVID)]
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
                    self._way, self._way_long = self.swap_modification(copy.deepcopy(self._way))

                return 

            self._way.append(min_weight_edge)
            lifo.put(self._way[-1]["to"])
    
        return 
    
    def swap_modification(self, way: list[dict]) -> list[dict]:
        way_long = 0
        way_node = [way[0]["from"]]
        for edge in way:
            way_long += edge["weight"]
            way_node.append(edge["to"])
        way_node.pop(-1)
        
        new_way_long = way_long
        way_long = float('inf')
        i_start = 0
        i = 0
        k = 1
        while new_way_long < way_long:
            way_long = new_way_long
            while True:
                test_way_node, test_way, test_way_long = self.swap_vertexes(way_node.copy(), copy.deepcopy(way), way_long, i, k)
                if test_way_long < way_long:
                    way_node = test_way_node.copy()
                    way = test_way.copy()
                    i_start = i
                    break
                i = (i + 1) % len(way_node)
                if i == i_start:
                    k += 1
                    if k == len(way_node): break 
                if test_way_long <= 0: return way, 10**6      
            new_way_long = test_way_long
        
        for i in range(len(way_node)):
            way[i] = {"from": way_node[i], "to": way_node[(i+1) % len(way_node)], "weight": way[i]["weight"]}
            
        return way, way_long
    
            
    def swap_vertexes(self, way_node, way, way_long, index, k = 1) -> tuple[list, list, int]:
        if k == 1:
            index_0 = (index - 1 + len(way_node)) % len(way_node)
            index_1 = index
            index_2 = (index + 1) % len(way_node)
            index_3 = (index + 2) % len(way_node)

            way_long -= way[index_0]["weight"] + way[index_1]["weight"] + way[index_2]["weight"]
            way_node[index_1], way_node[index_2] = way_node[index_2], way_node[index_1]
            way[index_0]["weight"] = self._graph[way_node[index_0]][way_node[index_1]]["weight"]
            way[index_1]["weight"] = self._graph[way_node[index_1]][way_node[index_2]]["weight"]
            way[index_2]["weight"] = self._graph[way_node[index_2]][way_node[index_3]]["weight"]

            way_long += way[index_0]["weight"] + way[index_1]["weight"] + way[index_2]["weight"]
        
        else:
            i_indexs = [
                (index - 1 + len(way_node)) % len(way_node),
                index,
                (index + 1) % len(way_node)
            ]
            k_indexs = [
                (index + k - 1 + len(way_node)) % len(way_node),
                (index + k) % len(way_node),
                (index + k + 1) % len(way_node)  
            ]


            way_long -= sum([way[j]["weight"] for j in i_indexs]) + sum([way[j]["weight"] for j in k_indexs])
            if k == 2: way_long += way[i_indexs[2]]["weight"]
            way_node[i_indexs[1]], way_node[k_indexs[1]] = way_node[k_indexs[1]], way_node[i_indexs[1]]

            for j in range(2):
                way[i_indexs[j]]["weight"] = self._graph[way_node[i_indexs[j]]][way_node[i_indexs[j+1]]]["weight"]
                way[k_indexs[j]]["weight"] = self._graph[way_node[k_indexs[j]]][way_node[k_indexs[j+1]]]["weight"]

            way_long += sum([way[j]["weight"] for j in i_indexs]) + sum([way[j]["weight"] for j in k_indexs])
            if k == 2: way_long -= way[i_indexs[2]]["weight"]
        
        return way_node, way, way_long      
                
            
            