import pygame, pickle
from constant import *
from menu import Menu

class StoryMenu(Menu):
    
    # 현재 몇 개의 스토리?
    story_amount = 4

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    # 가능한 메뉴 목록
    avail_menu = list(str(x) for x in range(story_amount))

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * (3 + 2*i) / 12, self.size[1]/3*2)

    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                self.progress = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            self.progress = []

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(self.progress, f)

    def __init__(self, pos=(0, 0), size=(150, 50), settings=None):
        self.progress = []
        self.progress_path = RESOURCE_PATH / "story_progress.ini"
        self.load_progress()
        super().__init__(pos, size, settings)
    
    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        print(f"{index}번 스토리 시작")

class StoryMap():

    def __init__(self, pos, size, settings):
        self.STORY_MENU = StoryMenu(pos, size, settings)

    def draw(self, screen):
        self.STORY_MENU.draw(screen)

    def handle_event(self, event):
        self.STORY_MENU.handle_event(event)
