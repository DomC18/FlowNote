import pygame as pyg
import constants

def play_sound(filedir:str) -> None:
    pyg.mixer.init()
    pyg.mixer.music.load(filedir)
    pyg.mixer.music.play()

def play_click() -> None:
    play_sound(constants.CLICK_SOUND)

def play_back() -> None:
    play_sound(constants.BACK_SOUND)

def play_pop() -> None:
    play_sound(constants.POP_SOUND)