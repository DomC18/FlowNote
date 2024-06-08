from PIL import ImageTk, Image, ImageGrab, ImageFilter
from tkinter import messagebox, filedialog
from datetime import datetime, date
import globalvariables as gv
import animations as anim
from cal import Calendar
import tkinter as tk
import random as rr
import constants
import projutil
import sounds
import proj

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

center_image = tk.PhotoImage(file=constants.CENTERSMALL_ICON)
delete_image = tk.PhotoImage(file=constants.DELETE_ICON)
edit_image = tk.PhotoImage(file=constants.EDIT_ICON)
edit_large_image = tk.PhotoImage(file=constants.EDITLARGE_ICON)
info_image = tk.PhotoImage(file=constants.INFO_ICON)
info_large_image = tk.PhotoImage(file=constants.INFOLARGE_ICON)
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
main_canvas_north_y = [0]
main_xs = [1/12, 7/24, 0.5, 17/24, 11/12]

gv.np_menu_items = []
edit_menu_items = []
info_menu_items = []

time_var = tk.IntVar(); time_var.set(0)
month_var = tk.StringVar(); month_var.set("")
day_var = tk.StringVar(); day_var.set("")
year_var = tk.StringVar(); year_var.set("")

new_project_button = tk.Button(text="New Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)
old_project_button = tk.Button(text="Open Project", font=("Consolas", 16, "bold"), bg="#404449", bd=0, highlightthickness=0)



def project_select_screen() -> None:
    try: 
        gv.window.after_cancel(gv.star_loop[0])
    except: 
        pass

    for star_comb in gv.stars:
        star_comb[0].destroy()
    for widget in gv.np_menu_items:
        try: 
            widget.place_forget()
        except: 
            pass

    sounds.play_click()
    sky_label.pack_forget()
    gv.np_menu_items.clear()

    gv.window.attributes("-fullscreen", False)
    gv.window.geometry("600x600")
    gv.window.configure(bg="#414449")
    for widget in gv.main_menu_buttons:
        widget.place_forget()
    anim.forward_blur_animation(1)
    
    back.configure(bg="#414449", fg="white", text="← Main Menu", font=("Helvetica", 16, "bold"), relief="flat")
    back.configure(command=lambda b=back, n=new_project_button, o=old_project_button : anim.backward_blur_animation(6, b, n, o))
    back.place(relx=0.02, rely=0.02, anchor="nw")
    gv.logo_label.pack()
    new_project_button.configure(command=lambda b=back : new_project_screen(b))
    old_project_button.configure(command=lambda b=back : choose_project(b))
    new_project_button.place(relx=0.5, rely=1/3, anchor="center")
    old_project_button.place(relx=0.5, rely=2/3, anchor="center")

def choose_project(back:tk.Button) -> None:
    projutil.update_existing_names()
    if len(gv.existing_names) == 0:
        messagebox.showerror("Error", "No projects found")
        return
    
    file_path = filedialog.askopenfilename(
        initialdir=rf"{constants.USER_PROJECTS_PATH}",
        title="Select a project json file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
    )
    if file_path:
        projutil.load_project(file_path)
        gv.window.attributes("-fullscreen", True)
        gv.logo_label.pack_forget()
        new_project_button.place_forget()
        old_project_button.place_forget()
        sky_label.pack()
        choices = [0, 1]
        choice = rr.choice(choices)
        if choice == 0:
            anim.proj_bg_hor()
        else:
            anim.proj_bg_vert()
        back.configure(command=project_select_screen, text="← Main Menu", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
        back.place(relx=0.002*9, rely=0.002*16, anchor="nw")
        back.tkraise()
        project_setup(gv.project)

def new_project_screen(back:tk.Button) -> None:
    sounds.play_click()
    gv.project = None
    gv.touched_gold = False
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
    gv.np_menu_items.append(date_to_complete_label)
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
    gv.np_menu_items.append(name_label)
    gv.np_menu_items.append(project_name)
    description_label = tk.Label(font=("Helvetica", 18, "bold"), text="Project Description", fg="white", bg="black")
    description_label.place(anchor="s", relx=0.5, rely=(2/7)-0.03)
    project_description = tk.Entry(font=("Helvetica", 18), validate="key", validatecommand=(char100, "%P"))
    project_description.place(relx=0.5, rely=2/7, anchor="center")
    gv.np_menu_items.append(project_description)
    gv.np_menu_items.append(description_label)
    time_sensitive_label = tk.Label(font=("Helvetica", 18, "bold"), text="Time Sensitive?*", fg="white", bg="black")
    time_sensitive_label.place(anchor="s", relx=0.5, rely=(3/7)-0.03)
    project_time_sensitive_y.configure(bg="green", text="YES", font=("Helvetica", 18))
    project_time_sensitive_y.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_true(a,b))
    project_time_sensitive_y.place(relx=0.5-0.00975, rely=3/7, anchor="e")
    gv.np_menu_items.append(project_time_sensitive_y)
    project_time_sensitive_n.configure(bg="red", text="NO", font=("Helvetica", 18))
    project_time_sensitive_n.configure(command=lambda a=project_time_sensitive_y, b=project_time_sensitive_n : time_sensitive_false(a,b))
    project_time_sensitive_n.place(relx=0.5+0.00975, rely=3/7, anchor="w")
    gv.np_menu_items.append(project_time_sensitive_n)
    gv.np_menu_items.append(time_sensitive_label)
    project_month.place(relx=0.5-0.035, rely=4/7, anchor="e")
    gv.np_menu_items.append(project_month)
    project_day.place(relx=0.5, rely=4/7, anchor="center")
    gv.np_menu_items.append(project_day)
    project_year.place(relx=0.5+0.035, rely=4/7, anchor="w")
    gv.np_menu_items.append(project_year)
    notes_label = tk.Label(font=("Helvetica", 18, "bold"), text="Notes", fg="white", bg="black")
    notes_label.place(anchor="s", relx=0.5, rely=(5/7)-0.03)
    project_notes = tk.Entry(font=("Helvetica", 18), validate="key", validatecommand=(char100, "%P"))
    project_notes.place(relx=0.5, rely=5/7, anchor="center")
    gv.np_menu_items.append(notes_label)
    gv.np_menu_items.append(project_notes)
    project_submit = tk.Button(font=("Helvetica", 25, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0)
    project_submit.configure(command=lambda na=project_name, dsc=project_description, ts=time_sensitive, yr=user_year, mo=user_month, day=user_day, rq=project_notes : new_project_submit(na, dsc, ts, yr, mo, day, rq))
    project_submit.place(relx=0.5, rely=6/7, anchor="center")
    gv.np_menu_items.append(project_submit)
    time_sensitive_true(project_time_sensitive_y, project_time_sensitive_n)
    back.configure(command=project_select_screen, text="← Main Menu", font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised")
    back.place(relx=0.002*9, rely=0.002*16, anchor="nw")
    back.tkraise()

def new_project_submit(name:tk.Entry, description:tk.Entry, time_sensitive:list, date_year:tk.StringVar, date_month:tk.StringVar, date_day:tk.StringVar, notes:tk.Entry) -> None:
    projutil.update_existing_names()
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
        date_mo = proj.determine_month(date_month.get())
        date_dy = proj.determine_day(date_day.get())
        if not proj.Project.date_after_current(date(int(date_year.get()), int(date_mo), int(date_dy))):
            messagebox.showerror("Invalid Date", "Date entered is before or equal to the date today.")
            return

    sounds.play_click()
    new_date = date_mo + "/" + date_dy + "/" + ((date_year.get()) if ((date_year.get()) != "") else ("0000"))
    
    gv.project = proj.Project(name.get(), description.get(), time_sensitive[0], new_date, notes.get())
    projutil.save_project()
    
    project_setup(gv.project)
    
def project_setup(main):
    for widget in gv.np_menu_items:
        try:
            widget.place_forget()
        except:
            pass
    gv.np_menu_items.clear()
    projutil.update_existing_names()

    calendar = Calendar(gv.window, gv.window.winfo_width(), gv.window.winfo_height(), "light blue", gv.np_menu_items, lambda m=gv.project : project_setup(m))
    calendar_button = tk.Button(master=gv.window, font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised", text="Calendar")
    calendar_button.configure(command=lambda f=(lambda m=gv.project : project_setup(m)) : calendar.toggle_show(f))
    calendar_button.place(anchor="nw", relx=0.15, rely=0.002*16)
    tree_button = tk.Button(master=gv.window, font=("Helvetica", 20, "bold"), bg="black", fg="white", relief="raised", text="Tree")
    tree_button.configure(command=projutil.update_curr_tree)
    tree_button.place(anchor="nw", relx=0.25, rely=0.002*16)
    gv.gold_button = tk.Button(master=gv.window, font=("Helvetica", 8, "bold"), bg="black", fg="white", relief="raised", text="P")
    if gv.touched_gold:
        gv.gold_button.configure(command=exit)
        gv.gold_button.place(anchor="ne", relx=0.95, rely=0.002*16)

    canvas = tk.Canvas(gv.window, width=665, height=315, bd=0, highlightthickness=0, bg="black")
    canvas.place(anchor="n", relx=0.5, rely=0)
    canvas.create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
    canvas.create_oval(7.5, 7.5, 650, 300, fill="#abcaf6", outline="white", width=3)
    name = tk.Label(text=main.name, bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    if len(main.name) <= 17:
        name.configure(font=("Helvetica", 50, "bold"))
        name.place(anchor="n", relx=0.5, rely=0.1175)
    elif len(main.name) <= 30:
        name.configure(font=("Helvetica", 32, "bold"))
        name.place(anchor="n", relx=0.5, rely=0.13125)
    
    desc = tk.Label(text=main.description[:31], font=("Helvetica", 14, "bold"), bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    desc.place(anchor="n", relx=0.5, rely=0.225)
    days = tk.Label(font=("Helvetica", 22, "bold"), bg="#abcaf6", fg="red", bd=0, highlightthickness=0)
    days.configure(text=f"{main.calculate_days_left()}")
    days.place(anchor="n", relx=0.5, rely=0.06875)
    edit = tk.Button(image=edit_image, bg="#abcaf6", bd=0, highlightthickness=0)
    edit.configure(command=lambda p=main, pl=name, dl=desc, dy=days : edit_interface(p, pl, dl, dy))
    edit.place(anchor="w", relx=0.356, rely=0.1175)
    info = tk.Button(image=info_image, bg="#abcaf6", bd=0, highlightthickness=0)
    info.configure(command=lambda m=main : info_interface(m))
    info.place(anchor="w", relx=0.356, rely=0.17)
    backward_parent = tk.Button(text="↑", font=("Helvetica", 40, "bold"), bg="#abcaf6", fg="black", bd=0, highlightthickness=0)
    if main != gv.project:
        backward_parent.configure(command=lambda m=main : back_parent(m))
        backward_parent.place(anchor="e", relx=0.644, rely=((0.13125+0.1175)/2))

    gv.np_menu_items.append(gv.gold_button)
    gv.np_menu_items.append(calendar_button)
    gv.np_menu_items.append(tree_button)
    gv.np_menu_items.append(canvas)
    gv.np_menu_items.append(name)
    gv.np_menu_items.append(desc)
    gv.np_menu_items.append(days)
    gv.np_menu_items.append(edit)
    gv.np_menu_items.append(info)
    gv.np_menu_items.append(backward_parent)
    mains_setup(main)

def mains_setup(parent) -> None:
    num_mains = len(parent.mains)

    canvases = [tk.Canvas(gv.window, bd=0, highlightthickness=0, bg="black") for _ in range(15)]
    name_labels = [tk.Label(font=("Helvetica", 18, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text="Name:") for _ in range(15)]
    main_names = [tk.Entry(font=("Helvetica", 18), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char15, "%P")) for _ in range(15)]
    main_creates = [tk.Button(font=("Helvetica", 16, "bold"), text="Submit", bg="green", bd=0, highlightthickness=0) for _ in range(15)]
    number_entry = tk.Entry(width=3, font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, justify="center", validate="key", validatecommand=(char2, "%P"))
    number_confirm = tk.Button(font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, justify="center", bg="green", fg="black", text="✅")
    gv.np_menu_items.append(number_entry)
    gv.np_menu_items.append(number_confirm)

    YOFF = 0.05
    YOFF2 = 0.17125
    for i in range(num_mains):
        canvases[i].configure(width=315, height=195)
        canvases[i].place(anchor="n", relx=main_xs[(i%5)], rely=0.4-YOFF+(int(i/5)*YOFF2))
        canvases[i].create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
        canvases[i].create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
        gv.np_menu_items.append(canvases[i])
        child_ui(parent.mains[i], canvases[i], main_xs[(i%5)], 0.435+(int(i/5)*YOFF2))

    def how_many_mains() -> None:
        sounds.play_click()
        number_entry.place(anchor="center", relx=0.5, rely=0.3375)
        number_confirm.configure(command=lambda e=number_entry : build_mains(e))
        number_confirm.place(anchor="e", relx=0.55, rely=0.3375)
    
    def build_mains(entry:tk.Entry) -> None:
        num_mains = len(parent.mains)
        num = int(entry.get())
        if num+num_mains > 15:
            messagebox.showerror("Too Many Mains", "Maximum number of mains was entered or exceeded.")
            return
        
        sounds.play_click()
        number_entry.delete(0, tk.END)
        number_entry.place_forget()
        number_confirm.place_forget()
        
        for i in range(num+num_mains):
            if i <= num_mains-1 and num_mains != 0:
                continue
            canvases[i].configure(width=315, height=195)
            canvases[i].place(anchor="n", relx=main_xs[(i%5)], rely=0.4-YOFF+(int(i/5)*YOFF2))
            canvases[i].create_image(0, 0, image=sky_mini_photo, anchor=tk.NW)
            canvases[i].create_oval(7.5, 7.5, 300, 180, fill="#abcaf6", outline="white", width=2)
            name_labels[i].place(anchor="s", relx=main_xs[(i%5)], rely=0.4475-YOFF+(int(i/5)*YOFF2))
            main_names[i].place(anchor="s", relx=main_xs[(i%5)], rely=0.48-YOFF+(int(i/5)*YOFF2))
            main_creates[i].configure(command=lambda p=parent, n=main_names[i], l=name_labels[i], c=main_creates[i], ca=canvases[i], x=main_xs[(i%5)], y=0.435+(int(i/5)*YOFF2) : setup_main(p, n, l, c, ca, x, y))
            main_creates[i].place(anchor="s", relx=main_xs[(i%5)], rely=0.5575-YOFF+(int(i/5)*YOFF2))
            gv.np_menu_items.append(canvases[i])
            gv.np_menu_items.append(name_labels[i])
            gv.np_menu_items.append(main_names[i])
            gv.np_menu_items.append(main_creates[i])

    plus = tk.Button(text="➕", font=("Helvetica", 16, "bold"), bd=0, highlightthickness=0, bg="black", fg="white")
    plus.configure(command=how_many_mains)
    plus.place(anchor="w", relx=0.45, rely=0.3375)
    gv.np_menu_items.append(plus)

def setup_main(parent, name:tk.Entry, label:tk.Label, create:tk.Button, canvas:tk.Canvas, relx:float, rely:float) -> None:
    if name.get() == "":
        messagebox.showerror("No Main Name", "Please enter a project name.")
        return None
    sounds.play_click()

    new_main = parent.add_main(name.get())
    projutil.save_project()

    name.destroy()
    label.destroy()
    create.destroy()
    child_ui(new_main, canvas, relx, rely)

def child_ui(new_main, canvas:tk.Canvas, relx:float, rely:float):
    del_items = []

    main_name_label = tk.Label(font=("Helvetica", 20, "bold"), bd=0, highlightthickness=0, bg="#abcaf6", justify="center", text=new_main.name)
    main_name_label.place(anchor="center", relx=relx, rely=rely)
    main_center = tk.Button(image=center_image, bg="#abcaf6", bd=0, highlightthickness=0)
    main_center.configure(command=lambda m=new_main : forward_parent(m))
    main_center.place(anchor="center", relx=relx, rely=rely-0.04)
    main_edit = tk.Button(image=edit_image, bg="#abcaf6", bd=0, highlightthickness=0)
    main_edit.configure(command=lambda m=new_main, ml=main_name_label : edit_interface(m, ml, None, None))
    main_edit.place(anchor="center", relx=relx-0.0575, rely=rely)
    main_delete = tk.Button(image=delete_image, bg="#abcaf6", bd=0, highlightthickness=0)
    main_delete.configure(command=lambda p=new_main.parent, n=new_main.name, i=del_items : delete_main(p, n, i))
    main_delete.place(anchor="center", relx=relx+0.0575, rely=rely)
    main_info = tk.Button(image=info_image, bg="#abcaf6", bd=0, highlightthickness=0)
    main_info.configure(command=lambda m=new_main : info_interface(m))
    main_info.place(anchor="center", relx=relx, rely=rely+0.04)

    del_items.append(canvas)
    gv.np_menu_items.append(main_name_label); del_items.append(main_name_label)
    gv.np_menu_items.append(main_center); del_items.append(main_center)
    gv.np_menu_items.append(main_edit); del_items.append(main_edit)
    gv.np_menu_items.append(main_delete); del_items.append(main_delete)
    gv.np_menu_items.append(main_info); del_items.append(main_info)

def edit_interface(main, name_label:tk.Label, desc_label:tk.Label, days_label:tk.Label) -> None:
    try: 
        gv.window.after_cancel(gv.star_loop[0])
    except: 
        pass

    if main != gv.project:
        desc_label = None
        days_label = None

    for star in gv.stars:
        star[0].destroy()
    gv.stars.clear()

    month_var.set("")
    day_var.set("")
    year_var.set("")
    time_var.set(2)

    def time_sensitive_true(a:tk.Button, b:tk.Button) -> None:
        time_var.set(1)
        a.configure(relief="sunken")
        b.configure(relief="raised")
        month_entry.place(relx=0.75, rely=4/6, anchor="w")
        day_entry.place(relx=0.85, rely=4/6, anchor="center")
        year_entry.place(relx=0.95, rely=4/6, anchor="e")
    def time_sensitive_false(a:tk.Button, b:tk.Button) -> None:
        time_var.set(0)
        a.configure(relief="raised")
        b.configure(relief="sunken")
        month_entry.place_forget()
        day_entry.place_forget()
        year_entry.place_forget()
        month_var.set("")
        day_var.set("")
        year_var.set("")

    x = gv.window.winfo_rootx()
    y = gv.window.winfo_rooty()
    w = gv.window.winfo_width()
    h = gv.window.winfo_height()
    frame = tk.Frame(gv.window, width=w, height=h)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    screenshot = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    screenshot_photo = ImageTk.PhotoImage(screenshot)
    screenshot_label = tk.Label(frame, image=screenshot_photo)
    screenshot_label.image = screenshot_photo
    screenshot_label.pack()
    blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(9))
    screenshot_photo = ImageTk.PhotoImage(blurred_screenshot)
    screenshot_label.configure(image=screenshot_photo)
    screenshot_label.image = screenshot_photo
    screenshot_label.pack()
    edit_menu_items.append(frame)
    edit_menu_items.append(screenshot_label)

    back_button = tk.Button(frame, bg="black", fg="white", text="←", font=("Helvetica", 75, "bold"), relief="flat")
    back_button.configure(command=lambda i=edit_menu_items : back_from_interface(i))
    back_button.place(relx=-0.005, rely=-0.055, anchor="nw")
    edit_menu_items.append(back_button)

    old_name = tk.Label(frame, text=main.name, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
    old_name.place(relx=0.25, rely=1/6, anchor="w")
    edit_menu_items.append(old_name)
    old_desc = tk.Label(frame, text=(main.description if main.description != "" else "description:"), bg="black", fg="white", font=("Times New Roman", 60, "bold"))
    old_desc.place(relx=0.25, rely=2/6, anchor="w")
    edit_menu_items.append(old_desc)
    old_time = tk.Label(frame, text="Is this Time Sensitive?", bg="black", fg="white", font=("Times New Roman", 50, "bold"))
    old_time.place(relx=0.25, rely=3/6, anchor="w")
    edit_menu_items.append(old_time)
    old_dead = tk.Label(frame, text=(main.deadline if main.deadline != "" else "deadline:"), bg="black", fg="white", font=("Times New Roman", 60, "bold"))
    old_dead.place(relx=0.25, rely=4/6, anchor="w")
    edit_menu_items.append(old_dead)
    old_notes = tk.Label(frame, text=(main.notes if main.notes != "" else "notes:"), bg="black", fg="white", font=("Times New Roman", 60, "bold"))
    old_notes.place(relx=0.25, rely=5/6, anchor="w")
    edit_menu_items.append(old_notes)

    name_entry = tk.Entry(frame, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
    name_entry.place(relx=0.95, rely=1/6, anchor="e")
    edit_menu_items.append(name_entry)
    desc_entry = tk.Entry(frame, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
    desc_entry.place(relx=0.95, rely=2/6, anchor="e")
    edit_menu_items.append(desc_entry)
    notes_entry = tk.Entry(frame, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
    notes_entry.place(relx=0.95, rely=5/6, anchor="e")
    edit_menu_items.append(notes_entry)

    time_y = tk.Button(frame, bg="green", fg="black", font=("Times New Roman", 30, "bold"), width=5, text="Yes")
    time_n = tk.Button(frame, bg="red", fg="black", font=("Times New Roman", 30, "bold"), width=5, text="No")
    time_y.configure(command=lambda y=time_y, n=time_n : time_sensitive_true(y, n))
    time_n.configure(command=lambda y=time_y, n=time_n : time_sensitive_false(y, n))
    time_y.place(relx=0.75, rely=3/6, anchor="w")
    time_n.place(relx=0.95, rely=3/6, anchor="e")
    edit_menu_items.append(time_y)
    edit_menu_items.append(time_n)

    years = [str(datetime.today().year+i) for i in range(11)]
    month_entry = tk.OptionMenu(frame, month_var,"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
    edit_menu_items.append(month_entry)
    day_entry = tk.OptionMenu(frame, day_var,  '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st')
    edit_menu_items.append(day_entry)
    year_entry = tk.OptionMenu(frame, year_var, *years)
    edit_menu_items.append(year_entry)

    edit_large = tk.Button(frame, image=edit_large_image, bd=0, bg="black")
    edit_large.configure(command=lambda m=main, ml=name_label, dl=desc_label, dy=days_label, nae=name_entry, de=desc_entry, tv=time_var, mv=month_var, dv=day_var, yv=year_var, ne=notes_entry : edit_main(m, ml, dl, dy, nae, de, tv, mv, dv, yv, ne))
    edit_large.place(relx=0.125, rely=0.5, anchor="s")
    edit_menu_items.append(edit_large)
    edit_label = tk.Label(frame, text="Edit Main", justify="center", font=("Times New Roman", 35, "bold"), bg="black", fg="white")
    edit_label.place(relx=0.125, rely=0.5, anchor="n")
    edit_menu_items.append(edit_label)

def edit_main(main, name_label:tk.Label, desc_label:tk.Label, days_label:tk.Label, name_entry:tk.Entry, desc_entry:tk.Entry, time_var:tk.IntVar, mo_var:tk.StringVar, dy_var:tk.StringVar, yr_var:tk.StringVar, notes_entry:tk.Entry) -> None:
    if not projutil.edit_main(main, name_entry, desc_entry, time_var, mo_var, dy_var, yr_var, notes_entry):
        return None
    
    projutil.save_project()
    name_label.configure(text=main.name)
    if desc_label != None and days_label != None:
        desc_label.configure(text=gv.project.description)
        days_label.configure(text=f"{gv.project.calculate_days_left()}")

    back_from_interface(edit_menu_items)

def back_from_interface(items:list):
    for i in range(len(items)):
        items[i].destroy()
    items.clear()

    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0:
        anim.proj_bg_hor()
    else:
        anim.proj_bg_vert()

def delete_main(parent, main_name:str, del_items:list) -> None:
    for main in parent.mains:
        if main.name == main_name:
            parent.mains.remove(main)
            break
    
    for item in del_items:
        try:
            item.place_forget()
        except:
            pass
    
    projutil.save_project()

def info_interface(main) -> None:
    try: 
        gv.window.after_cancel(gv.star_loop[0])
    except: 
        pass

    for star in gv.stars:
        star[0].destroy()
    gv.stars.clear()

    x = gv.window.winfo_rootx()
    y = gv.window.winfo_rooty()
    w = gv.window.winfo_width()
    h = gv.window.winfo_height()
    frame = tk.Frame(gv.window, width=w, height=h)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    screenshot = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    screenshot_photo = ImageTk.PhotoImage(screenshot)
    screenshot_label = tk.Label(frame, image=screenshot_photo)
    screenshot_label.image = screenshot_photo
    screenshot_label.pack()
    blurred_screenshot = screenshot.filter(ImageFilter.GaussianBlur(9))
    screenshot_photo = ImageTk.PhotoImage(blurred_screenshot)
    screenshot_label.configure(image=screenshot_photo)
    screenshot_label.image = screenshot_photo
    screenshot_label.pack()
    info_menu_items.append(frame)
    info_menu_items.append(screenshot_label)

    back_button = tk.Button(gv.window, bg="black", fg="white", text="←", font=("Helvetica", 75, "bold"), relief="flat")
    back_button.configure(command=lambda i=info_menu_items : back_from_interface(i))
    back_button.place(relx=-0.005, rely=-0.055, anchor="nw")
    info_menu_items.append(back_button)

    info_large = tk.Label(gv.window, image=info_large_image, bd=0, bg="black")
    info_large.place(relx=0.125, rely=0.5, anchor="s")
    info_menu_items.append(info_large)
    info_icon_label = tk.Label(gv.window, text="Info", bg="black", fg="white", font=("Times New Roman", 35, "bold"))
    info_icon_label.place(relx=0.125, rely=0.5, anchor="n")
    info_menu_items.append(info_icon_label)
    name_label = tk.Label(gv.window, text=f"Name: {main.name}", bg="black", fg="white", font=("Times New Roman", 30, "bold"))
    name_label.place(relx=0.5, rely=1/6, anchor="center")
    info_menu_items.append(name_label)
    desc_label = tk.Label(gv.window, text=f"Description: {main.description}", bg="black", fg="white", font=("Times New Roman", 30, "bold"))
    desc_label.place(relx=0.5, rely=2/6, anchor="center")
    info_menu_items.append(desc_label)
    time_sensitive_label = tk.Label(gv.window, text=f"Time Sensitive: {main.time_sensitive}", bg="black", fg="white", font=("Times New Roman", 30, "bold"))
    time_sensitive_label.place(relx=0.5, rely=3/6, anchor="center")
    info_menu_items.append(time_sensitive_label)
    deadline_label = tk.Label(gv.window, text=f"Deadline: {main.deadline}", bg="black", fg="white", font=("Times New Roman", 30, "bold"))
    deadline_label.place(relx=0.5, rely=4/6, anchor="center")
    info_menu_items.append(deadline_label)
    notes_label = tk.Label(gv.window, text=f"Notes: {main.notes}", bg="black", fg="white", font=("Times New Roman", 30, "bold"))
    notes_label.place(relx=0.5, rely=5/6, anchor="center")
    info_menu_items.append(notes_label)

def forward_parent(main:proj.Main) -> None:
    project_setup(main)

def back_parent(main:proj.Main) -> None:
    parent = main.parent
    project_setup(parent)

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
    cntue.tkraise()

    gv.main_menu_buttons = [cntue, cntue2, cntue3, cntue4, cntue5, cntue6, cntue7, cntue8, cntue9]
    gv.window.mainloop()