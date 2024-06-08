from treevis import TreeNode, TreeVisualizer
import tkinter as tk
import ds

window : tk.Tk
logo_label : tk.Label
main_menu_buttons : list[tk.Button]

stars : list
star_loop : list
star_score : int = 0

existing_names : list[str]
project : ds.Project

tree_root : TreeNode
tree_visualizer : TreeVisualizer