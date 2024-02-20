import gui.gui as gui
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    Gui = gui.GUI(root, "алгоритм k ближайших соседей")
    Gui.read_json()