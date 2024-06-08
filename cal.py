from datetime import datetime, timedelta
import globalvariables as gv
import tkinter as tk
import constants
import projutil
import sounds
import time

class Calendar:
    show_ctr:int = 0

    month_keycodes = {
        "1":"January",
        "2":"February",
        "3":"March",
        "4":"April",
        "5":"May",
        "6":"June",
        "7":"July",
        "8":"August",
        "9":"September",
        "10":"October",
        "11":"November",
        "12":"December"
    }

    def __init__(self, root:tk.Tk=None, width=0, height=0, bg="white", menu_items=[], reveal_func=(), **kwargs) -> None:
        self.base_frame = tk.Frame(root, width=width, height=height, bg=bg, **kwargs)
        self.reveal_func = reveal_func
        self.menu_items = menu_items
        self.height_offset = 925
        self.root = root
        self.bg = bg

        self.calendar_icon = tk.PhotoImage(file=constants.CALENDAR_ICON)
        self.show_button = tk.Button(self.base_frame, bd=0, bg="light blue", text="Back", fg="black", font=("Times New Roman", 40, "bold"))
        self.show_button.configure(command=lambda f=self.reveal_func : self.toggle_show(f))

        self.curr_day = self.get_this_date()
        self.curr_day_mains = tk.StringVar()
        self.curr_day_formatted = self.date_list_to_string(self.curr_day)
        self.curr_day_mains.set(projutil.mains_with_deadline(self.curr_day_formatted))
        self.curr_week = self.get_this_week()
        self.week_values = self.get_this_week_dates()
        self.curr_week_mains = [tk.StringVar() for _ in range(7)]
        for i in range(7):
            self.curr_week_mains[i].set(projutil.mains_with_deadline(self.week_values[i]))
        self.curr_month = self.month_keycodes[str(self.curr_day.month)]
        self.month_values = self.get_this_month_dates()
        self.curr_month_mains = [tk.StringVar() for _ in range(35)]
        for i in range(35):
            self.curr_month_mains[i].set(projutil.mains_with_deadline(self.month_values[i]))

        self.cal_frame = tk.Frame(self.base_frame, width=width-2, height=self.height_offset, bg=bg)
        self.day_frame = tk.Frame(self.cal_frame, width=width-2, height=self.height_offset, bg=bg, relief="groove", borderwidth=5)
        self.day_label = tk.Label(self.day_frame, bg=bg, font=("Times New Roman", 40, "bold"), justify="left", fg="black", textvariable=self.curr_day_mains)
        self.week_frames = [tk.Frame(self.cal_frame, width=int(width-2/7), height=self.height_offset, bg=bg, relief="groove", borderwidth=5) for _ in range(7)]
        for i in range(7):
            self.week_frames[i].grid_propagate(False)
        self.week_labels = [tk.Label(master=self.week_frames[i], bg=bg, font=("Times New Roman", 30, "bold"), justify="left", fg="black") for i in range(7)]
        self.month_frames = [tk.Frame(self.cal_frame, width=int(width-2/7), height=int(self.height_offset/5), bg=bg, relief="groove", borderwidth=5) for _ in range(35)]
        for i in range(35):
            self.month_frames[i].grid_propagate(False)
        self.month_labels = [tk.Label(master=self.month_frames[i], bg=bg, font=("Times New Roman", 20, "bold"), justify="left", fg="black", text=self.curr_month_mains[i].get()) for i in range(35)]
        
        self.day_active = False
        self.week_active = False
        self.month_active = False

        self.next_button = tk.Button(self.base_frame, bd=0, bg="light blue", text="→", fg="black", font=("Times New Roman", 40, "bold"))
        self.next_button.configure(command=self.next)
        self.prev_button = tk.Button(self.base_frame, bd=0, bg="light blue", text="←", fg="black", font=("Times New Roman", 40, "bold"))
        self.prev_button.configure(command=self.prev)
        self.group_display = tk.StringVar()
        self.group_display.set(self.curr_month + " " + str(self.curr_day.year))
        self.group_select = tk.StringVar()
        self.group_select.set("Month")
        self.group_label = tk.Label(self.base_frame, bg="light blue", fg="black", font=("Times New Roman", 55, "bold"), textvariable=self.group_display)
        self.group_option = tk.OptionMenu(self.base_frame, self.group_select, "Day", "Week", "Month")
        self.group_option.configure(bg="light blue", fg="black", font=("Times New Roman", 46, "bold"))

        self.month_days_keycodes = {
            1:31,
            2:29 if self.curr_day.year % 4 == 0 else 28,
            3:31,
            4:30,
            5:31,
            6:30,
            7:31,
            8:31,
            9:30,
            10:31,
            11:30,
            12:31
        }

    def get_this_week_dates(self, day=datetime.today()) -> list[str]:
        start_of_week = day - timedelta(days=day.weekday())
        week_dates_formatted = []

        for i in range(7):
            formatted_date = (start_of_week + timedelta(days=i)).strftime("%m/%d/%Y")
            week_dates_formatted.append(formatted_date)

        return week_dates_formatted

    def get_this_month_dates(self, day=datetime.today()) -> list[str]:
        first_day_of_month = day.replace(day=1)
        start_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday())

        start_of_month_range = start_of_week - timedelta(days=1)
        month_dates_formatted = []

        for i in range(35):
            formatted_date = (start_of_month_range + timedelta(days=i)).strftime("%m/%d/%y")
            month_dates_formatted.append(formatted_date)

        return month_dates_formatted
    
    def get_this_date(self) -> datetime:
        localtime = time.localtime()
        current_date = [localtime[1], localtime[2], localtime[0]]
        return datetime(current_date[2], current_date[0], current_date[1])

    def get_this_week(self, day=datetime.today()) -> str:
        return self.get_this_week_dates(day)[0][0:5] + "-" + self.get_this_week_dates(day)[-1][0:5]

    def get_this_month(self) -> str:
        return self.month_keycodes[str(self.get_this_date()[0])]
    
    def get_this_month_raw(self, day=datetime.today()) -> str:
        if len(str(day.month)) == 1:
            return "0" + str(day.month)
        return str(day.month)

    def date_list_to_string(self, date:datetime) -> str:
        if len(str(date.month)) == 1:
            if len(str(date.day)) == 1:
                return "0" + str(date.month) + "/0" + str(date.day) + "/" + str(date.year)
            return "0" + str(date.month) + "/" + str(date.day) + "/" + str(date.year)
        return str(date.month) + "/" + str(date.day) + "/" + str(date.year)

    def update_group_label(self):
        self.month_days_keycodes[2] = 29 if self.curr_day.year % 4 == 0 else 28
        if self.group_select.get() == "Day":
            self.group_display.set(self.date_list_to_string(self.curr_day))
            self.curr_day_formatted = self.date_list_to_string(self.curr_day)
            self.curr_day_mains.set(projutil.mains_with_deadline(self.curr_day_formatted))
            self.show_day()
            self.this_loop = self.root.after(100, self.update_group_label)
        elif self.group_select.get() == "Week":
            self.group_display.set(self.get_this_week(self.curr_day) + " " + str(self.curr_day.year))
            self.curr_week = self.get_this_week(self.curr_day)
            self.week_values = self.get_this_week_dates(self.curr_day)
            for i in range(7):
                self.curr_week_mains[i].set(projutil.mains_with_deadline(self.week_values[i]))
            self.show_week()
            self.this_loop = self.root.after(333, self.update_group_label)
        elif self.group_select.get() == "Month":
            self.group_display.set(self.month_keycodes[str(self.curr_day.month)] + " " + str(self.curr_day.year))
            self.curr_month = self.get_this_month_raw(self.curr_day)
            self.month_values = self.get_this_month_dates(self.curr_day)
            for i in range(35):
                self.curr_month_mains[i].set(
                    projutil.mains_with_deadline(self.month_values[i])
                )
            self.show_month()
            self.this_loop = self.root.after(1000, self.update_group_label)

    def next(self) -> None:
        if self.group_select.get() == "Day":
            if self.curr_day.month == 12 and self.curr_day.day == 31:
                self.curr_day = datetime(month=1, year=self.curr_day.year + 1, day=1)
            elif self.curr_day.month != 12 and self.curr_day.day == self.month_days_keycodes[self.curr_day.month]:
                self.curr_day = datetime(month=self.curr_day.month + 1, day=1, year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day + 1, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Week":
            day_offset = self.curr_day.day + 7
            if day_offset > self.month_days_keycodes[self.curr_day.month]:
                if self.curr_day.month == 12:
                    self.curr_day = datetime(month=1, year=self.curr_day.year + 1, day=day_offset-self.month_days_keycodes[self.curr_day.month])
                elif self.curr_day.month != 12:
                    self.curr_day = datetime(month=self.curr_day.month + 1, day=day_offset-self.month_days_keycodes[self.curr_day.month], year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day + 7, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Month":
            if self.curr_day.month < 12:
                self.curr_day = datetime(day=self.curr_day.day, month=self.curr_day.month + 1, year=self.curr_day.year)
            elif self.curr_day.month == 12:
                self.curr_day = datetime(day=self.curr_day.day, month=1, year=self.curr_day.year + 1)
        sounds.play_click()

    def prev(self) -> None:
        if self.group_select.get() == "Day":
            if self.curr_day.month == 1 and self.curr_day.day == 1:
                self.curr_day = datetime(month=12, year=self.curr_day.year - 1, day=31)
            elif self.curr_day.month != 1 and self.curr_day.day == 1:
                self.curr_day = datetime(month=self.curr_day.month - 1, day=self.month_days_keycodes[self.curr_day.month-1], year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day - 1, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Week":
            day_offset = self.curr_day.day - 7
            if day_offset <= 0:
                if self.curr_day.month == 1:
                    self.curr_day = datetime(month=12, year=self.curr_day.year - 1, day=self.month_days_keycodes[12]+day_offset)
                elif self.curr_day.month != 1:
                    self.curr_day = datetime(month=self.curr_day.month - 1, day=self.month_days_keycodes[self.curr_day.month-1]+day_offset, year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day - 7, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Month":
            if self.curr_day.month > 1:
                self.curr_day = datetime(day=self.curr_day.day, month=self.curr_day.month - 1, year=self.curr_day.year)
            elif self.curr_day.month == 1:
                self.curr_day = datetime(day=self.curr_day.day, month=12, year=self.curr_day.year - 1)
        sounds.play_click()
        
    def show_day(self) -> None:
        if not self.day_active:
            for i in range(35):
                self.month_frames[i].place_forget()
            for i in range(7):
                self.week_frames[i].place_forget()
            self.day_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.day_label.place(relx=0.5, rely=0, anchor="n")
            self.day_active = True
        self.week_active = False
        self.month_active = False

    def show_week(self) -> None:
        if not self.week_active:
            for i in range(35):
                self.month_frames[i].place_forget()
            self.day_frame.place_forget()
        for i in range(7):
            self.week_frames[i].place(relx=((1/7)*((i+7)%7)), rely=0.5, anchor="w")
            self.week_labels[i].configure(text=(((self.week_values[i])+"\n\n"+(self.curr_week_mains[i].get())) 
                                                if ((self.curr_week_mains[i].get()) != "") 
                                                else (self.week_values[i])))
            self.week_labels[i].grid(row=0, column=0)
        self.week_active = True
        self.day_active = False
        self.month_active = False

    def show_month(self) -> None:
        if not self.month_active:
            self.day_frame.place_forget()
            for i in range(7):
                self.week_frames[i].place_forget()
        for i in range(35):
            self.month_frames[i].place(relx=((1/7)*((i+7)%7)), rely=(0.2*(int(i/7))), anchor="nw")
            self.month_labels[i].configure(text=(((self.month_values[i])+"\n"+(self.curr_month_mains[i].get())) 
                                                 if ((self.curr_month_mains[i].get()) != "") 
                                                 else (self.month_values[i])))
            self.month_labels[i].grid(row=0, column=0)
        self.month_active = True
        self.day_active = False
        self.week_active = False

    def toggle_show(self, reveal_func) -> None:
        if self.show_ctr % 2 == 0:
            for widget in self.menu_items:
                try:
                    widget.place_forget()
                except:
                    pass
            self.menu_items.clear()

            self.base_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.group_select.set("Month")
            self.show_button.place(relx=0, rely=0, anchor="nw")
            self.prev_button.place(relx=0.25, rely=0, anchor="n")
            self.group_label.place(relx=0.5, rely=0.0125, anchor="n")
            self.next_button.place(relx=0.75, rely=0, anchor="n")
            self.group_option.place(relx=1, rely=0, anchor="ne")
            self.cal_frame.place(relx=0.5, rely=1, anchor="s")
            for i in range(35):
                self.month_frames[i].place(relx=((1/7)*((i+7)%7)), rely=(0.2*(int(i/7))), anchor="nw")
                self.month_labels[i].configure(text=(((self.month_values[i])+"\n"+(self.curr_month_mains[i].get())) 
                                                 if ((self.curr_month_mains[i].get()) != "") 
                                                 else (self.month_values[i])))
                self.month_labels[i].grid(row=0, column=0)
            self.month_active = True
            self.this_loop = self.root.after(1000, self.update_group_label)
        else:
            self.curr_day = self.get_this_date()
            self.base_frame.place_forget()
            reveal_func()
            self.root.after_cancel(self.this_loop)
        self.show_ctr += 1
        sounds.play_click()