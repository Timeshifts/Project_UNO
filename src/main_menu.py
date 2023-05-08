import pygame
from constant import *
from menu import Menu


# 메인 메뉴
class Main_menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["싱글플레이", "멀티플레이", "스토리모드", "업적", "설정", "게임 종료"]

    # 버튼이 있어야 할 위치 반환
    def pos_formula(self, i): 
        if i < len(self.avail_menu) / 2:
            return (self.size[0] * 0.35, self.size[1] * (7 + i) / 10)
        else:
            return (self.size[0] * 0.65, self.size[1] * (7 + i-len(self.avail_menu) / 2) / 10)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.avail_menu[index] == "게임 종료":
            pygame.event.post(pygame.event.Event(EVENT_QUIT_GAME))  # 게임 종료
        elif self.avail_menu[index] == "설정":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_OPTION))  # 옵션 열기
        elif self.avail_menu[index] == "싱글플레이":
            pygame.event.post(pygame.event.Event(EVENT_START_LOBBY))  # 싱글플레이 로비
        elif self.avail_menu[index] == "스토리모드":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_STORYMAP))  # 스토리 모드
        elif self.avail_menu[index] == "멀티플레이":
            pygame.event.post(pygame.event.Event(EVENT_START_LOBBY_MULTI)) # 멀티플레이 로비
        elif self.avail_menu[index] == "업적":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_ACHIEVEMENT))  # 업적 열기
