import random
import pygame
from setting import Settings
from constant import *


class Card:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.is_blind = Settings.default_setting["colorblind"]
        if self.is_blind == False:
            self.filename = "card/" + self.color + "_" + self.name + ".png"
        else:
            self.filename = "card_colorblind/" + self.color + "_" + self.name + ".png"
        self.card_data = pygame.image.load(RESOURCE_PATH / self.filename)
        self.rect = self.card_data.get_rect()  # card_data 의 위치정보를 가져온다
        self.score = score(self.name, self.color)

    def __str__(self):
        return "name: {0},color: {1},filename: {2},score: {3}, is_blind: {4}".format(
            self.name, self.color, self.filename, self.score, self.is_blind
        )

    def colorblind(self, blind):
        if blind == False:
            self.filename = "card/" + self.color + "_" + self.name + ".png"
        else:
            self.filename = "card_colorblind/" + self.color + "_" + self.name + ".png"
        self.card_data = pygame.image.load(RESOURCE_PATH / self.filename)
        self.rect = self.card_data.get_rect()  # card_data 의 위치정보를 가져온다
        self.is_blind = blind


def score(name, color):
    if color == "wild":
        return 50
    elif name.isdigit():
        return int(name)
    else:
        return 20
