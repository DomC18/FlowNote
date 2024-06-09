from PIL import ImageTk, ImageFilter, Image
from tkinter import messagebox
import globalvariables as gv
import tkinter as tk
import random as rr
import constants
import projutil
import sounds

gv.window = tk.Tk()
logo = Image.open(constants.LOGO_UNSIGNED_ICON)
logo = logo.resize((600, 600), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo)
gv.logo_label = tk.Label(gv.window, image=logo_photo)
gv.logo_label.image = logo_photo
gv.logo_label.pack()
gv.stars = []
gv.star_loop = [None]
blur_func_calls = 0

def forward_blur_animation(radius:int) -> None:
    blurred_logo = logo.filter(ImageFilter.GaussianBlur(radius))
    logo_photo = ImageTk.PhotoImage(blurred_logo)
    gv.logo_label.configure(image=logo_photo)
    gv.logo_label.image = logo_photo
    if radius < 6:
        gv.window.after(75, forward_blur_animation, radius + 1)

def backward_blur_animation(radius:int, back:tk.Button, new_project:tk.Button, old_project:tk.Button) -> None:
    global blur_func_calls
    if blur_func_calls == 0:
        sounds.play_click()
    if radius == 6:
        back.place_forget()
        new_project.place_forget()
        old_project.place_forget()
    blurred_logo = logo.filter(ImageFilter.GaussianBlur(radius))
    logo_photo = ImageTk.PhotoImage(blurred_logo)
    gv.logo_label.configure(image=logo_photo)
    gv.logo_label.image = logo_photo
    blur_func_calls += 1
    if radius > 0:
        gv.window.after(75, backward_blur_animation, radius - 1, back, new_project, old_project)
    else:
        for i in range(len(gv.main_menu_buttons)):
            if i == 0:
                gv.main_menu_buttons[i].place(relx=0.4875, rely=0.4, anchor="center")
            elif i == 1:
                gv.main_menu_buttons[i].place(relx=0.45, rely=0.3825)
            elif i == 2:
                gv.main_menu_buttons[i].place(relx=0.5075, rely=0.3775)
            elif i == 3:
                gv.main_menu_buttons[i].place(relx=0.4875, rely=0.42, anchor="center")
            elif i == 4:
                gv.main_menu_buttons[i].place(relx=0.52625, rely=0.3825)
            elif i == 5:
                gv.main_menu_buttons[i].place(relx=0.5, rely=0.38875)
            elif i == 6:
                gv.main_menu_buttons[i].place(relx=0.49, rely=0.395)
            elif i == 7:
                gv.main_menu_buttons[i].place(relx=0.515, rely=0.3775)
            elif i == 8:
                gv.main_menu_buttons[i].place(relx=0.435, rely=0.3875)
            elif i == 9:
                gv.main_menu_buttons[i].place(relx=0.87, rely=0.87)
        gv.main_menu_buttons[0].tkraise()
        blur_func_calls = 0


def inc_score(inc=1):
    gv.star_score += inc
    print(gv.star_score)

def gold_score():
    inc_score(50)
    if not gv.touched_gold and gv.project != None:
        gv.touched_gold = True
        projutil.save_project()
        messagebox.showinfo("Gold Clicked", "You clicked a gold star! Your project is now enchanted!")

def proj_bg_pos_generator() -> list:
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

def proj_bg_hor() -> None:
    gv.stars = []
    logo : Image
    regular_logo = Image.open(constants.LOGO_WITH_SKY_ICON)
    gold_logo = Image.open(constants.GOLDLOGO_WITH_SKY_ICON)
    x_increase = 1/42
    y_positions = proj_bg_pos_generator()
    speed_range = range(20,201)
    idx = 1
    for y in y_positions:
        resizing = rr.choice(range(10, 41))
        if not gv.touched_gold:
            initisGold = rr.choice(range(1, 1001)) == 1000
            logo = gold_logo if initisGold else regular_logo
        else:
            initisGold = True
            logo = gold_logo
        logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo)
        logo_label = tk.Button(gv.window, image=logo_photo, relief="flat", bd=0, highlightthickness=0)
        logo_label.image = logo_photo
        logo_label.place(relx=x_increase*idx, rely=y)
        if initisGold: logo_label.configure(command=gold_score)
        else: logo_label.configure(command=inc_score)
        idx += 1
        gv.stars.append((logo_label, x_increase*idx, y, rr.choice(speed_range) / 10000))
    
    def loop_l() -> str:
        for idx, star_comb in enumerate(gv.stars):
            star_comb = list(star_comb)
            try:
                star_comb[0].place_forget()
                if star_comb[1] - star_comb[3] <= 0:
                    resizing = rr.choice(range(10, 41))
                    if not gv.touched_gold:
                        isGold = rr.choice(range(1, 1001)) == 1000
                        logo = gold_logo if isGold else regular_logo
                    else:
                        isGold = True
                        logo = gold_logo
                    logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
                    logo_photo = ImageTk.PhotoImage(logo)
                    star_comb[0].configure(image=logo_photo)
                    star_comb[0].image = logo_photo
                    if isGold: star_comb[0].configure(command=gold_score)
                    else: star_comb[0].configure(command=inc_score)
                    star_comb[1] = 1
                    star_comb[3] = rr.choice(speed_range) / 10000
                else:
                    star_comb[1] = star_comb[1] - star_comb[3]
                star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
                gv.stars[idx] = tuple(star_comb)
            except:
                pass
        this_loop = gv.window.after(33, loop_l)
        gv.star_loop[0] = this_loop
        return this_loop

    def loop_r() -> str:
        for idx, star_comb in enumerate(gv.stars):
            star_comb = list(star_comb)
            try:
                star_comb[0].place_forget()
                if star_comb[1] - star_comb[3] >= 1:
                    resizing = rr.choice(range(10, 41))
                    if not gv.touched_gold:
                        isGold = rr.choice(range(1, 1001)) == 1000
                        logo = gold_logo if isGold else regular_logo
                    else:
                        isGold = True
                        logo = gold_logo
                    logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
                    logo_photo = ImageTk.PhotoImage(logo)
                    star_comb[0].configure(image=logo_photo)
                    star_comb[0].image = logo_photo
                    if isGold: star_comb[0].configure(command=gold_score)
                    else: star_comb[0].configure(command=inc_score)
                    star_comb[1] = 0
                    star_comb[3] = rr.choice(speed_range) / 10000
                else:
                    star_comb[1] = star_comb[1] + star_comb[3]
                star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
                gv.stars[idx] = tuple(star_comb)
            except:
                pass
        this_loop = gv.window.after(33, loop_r)
        gv.star_loop[0] = this_loop
        return this_loop
    
    def start_lstar_loop():
        gv.star_loop[0] = loop_l()

    def start_rstar_loop():
        gv.star_loop[0] = loop_r()
    
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0 :
        start_lstar_loop()
    else:
        start_rstar_loop()

