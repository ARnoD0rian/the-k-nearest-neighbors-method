import networkx as nx
import copy
import random


class Algoritm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        self._result = nx.DiGraph()
        
    def init_graph(self, vertex_num: int, edges: list[dict]):
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight = edge["weight"])
            
    def search_gamiltonov_cycle(self) -> list[dict]:
        way = list()
        way_long = 0
        
        way_node = list(self._graph.nodes)
        for i in range(len(way_node) - 1):
            way.append({"from": i + 1, "to": i + 2, "weight": self._graph[i+1][i+2]["weight"]})
        
        way.append({"from": len(way_node), "to": 1, "weight": self._graph[len(way_node)][1]["weight"]})
        for edge in way: way_long += edge["weight"]
        
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
                # if test_way_long <= 0: print("pizda")        
            new_way_long = test_way_long
        
        for i in range(len(way_node)):
            way[i] = {"from": way_node[i], "to": way_node[(i+1) % len(way_node)], "weight": way[i]["weight"]}
            
        return way
            
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
        