import pygame
import random
import numpy
import sys
import webbrowser
import os

sc = 40
esay_score = 50
medium_score = 160
hard_score = 500
flag_esay = False
flag_medium = False
flag_hard = False

size = width, height = 1000, 700
board_size = [700, 700]
info_size = [width - height, height]
link = 'http://xn--80aafypuh.xn--80aa1agjdchjh2p.xn--p1ai/'
font = 'Times New Roman'
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")
h1 = pygame.font.SysFont(font, 40)
h2 = pygame.font.SysFont(font, 20)

music = pygame.mixer.music.load('music/One-Love-Emotional-Piano-Strings(chosic.com).mp3')
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0)
