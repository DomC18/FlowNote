from treevis import TreeNode
from datetime import datetime, date
import globalvariables as gv
import time

def determine_month(month:str) -> str:
    months = {"": "00", "January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
    return months[month]

def determine_day(day:str) -> str:
    days = {"": "00", '1st':"01", '2nd':"02", '3rd':"03", '4th':"04", '5th':"05", '6th':"06", '7th':"07", '8th':"08", '9th':"09", '10th':"10", '11th':"11", '12th':"12", '13th':"13", '14th':"14", '15th':"15", '16th':"16", '17th':"17", '18th':"18", '19th':"19", '20th':"20", '21st':"21", '22nd':"22", '23rd':"23", '24th':"24", '25th':"25", '26th':"26", '27th':"27", '28th':"28", '29th':"29", '30th':"30", '31st':"31"}
    return days[day]

class Main:
    def __init__(self, parent, name:str, description="description", time_sensitive=False, deadline="00/00/0000", notes="notes") -> None:
        self.parent = parent
        self.name = name
        self.description = description
        self.time_sensitive = time_sensitive
        self.notes = notes
        self.mains = []

        if self.time_sensitive:
            if deadline == "00/00/0000":
                self.deadline = self.date_list_to_string(self.get_current_date())
            else:
                self.deadline = deadline
        else:
            self.deadline = ""

    def add_main(self, name:str, desc="description", time_sensitive=False, deadline="00/00/0000", notes="notes"):
        new_main = Main(self, name, desc, time_sensitive, deadline, notes)
        self.mains.append(new_main)
        return new_main

    def date_after_current(date_to_complete:date) -> bool:
        if (date_to_complete - datetime.now().date()).days <= 0:
            return False
        else:
            return True

    def get_current_date(self) -> list:
        localtime = time.localtime()
        current_date = [localtime[1], (localtime[2] if len(str(localtime[2])) == 2 else ("0" + str(localtime[2]))), localtime[0]]
        return current_date
    
    def date_list_to_string(self, date_list:list) -> str:
        new_month:str = ""

        if date_list[0] < 10:
            new_month = "0" + str(date_list[0])
        
        return new_month + "/" + str(date_list[1]) + "/" + str(date_list[2])

    def mains_with_deadline(self, deadline:str, mains:list, curr_mains:list):
        for main in curr_mains:
            if main.deadline == deadline or main.deadline == str(deadline[0:-2] + "20" + deadline[-2:]):
                mains.append(f"{main.name.casefold().capitalize()}\n\n")
            main.mains_with_deadline(deadline, mains, main.mains)

    def calculate_days_left(self) -> float:
        if not self.time_sensitive:
            return ""

        deadline_as_date = date(int(self.deadline[-4:]), ((int(self.deadline[0:2])) if (int(self.deadline[0:2]) >= 10) else (int(self.deadline[1:2]))), ((int(self.deadline[3:5])) if ((int(self.deadline[3:5]) >= 10)) else (int(self.deadline[4:5]))))
        return str((deadline_as_date - datetime.now().date()).days) + " DAYS LEFT"

    def __repr__(self) -> str:
        return f'(Name:"{self.name}", Description:"{self.description}", TimeSensitive:"{self.time_sensitive}", Deadline:"{self.deadline}", Notes:"{self.notes}", Mains:{self.mains})'

class Project:
    def __init__(self, name="", description="description", time_sensitive=False, deadline="00/00/0000", notes="notes") -> None:
        self.name = name
        self.description = description
        self.time_sensitive = time_sensitive
        self.notes = notes
        self.mains = []
        self.result = []

        if self.time_sensitive:
            if deadline == "00/00/0000":
                self.deadline = self.date_list_to_string(self.get_current_date())
            else:
                self.deadline = deadline
        else:
            self.deadline = ""

    def add_main(self, name:str, desc="description", time_sensitive=False, deadline="00/00/0000", notes="notes") -> Main:
        new_main = Main(self, name, desc, time_sensitive, deadline, notes)
        self.mains.append(new_main)
        return new_main

    def date_after_current(date_to_complete:date) -> bool:
        if (date_to_complete - datetime.now().date()).days <= 0:
            return False
        else:
            return True

    def get_current_date(self) -> list:
        localtime = time.localtime()
        current_date = [localtime[1], (localtime[2] if len(str(localtime[2])) == 2 else ("0" + str(localtime[2]))), localtime[0]]
        return current_date
    
    def date_list_to_string(self, date_list:list) -> str:
        new_month:str = ""

        if date_list[0] < 10:
            new_month = "0" + str(date_list[0])
        
        return new_month + "/" + str(date_list[1]) + "/" + str(date_list[2])

    def calculate_days_left(self) -> float:
        if not self.time_sensitive:
            return ""

        deadline_as_date = date(int(self.deadline[-4:]), ((int(self.deadline[0:2])) if (int(self.deadline[0:2]) >= 10) else (int(self.deadline[1:2]))), ((int(self.deadline[3:5])) if ((int(self.deadline[3:5]) >= 10)) else (int(self.deadline[4:5]))))
        return str((deadline_as_date - datetime.now().date()).days) + " DAYS LEFT"

    def __repr__(self) -> str:
        return f'(Name:"{self.name}", Description:"{self.description}", TimeSensitive:"{self.time_sensitive}", Deadline:"{self.deadline}", Notes:"{self.notes}", Mains:{self.mains})'

    def build_mains(self, parent, mains=[]) -> None:
        if len(mains) == 0:
            return
        
        for main in mains:
            new_main = parent.add_main(main["Name"], main["Description"], bool(main["TimeSensitive"]) if main["TimeSensitive"] == "True" else False, main["Deadline"], main["Notes"])
            if (len(main["Mains"]) == 0):
                continue
            self.build_mains(new_main, main["Mains"])

    def build_tree(self, parent, mains=[]) -> None:
        if parent == gv.tree_root:
            gv.tree_root = TreeNode(self.name)
            parent = gv.tree_root
            if len(mains) == 0:
                return

        for main in mains:
            new_branch = TreeNode(main.name)
            parent.add_child(new_branch)
            if (len(main.mains) == 0):
                continue
            self.build_tree(new_branch, main.mains)

    def mains_dict_list(self, mains:list[Main]) -> list:
        result = []
        for main in mains:
            result.append({
                "Name": main.name,
                "Description": main.description,
                "TimeSensitive": str(main.time_sensitive),
                "Deadline": main.deadline,
                "Notes": main.notes,
                "Mains": self.mains_dict_list(main.mains)
            })
        return result       

    def as_dict(self) -> dict:
        return {
            "Name": self.name,
            "Description": self.description,
            "TimeSensitive": str(self.time_sensitive),
            "Deadline": self.deadline,
            "Notes": self.notes,
            "Mains": self.mains_dict_list(self.mains)
        }
    