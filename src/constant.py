import pygame
from pathlib import Path

RESOURCE_PATH = Path.cwd() / "resources"

EVENT_QUIT_GAME = pygame.event.custom_type()
EVENT_MAIN = pygame.event.custom_type()

EVENT_START_LOBBY = pygame.event.custom_type()
EVENT_START_SINGLE = pygame.event.custom_type()
EVENT_OPEN_RENAME = pygame.event.custom_type()
EVENT_CLOSE_RENAME = pygame.event.custom_type()

EVENT_COMPUTER_THINK = pygame.event.custom_type()
EVENT_TURN_END = pygame.event.custom_type()
EVENT_END_GAME = pygame.event.custom_type()

EVENT_OPEN_OPTION = pygame.event.custom_type()
EVENT_OPTION_CHANGED = pygame.event.custom_type()
EVENT_CLOSE_OPTION = pygame.event.custom_type()

EVENT_OPEN_STORYMAP = pygame.event.custom_type()
EVENT_PLAY_SE = pygame.event.custom_type()

EVENT_OPEN_ACHIEVEMENT = pygame.event.custom_type()
EVENT_ACQUIRE_ACHIEVEMENT = pygame.event.custom_type()

EVENT_START_LOBBY_MULTI = pygame.event.custom_type()
EVENT_START_MULTI = pygame.event.custom_type()
EVENT_OPEN_HOST_PASSWORD = pygame.event.custom_type()
EVENT_CLOSE_HOST_PASSWORD = pygame.event.custom_type()
EVENT_OPEN_CLIENT_PASSWORD = pygame.event.custom_type()
EVENT_CLOSE_CLIENT_PASSWORD = pygame.event.custom_type()
EVENT_OPEN_ENTER_IP = pygame.event.custom_type()
EVENT_CLOSE_ENTER_IP = pygame.event.custom_type()

EVENT_UPDATE = pygame.event.custom_type()
