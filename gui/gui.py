import tkinter as tk
from tkinter import ttk
import json

class GUI:
    def __init__(self, root: tk.Tk, title: str) -> None:
        
        #parametres
        
        self._vertex_num = 0
        self._edge_num = 0
        
        self._edge = list()
        self._vertex = list()
        
        #interface 
    
        self.root = root
        self.root.title(title)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(side=tk.LEFT)
        
        self.tree = ttk.Treeview(self.root, columns=('From', 'To', 'Weight'), show='headings')
        self.tree.heading('From', text='From')
        self.tree.heading('To', text='To')
        self.tree.heading('Weight', text='Weight')
        self.tree.pack()
        
        self.from_label = ttk.Label(self.root, text="From:")
        self.from_label.pack()
        self.from_entry = ttk.Entry(self.root)
        self.from_entry.pack()
        
        self.to_label = ttk.Label(self.root, text="To:")
        self.to_label.pack()
        self.to_entry = ttk.Entry(self.root)
        self.to_entry.pack()
        
        self.weight_label = ttk.Label(self.root, text="Weight:")
        self.weight_label.pack()
        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.pack()
        
        self.add_button = ttk.Button(self.root, text="Add Edge", command=self.add_edge)
        self.add_button.pack()
        
        self.canvas.bind("<Button-1>", self.add_vertex)

        self.root.mainloop()

    def add_vertex(self, event) -> None:
        x, y = event.x, event.y
        self._vertex_num += 1
        
        self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='green')
        self.canvas.create_text(x, y, text=str(self._vertex_num), fill='white') 
        
        self._vertex.append((x, y))
        if self._vertex_num == 6: self.read_json()
    
    def add_edge(self) -> None:
        from_vertex = int(self.from_entry.get())
        to_vertex = int(self.to_entry.get())
        weight = int(self.weight_entry.get())
        
        if from_vertex > 0 and from_vertex < self._vertex_num and to_vertex > 0 and to_vertex < self._vertex_num:
            self.draw_edge(from_vertex, to_vertex, weight)
        else:
            return
        
    def draw_edge(self, from_vertex, to_vertex, weight):
            self.tree.insert('', 'end', values=(from_vertex, to_vertex, weight))
            self._edge.append({"from": from_vertex, "to": to_vertex, "weight": weight})
            self._edge_num += 1
            
            from_x, from_y = self.get_vertex_coordinates(from_vertex)
            to_x, to_y = self.get_vertex_coordinates(to_vertex)
            
            to_x, to_y = self.get_coordinate_edge(from_x, from_y, to_x, to_y)

            line = self.canvas.create_line(from_x, from_y, to_x, to_y, width=2, fill= 'red' if from_vertex < to_vertex else 'blue', arrow='last', tag = 'line')
            self.canvas.create_text((to_x + from_x) / 2 + 5, (to_y + from_y) / 2 + 5, text=str(weight), fill='red' if from_vertex < to_vertex else 'blue')
            self.canvas.tag_lower(line)
            
        
    
    def get_vertex_coordinates(self, vertex: int) -> tuple:
                    return self._vertex[vertex - 1]
           
    def get_coordinate_edge(self, x_1, y_1, x_2, y_2, r = 10) -> tuple:
        k = (y_2-y_1) / (x_2 - x_1)
        d = (x_2 + k**2 * x_1 + k *(y_2 - y_1))**2 - (k** 2 + 1) * (x_2**2 + (k*x_1)**2 + 2*k*x_1*(y_2-y_1) + (y_2-y_1)**2 - r**2)
        
        x = (x_2 + k**2 * x_1 + k *(y_2 - y_1) - d**0.5) / (k**2 + 1)
        y = (x - x_1) * k + y_1
        o_1 = (x, y)
        
        x = (x_2 + k**2 * x_1 + k *(y_2 - y_1) + d**0.5) / (k**2 + 1)
        y = (x - x_1) * k + y_1
        o_2 = (x, y)
        
        return o_1 if (x_1 - o_1[0])**2 + (y_1 - o_1[1]) ** 2 < (x_1 - o_2[0])**2 + (y_1 - o_2[1]) ** 2 else o_2
    
    def read_json(self, name = "data/data.json"):
        with open(f"{name}", 'r') as file:
            data = json.load(file)
            if data["num_vertex"] > self._vertex_num: return
            
            for i in range(len(data["edges"])):
                edge = data["edges"][i]
                self._edge.append(edge)
                self.draw_edge(edge["from"], edge["to"], edge["weight"])
                
                
    
    @property
    def edge(self):
        return self._edge
    
    @property
    def vartex(self):
        return self._vertex
    

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root, "алгоритм k ближайших соседей")
    
