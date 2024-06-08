from treevis import TreeNode, TreeVisualizer
import tkinter as tk
import proj

window : tk.Tk
logo_label : tk.Label
main_menu_buttons : list[tk.Button]
np_menu_items : list

stars : list
star_loop : list
star_score : int = 0
touched_gold : bool
gold_button : tk.Button

existing_names : list[str]
project : proj.Project

tree_root : TreeNode
tree_visualizer : TreeVisualizer