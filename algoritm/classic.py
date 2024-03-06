import networkx as nx
import numpy as np 
import matplotlib.pyplot as plt
import queue as q

class Algoritm:
    def __init__(self) -> None:
        # Инициализация атрибутов графа и результата
        self._graph = nx.DiGraph()  # Ориентированный граф NetworkX для хранения входных данных
        self._result = nx.DiGraph()  # Ориентированный граф NetworkX для хранения результата
        
    def init_graph(self, vertex_num: int, edges: list[dict])->None:
        # Инициализация графа с узлами и ребрами
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])  # Добавление узлов в граф
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight=edge["weight"])  # Добавление ребер с весами
            
    def search_gamiltonov_cycle(self) -> list[dict]:
        # Поиск гамильтонова цикла с помощью алгоритма ближайшего соседа
        lifo = q.LifoQueue()  # LIFO очередь для хранения вершин
        lifo.put(1)  # Начинаем с вершины 1
        visited = dict.fromkeys(self._graph.nodes, False)  # Словарь для отслеживания посещенных вершин
        way = list()  # Список для хранения найденного пути
        
        while not lifo.empty():
            min_weight_edge = {"from": None, "to": None, "weight": float('inf')}  # Минимальное ребро из текущей вершины
            vertex = lifo.get()  # Получаем текущую вершину из очереди
            if visited[vertex]:  # Если вершина уже посещена, пропускаем ее
                continue
            else:
                visited[vertex] = True  # Помечаем вершину как посещенную
            
            for neighbor in self._graph.neighbors(vertex):  # Просматриваем соседей текущей вершины
                weight = self._graph[vertex][neighbor]["weight"]  # Получаем вес ребра до соседней вершины
                if weight < min_weight_edge["weight"] and not visited[neighbor]:  # Если вес меньше минимального и соседняя вершина не посещена
                    min_weight_edge = {"from": vertex, "to": neighbor, "weight": weight}  # Обновляем минимальное ребро
                    
            if min_weight_edge["weight"] == float('inf'):  # Если не найдено подходящего ребра
                if all([visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):  # Если все вершины посещены и есть ребро к начальной вершине
                    way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})  # Добавляем ребро к начальной вершине
                    return way  # Возвращаем найденный путь
                
                return way  # Возвращаем найденный путь
                    
            way.append(min_weight_edge)  # Добавляем минимальное ребро в путь
            lifo.put(way[-1]["to"])  # Помещаем следующую вершину в очередь
        
        return way  # Возвращаем путь (может быть неполным)
