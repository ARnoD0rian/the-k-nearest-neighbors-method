import networkx as nx

# Создаем ориентированный граф
G = nx.DiGraph()
G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])

# Генерируем гамильтонов цикл
hamiltonian_cycle = list(nx.hamiltonian_cycle(G))

print("Гамильтонов цикл:", hamiltonian_cycle)
