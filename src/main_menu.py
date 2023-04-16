import pygame
from constant import *
from menu import Menu


# 메인 메뉴
class Main_menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["PLAY", "STORY", "OPTIONS", "QUIT"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] / 2, self.size[1] * (6 + i) / 10)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.avail_menu[index] == "QUIT":
            pygame.event.post(pygame.event.Event(EVENT_QUIT_GAME))  # 게임 종료
        elif self.avail_menu[index] == "OPTIONS":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_OPTION))  # 옵션 열기
        elif self.avail_menu[index] == "PLAY":
            pygame.event.post(pygame.event.Event(EVENT_START_LOBBY))  # 싱글플레이 로비
        elif self.avail_menu[index] == "STORY":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_STORYMAP))  # 스토리 모드
