import time
import queue
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import pyautogui

currentGraph = 'bfs'  # Declare currentGraph as a global variable

def dfs():
    global currentGraph
    currentGraph = 'dfs'
    update_visualization()

def bfs():
    global currentGraph
    currentGraph = 'bfs'
    update_visualization()

def update_visualization():
    if currentGraph == 'bfs':
        visualize_Search(order_bfs(G, 'A', 'J'), 'BFS Visualization', G, pos, 1, root)
    elif currentGraph == 'dfs':
        visualize_Search(order_dfs(G, 'A', 'G'), 'DFS Visualization', G, pos, 1, root)

def order_bfs(graph, start_node, destination_node):
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []

    while not q.empty():
        vertex = q.get()

        if vertex == destination_node:
            # Stop the traversal if the destination node is reached
            order.append(vertex)
            break

        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node)

    return order

def order_dfs(graph, start_node, destination_node, visited=None):
    if visited is None:
        visited = set()
    order = []

    if start_node == destination_node:
        # Stop the traversal if the destination node is reached
        order.append(start_node)
        pyautogui.alert(order)
        return order

    if start_node not in visited:
        order.append(start_node)
        visited.add(start_node)

        for node in graph[start_node]:
            if node not in visited:
                order.extend(order_dfs(graph, node, destination_node, visited))
                
                # Check if the destination node is reached after the recursive call
                if destination_node in order:
                    return order
    return order

def visualize_Search(order, title, G, pos, speed, root):
    fig = plt.figure()
    plt.title(title)
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    current_step = 0

    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}  # Create edge labels

    def show_state(step):
        node = order[step]
        plt.clf()
        plt.title(title)
        nx.draw(G, pos, with_labels=True, node_color=['r' if n == node else 'c' for n in G.nodes])
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Draw edge labels
        canvas.draw()

    def next_step():
        nonlocal current_step
        if current_step < len(order) - 1:
            current_step += 1
            show_state(current_step)

    def prev_step():
        nonlocal current_step
        if current_step > 0:
            current_step -= 1
            show_state(current_step)

    def auto_play():
        nonlocal current_step
        while current_step < len(order) - 1:
            current_step += 1
            show_state(current_step)
            root.update()
            time.sleep(speed)

    # Clear previous canvas if it exists
    for widget in root.winfo_children():
        if isinstance(widget, tk.Widget) and widget.winfo_ismapped():
            widget.pack_forget()

    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, padx=5, pady=5)
    prev_button = ttk.Button(button_frame, text="Previous Step", command=prev_step)
    prev_button.pack(side=tk.LEFT)
    next_button = ttk.Button(button_frame, text="Next Step", command=next_step)
    next_button.pack(side=tk.LEFT)
    auto_play_button = ttk.Button(button_frame, text="Auto Play", command=auto_play)
    auto_play_button.pack(side=tk.LEFT)
    dfs_button = ttk.Button(button_frame, text="DFS", command=dfs)
    dfs_button.pack(side=tk.LEFT)
    bfs_button = ttk.Button(button_frame, text="BFS", command=bfs)
    bfs_button.pack(side=tk.LEFT)

    # Show initial state automatically when the program runs
    show_state(current_step)

# Create a graph
G = nx.Graph()
G.add_edge('A', 'B', weight=2)
G.add_edge('A', 'D', weight=4)
G.add_edge('A', 'H', weight=2)
G.add_edge('B', 'C', weight=1)
G.add_edge('D', 'G', weight=2)
G.add_edge('D', 'E', weight=3)
G.add_edge('D', 'I', weight=2)
G.add_edge('E', 'F', weight=2)
G.add_edge('G', 'J', weight=2)
pos = nx.spring_layout(G)

# Create the Tkinter window
root = tk.Tk()
root.title("Graph Visualization")

# Show initial state automatically when the program runs
update_visualization()

root.mainloop()
