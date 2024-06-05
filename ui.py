from PIL import ImageTk, Image
from datetime import datetime, date
from tkinter import messagebox
import globalvariables as gv
import animations as anim
import tkinter as tk
import random as rr
import constants
import fileutil
import sounds
import uiutil
import ds

gv.window.title("FlowNote")
width = 600
height = 600
horiz_offset = (gv.window.winfo_screenwidth() - width) / 2
vert_offset = (gv.window.winfo_screenheight() - height) / 2
gv.window.geometry(f"{width}x{height}+{int(horiz_offset)}+{int(vert_offset)}")
gv.window.resizable(width=False, height=False)
gv.window.configure(bg="#414449")
gv.window.bind("<Escape>", quit)
char2 = gv.window.register((lambda text: (True if len(text) <= 2 else False)))
char15 = gv.window.register((lambda text: (True if len(text) <= 15 else False)))
char30 = gv.window.register((lambda text: (True if len(text) <= 30 else False)))
char100 = gv.window.register((lambda text: (True if len(text) <= 100 else False)))

transparent_image = Image.open(constants.ACTUALLY_TRANSPARENT_ICON)
transparent_photo = ImageTk.PhotoImage(transparent_image)
sky = Image.open(constants.SKY_ICON)
sky = sky.resize((1920, 1080), Image.Resampling.LANCZOS)
sky_photo = ImageTk.PhotoImage(sky)
sky_mini = Image.open(constants.SKY_ICON)
sky_mini_photo = ImageTk.PhotoImage(sky_mini)
sky_label = tk.Label(gv.window, image=sky_photo)
sky_label.image = sky_photo
back = tk.Button()
undo = tk.Button(text="↩", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
np_menu_items = []
main_ct = [0]
main_canvas_size = []
main_canvas_north_y = [0]
main_xs = []
main_cys = []

new_project_button = tk.Button(text="New Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)
old_project_button = tk.Button(text="Open Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)



def project_select_screen() -> None:
    global np_menu_items

    try: 
        gv.window.after_cancel(gv.star_loop[0])
    except: 
        pass

    for star_comb in gv.stars:
        star_comb[0].destroy()
    for widget in np_menu_items:
        try: 
            widget.place_forget()
        except: 
            pass

    sounds.play_click()
    sky_label.pack_forget()
    np_menu_items = []

    gv.window.attributes("-fullscreen", False)
    gv.window.geometry("600x600")
    gv.window.configure(bg="#414449")
    anim.forward_blur_animation(1)
    back.configure(bg="#414449", fg="white", text="← Main Menu", font=("Helvetica", 16, "bold"), relief="flat")
    back.configure(command=lambda b=back, n=new_project_button, o=old_project_button : anim.backward_blur_animation(6, b, n, o))
    back.place(relx=0.02, rely=0.02, anchor="nw")
    gv.logo_label.pack()
    new_project_button.configure(command=lambda b=back : new_project_screen(b))
    new_project_button.place(relx=0.5, rely=1/3, anchor="center")
    old_project_button.place(relx=0.5, rely=2/3, anchor="center")

def new_project_screen(back:tk.Button) -> None:
    sounds.play_click()
    sky_label.pack()
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0:
        anim.proj_bg_hor()
    else:
        anim.proj_bg_vert()
    time_sensitive = [True]
    user_month = tk.StringVar()
    user_month.set("")
    user_day = tk.StringVar()
    user_day.set("")
    user_year = tk.StringVar()
    user_year.set("")
    date_to_complete_label = tk.Label(font=("Helvetica", 18, "bold"), text="Date To Complete*", fg="white", bg="black")
    np_menu_items.append(date_to_complete_label)
    years = [str(datetime.today().year+i) for i in range(11)]
    project_month = tk.OptionMenu(gv.window, user_month, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    project_day = tk.OptionMenu(gv.window, user_day, '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st')
    project_year = tk.OptionMenu(gv.window, user_year, *years)
    project_month.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)
    project_day.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)
    project_year.configure(font=("Helvetica", 18), bd=0, highlightthickness=0)

    def time_sensitive_true(a:tk.Button, b:tk.Button) -> None:
        sounds.play_click()
        time_sensitive[0] = True
        a.configure(relief="sunken")
        b.configure(relief="raised")
        project_month.place(relx=0.5-0.035, rely=4/7, anchor="e")
        project_day.place(relx=0.5, rely=4/7, anchor="center")
        project_year.place(relx=0.5+0.035, rely=4/7, anchor="w")
        date_to_complete_label.place(anchor="s", relx=0.5, rely=(4/7)-0.03)
    def time_sensitive_false(a:tk.Button, b:tk.Button) -> None:
        sounds.play_click()
        time_sensitive[0] = False
        a.configure(relief="raised")
        b.configure(relief="sunken")
        project_month.place_forget()
        project_day.place_forget()
        project_year.place_forget()
        date_to_complete_label.place_forget()
    
    project_time_sensitive_y = tk.Button()
    project_time_sensitive_n = tk.Button()
    gv.logo_label.pack_forget()
    new_project_button.place_forget()
    old_project_button.place_forget()
    gv.window.attributes("-fullscreen", True)
    name_label = tk.Label(font=("Helvetica", 18, "bold"), text="Project Name*", fg="white", bg="black")
    name_label.place(anchor="s", relx=0.5, rely=(1/7)-0.03)
    project_name = tk.Entry(gv.window, validate="key", validatecommand=(char30, "%P"), font=("Helvetica", 18))
    project_name.place(relx=0.5, rely=1/7, anchor="center")
    np_menu_items.append(name_label)
    np_menu_items.append(project_name)
    description_label = tk.Label(font=("Helvetica", 18, "bold"), text="Project Description", fg="white", bg="black")
    description_label.place(anchor="s", relx=0.5, rely=(2/7)-0.03)
    project_description = tk.Entry(font=("Helvetica", 18), validate="key", validatecommand=(char100, "%P"))
    project_description.place(relx=0.5, rely=2/7, anchor="center")
    np_menu_items.append(project_description)
    np_menu_items.append(description_label)
    time_sensitive_label = tk.Label(font=("Helvetica", 18, "bold"), text="Time Sensitive?*", fg="white", bg="black")
    time_sensitive_label.place(anchor="s", relx=0.5, rely=(3/7)-0.03)
    project_time_sensitive_y.configure(bg="green", text="YES", font=("Helvetica", 18))
    project_time_sensitive_y.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_true(a,b))
    project_time_sensitive_y.place(relx=0.5-0.00975, rely=3/7, anchor="e")
    np_menu_items.append(project_time_sensitive_y)
    project_time_sensitive_n.configure(bg="red", text="NO", font=("Helvetica", 18))
    project_time_sensitive_n.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_false(a,b))
    project_time_sensitive_n.place(relx=0.5+0.00975, rely=3/7, anchor="w")
    np_menu_items.append(project_time_sensitive_n)
    np_menu_items.append(time_sensitive_label)
    project_month.place(relx=0.5-0.035, rely=4/7, anchor="e")
    np_menu_items.append(project_month)
    project_day.place(relx=0.5, rely=4/7, anchor="center")
    np_menu_items.append(project_day)
    project_year.place(relx=0.5+0.035, rely=4/7, anchor="w")
    np_menu_items.append(project_year)
    notes_label = tk.Label(font=("Helvetica", 18, "bold"), text="Notes", fg="white", bg="black")
    notes_label.place(anchor="s", relx=0.5, rely=(5/7)-0.03)
    project_notes = tk.Entry(font=("Helvetica", 18), validate="key", validatecommand=(char100, "%P"))
    project_notes.place(relx=0.5, rely=5/7, anchor="center")
    np_menu_items.append(notes_label)
    np_menu_items.append(project_notes)
    project_submit = tk.Button(font=("Helvetica", 25, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    project_submit.configure(command=lambda na=project_name, dsc=project_description, ts=time_sensitive, yr=user_year, mo=user_month, day=user_day, rq=project_notes : new_project_submit(na, dsc, ts, yr, mo, day, rq))
    project_submit.place(relx=0.5, rely=6/7, anchor="center")
    np_menu_items.append(project_submit)
    time_sensitive_true(project_time_sensitive_y, project_time_sensitive_n)
    back.configure(command=project_select_screen, text="← Main Menu", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
    back.place(relx=0.002*9, rely=0.002*16, anchor="nw")
    back.tkraise()

def new_project_submit(name:tk.Entry, description:tk.Entry, time_sensitive:list, date_year:tk.StringVar, date_month:tk.StringVar, date_day:tk.StringVar, notes:tk.Entry) -> None:
    fileutil.update_existing_names()
    if name.get() == "":
        messagebox.showerror("No Project Name", "Please enter a project name.")
        return
    elif name.get() in gv.existing_names:
        messagebox.showerror("Duplicate Project Name", "A project with that name already exists.")
        return
    
    date_mo = ""
    date_dy = ""
    if time_sensitive[0] == True and ((date_month.get() == "") or (date_day.get() == "") or (date_year.get() == "")):
        messagebox.showerror("No Project Date", "Please enter a project date.")
        return
    elif time_sensitive[0] == True:
        date_mo = uiutil.determine_month(date_month.get())
        date_dy = uiutil.determine_day(date_day.get())
        if not ds.Project.date_after_current(date(int(date_year.get()), int(date_mo), int(date_dy))):
            messagebox.showerror("Invalid Date", "Date entered is before or equal to the date today.")
            return

    sounds.play_click()
    new_date = date_mo + "/" + date_dy + "/" + ((date_year.get()) if ((date_year.get()) != "") else ("0000"))
    
    gv.project = ds.Project(name.get(), description.get(), time_sensitive[0], new_date, notes.get())
    fileutil.save_project()

    for widget in np_menu_items:
        widget.place_forget()
    
    canvas = tk.Canvas(gv.window, width=665, height=315, bd=0, highlightthickness=0, bg="black")
    canvas.place(anchor="n", relx=0.5, rely=0)
    canvas.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
    canvas.create_oval(7.5, 7.5, 650, 300, fill="#abcaf6", outline="white", width=3)
    Lproject_name = tk.Label(text=gv.project.name, bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    if len(gv.project.name) <= 17:
        Lproject_name.configure(font=("Helvetica", 50, "bold"))
        Lproject_name.place(anchor="n", relx=0.5, rely=0.1175)
    elif len(gv.project.name) <= 30:
        Lproject_name.configure(font=("Helvetica", 32, "bold"))
        Lproject_name.place(anchor="n", relx=0.5, rely=0.13125)
    
    Lproject_desc = tk.Label(text=gv.project.description, font=("Helvetica", 14, "bold"), bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    Lproject_desc.place(anchor="n", relx=0.5, rely=0.225)
    Lproject_days_left = tk.Label(font=("Helvetica", 22, "bold"), bg="#abcaf6", fg="red", bd=0, highlightthickness=0)
    Lproject_days_left.configure(text=f"{gv.project.calculate_days_left()}") 
    Lproject_days_left.place(anchor="n", relx=0.5, rely=0.06875)

    np_menu_items.append(canvas)
    np_menu_items.append(Lproject_name)
    np_menu_items.append(Lproject_desc)
    np_menu_items.append(Lproject_days_left)
    mains_setup()


def mains_setup() -> None:
    canvases = [tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black") for _ in range(15)]
    name_labels = [tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:") for _ in range(15)]
    main_names = [tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char15, "%P")) for _ in range(15)]
    main_creates = [tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0) for _ in range(15)]
    quick_number_buttons = [tk.Button(text=str(i+1), font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="green", fg="black") for i in range(15)]
    number_entry = tk.Entry(width=2, font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char2, "%P"))
    or_label = tk.Label(font=("Helvetica", 24, "bold"), bd=0, highlightthickness=0, justify="center", bg="green", fg="black", text="or")
    number_confirm = tk.Button(font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, justify="center", bg="green", fg="black", text="✅")
    for i in range(5):
        np_menu_items.append(quick_number_buttons[i])
    np_menu_items.append(number_entry)
    np_menu_items.append(number_confirm)
    np_menu_items.append(or_label)

    main_items = []
    def how_many_mains() -> None:
        sounds.play_click()
        for i in range(5):
            quick_number_buttons[i].configure(command=lambda n=i+1 : build_mains(n))
            quick_number_buttons[i].place(anchor="e", relx=0.424+((i-2)*0.019), rely=0.5)
        or_label.place(anchor="center", relx=0.5, rely=0.5)
        number_entry.place(anchor="w", relx=0.538, rely=0.5)
        number_confirm.configure(command=lambda n=number_entry : build_many(n))
        number_confirm.place(anchor="w", relx=0.56, rely=0.5)
    
    def build_many(entry:tk.Entry) -> None:
        num = int(entry.get())
        if num <= 5:
            build_mains(num)
            return
        elif num > 15:
            messagebox.showerror("Too Many Mains", "Please enter a number between 1 and 15.")
            return
        
        sounds.play_click()
        plus.place_forget()
        for i in range(5):
            quick_number_buttons[i].place_forget()
        number_entry.place_forget()
        number_confirm.place_forget()
        or_label.place_forget()
        undo.place(anchor="nw", relx=0.0145*9, rely=0.002*16)
        undo.tkraise()
        np_menu_items.append(undo)
        
        YOFF = 0.05
        YOFF2 = 0.17125
        main_xs.append([0.5/6, (0.5+(5/4))/6, (0.5+2*(5/4))/6, (0.5+3*(5/4))/6, 5.5/6])
        main_cys.append(0.5575); main_cys.append(0.72875); main_cys.append(0.9)
        main_canvas_size.append(315)
        main_canvas_size.append(195)

        for i in range(num):
            canvases[i].configure(width=main_canvas_size[0], height=main_canvas_size[1])
            canvases[i].place(anchor="n", relx=main_xs[0][(i%5)], rely=0.4-YOFF+(int(i/5)*YOFF2))
            canvases[i].create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvases[i].create_oval(7.5, 7.5, main_canvas_size[0]-15, main_canvas_size[1]-15, fill="#abcaf6", outline="white", width=2)
            name_labels[i].place(anchor="s", relx=main_xs[0][(i%5)], rely=0.4475-YOFF+(int(i/5)*YOFF2))
            main_names[i].place(anchor="s", relx=main_xs[0][(i%5)], rely=0.48-YOFF+(int(i/5)*YOFF2))
            main_creates[i].configure(command=lambda p=gv.project, n=main_names[i], l=name_labels[i], c=main_creates[i] : create_new_main(p, n, l, c, main_xs[0][(i%5)]))
            main_creates[i].place(anchor="s", relx=main_xs[0][(i%5)], rely=main_cys[0]-YOFF+(int(i/5)*YOFF2))
            np_menu_items.append(canvases[i])
            np_menu_items.append(name_labels[i])
            np_menu_items.append(main_names[i])
            np_menu_items.append(main_creates[i])
            main_items.append(canvases[i])
            main_items.append(name_labels[i])
            main_items.append(main_names[i])
            main_items.append(main_creates[i])
        main_ct[0] = num

    def build_mains(num:int) -> None:
        sounds.play_click()
        plus.place_forget()
        for i in range(5):
            quick_number_buttons[i].place_forget()
        number_entry.place_forget()
        number_confirm.place_forget()
        or_label.place_forget()
        undo.place(anchor="nw", relx=0.0145*9, rely=0.002*16)
        undo.tkraise()
        np_menu_items.append(undo)
        YOFF = 0.05
        main_canvas_north_y[0] = 0.35

        if num == 1:
            main_xs.append([0.5])
            main_cys.append(0.6125)
            main_canvas_size.append(415)
            main_canvas_size.append(255)
        elif num == 2:
            main_xs.append([1/3, 2/3])
            main_cys.append(0.6125)
            main_canvas_size.append(415)
            main_canvas_size.append(255)
        elif num == 3:
            main_xs.append([1/4, 2/4, 3/4])
            main_cys.append(0.6125)
            main_canvas_size.append(415)
            main_canvas_size.append(255)
        elif num == 4:
            main_xs.append([0.75/5, (0.75+(3.5/3))/5, (0.75+2*(3.5/3))/5, 4.25/5])
            main_cys.append(0.5875)
            main_canvas_size.append(365)
            main_canvas_size.append(225)
        elif num == 5:
            main_xs.append([0.5/6, (0.5+(5/4))/6, (0.5+2*(5/4))/6, (0.5+3*(5/4))/6, 5.5/6])
            main_cys.append(0.5575)
            main_canvas_size.append(315)
            main_canvas_size.append(195)
    
        for i in range(num):
            canvases[i].configure(width=main_canvas_size[0], height=main_canvas_size[1])
            canvases[i].place(anchor="n", relx=main_xs[0][i], rely=0.35)
            canvases[i].create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvases[i].create_oval(7.5, 7.5, main_canvas_size[0]-15, main_canvas_size[1]-15, fill="#abcaf6", outline="white", width=2)
            name_labels[i].place(anchor="s", relx=main_xs[0][i], rely=0.4475-YOFF)
            main_names[i].place(anchor="s", relx=main_xs[0][i], rely=0.48-YOFF)
            main_creates[i].configure(command=lambda p=gv.project, n=main_names[i], l=name_labels[i], c=main_creates[i] : create_new_main(p, n, l, c, main_xs[0][i]))
            main_creates[i].place(anchor="s", relx=main_xs[0][i], rely=main_cys[0]-YOFF)
            np_menu_items.append(canvases[i])
            np_menu_items.append(name_labels[i])
            np_menu_items.append(main_names[i])
            np_menu_items.append(main_creates[i])
            main_items.append(canvases[i])
            main_items.append(name_labels[i])
            main_items.append(main_names[i])
            main_items.append(main_creates[i])
        main_ct[0] = num

    def clear_mains() -> None:
        global main_xs, main_canvas_size, main_cys
        main_xs.clear()
        main_cys.clear()
        main_canvas_size.clear()
        for widget in main_items:
            widget.place_forget()
        undo.place_forget()
        plus.place(anchor="n", relx=0.5, rely=0.4)
    
    undo.configure(command=clear_mains)

    plus = tk.Button(text="➕", font=("Helvetica", 16, "bold"), bd=0, highlightthickness=0, bg="black", fg="white")
    plus.configure(command=how_many_mains)
    plus.place(anchor="n", relx=0.5, rely=0.4)
    np_menu_items.append(plus)

def create_new_main(project:ds.Project, name:tk.Entry, label:tk.Label, create:tk.Button, relx:float) -> None:
    sub_items = []
    sounds.play_click()
    if name.get() == "":
        messagebox.showerror("No Main Name", "Please enter a project name.")
        return None
    YOFF = 0.05
    new_main = project.add_main(name.get())
    main_name_label = tk.Label(font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center")
    np_menu_items.append(main_name_label)
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
    np_menu_items.append(one_main)
    np_menu_items.append(two_main)
    np_menu_items.append(three_main)
    canvas1 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label1 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name1 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char15, "%P"))
    sub_create1 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas2 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label2 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name2 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char15, "%P"))
    sub_create2 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    canvas3 = tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black")
    name_label3 = tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:")
    sub_name3 = tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char15, "%P"))
    sub_create3 = tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    sub_create = tk.Button(text="➕", font=("Helvetica", 14, "bold"), bd=0, highlightthickness=0, bg="black", fg="white")
    def how_many_subs() -> None:
        sounds.play_click()
        one_main.configure(command=lambda n=1 : build_subs(n))
        two_main.configure(command=lambda n=2 : build_subs(n))
        three_main.configure(command=lambda n=3 : build_subs(n))
        one_main.place(anchor="e", relx=relx-0.01, rely=0.765-0.0425)
        two_main.place(anchor="center", relx=relx, rely=0.765-0.0425)
        three_main.place(anchor="w", relx=relx+0.01, rely=0.765-0.0425)
    def build_subs(num:int) -> None:
        sounds.play_click()
        sub_create.place_forget()
        one_main.place_forget()
        two_main.place_forget()
        three_main.place_forget()
        undo.place(anchor="nw", relx=0.0145*9, rely=0.002*16)
        undo.tkraise()
        np_menu_items.append(undo)
        YOFF = 0.05
        if num == 1:
            canvas1.configure(width=240, height=150)
            canvas1.place(anchor="center", relx=relx, rely=uiutil.calc_dist2(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 225, 135, fill="#abcaf6", outline="white", width=2)
            sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/2))
            name_label1.place(anchor="center", relx=relx, rely=0.765+0.0315)
            sub_name1.place(anchor="center", relx=relx, rely=0.765+0.0515)
            sub_create1.place(anchor="center", relx=relx, rely=0.765+0.15235)
            np_menu_items.append(canvas1)
            np_menu_items.append(name_label1)
            np_menu_items.append(sub_name1)
            np_menu_items.append(sub_create1)
            sub_items.append(canvas1)
            sub_items.append(name_label1)
            sub_items.append(sub_name1)
            sub_items.append(sub_create1)
        elif num == 2:
            if main_ct[0] < 5:
                canvas1.configure(width=192, height=120)
                canvas1.place(anchor="center", relx=relx-0.05, rely=uiutil.calc_dist2(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas1.create_oval(7.5, 7.5, 177, 105, fill="#abcaf6", outline="white", width=2)
                sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
                name_label1.place(anchor="center", relx=relx-0.05, rely=0.765+0.0315)
                sub_name1.place(anchor="center", relx=relx-0.05, rely=0.765+0.0515)
                sub_create1.place(anchor="center", relx=relx-0.05, rely=0.765+0.15235)
                canvas2.configure(width=192, height=120)
                canvas2.place(anchor="center", relx=relx+0.05, rely=uiutil.calc_dist2(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas2.create_oval(7.5, 7.5, 177, 105, fill="#abcaf6", outline="white", width=2)
                sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
                name_label2.place(anchor="center", relx=relx+0.05, rely=0.765+0.0315)
                sub_name2.place(anchor="center", relx=relx+0.05, rely=0.765+0.0515)
                sub_create2.place(anchor="center", relx=relx+0.05, rely=0.765+0.15235)
            elif main_ct[0] == 5:
                canvas1.configure(width=159, height=105)
                canvas1.place(anchor="center", relx=relx-0.04, rely=uiutil.calc_dist2(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas1.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
                sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
                name_label1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0315)
                sub_name1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0515)
                sub_create1.place(anchor="center", relx=relx-0.04, rely=0.765+0.15235)
                canvas2.configure(width=159, height=105)
                canvas2.place(anchor="center", relx=relx+0.04, rely=uiutil.calc_dist2(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
                canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
                canvas2.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
                sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
                name_label2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0315)
                sub_name2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0515)
                sub_create2.place(anchor="center", relx=relx+0.04, rely=0.765+0.15235)
            np_menu_items.append(canvas1)
            np_menu_items.append(name_label1)
            np_menu_items.append(sub_name1)
            np_menu_items.append(sub_create1)
            np_menu_items.append(canvas2)
            np_menu_items.append(name_label2)
            np_menu_items.append(sub_name2)
            np_menu_items.append(sub_create2)
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
            canvas1.place(anchor="center", relx=relx-0.04, rely=uiutil.calc_dist3(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas1.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas1.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create1.configure(command=lambda m=new_main, n=sub_name1, l=name_label1, c=sub_create1 : create_new_sub(m, n, l, c, 1/3))
            name_label1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0315)
            sub_name1.place(anchor="center", relx=relx-0.04, rely=0.765+0.0515)
            sub_create1.place(anchor="center", relx=relx-0.04, rely=0.765+0.15235)
            canvas2.configure(width=159, height=105)
            canvas2.place(anchor="center", relx=relx+0.04, rely=uiutil.calc_dist3(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas2.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas2.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create2.configure(command=lambda m=new_main, n=sub_name2, l=name_label2, c=sub_create2 : create_new_sub(m, n, l, c, 2/3))
            name_label2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0315)
            sub_name2.place(anchor="center", relx=relx+0.04, rely=0.765+0.0515)
            sub_create2.place(anchor="center", relx=relx+0.04, rely=0.765+0.15235)
            canvas3.configure(width=159, height=105)
            canvas3.place(anchor="center", relx=relx, rely=uiutil.calc_dist23(uiutil.get_south_y(main_canvas_size[0], main_canvas_north_y[0])))
            canvas3.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvas3.create_oval(7.5, 7.5, 144, 90, fill="#abcaf6", outline="white", width=2)
            sub_create3.configure(command=lambda m=new_main, n=sub_name3, l=name_label3, c=sub_create3 : create_new_sub(m, n, l, c, 1/3))
            name_label3.place(anchor="center", relx=relx, rely=0.765+0.0315)
            sub_name3.place(anchor="center", relx=relx, rely=0.765+0.0515)
            sub_create3.place(anchor="center", relx=relx, rely=0.765+0.15235)
            np_menu_items.append(canvas1)
            np_menu_items.append(name_label1)
            np_menu_items.append(sub_name1)
            np_menu_items.append(sub_create1)
            np_menu_items.append(canvas2)
            np_menu_items.append(name_label2)
            np_menu_items.append(sub_name2)
            np_menu_items.append(sub_create2)
            np_menu_items.append(canvas3)
            np_menu_items.append(name_label3)
            np_menu_items.append(sub_name3)
            np_menu_items.append(sub_create3)
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
    np_menu_items.append(sub_create)
    return new_main

def create_new_sub(main:ds.Main, name_entry:tk.Entry) -> None:
    sounds.play_click()
    new_sub = main.add_main(name_entry.get())

def exploded_view() -> None:
    #Create view for exploded view of any project/main/sub
    pass

def edit_details() -> None:
    #Create UI for editing (exploded view) and edit details of project/main/sub
    pass

def add_notes() -> None:
    #Create UI for notetaking on project/main/sub and add to project/main/sub
    pass

def process_data() -> None:
    #Goes through Previous User JSONs with Project Data and puts it into a format where the file can be edited
    pass

def old_project_screen() -> None:
    #Create UI for saved projects screen by accessing User Projects folder
    pass

def open_project() -> None:
    #Create UI for created project by reading json file
    pass


def init() -> None:
    cntue = tk.Button(text="▶", fg="black", bg="#e4eff6", bd=0, highlightthickness=0, font=("Helvetica", 16, "bold"), height=0)
    cntue2 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
    cntue3 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
    cntue4 = tk.Button(bg="#e4eff6", font=("Times New Roman", 10, "bold"), bd=0, highlightthickness=0)
    cntue5 = tk.Button(bg="#e4eff6", font=("Times New Roman", 6, "bold"), bd=0, highlightthickness=0)
    cntue6 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
    cntue7 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
    cntue8 = tk.Button(bg="#e4eff6", font=("Times New Roman", 8, "bold"), bd=0, highlightthickness=0)
    cntue9 = tk.Button(bg="#e4eff6", font=("Times New Roman", 6, "bold"), bd=0, highlightthickness=0)
    settings = tk.Button(text="⚙️", bg="#414449", bd=0, highlightthickness=0, font=("Helvetica", 26), height=0, fg="white")
    cntue.configure(command=project_select_screen)
    cntue2.configure(command=project_select_screen)
    cntue3.configure(command=project_select_screen)
    cntue4.configure(command=project_select_screen)
    cntue5.configure(command=project_select_screen)
    cntue6.configure(command=project_select_screen)
    cntue7.configure(command=project_select_screen)
    cntue8.configure(command=project_select_screen)
    cntue9.configure(command=project_select_screen)
    cntue.place(relx=0.49, rely=0.4, anchor="center")
    cntue2.place(relx=0.45, rely=0.3825)
    cntue3.place(relx=0.5075, rely=0.3775)
    cntue4.place(relx=0.4875, rely=0.42, anchor="center")
    cntue5.place(relx=0.52625, rely=0.3825)
    cntue6.place(relx=0.5, rely=0.38875)
    cntue7.place(relx=0.49, rely=0.395)
    cntue8.place(relx=0.515, rely=0.3775)
    cntue9.place(relx=0.43975, rely=0.3875)
    settings.place(relx=0.87, rely=0.87)
    cntue.tkraise()

    gv.main_menu_buttons = [cntue, cntue2, cntue3, cntue4, cntue5, cntue6, cntue7, cntue8, cntue9, settings]
    gv.window.mainloop()