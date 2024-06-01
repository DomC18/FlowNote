from PIL import ImageTk, ImageFilter, Image
from datetime import datetime, date
from tkinter import messagebox
import globalvariables as gv
import pygame as pyg
import tkinter as tk
import random as rr
import constants
import ds

def get_south_y(y_size_pixels:int, north_y:float):
    return (y_size_pixels/1080)+north_y

def calc_dist2(south_y):
    return south_y+((0.95-south_y)/2)

def calc_dist3(south_y):
    return south_y+((0.95-south_y)/3)

def calc_dist23(south_y):
    return south_y+((2*(0.95-south_y))/3)

def determine_month(month):
    months = {"January":"01", "February":"02", "March":"03", "April":"04", "May":"05", "June":"06", "July":"07", "August":"08", "September":"09", "October":"10", "November":"11", "December":"12"}
    return months[month]

def determine_day(day):
    days = {'1st':"01", '2nd':"02", '3rd':"03", '4th':"04", '5th':"05", '6th':"06", '7th':"07", '8th':"08", '9th':"09", '10th':"10", '11th':"11", '12th':"12", '13th':"13", '14th':"14", '15th':"15", '16th':"16", '17th':"17", '18th':"18", '19th':"19", '20th':"20", '21st':"21", '22nd':"22", '23rd':"23", '24th':"24", '25th':"25", '26th':"26", '27th':"27", '28th':"28", '29th':"29", '30th':"30", '31st':"31"}
    return days[day]

def char_limit(text):
    if len(text) <= 30:
        return True
    else:
        return False

def play_sound(filedir:str):
    pyg.mixer.init()
    pyg.mixer.music.load(filedir)
    pyg.mixer.music.play()

def play_click():
    play_sound(constants.CLICK_SOUND)

def play_back():
    play_sound(constants.BACK_SOUND)

def play_pop():
    play_sound(constants.POP_SOUND)

gv.window = tk.Tk()
gv.window.title("FlowNote")
gv.window.geometry("600x600")
gv.window.resizable(width=False, height=False)
gv.window.configure(bg="#414449")
gv.window.bind("<Escape>", quit)
char_limit_cmd = gv.window.register(char_limit)

logo = Image.open(constants.LOGO_UNSIGNED_ICON)
logo = logo.resize((600, 600), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(gv.window, image=logo_photo)
logo_label.image = logo_photo
logo_label.pack()

transparent_image = Image.open(constants.ACTUALLY_TRANSPARENT_ICON)
transparent_photo = ImageTk.PhotoImage(transparent_image)
blur_func_calls = 0
stars = []
star_loop = [None]
sky = Image.open(constants.SKY_ICON)
sky = sky.resize((1920, 1080), Image.Resampling.LANCZOS)
sky_photo = ImageTk.PhotoImage(sky)
sky_mini = Image.open(constants.SKY_ICON)
sky_mini_photo = ImageTk.PhotoImage(sky_mini)
sky_label = tk.Label(gv.window, image=sky_photo)
sky_label.image = sky_photo
back = tk.Button()
undo = tk.Button(text="↩", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
new_project:ds.Project
new_project_menu_items = []
main_ct = [0]
main_canvas_size = [0]
main_canvas_north_y = [0]
main_xs = []




def proj_bg_pos_generator():
    screen_range = range(1, 1001)
    current_poss = []
    all_poss = []
    for _ in range(1, 21):
        curr_pos = rr.choice(screen_range) / 1000
        while curr_pos in current_poss:
            curr_pos = rr.choice(screen_range) / 1000
        current_poss.append(curr_pos)
        if len(current_poss) == 6:
            current_poss.pop(0)
        all_poss.append(curr_pos)
    return all_poss

def proj_bg_hor():
    global stars
    global star_loop
    stars = []
    logo = Image.open(constants.LOGO_WITH_SKY_ICON)
    x_increase = 1/42
    y_positions = proj_bg_pos_generator()
    speed_range = range(10,601)
    degrees_range = range(1,21)
    idx = 1
    for y in y_positions:
        resizing = rr.choice(range(10, 41))
        logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo)
        logo_label = tk.Button(gv.window, image=logo_photo, relief="flat", bd=0, highlightthickness=0)
        logo_label.image = logo_photo
        logo_label.place(relx=x_increase*idx, rely=y)
        idx += 1
        stars.append((logo_label, x_increase*idx, y, rr.choice(speed_range) / 10000, rr.choice(degrees_range)))
    
    def loop_l():
        for idx, star_comb in enumerate(stars):
            star_comb = list(star_comb)
            star_comb[0].place_forget()
            if star_comb[1] - star_comb[3] <= 0:
                star_comb[1] = 1
                star_comb[3] = rr.choice(speed_range) / 10000
            else:
                star_comb[1] = star_comb[1] - star_comb[3]
            star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
            stars[idx] = tuple(star_comb)
        this_loop = gv.window.after(50, loop_l)
        star_loop[0] = this_loop
        return this_loop

    def loop_r():
        for idx, star_comb in enumerate(stars):
            star_comb = list(star_comb)
            star_comb[0].place_forget()
            if star_comb[1] - star_comb[3] >= 1:
                star_comb[1] = 0
                star_comb[3] = rr.choice(speed_range) / 10000
            else:
                star_comb[1] = star_comb[1] + star_comb[3]
            star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
            stars[idx] = tuple(star_comb)
        this_loop = gv.window.after(50, loop_r)
        star_loop[0] = this_loop
        return this_loop
    
    def start_lstar_loop():
        star_loop[0] = loop_l()

    def start_rstar_loop():
        star_loop[0] = loop_r()
    
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0 :
        start_lstar_loop()
    else:
        start_rstar_loop()

def proj_bg_vert():
    global stars
    global star_loop
    stars = []
    logo = Image.open(constants.LOGO_WITH_SKY_ICON)
    x_positions = proj_bg_pos_generator()
    y_increase = 1/42
    speed_range = range(10,601,1)
    degrees_range = range(1,21)
    idx = 1
    for x in x_positions:
        resizing = rr.choice(range(10, 41))
        logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo)
        logo_label = tk.Button(gv.window, image=logo_photo, relief="flat", bd=0, highlightthickness=0)
        logo_label.image = logo_photo
        logo_label.place(relx=x, rely=y_increase*idx)
        idx += 1
        stars.append((logo_label, x, y_increase*idx, rr.choice(speed_range) / 10000, rr.choice(degrees_range)))
    
    def loop_n():
        for idx, star_comb in enumerate(stars):
            star_comb = list(star_comb)
            star_comb[0].place_forget()
            if star_comb[2] - star_comb[3] <= 0:
                star_comb[2] = 1
                star_comb[3] = rr.choice(speed_range) / 10000
            else:
                star_comb[2] = star_comb[2] - star_comb[3]
            star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
            stars[idx] = tuple(star_comb)
        this_loop = gv.window.after(50, loop_n)
        star_loop[0] = this_loop
        return this_loop
    
    def loop_s():
        for idx, star_comb in enumerate(stars):
            star_comb = list(star_comb)
            star_comb[0].place_forget()
            if star_comb[2] - star_comb[3] >= 1:
                star_comb[2] = 0
                star_comb[3] = rr.choice(speed_range) / 10000
            else:
                star_comb[2] = star_comb[2] + star_comb[3]
            star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
            stars[idx] = tuple(star_comb)
        this_loop = gv.window.after(50, loop_s)
        star_loop[0] = this_loop
        return this_loop
    
    def start_nstar_loop():
        star_loop[0] = loop_n()
    
    def start_sstar_loop():
        star_loop[0] = loop_s()
    
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0 :
        start_nstar_loop()
    else:
        start_sstar_loop()

