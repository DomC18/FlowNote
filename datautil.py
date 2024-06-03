import globalvariables as gv
import json
import ds
import os

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

def save_project(filename:str) -> None:
    data:dict = {}
    file_dir = rf"{filename}"

    data = {
        "projectdata": gv.project.as_dict()
    }

    try:
        os.remove(file_dir)
    except FileNotFoundError:
        return
    
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)
    
load_project(r"C:\Users\Domth\Desktop\MyCode\FlowNote\UserProjects\projectname.json")
print()
print(gv.project)
save_project(r"C:\Users\Domth\Desktop\MyCode\FlowNote\UserProjects\project.json")