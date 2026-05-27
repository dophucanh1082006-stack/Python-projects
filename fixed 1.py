from math import dist
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tracemalloc import start
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphVisualizer:
    def dijkstra(self, G, start, end):
    # Khởi tạo
        dist = {node: float('inf') for node in G.nodes}
        prev = {node: None for node in G.nodes}
        visited = set()

        dist[start] = 0

        while len(visited) < len(G.nodes):
        # Tìm đỉnh chưa thăm có khoảng cách nhỏ nhất
            current = None
            current_dist = float('inf')

            for node in G.nodes:
                if node not in visited and dist[node] < current_dist:
                    current = node
                    current_dist = dist[node]

            if current is None:
                break

            visited.add(current)

        # Cập nhật các đỉnh kề
            for neighbor in G.neighbors(current):
                weight = G[current][neighbor]['weight']
                if dist[current] + weight < dist[neighbor]:
                    dist[neighbor] = dist[current] + weight
                    prev[neighbor] = current

        
        path = []
        node = end  
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
        if not path or path[0] != start:
            path = []

        return dist, prev, path

    def __init__(self, root):
        self.root = root
        self.root.title("Trình Vẽ Đồ Thị Trực Quan")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2f")

        # --- PHẦN 1: GIAO DIỆN NHẬP LIỆU (BÊN TRÁI) ---
        input_frame = tk.Frame(self.root, padx=15, pady=15, bg="#1e1e2f")
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(input_frame, text="Đỉnh bắt đầu:", bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        self.entry_start = tk.Entry(input_frame, width=10,bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
        self.entry_start.pack(pady=2)
        tk.Label(input_frame, text="Đỉnh kết thúc:", bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        self.entry_end = tk.Entry(input_frame, width=10, bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
        self.entry_end.pack(pady=2)
        tk.Label(input_frame, text="1. Nhập số lượng", font=('Arial', 10, 'bold'),bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        
        # Nhập số đỉnh
        tk.Label(input_frame, text="Số đỉnh:", bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        self.entry_nodes = tk.Entry(input_frame, width=10, bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
        self.entry_nodes.pack(pady=2)

        # Nhập số cạnh
        tk.Label(input_frame, text="Số cạnh:", bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        self.entry_edges_count = tk.Entry(input_frame, width=10, bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
        self.entry_edges_count.pack(pady=2)

        tk.Label(input_frame, text="\n2. Nhập các cạnh (u v w)", font=('Arial', 10, 'bold'), bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        tk.Label(input_frame, text="Ví dụ: a b 5 (đỉnh a nối b, nặng 5)", font=('Arial', 8), bg="#1e1e2f", fg="#ccccff").pack(anchor="w")
        
        # Ô nhập danh sách cạnh
        self.txt_edges = scrolledtext.ScrolledText(input_frame, width=25, height=12,bg="#2b2b3c", fg="white", insertbackground="white", font=("Consolas", 11), relief="flat")
        self.txt_edges.pack(pady=5)

        # Nút bấm thực hiện
        self.btn_draw = tk.Button(input_frame, text="VẼ ĐỒ THỊ & TÌM ĐƯỜNG", command=self.process_data, 
                                  bg="#4da6ff", fg="white", font=('Segoe UI', 13, 'bold'), height=2,activebackground="#3399ff",relief="flat")
        self.btn_draw.pack(fill=tk.X, pady=10)

        # --- PHẦN 2: KHU VỰC VẼ (BÊN PHẢI) ---
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.fig.patch.set_facecolor("#2b2b3c")
        self.ax.set_facecolor("#2b2b3c")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        tk.Label(self.root, text="DIJKSTRA",
         font=("Segoe UI", 14, "bold"),
         bg="#1e1e2f", fg="#66ccff").pack(side=tk.TOP, anchor="n", pady=10)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def process_data(self):
        try:
            # Đọc dữ liệu từ các ô nhập
            num_nodes = int(self.entry_nodes.get())
            num_edges = int(self.entry_edges_count.get())
            start = self.entry_start.get().strip()
            end = self.entry_end.get().strip()


            raw_input = self.txt_edges.get("1.0", tk.END).strip().split('\n')            # Lọc các dòng trống
            edge_data = [line.split() for line in raw_input if line.strip()]

            if len(edge_data) != num_edges:
                messagebox.showwarning("Lưu ý", f"Số cạnh thực tế ({len(edge_data)}) khác với khai báo ({num_edges}).")

            # Tạo đồ thị
            G = nx.Graph()
            for item in edge_data:
                if len(item) == 3:
                    u, v, w = item[0], item[1], int(item[2])
                    G.add_edge(u, v, weight=w)
            if G.number_of_nodes() != num_nodes:
                messagebox.showerror("Lỗi", f"Số đỉnh thực tế ({G.number_of_nodes()}) khác khai báo ({num_nodes})!")
                return

            dist, prev, path = self.dijkstra(G, start, end)
            result = f"Kết quả từ đỉnh {start}:\n"
            if not path:
                messagebox.showinfo("Kết quả", f"Không có đường đi từ {start} đến {end}!")
            else:
                messagebox.showinfo("Kết quả Dijkstra",
                    f"Khoảng cách: {dist[end]}\nLộ trình: {' → '.join(path)}")

            self.draw_graph(G, path)

        except Exception:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập số nguyên cho số đỉnh, cạnh và trọng số.")

    def draw_graph(self, G, path=[]):
        self.ax.clear()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        # Bố trí các đỉnh (layout)
        pos = nx.spring_layout(G, seed=42) 
        
        # Vẽ các nút (nodes)
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='#3498db', node_size=800)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_color='white', font_weight='bold')

        # Vẽ các cạnh (edges)
        path_edges = list(zip(path, path[1:])) if path else []
        normal_edges = [e for e in G.edges() if e not in path_edges and (e[1], e[0]) not in path_edges]

        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=self.ax, edge_color='#7f8c8d', width=2)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=self.ax, edge_color='#00ffcc', width=4)
            
        # Vẽ nhãn trọng số trên cạnh
        edge_labels = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, 
                            font_size=13, font_color='black', font_weight='bold')
        self.ax.set_title("Đồ thị trực quan", color="white", fontweight="bold")
        self.ax.axis('off') # Ẩn trục tọa độ
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()



import tkinter as tk
from tkinter import messagebox
import heapq

# 1. Cài đặt thuật toán Dijkstra (Hàm xử lý & tính toán)
def dijkstra(graph, start, end):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    precedents = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = precedents[current_node]
            return distances[end], path[::-1]

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                precedents[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return float('infinity'), []

# 2. Xử lý & tính toán + Trả kết quả ra giao diện
def handle_calculate():
    try:
        # Giả lập dữ liệu đồ thị (Trong thực tế có thể đọc từ file hoặc ô nhập liệu khác)
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }
        
        # Đọc dữ liệu từ giao diện
        start_node = entry_start.get().upper()
        end_node = entry_end.get().upper()

        if start_node not in graph or end_node not in graph:
            messagebox.showerror("Lỗi", "Điểm bắt đầu hoặc kết thúc không tồn tại!")
            return

        # Xử lý & tính toán kết qu
        distance, path = dijkstra(graph, start_node, end_node)

        # Trả kết quả ra giao diện
        if distance == float('infinity'):
            label_result.config(text="Không có đường đi!", fg="red")
        else:
            result_text = f"Khoảng cách: {distance}\nLộ trình: {' -> '.join(path)}"
            label_result.config(text=result_text, fg="blue")
            
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Thiết lập Giao diện (Tkinter)
root = tk.Tk()
root.title("Dijkstra Solver")
root.geometry("300x250")

tk.Label(root, text="Điểm bắt đầu (A, B, C, D):").pack(pady=5)
entry_start = tk.Entry(root,bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
entry_start.pack()

tk.Label(root, text="Điểm kết thúc:").pack(pady=5)
entry_end = tk.Entry(root,bg="#2b2b3c", fg="white", insertbackground="white", relief="flat")
entry_end.pack()

btn_calc = tk.Button(root, text="Tính toán lộ trình", command=handle_calculate)
btn_calc.pack(pady=15)

label_result = tk.Label(root, text="", font=("Arial", 10, "bold"))
label_result.pack(pady=10)

root.mainloop()
