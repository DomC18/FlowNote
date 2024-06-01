import os

FOLDERPATH = os.path.abspath(__file__)[:-12]
USER_PROJECTS_PATH = FOLDERPATH + r"UserProjects"
UI_PATH = FOLDERPATH + r"Icons"
LOGO_UNSIGNED_ICON = UI_PATH + r"\logounsigned.jpg"
ACTUALLY_TRANSPARENT_ICON = UI_PATH + r"\actuallytransparent.png"
SKY_ICON = UI_PATH + r"\sky.jpg"
LOGO_WITH_SKY_ICON = UI_PATH + r"\logowithsky.jpg"
SOUNDS_PATH = FOLDERPATH + r"Sounds"
CLICK_SOUND = SOUNDS_PATH + r"\click.wav"
BACK_SOUND = SOUNDS_PATH + r"\back.wav"
POP_SOUND = SOUNDS_PATH + r"\pop.wav"