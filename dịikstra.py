import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình Vẽ Đồ Thị Trực Quan")
        self.root.geometry("900x600")

        # --- PHẦN 1: GIAO DIỆN NHẬP LIỆU (BÊN TRÁI) ---
        input_frame = tk.Frame(self.root, padx=15, pady=15)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(input_frame, text="1. Nhập số lượng", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        # Nhập số đỉnh
        tk.Label(input_frame, text="Số đỉnh:").pack(anchor="w")
        self.entry_nodes = tk.Entry(input_frame, width=10)
        self.entry_nodes.pack(pady=2)

        # Nhập số cạnh
        tk.Label(input_frame, text="Số cạnh:").pack(anchor="w")
        self.entry_edges_count = tk.Entry(input_frame, width=10)
        self.entry_edges_count.pack(pady=2)

        tk.Label(input_frame, text="\n2. Nhập các cạnh (u v w)", font=('Arial', 10, 'bold')).pack(anchor="w")
        tk.Label(input_frame, text="Ví dụ: a b 5 (đỉnh a nối b, nặng 5)", fg="blue", font=('Arial', 8)).pack(anchor="w")
        
        # Ô nhập danh sách cạnh
        self.txt_edges = scrolledtext.ScrolledText(input_frame, width=25, height=15)
        self.txt_edges.pack(pady=5)

        # Nút bấm thực hiện
        self.btn_draw = tk.Button(input_frame, text="VẼ ĐỒ THỊ", command=self.process_data, 
                                  bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'), height=2)
        self.btn_draw.pack(fill=tk.X, pady=10)

        # --- PHẦN 2: KHU VỰC VẼ (BÊN PHẢI) ---
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def process_data(self):
        try:
            # Đọc dữ liệu từ các ô nhập
            num_nodes = int(self.entry_nodes.get())
            num_edges = int(self.entry_edges_count.get())
            raw_input = self.txt_edges.get("1.0", tk.END).strip().split('\n')
            
            # Lọc các dòng trống
            edge_data = [line.split() for line in raw_input if line.strip()]

            if len(edge_data) != num_edges:
                messagebox.showwarning("Lưu ý", f"Số cạnh thực tế ({len(edge_data)}) khác với khai báo ({num_edges}).")

            # Tạo đồ thị
            G = nx.Graph()
            for item in edge_data:
                if len(item) == 3:
                    u, v, w = item[0], item[1], int(item[2])
                    G.add_edge(u, v, weight=w)
            
            self.draw_graph(G)

        except ValueError:
            messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập số nguyên cho số đỉnh, cạnh và trọng số.")

    def draw_graph(self, G):
        self.ax.clear()
        
        # Bố trí các đỉnh (layout)
        pos = nx.spring_layout(G, seed=42) 
        
        # Vẽ các nút (nodes)
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color='#3498db', node_size=800)
        nx.draw_networkx_labels(G, pos, ax=self.ax, font_color='white', font_weight='bold')

        # Vẽ các cạnh (edges)
        nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='#7f8c8d', width=2)
        
        # Vẽ nhãn trọng số trên cạnh
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax)

        self.ax.set_title("Đồ thị trực quan")
        self.ax.axis('off') # Ẩn trục tọa độ
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()