from tkinter import messagebox
import globalvariables as gv
from datetime import date
import tkinter as tk
import constants
import uiutil
import json
import ds
import os

def update_existing_names() -> None:
    gv.existing_names = []
    for file in os.listdir(constants.USER_PROJECTS_PATH):
        gv.existing_names.append(file.split(".")[0])

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

    main.time_sensitive = (time_var.get() == 1 or time_var.get() == 2)

    if mo_var.get() != "" and dy_var.get() != "" and yr_var.get() != "":
        new_date = uiutil.determine_month(mo_var.get()) + "/" + uiutil.determine_day(dy_var.get()) + "/" + yr_var.get()
        if name_entry.get() != "":
            main.name = name_entry.get()

        if main.time_sensitive == True:
            main.deadline = new_date
        elif time_var.get() == 2:
            pass
        else:
            main.deadline = "deadline"
            
        return True
    elif mo_var.get() == "" and dy_var.get() == "" and yr_var.get() == "":
        if name_entry.get() != "":
            main.name = name_entry.get()
        return True
    
    return False

def load_project(filename:str) -> None:
    data:dict = {}
    file_dir = rf"{filename}"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    gv.project = ds.Project(data["projectdata"]["name"], 
                            data["projectdata"]["description"], 
                            data["projectdata"]["time_sensitive"], 
                            data["projectdata"]["deadline"], 
                            data["projectdata"]["notes"]
    )

    mains = data["projectdata"]["mains"]
    gv.project.build_mains(gv.project, mains)

def save_project() -> None:
    data:dict = {}
    file_dir = constants.USER_PROJECTS_PATH + rf"\{gv.project.name}.json"

    data = {
        gv.project.name : gv.project.as_dict()
    }

    try:
        os.remove(file_dir)
    except FileNotFoundError:
        pass
    
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)