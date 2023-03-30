import pygame
from pathlib import Path

RESOURCE_PATH = Path.cwd() / "resources"

EVENT_QUIT_GAME = pygame.event.custom_type()
EVENT_MAIN = pygame.event.custom_type()
EVENT_START_LOBBY = pygame.event.custom_type()
EVENT_START_SINGLE = pygame.event.custom_type()
EVENT_OPEN_OPTION = pygame.event.custom_type()
EVENT_OPTION_CHANGED = pygame.event.custom_type()
EVENT_CLOSE_OPTION = pygame.event.custom_type()
EVENT_START_MENU = pygame.event.custom_type()
EVENT_START_STORY = pygame.event.custom_type()
EVENT_PLAY_SE = pygame.event.custom_type()
EVENT_OPEN_RENAME = pygame.event.custom_type()
EVENT_CLOSE_RENAME = pygame.event.custom_type()