import tkinter as tk

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class TreeVisualizer:
    def __init__(self, root:TreeNode):
        self.root = root
        self.window = tk.Tk()
        self.window.title("Tree Visualization")
        self.width = int(self.window.winfo_screenwidth()/2)
        self.height = int(self.window.winfo_screenheight()/2)
        self.horiz_offset = int((self.window.winfo_screenwidth() - self.width) / 2)
        self.vert_offset = int((self.window.winfo_screenheight() - self.height) / 2)
        self.window.geometry(f"{self.width}x{self.height}+{self.horiz_offset}+{self.vert_offset}")
        self.window.resizable(width=False, height=False)
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, bg='light blue')
        self.canvas.pack()
        self.base_node_radius = 20  # Base radius
        self.level_separation = 100
        self.sibling_separation = 40

    def get_node_radius(self, value):
        text_length = len(str(value))
        return max(self.base_node_radius, self.base_node_radius + text_length * 2)

    def calculate_positions(self):
        positions = {}
        subtree_widths = {}

        def calc_subtree_width(node):
            if not node.children:
                node_radius = self.get_node_radius(node.value)
                subtree_widths[node] = node_radius * 2
                return subtree_widths[node]

            width = 0
            for child in node.children:
                width += calc_subtree_width(child)
            
            subtree_widths[node] = max(width, self.get_node_radius(node.value) * 2)
            return subtree_widths[node]

        def assign_positions(node, x, y):
            positions[node] = (x, y)
            if node.children:
                total_width = sum(subtree_widths[child] for child in node.children)
                start_x = x - total_width // 2
                for child in node.children:
                    child_width = subtree_widths[child]
                    assign_positions(child, start_x + child_width // 2, y + self.level_separation)
                    start_x += child_width

        calc_subtree_width(self.root)
        assign_positions(self.root, 400, 20)
        return positions

    def draw_tree(self):
        positions = self.calculate_positions()
        for node, (x, y) in positions.items():
            radius = self.get_node_radius(node.value)
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="lightblue")
            self.canvas.create_text(x, y, text=str(node.value), fill="black")
            for child in node.children:
                child_x, child_y = positions[child]
                self.canvas.create_line(x, y + radius, child_x, child_y - radius)

    def run(self):
        self.draw_tree()
        self.window.mainloop()