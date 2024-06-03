import globalvariables as gv
import constants
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