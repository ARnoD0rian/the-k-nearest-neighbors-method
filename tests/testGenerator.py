import random
import json

def gamilton_generation(number: int)->None:
    N = number
    data = {"num_vertex": N, "vertexes": [], "edges": []}
    coordinate_x = set()
    coordinate_y = set()
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i != j:
                data["edges"].append({"from": i, "to": j, "weight": random.randint(1, 100)})
    k = 0
    while k < N:
        coor = (random.randint(1, 600), random.randint(1, 400))
        if coor[0] in coordinate_x: continue
        if coor[1] in coordinate_y: continue
        coordinate_x.add(coor[0])
        coordinate_y.add(coor[1])
        data["vertexes"].append({"x": coor[0], "y": coor[1]})
        k += 1
        
    
    with open(f"tests/test_{number}.json", "w") as file:
        json.dump(data, file)


def main():
    for i in range(100):
        gamilton_generation(i + 1)

if __name__ == "__main__":
    main()
