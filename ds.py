from datetime import datetime, date
import time

class Main:
    def __init__(self, parent, name:str, description="", time_sensitive=False, deadline="00/00/0000", notes="") -> None:
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
            self.deadline = None

    def add_main(self, name:str) -> None:
        new_main = Main(self, name)
        self.mains.append(new_main)
    
    def edit_name(self, new_name:str) -> None:
        self.name = new_name
    
    def edit_description(self, new_description:str) -> None:
        self.description = new_description
    
    def edit_time_sensitivity(self, new_timesensitivity:bool) -> None:
        self.time_sensitive = new_timesensitivity
    
    def edit_deadline(self, new_deadline) -> None:
        self.deadline = new_deadline
    
    def edit_notes(self, new_notes:str) -> None:
        self.notes = new_notes

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
        deadline_as_date = date(int(self.deadline[-4]), int(self.deadline[3:5]), int(self.deadline[0:2]))
        return (deadline_as_date - datetime.now().date()).days

    def __repr__(self) -> str:
        return f'(Name:"{self.name}", Description:"{self.description}", TimeSensitive:"{self.time_sensitive}", Deadline:"{self.deadline}", Notes:"{self.notes}", Children:{self.subs})'

class Project:
    def __init__(self, name="", description="", time_sensitive=False, deadline="00/00/0000", notes="") -> None:
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
            self.deadline = None

    def add_main(self, name:str) -> None:
        new_main = Main(self, name)
        self.mains.append(new_main)

    def edit_name(self, new_name:str) -> None:
        self.name = new_name

    def edit_description(self, new_description:str) -> None:
        self.description = new_description

    def edit_time_sensitivity(self, new_timesensitivity:bool) -> None:
        self.time_sensitive = new_timesensitivity

    def edit_deadline(self, new_deadline) -> None:
        self.deadline = new_deadline

    def edit_notes(self, new_notes:str) -> None:
        self.notes = new_notes

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
        deadline_as_date = date(int(self.deadline[-4:]), ((int(self.deadline[0:2])) if (int(self.deadline[0:2]) >= 10) else (int(self.deadline[1:2]))), ((int(self.deadline[3:5])) if ((int(self.deadline[3:5]) >= 10)) else (int(self.deadline[4:5]))))
        return (deadline_as_date - datetime.now().date()).days

    def __repr__(self) -> str:
        return f'(Name:"{self.name}", Description:"{self.description}", TimeSensitive:"{self.time_sensitive}", Deadline:"{self.deadline}", Notes:"{self.notes}", Mains:{self.mains})'
    
    def return_as_dict(self) -> dict:
        return {
            "Name": self.name,
            "Description": self.description,
            "TimeSensitive": self.time_sensitive,
            "Deadline": self.deadline,
            "Notes": self.notes,
            "Mains": self.mains
        }
