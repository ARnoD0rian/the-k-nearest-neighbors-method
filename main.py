from gui.gui import GUI
from algoritm.modificationSwap import Algoritm as Swap
from algoritm.classic import Algoritm as Clas
from algoritm.classicSwap import Algoritm as ClasSwap
from algoritm.polupationMod import Algoritm as PopMod
from algoritm.populationModSwap import Algoritm as PopModSwap
import tkinter as tk
import json
import os
import time

N = 50

def test(algorithm, filename) -> float:
    total_sum = 0
    with open(f"results/{filename}.txt", "w") as file:
        for i in range(4, N + 1):
            name = f"tests/test_{i}.json"
            with open(name, "r") as json_file:
                data = json.load(json_file)
                algo = algorithm
                algo.init_graph(data["num_vertex"], data["edges"])
                sum_1 = 0
                for edge in algo.search_gamiltonov_cycle():
                    sum_1 += edge["weight"]
                    
                total_sum += sum_1
                file.write(f"{sum_1}\n")
                print(i)
    print(filename)
    return total_sum / (N - 3)

if __name__ == "__main__":
    
    # algoritm = Clas()
    # t_start = time.time()
    # print(test(algoritm, "classic"))
    # t_end = time.time()
    # print(f"classic: {(t_end - t_start) / (N - 3)}")

    # algoritm = Swap()
    # t_start = time.time()
    # print(test(algoritm, "Swap"))
    # t_end = time.time()
    # print(f"Swap: {(t_end - t_start) / (N - 3)}")
    
    # algoritm = ClasSwap()
    # t_start = time.time()
    # print(test(algoritm, "ClasSwap"))
    # t_end = time.time()
    # print(f"clasSwap: {(t_end - t_start) / (N - 3)}")
    
    # algoritm = PopMod()
    # t_start = time.time()
    # print(test(algoritm, "PopMod"))
    # t_end = time.time()
    # print(f"popMod: {(t_end - t_start) / (N - 3)}")
    
    algoritm = PopModSwap()
    t_start = time.time()
    print(test(algoritm, "PopModSwap"))
    t_end = time.time()
    print(f"popModSwap: {(t_end - t_start) / (N - 3)}")
            