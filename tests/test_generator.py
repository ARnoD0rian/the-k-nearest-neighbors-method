import random
import json

N = 10

def gamilton_generation(number: int)->None:
    data = {"num_vertex": N, "vertexes": [], "edges": []}
    isEdges = [[False for _ in range(N)] for _ in range(N)]
    for i in range(N):
        isEdges[i][(i+1) % N] = True
        data["vertexes"].append({"x": random.randint(1, 600), "y": random.randint(1, 400)})
        data["edges"].append({"from": i+1, "to": i+2, "weight": random.randint(1, 100)})
        
    data["edges"][-1]["to"] = 1
    with open(f"tests/test_{number}.json", "w") as file:
        json.dump(data, file)

def main():
    for i in range(N):
        gamilton_generation(i)

if __name__ == "__main__":
    main()