def forward_blur_animation(radius):
    if radius == 1:
        cntue.place_forget()
        cntue2.place_forget()
        cntue3.place_forget()
        cntue4.place_forget()
        cntue5.place_forget()
        cntue6.place_forget()
        cntue7.place_forget()
        cntue8.place_forget()
        cntue9.place_forget()
    blurred_logo = logo.filter(ImageFilter.GaussianBlur(radius))
    logo_photo = ImageTk.PhotoImage(blurred_logo)
    logo_label.configure(image=logo_photo)
    logo_label.image = logo_photo
    if radius < 6:
        gv.window.after(75, forward_blur_animation, radius + 1)

def backward_blur_animation(radius, back, new_project, old_project):
    global blur_func_calls
    if blur_func_calls == 0:
        play_click()
    if radius == 6:
        back.place_forget()
        new_project.place_forget()
        old_project.place_forget()
    blurred_logo = logo.filter(ImageFilter.GaussianBlur(radius))
    logo_photo = ImageTk.PhotoImage(blurred_logo)
    logo_label.configure(image=logo_photo)
    logo_label.image = logo_photo
    blur_func_calls += 1
    if radius > 0:
        gv.window.after(75, backward_blur_animation, radius - 1, back, new_project, old_project)
    else:
        cntue2.place(relx=0.45, rely=0.3825)
        cntue3.place(relx=0.5075, rely=0.3775)
        cntue4.place(relx=0.4875, rely=0.42, anchor="center")
        cntue5.place(relx=0.52625, rely=0.3825)
        cntue6.place(relx=0.5, rely=0.38875)
        cntue7.place(relx=0.49, rely=0.395)
        cntue8.place(relx=0.515, rely=0.3775)
        cntue9.place(relx=0.435, rely=0.3875)
        cntue.place(relx=0.4875, rely=0.4, anchor="center")
        settings.place(relx=0.87, rely=0.87)
        blur_func_calls = 0

def new_or_old_project_screen():
    try: print(new_project)
    except:pass
    play_click()
    global star_loop
    settings.place_forget()
    try: gv.window.after_cancel(star_loop[0])
    except: pass
    for star_comb in stars:
        star_comb[0].place_forget()
    global new_project_menu_items
    for widget in new_project_menu_items:
        try: widget.place_forget()
        except: pass
    sky_label.pack_forget()
    new_project_menu_items = []
    gv.window.attributes("-fullscreen", False)
    gv.window.geometry("600x600")
    gv.window.configure(bg="#414449")
    forward_blur_animation(1)
    back.configure(bg="#414449", fg="white", text="← Main Menu", font=("Helvetica", 16, "bold"), relief="flat")
    def button_press(event):
        back.config(relief=tk.RAISED)
    back.configure(command=lambda b=back, n=new_project_button, o=old_project_button : backward_blur_animation(6, b, n, o))
    back.bind("<ButtonPress-1>", button_press)
    back.place(relx=0.02, rely=0.02, anchor="nw")
    logo_label.pack()
    new_project_button.configure(command=lambda b=back : new_project_screen(b))
    new_project_button.place(relx=0.5, rely=1/3, anchor="center")
    #old_project_button.configure(command=)
    old_project_button.place(relx=0.5, rely=2/3, anchor="center")

