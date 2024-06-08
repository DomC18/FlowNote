from tkinter import messagebox
from treevis import TreeVisualizer
import globalvariables as gv
from datetime import date
import tkinter as tk
import constants
import uiutil
import sounds
import json
import ds
import os

def update_existing_names() -> None:
    gv.existing_names = []
    for file in os.listdir(constants.USER_PROJECTS_PATH):
        gv.existing_names.append(file.split(".")[0])

def update_curr_tree() -> None:
    sounds.play_click()
    gv.tree_root = None
    gv.project.build_tree(gv.tree_root, gv.project.mains)
    gv.tree_visualizer = None
    gv.tree_visualizer = TreeVisualizer(gv.tree_root)
    gv.tree_visualizer.run()

def edit_main(main, name_entry:tk.Entry, desc_entry:tk.Entry, time_var:tk.IntVar, mo_var:tk.StringVar, dy_var:tk.StringVar, yr_var:tk.StringVar, notes_entry:tk.Entry):
    if time_var.get() == 1:
        date_mo = uiutil.determine_month(mo_var.get())
        date_dy = uiutil.determine_day(dy_var.get())
        if date_mo == "" or date_dy == "" or yr_var.get() == "":
            messagebox.showerror("Invalid Date", "Please enter a valid date.")
            return
        if not ds.Project.date_after_current(date(int(yr_var.get()), int(date_mo), int(date_dy))):
            messagebox.showerror("Invalid Date", "Date entered is before or equal to the date today.")
            return
    
    new_date = ""
    if desc_entry.get() != "":
        main.description = desc_entry.get()
    if notes_entry.get() != "":
        main.notes = notes_entry.get()

    if mo_var.get() != "" and dy_var.get() != "" and yr_var.get() != "":
        new_date = uiutil.determine_month(mo_var.get()) + "/" + uiutil.determine_day(dy_var.get()) + "/" + yr_var.get()
        if name_entry.get() != "":
            main.name = name_entry.get()

        main.time_sensitive = True
        main.deadline = new_date
            
        return True
    elif time_var.get() == 0 or time_var.get() == 2:
        if name_entry.get() != "":
            main.name = name_entry.get()
        
        if time_var.get() == 0:
            main.time_sensitive = False
            main.deadline = "deadline"
        return True
    
    return False

def mains_with_deadline(deadline:str) -> list:
    mains = []
    if gv.project.deadline == deadline or gv.project.deadline == str(deadline[0:-2] + "20" + deadline[-2:]):
        mains.append(f"{gv.project.name.casefold().capitalize()}\n\n")
    for main in gv.project.mains:
        if main.deadline == deadline or main.deadline == str(deadline[0:-2] + "20" + deadline[-2:]):
            mains.append(f"{main.name.casefold().capitalize()}\n\n")
        main.mains_with_deadline(deadline, mains, main.mains)
    label_text = ""
    for main in mains:
        label_text += main
    return label_text

def load_project(filename:str) -> None:
    data:dict = {}
    file_dir = rf"{filename}"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    gv.project = ds.Project(data["projectdata"]["Name"], 
                            data["projectdata"]["Description"], 
                            data["projectdata"]["TimeSensitive"], 
                            data["projectdata"]["Deadline"], 
                            data["projectdata"]["Notes"]
    )

    mains = data["projectdata"]["Mains"]
    gv.project.build_mains(gv.project, mains)

def save_project() -> None:
    data:dict = {}
    file_dir = constants.USER_PROJECTS_PATH + rf"\{gv.project.name}.json"

    data = {
        "projectdata" : gv.project.as_dict()
    }

    try:
        os.remove(file_dir)
    except FileNotFoundError:
        pass
    
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)