def proj_bg_vert() -> None:
    gv.stars = []
    logo : Image
    regular_logo = Image.open(constants.LOGO_WITH_SKY_ICON)
    gold_logo = Image.open(constants.GOLDLOGO_WITH_SKY_ICON)
    x_positions = proj_bg_pos_generator()
    y_increase = 1/42
    speed_range = range(20,201)
    idx = 1
    for x in x_positions:
        resizing = rr.choice(range(10, 41))
        if not gv.touched_gold:
            initisGold = rr.choice(range(1, 1001)) == 1000
            logo = gold_logo if initisGold else regular_logo
        else:
            initisGold = True
            logo = gold_logo
        logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo)
        logo_label = tk.Button(gv.window, image=logo_photo, relief="flat", bd=0, highlightthickness=0)
        logo_label.image = logo_photo
        logo_label.place(relx=x, rely=y_increase*idx)
        if initisGold: logo_label.configure(command=gold_score)
        else: logo_label.configure(command=inc_score)
        idx += 1
        gv.stars.append((logo_label, x, y_increase*idx, rr.choice(speed_range) / 10000))
    
    def loop_n() -> str:
        for idx, star_comb in enumerate(gv.stars):
            star_comb = list(star_comb)
            try:
                star_comb[0].place_forget()
                if star_comb[2] - star_comb[3] <= 0:
                    resizing = rr.choice(range(10, 41))
                    if not gv.touched_gold:
                        isGold = rr.choice(range(1, 1001)) == 1000
                        logo = gold_logo if isGold else regular_logo
                    else:
                        isGold = True
                        logo = gold_logo
                    logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
                    logo_photo = ImageTk.PhotoImage(logo)
                    star_comb[0].configure(image=logo_photo)
                    star_comb[0].image = logo_photo
                    if isGold: star_comb[0].configure(command=gold_score)
                    else: star_comb[0].configure(command=inc_score)
                    star_comb[2] = 1
                    star_comb[3] = rr.choice(speed_range) / 10000
                else:
                    star_comb[2] = star_comb[2] - star_comb[3]
                star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
                gv.stars[idx] = tuple(star_comb)
            except:
                pass
        this_loop = gv.window.after(33, loop_n)
        gv.star_loop[0] = this_loop
        return this_loop
    
    def loop_s() -> str:
        for idx, star_comb in enumerate(gv.stars):
            star_comb = list(star_comb)
            try:
                star_comb[0].place_forget()
                if star_comb[2] - star_comb[3] >= 1:
                    resizing = rr.choice(range(10, 41))
                    if not gv.touched_gold:
                        isGold = rr.choice(range(1, 1001)) == 1000
                        logo = gold_logo if isGold else regular_logo
                    else:
                        isGold = True
                        logo = gold_logo
                    logo = logo.resize((resizing, resizing), Image.Resampling.LANCZOS)
                    logo_photo = ImageTk.PhotoImage(logo)
                    star_comb[0].configure(image=logo_photo)
                    star_comb[0].image = logo_photo
                    if isGold: star_comb[0].configure(command=gold_score)
                    else: star_comb[0].configure(command=inc_score)
                    star_comb[2] = 0
                    star_comb[3] = rr.choice(speed_range) / 10000
                else:
                    star_comb[2] = star_comb[2] + star_comb[3]
                star_comb[0].place(relx=star_comb[1], rely=star_comb[2])
                gv.stars[idx] = tuple(star_comb)
            except:
                pass
        this_loop = gv.window.after(33, loop_s)
        gv.star_loop[0] = this_loop
        return this_loop
    
    def start_nstar_loop():
        gv.star_loop[0] = loop_n()
    
    def start_sstar_loop():
        gv.star_loop[0] = loop_s()
    
    choices = [0, 1]
    choice = rr.choice(choices)
    if choice == 0 :
        start_nstar_loop()
    else:
        start_sstar_loop()