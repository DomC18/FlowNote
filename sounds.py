import pygame as pyg
import constants

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