def new_project_screen(back):
    play_click()
    sky_label.pack()
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0:
        proj_bg_hor()
    else:
        proj_bg_vert()
    time_sensitive = [True]
    user_month = tk.StringVar()
    user_month.set("")
    user_day = tk.StringVar()
    user_day.set("")
    user_year = tk.StringVar()
    user_year.set("")
    date_to_complete_label = tk.Label(font=("Helvetica", 18, "bold"), text="Date To Complete*", fg="white", bg="black")
    new_project_menu_items.append(date_to_complete_label)
    years = [str(datetime.today().year+i) for i in range(11)]
    project_month = tk.OptionMenu(gv.window, user_month, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    project_day = tk.OptionMenu(gv.window, user_day, '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st')
    project_year = tk.OptionMenu(gv.window, user_year, *years)
    project_month.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)
    project_day.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)
    project_year.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)

    def time_sensitive_true(a:tk.Button, b:tk.Button):
        play_click()
        time_sensitive[0] = True
        a.configure(relief="sunken")
        b.configure(relief="raised")
        project_month.place(relx=0.5-0.035, rely=4/7, anchor="e")
        project_day.place(relx=0.5, rely=4/7, anchor="center")
        project_year.place(relx=0.5+0.035, rely=4/7, anchor="w")
        date_to_complete_label.place(anchor="s", relx=0.5, rely=(4/7)-0.03)
    def time_sensitive_false(a:tk.Button, b:tk.Button):
        play_click()
        time_sensitive[0] = False
        a.configure(relief="raised")
        b.configure(relief="sunken")
        project_month.place_forget()
        project_day.place_forget()
        project_year.place_forget()
        date_to_complete_label.place_forget()
    
    project_time_sensitive_y = tk.Button()
    project_time_sensitive_n = tk.Button()
    logo_label.pack_forget()
    new_project_button.place_forget()
    old_project_button.place_forget()
    gv.window.attributes("-fullscreen", True)
    name_label = tk.Label(font=("Helvetica", 18, "bold"), text="Project Name*", fg="white", bg="black")
    name_label.place(anchor="s", relx=0.5, rely=(1/7)-0.03)
    project_name = tk.Entry(gv.window, validate="key", validatecommand=(char_limit_cmd, "%P"), font=("Helvetica", 18))
    project_name.place(relx=0.5, rely=1/7, anchor="center")
    new_project_menu_items.append(name_label)
    new_project_menu_items.append(project_name)
    description_label = tk.Label(font=("Helvetica", 18, "bold"), text="Project Description", fg="white", bg="black")
    description_label.place(anchor="s", relx=0.5, rely=(2/7)-0.03)
    project_description = tk.Entry(font=("Helvetica", 18))
    project_description.place(relx=0.5, rely=2/7, anchor="center")
    new_project_menu_items.append(project_description)
    new_project_menu_items.append(description_label)
    time_sensitive_label = tk.Label(font=("Helvetica", 18, "bold"), text="Time Sensitive?*", fg="white", bg="black")
    time_sensitive_label.place(anchor="s", relx=0.5, rely=(3/7)-0.03)
    project_time_sensitive_y.configure(bg="green", text="YES", font=("Helvetica", 18))
    project_time_sensitive_y.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_true(a,b))
    project_time_sensitive_y.place(relx=0.5-0.00975, rely=3/7, anchor="e")
    new_project_menu_items.append(project_time_sensitive_y)
    project_time_sensitive_n.configure(bg="red", text="NO", font=("Helvetica", 18))
    project_time_sensitive_n.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_false(a,b))
    project_time_sensitive_n.place(relx=0.5+0.00975, rely=3/7, anchor="w")
    new_project_menu_items.append(project_time_sensitive_n)
    new_project_menu_items.append(time_sensitive_label)
    project_month.place(relx=0.5-0.035, rely=4/7, anchor="e")
    new_project_menu_items.append(project_month)
    project_day.place(relx=0.5, rely=4/7, anchor="center")
    new_project_menu_items.append(project_day)
    project_year.place(relx=0.5+0.035, rely=4/7, anchor="w")
    new_project_menu_items.append(project_year)
    notes_label = tk.Label(font=("Helvetica", 18, "bold"), text="Notes", fg="white", bg="black")
    notes_label.place(anchor="s", relx=0.5, rely=(5/7)-0.03)
    project_notes = tk.Entry(font=("Helvetica", 18))
    project_notes.place(relx=0.5, rely=5/7, anchor="center")
    new_project_menu_items.append(notes_label)
    new_project_menu_items.append(project_notes)
    project_submit = tk.Button(font=("Helvetica", 25, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    project_submit.configure(command=lambda na=project_name, dsc=project_description, ts=time_sensitive, yr=user_year, mo=user_month, day=user_day, rq=project_notes : new_project_submit(na, dsc, ts, yr, mo, day, rq))
    project_submit.place(relx=0.5, rely=6/7, anchor="center")
    new_project_menu_items.append(project_submit)
    time_sensitive_true(project_time_sensitive_y, project_time_sensitive_n)
    back.configure(command=new_or_old_project_screen, text="← Main Menu", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
    back.place(relx=0.002*9, rely=0.002*16, anchor="nw")
    back.tkraise()

def new_project_submit(name, description, time_sensitive, date_year, date_month, date_day, notes):
    global new_project
    play_click()
    if name.get() == "":
        messagebox.showerror("No Project Name", "Please enter a project name.")
        return
    
    try:
        date_mo = determine_month(date_month.get())
        date_dy = determine_day(date_day.get())
    except:
        if time_sensitive[0] == True:
            messagebox.showerror("No Project Date", "Please enter a project date.")
        else:
            pass

    new_date = date_mo + "/" + date_dy + "/" + date_year.get()
    
    if time_sensitive[0] == True:
        if not ds.Project.date_after_current(date(int(date_year.get()), int(date_mo), int(date_dy))):
            messagebox.showerror("Invalid Date", "Date entered is before or equal to the date today.")
            return
    
    try:
        new_project = ds.Project(name.get(), description.get(), time_sensitive[0], new_date, notes.get())
    except ValueError:
        new_project = ds.Project(name.get(), description.get(), False, None, notes.get())

    for widget in new_project_menu_items:
        widget.place_forget()
    
    canvas = tk.Canvas(gv.window, width=665, height=315, bd=0, highlightthickness=0, bg="black")
    canvas.place(anchor="n", relx=0.5, rely=0)
    canvas.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
    canvas.create_oval(7.5, 7.5, 650, 300, fill="#abcaf6", outline="white", width=3)
    Lproject_name = tk.Label(text=new_project.name, bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    if len(new_project.name) <= 17:
        Lproject_name.configure(font=("Helvetica", 50, "bold"))
        Lproject_name.place(anchor="n", relx=0.5, rely=0.1175)
    elif len(new_project.name) <= 30:
        Lproject_name.configure(font=("Helvetica", 32, "bold"))
        Lproject_name.place(anchor="n", relx=0.5, rely=0.13125)
    
    Lproject_desc = tk.Label(text=new_project.description, font=("Helvetica", 14, "bold"), bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    Lproject_desc.place(anchor="n", relx=0.5, rely=0.225)
    Lproject_days_left = tk.Label(font=("Helvetica", 22, "bold"), bg="#abcaf6", fg="red", bd=0, highlightthickness=0)
    Lproject_days_left.configure(text=f"{new_project.calculate_days_left()} DAYS LEFT") 
    Lproject_days_left.place(anchor="n", relx=0.5, rely=0.06875)

    Lproject_notes = tk.Label(text=new_project.notes, font=("Helvetica", 14, "bold"), bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    new_project_menu_items.append(canvas)
    new_project_menu_items.append(Lproject_name)
    new_project_menu_items.append(Lproject_desc)
    new_project_menu_items.append(Lproject_days_left)
    new_project_menu_items.append(Lproject_notes)

    canvas1 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label1 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    main_name1 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    main_create1 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas2 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label2 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    main_name2 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    main_create2 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas3 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label3 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    main_name3 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    main_create3 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas4 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label4 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    main_name4 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    main_create4 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas5 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label5 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    main_name5 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    main_create5 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    one = tk.Button(text="1", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    two = tk.Button(text="2", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    three = tk.Button(text="3", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    four = tk.Button(text="4", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    five = tk.Button(text="5", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    new_project_menu_items.append(one)
    new_project_menu_items.append(two)
    new_project_menu_items.append(three)
    new_project_menu_items.append(four)
    new_project_menu_items.append(five)

    main_items = []
    def how_many_mains():
        play_click()
        one.configure(command=lambda n=1 : build_mains(n))
        two.configure(command=lambda n=2 : build_mains(n))
        three.configure(command=lambda n=3 : build_mains(n))
        four.configure(command=lambda n=4 : build_mains(n))
        five.configure(command=lambda n=5 : build_mains(n))
        one.place(anchor="e", relx=0.5095-0.038, rely=0.5)
        two.place(anchor="e", relx=0.5095-0.019, rely=0.5)
        three.place(anchor="center", relx=0.5, rely=0.5)
        four.place(anchor="e", relx=0.5095+0.019, rely=0.5)
        five.place(anchor="e", relx=0.5095+0.038, rely=0.5)
    
    def build_mains(num:int):
        play_click()
        plus.place_forget()
        one.place_forget()
        two.place_forget()
        three.place_forget()
        four.place_forget()
        five.place_forget()
        undo.place(anchor="nw", relx=0.0145*9, rely=0.002*16)
        undo.tkraise()
        new_project_menu_items.append(undo)
        YOFF = 0.05
        if num == 1:
            main_canvas_size[0] = 255
            main_canvas_north_y[0] = 0.4-YOFF
            main_xs.append([0.5])
            canvas1.configure(width=415, height=255)
            canvas1.place(anchor="n", relx=0.5, rely=0.4-YOFF)
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label1.place(anchor="s", relx=0.5, rely=0.4475-YOFF)
            main_name1.place(anchor="s", relx=0.5, rely=0.48-YOFF)
            main_create1.configure(command=lambda p=new_project, n=main_name1, l=name_label1, c=main_create1 : create_new_main(p, n, l, c, 1/2))
            main_create1.place(anchor="s", relx=0.5, rely=0.6125-YOFF)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(main_name1)
            new_project_menu_items.append(main_create1)
            main_items.append(canvas1)
            main_items.append(name_label1)
            main_items.append(main_name1)
            main_items.append(main_create1)
        elif num == 2:
            main_canvas_size[0] = 255
            main_canvas_north_y[0] = 0.4-YOFF
            main_xs.append([1/3, 2/3])
            canvas1.configure(width=415, height=255)
            canvas1.place(anchor="n", relx=1/3, rely=0.4-YOFF)
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label1.place(anchor="s", relx=1/3, rely=0.4475-YOFF)
            main_name1.place(anchor="s", relx=1/3, rely=0.48-YOFF)
            main_create1.configure(command=lambda p=new_project, n=main_name1, l=name_label1, c=main_create1 : create_new_main(p, n, l, c, 1/3))
            main_create1.place(anchor="s", relx=1/3, rely=0.6125-YOFF)
            canvas2.configure(width=415, height=255)
            canvas2.place(anchor="n", relx=2/3, rely=0.4-YOFF)
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label2.place(anchor="s", relx=2/3, rely=0.4475-YOFF)
            main_name2.place(anchor="s", relx=2/3, rely=0.48-YOFF)
            main_create2.configure(command=lambda p=new_project, n=main_name2, l=name_label2, c=main_create2 : create_new_main(p, n, l, c, 2/3))
            main_create2.place(anchor="s", relx=2/3, rely=0.6125-YOFF)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(main_name1)
            new_project_menu_items.append(main_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(main_name2)
            new_project_menu_items.append(main_create2)
            main_items.append(canvas1)
            main_items.append(name_label1)
            main_items.append(main_name1)
            main_items.append(main_create1)
            main_items.append(canvas2)
            main_items.append(name_label2)
            main_items.append(main_name2)
            main_items.append(main_create2)
        elif num == 3:
            main_canvas_size[0] = 255
            main_canvas_north_y[0] = 0.4-YOFF
            main_xs.append([1/4, 2/4, 3/4])
            canvas1.configure(width=415, height=255)
            canvas1.place(anchor="n", relx=1/4, rely=0.4-YOFF)
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label1.place(anchor="s", relx=1/4, rely=0.4475-YOFF)
            main_name1.place(anchor="s", relx=1/4, rely=0.48-YOFF)
            main_create1.configure(command=lambda p=new_project, n=main_name1, l=name_label1, c=main_create1 : create_new_main(p, n, l, c, 1/4))
            main_create1.place(anchor="s", relx=1/4, rely=0.6125-YOFF)
            canvas2.configure(width=415, height=255)
            canvas2.place(anchor="n", relx=2/4, rely=0.4-YOFF)
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label2.place(anchor="s", relx=2/4, rely=0.4475-YOFF)
            main_name2.place(anchor="s", relx=2/4, rely=0.48-YOFF)
            main_create2.configure(command=lambda p=new_project, n=main_name2, l=name_label2, c=main_create2 : create_new_main(p, n, l, c, 2/4))
            main_create2.place(anchor="s", relx=2/4, rely=0.6125-YOFF)
            canvas3.configure(width=415, height=255)
            canvas3.place(anchor="n", relx=3/4, rely=0.4-YOFF)
            canvas3.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas3.create_oval(7.5, 7.5, 400, 240, fill="#abcaf6", outline="white", width=2)
            name_label3.place(anchor="s", relx=3/4, rely=0.4475-YOFF)
            main_name3.place(anchor="s", relx=3/4, rely=0.48-YOFF)
            main_create3.configure(command=lambda p=new_project, n=main_name3, l=name_label3, c=main_create3 : create_new_main(p, n, l, c, 3/4))
            main_create3.place(anchor="s", relx=3/4, rely=0.6125-YOFF)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(main_name1)
            new_project_menu_items.append(main_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(main_name2)
            new_project_menu_items.append(main_create2)
            new_project_menu_items.append(canvas3)
            new_project_menu_items.append(name_label3)
            new_project_menu_items.append(main_name3)
            new_project_menu_items.append(main_create3)
            main_items.append(canvas1)
            main_items.append(name_label1)
            main_items.append(main_name1)
            main_items.append(main_create1)
            main_items.append(canvas2)
            main_items.append(name_label2)
            main_items.append(main_name2)
            main_items.append(main_create2)
            main_items.append(canvas3)
            main_items.append(name_label3)
            main_items.append(main_name3)
            main_items.append(main_create3)
        elif num == 4:
            main_canvas_size[0] = 225
            main_canvas_north_y[0] = 0.4-YOFF
            main_xs.append([1/5, 2/5, 3/5, 4/5])
            canvas1.configure(width=365, height=225)
            canvas1.place(anchor="n", relx=1/5, rely=0.4-YOFF)
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 350, 210, fill="#abcaf6", outline="white", width=2)
            name_label1.place(anchor="s", relx=1/5, rely=0.4475-YOFF)
            main_name1.place(anchor="s", relx=1/5, rely=0.48-YOFF)
            main_create1.configure(command=lambda p=new_project, n=main_name1, l=name_label1, c=main_create1 : create_new_main(p, n, l, c, 1/5))
            main_create1.place(anchor="s", relx=1/5, rely=0.5875-YOFF)
            canvas2.configure(width=365, height=225)
            canvas2.place(anchor="n", relx=2/5, rely=0.4-YOFF)
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 350, 210, fill="#abcaf6", outline="white", width=2)
            name_label2.place(anchor="s", relx=2/5, rely=0.4475-YOFF)
            main_name2.place(anchor="s", relx=2/5, rely=0.48-YOFF)
            main_create2.configure(command=lambda p=new_project, n=main_name2, l=name_label2, c=main_create2 : create_new_main(p, n, l, c, 2/5))
            main_create2.place(anchor="s", relx=2/5, rely=0.5875-YOFF)
            canvas3.configure(width=365, height=225)
            canvas3.place(anchor="n", relx=3/5, rely=0.4-YOFF)
            canvas3.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas3.create_oval(7.5, 7.5, 350, 210, fill="#abcaf6", outline="white", width=2)
            name_label3.place(anchor="s", relx=3/5, rely=0.4475-YOFF)
            main_name3.place(anchor="s", relx=3/5, rely=0.48-YOFF)
            main_create3.configure(command=lambda p=new_project, n=main_name3, l=name_label3, c=main_create3 : create_new_main(p, n, l, c, 3/5))
            main_create3.place(anchor="s", relx=3/5, rely=0.5875-YOFF)
            canvas4.configure(width=365, height=225)
            canvas4.place(anchor="n", relx=4/5, rely=0.4-YOFF)
            canvas4.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas4.create_oval(7.5, 7.5, 350, 210, fill="#abcaf6", outline="white", width=2)
            name_label4.place(anchor="s", relx=4/5, rely=0.4475-YOFF)
            main_name4.place(anchor="s", relx=4/5, rely=0.48-YOFF)
            main_create4.configure(command=lambda p=new_project, n=main_name4, l=name_label4, c=main_create4 : create_new_main(p, n, l, c, 4/5))
            main_create4.place(anchor="s", relx=4/5, rely=0.5875-YOFF)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(main_name1)
            new_project_menu_items.append(main_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(main_name2)
            new_project_menu_items.append(main_create2)
            new_project_menu_items.append(canvas3)
            new_project_menu_items.append(name_label3)
            new_project_menu_items.append(main_name3)
            new_project_menu_items.append(main_create3)
            new_project_menu_items.append(canvas4)
            new_project_menu_items.append(name_label4)
            new_project_menu_items.append(main_name4)
            new_project_menu_items.append(main_create4)
            main_items.append(canvas1)
            main_items.append(name_label1)
            main_items.append(main_name1)
            main_items.append(main_create1)
            main_items.append(canvas2)
            main_items.append(name_label2)
            main_items.append(main_name2)
            main_items.append(main_create2)
            main_items.append(canvas3)
            main_items.append(name_label3)
            main_items.append(main_name3)
            main_items.append(main_create3)
            main_items.append(canvas4)
            main_items.append(name_label4)
            main_items.append(main_name4)
            main_items.append(main_create4)
        elif num == 5:
            main_canvas_size[0] = 195
            main_canvas_north_y[0] = 0.4-YOFF
            main_xs.append([1/6, 2/6, 3/6, 4/6, 5/6])
            canvas1.configure(width=315, height=195)
            canvas1.place(anchor="n", relx=1/6, rely=0.4-YOFF)
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_label1.place(anchor="s", relx=1/6, rely=0.4475-YOFF)
            main_name1.place(anchor="s", relx=1/6, rely=0.48-YOFF)
            main_create1.configure(command=lambda p=new_project, n=main_name1, l=name_label1, c=main_create1 : create_new_main(p, n, l, c, 1/6))
            main_create1.place(anchor="s", relx=1/6, rely=0.5575-YOFF)
            canvas2.configure(width=315, height=195)
            canvas2.place(anchor="n", relx=2/6, rely=0.4-YOFF)
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_label2.place(anchor="s", relx=2/6, rely=0.4475-YOFF)
            main_name2.place(anchor="s", relx=2/6, rely=0.48-YOFF)
            main_create2.configure(command=lambda p=new_project, n=main_name2, l=name_label2, c=main_create2 : create_new_main(p, n, l, c, 2/6))
            main_create2.place(anchor="s", relx=2/6, rely=0.5575-YOFF)
            canvas3.configure(width=315, height=195)
            canvas3.place(anchor="n", relx=3/6, rely=0.4-YOFF)
            canvas3.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas3.create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_label3.place(anchor="s", relx=3/6, rely=0.4475-YOFF)
            main_name3.place(anchor="s", relx=3/6, rely=0.48-YOFF)
            main_create3.configure(command=lambda p=new_project, n=main_name3, l=name_label3, c=main_create3 : create_new_main(p, n, l, c, 3/6))
            main_create3.place(anchor="s", relx=3/6, rely=0.5575-YOFF)
            canvas4.configure(width=315, height=195)
            canvas4.place(anchor="n", relx=4/6, rely=0.4-YOFF)
            canvas4.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas4.create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_label4.place(anchor="s", relx=4/6, rely=0.4475-YOFF)
            main_name4.place(anchor="s", relx=4/6, rely=0.48-YOFF)
            main_create4.configure(command=lambda p=new_project, n=main_name4, l=name_label4, c=main_create4 : create_new_main(p, n, l, c, 4/6))
            main_create4.place(anchor="s", relx=4/6, rely=0.5575-YOFF)
            canvas5.configure(width=315, height=195)
            canvas5.place(anchor="n", relx=5/6, rely=0.4-YOFF)
            canvas5.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas5.create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_label5.place(anchor="s", relx=5/6, rely=0.4475-YOFF)
            main_name5.place(anchor="s", relx=5/6, rely=0.48-YOFF)
            main_create5.configure(command=lambda p=new_project, n=main_name5, l=name_label5, c=main_create5 : create_new_main(p, n, l, c, 5/6))
            main_create5.place(anchor="s", relx=5/6, rely=0.5575-YOFF)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(main_name1)
            new_project_menu_items.append(main_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(main_name2)
            new_project_menu_items.append(main_create2)
            new_project_menu_items.append(canvas3)
            new_project_menu_items.append(name_label3)
            new_project_menu_items.append(main_name3)
            new_project_menu_items.append(main_create3)
            new_project_menu_items.append(canvas4)
            new_project_menu_items.append(name_label4)
            new_project_menu_items.append(main_name4)
            new_project_menu_items.append(main_create4)
            new_project_menu_items.append(canvas5)
            new_project_menu_items.append(name_label5)
            new_project_menu_items.append(main_name5)
            new_project_menu_items.append(main_create5)
            main_items.append(canvas1)
            main_items.append(name_label1)
            main_items.append(main_name1)
            main_items.append(main_create1)
            main_items.append(canvas2)
            main_items.append(name_label2)
            main_items.append(main_name2)
            main_items.append(main_create2)
            main_items.append(canvas3)
            main_items.append(name_label3)
            main_items.append(main_name3)
            main_items.append(main_create3)
            main_items.append(canvas4)
            main_items.append(name_label4)
            main_items.append(main_name4)
            main_items.append(main_create4)
            main_items.append(canvas5)
            main_items.append(name_label5)
            main_items.append(main_name5)
            main_items.append(main_create5)
        main_ct[0] = num

    def clear_mains():
        for widget in main_items:
            widget.place_forget()
        undo.place_forget()
        plus.place(anchor="n", relx=0.5, rely=0.4)
    
    undo.configure(command=clear_mains)

    plus = tk.Button(text="➕", font=("Helvetica", 16, "bold"), bd=0, highlightthickness=0, bg="black", fg="white")
    plus.configure(command=how_many_mains)
    plus.place(anchor="n", relx=0.5, rely=0.4)
    new_project_menu_items.append(plus)

def create_new_main(project:ds.Project, name:tk.Entry, label, create, relx):
    sub_items = []
    play_click()
    if name.get() == "":
        messagebox.showerror("No Main Name", "Please enter a project name.")
        return None
    YOFF = 0.05
    new_main = project.add_main(name.get())
    main_name_label = tk.Label(font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center")
    new_project_menu_items.append(main_name_label)
    main_name_label.configure(text=name.get())
    try:
        label.destroy()
        name.destroy()
        create.destroy()
    except:
        return None
    main_name_label.place(anchor="center", relx=relx, rely=0.48-YOFF)
    one_main = tk.Button(text="1", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    two_main = tk.Button(text="2", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    three_main = tk.Button(text="3", font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black")
    new_project_menu_items.append(one_main)
    new_project_menu_items.append(two_main)
    new_project_menu_items.append(three_main)
    canvas1 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label1 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name1 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    sub_create1 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas2 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label2 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name2 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    sub_create2 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas3 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label3 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name3 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center")
    sub_create3 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    sub_create = tk.Button(text="➕", font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, bg="black", fg="white")
    def how_many_subs():
        play_click()
        one_main.configure(command=lambda n=1 : build_subs(n))
        two_main.configure(command=lambda n=2 : build_subs(n))
        three_main.configure(command=lambda n=3 : build_subs(n))
        one_main.place(anchor="e", relx=relx-0.01, rely=0.765-0.0425)
        two_main.place(anchor="center", relx=relx, rely=0.765-0.0425)
        three_main.place(anchor="w", relx=relx+0.01, rely=0.765-0.0425)
    def build_subs(num:int):
        play_click()
        sub_create.place_forget()
        one_main.place_forget()
        two_main.place_forget()
        three_main.place_forget()
        undo.place(anchor="nw", relx=0.0145*9, rely=0.002*16)
        undo.tkraise()
        new_project_menu_items.append(undo)
        YOFF = 0.05
        if num == 1:
            canvas1.configure(width=240, height=150)
            canvas1.place(anchor="center", relx=relx, rely=calc_dist2(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 225, 135, fill="#abcaf6", outline="white", width=2)
            sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/2))
            name_label1.place(anchor="center", relx=relx, rely=0.765+0.0315)
            sub_name1.place(anchor="center", relx=relx, rely=0.765+0.0515)
            sub_create1.place(anchor="center", relx=relx, rely=0.765+0.15235)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(sub_name1)
            new_project_menu_items.append(sub_create1)
            sub_items.append(canvas1)
            sub_items.append(name_label1)
            sub_items.append(sub_name1)
            sub_items.append(sub_create1)
        elif num == 2:
            if main_ct[0] < 5:
                canvas1.configure(width=192, height=120)
                canvas1.place(anchor="center", relx=relx-0.05, rely=calc_dist2(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas1.create_oval(7.5, 7.5, 177, 105, fill="#abcaf6", outline="white", width=2)
                sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
                name_label1.place(anchor="center", relx=relx-0.05, rely=0.765+0.0315)
                sub_name1.place(anchor="center", relx=relx-0.05, rely=0.765+0.0515)
                sub_create1.place(anchor="center", relx=relx-0.05, rely=0.765+0.15235)
                canvas2.configure(width=192, height=120)
                canvas2.place(anchor="center", relx=relx+0.05, rely=calc_dist2(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas2.create_oval(7.5, 7.5, 177, 105, fill="#abcaf6", outline="white", width=2)
                sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
                name_label2.place(anchor="center", relx=relx+0.05, rely=0.765+0.0315)
                sub_name2.place(anchor="center", relx=relx+0.05, rely=0.765+0.0515)
                sub_create2.place(anchor="center", relx=relx+0.05, rely=0.765+0.15235)
            elif main_ct[0] == 5:
                canvas1.configure(width=159, height=105)
                canvas1.place(anchor="center", relx=relx-0.04, rely=calc_dist2(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas1.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
                sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
                name_label1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0315)
                sub_name1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0515)
                sub_create1.place(anchor="center", relx=relx-0.04, rely=0.765+0.15235)
                canvas2.configure(width=159, height=105)
                canvas2.place(anchor="center", relx=relx+0.04, rely=calc_dist2(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas2.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
                sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
                name_label2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0315)
                sub_name2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0515)
                sub_create2.place(anchor="center", relx=relx+0.04, rely=0.765+0.15235)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(sub_name1)
            new_project_menu_items.append(sub_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(sub_name2)
            new_project_menu_items.append(sub_create2)
            sub_items.append(canvas1)
            sub_items.append(name_label1)
            sub_items.append(sub_name1)
            sub_items.append(sub_create1)
            sub_items.append(canvas2)
            sub_items.append(name_label2)
            sub_items.append(sub_name2)
            sub_items.append(sub_create2)
        elif num == 3:
            canvas1.configure(width=159, height=105)
            canvas1.place(anchor="center", relx=relx-0.04, rely=calc_dist3(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
            name_label1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0315)
            sub_name1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0515)
            sub_create1.place(anchor="center", relx=relx-0.04, rely=0.765+0.15235)
            canvas2.configure(width=159, height=105)
            canvas2.place(anchor="center", relx=relx+0.04, rely=calc_dist3(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
            name_label2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0315)
            sub_name2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0515)
            sub_create2.place(anchor="center", relx=relx+0.04, rely=0.765+0.15235)
            canvas3.configure(width=159, height=105)
            canvas3.place(anchor="center", relx=relx, rely=calc_dist23(get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas3.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas3.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create3.configure(command=lambda m=new_main, n=sub_name3, l=name_label3, c=sub_create3 : create_new_sub(m, n, l, c, 1/3))
            name_label3.place(anchor="center", relx=relx, rely=0.765+0.0315)
            sub_name3.place(anchor="center", relx=relx, rely=0.765+0.0515)
            sub_create3.place(anchor="center", relx=relx, rely=0.765+0.15235)
            new_project_menu_items.append(canvas1)
            new_project_menu_items.append(name_label1)
            new_project_menu_items.append(sub_name1)
            new_project_menu_items.append(sub_create1)
            new_project_menu_items.append(canvas2)
            new_project_menu_items.append(name_label2)
            new_project_menu_items.append(sub_name2)
            new_project_menu_items.append(sub_create2)
            new_project_menu_items.append(canvas3)
            new_project_menu_items.append(name_label3)
            new_project_menu_items.append(sub_name3)
            new_project_menu_items.append(sub_create3)
            sub_items.append(canvas1)
            sub_items.append(name_label1)
            sub_items.append(sub_name1)
            sub_items.append(sub_create1)
            sub_items.append(canvas2)
            sub_items.append(name_label2)
            sub_items.append(sub_name2)
            sub_items.append(sub_create2)
            sub_items.append(canvas3)
            sub_items.append(name_label3)
            sub_items.append(sub_name3)
            sub_items.append(sub_create3)
    sub_create.configure(command=how_many_subs)
    sub_create.place(anchor="center", relx=relx, rely=0.765)
    new_project_menu_items.append(sub_create)
    return new_main

def create_new_sub(main:ds.Main, name_entry:tk.Entry):
    play_click()
    new_sub = main.add_main(name_entry.get())
    print(new_sub)

def exploded_view():
    #Create view for exploded view of any project/main/sub
    pass

def edit_details():
    #Create UI for editing (exploded view) and edit details of project/main/sub
    pass

def add_notes():
    #Create UI for notetaking on project/main/sub and add to project/main/sub
    pass

def process_data():
    #Goes through Previous User JSONs with Project Data and puts it into a format where the file can be edited
    pass

def old_project_list_screen():
    #Create UI for saved projects screen by accessing User Projects folder
    pass

def open_project():
    #Create UI for created project by reading json file
    pass

cntue2 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
cntue3 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
cntue4 = tk.Button(bg="#e4eff6", font=("Times New Roman", 10, "bold"), bd=0, highlightthickness=0)
cntue5 = tk.Button(bg="#e4eff6", font=("Times New Roman", 6, "bold"), bd=0, highlightthickness=0)
cntue6 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
cntue7 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
cntue8 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
cntue9 = tk.Button(bg="#e4eff6", font=("Times New Roman", 6, "bold"), bd=0, highlightthickness=0)
cntue2.configure(command=new_or_old_project_screen)
cntue3.configure(command=new_or_old_project_screen)
cntue4.configure(command=new_or_old_project_screen)
cntue5.configure(command=new_or_old_project_screen)
cntue6.configure(command=new_or_old_project_screen)
cntue7.configure(command=new_or_old_project_screen)
cntue8.configure(command=new_or_old_project_screen)
cntue9.configure(command=new_or_old_project_screen)
cntue2.place(relx=0.45, rely=0.3825)
cntue3.place(relx=0.5075, rely=0.3775)
cntue4.place(relx=0.4875, rely=0.42, anchor="center")
cntue5.place(relx=0.52625, rely=0.3825)
cntue6.place(relx=0.5, rely=0.38875)
cntue7.place(relx=0.49, rely=0.395)
cntue8.place(relx=0.515, rely=0.3775)
cntue9.place(relx=0.43975, rely=0.3875)
cntue = tk.Button(text="▶", bg="#e4eff6", bd=0, highlightthickness=0, font=("Helvetica", 16, "bold"), height=0)
cntue.configure(command=new_or_old_project_screen)
cntue.place(relx=0.49, rely=0.4, anchor="center")
settings = tk.Button(text="⚙️", bg="#414449", bd=0, highlightthickness=0, font=("Helvetica", 26), height=0, fg="white")
settings.place(relx=0.87, rely=0.87)
new_project_button = tk.Button(text="New Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)
old_project_button = tk.Button(text="Open Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)

gv.window.mainloop()