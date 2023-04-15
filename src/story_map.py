import pygame, pickle
from constant import *
from menu import Menu


class StoryMenu(Menu):
    # 현재 몇 개의 스토리?
    story_amount = 4

    # 스토리 진행도 (몇 번 스토리까지 클리어?)
    story_progress = 0

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    # 가능한 메뉴 목록
    avail_menu = ("", "", "", "", "돌아가기")

    # 버튼이 있어야 할 위치 반환
    def pos_formula(self, i):
        if i != self.story_amount:
            x_pos = self.size[0] * (3 + 3 * i) / 15
        else:
            x_pos = self.size[0] / 2
        if i != self.story_amount:
            y_pos = self.size[1] / 2
        else:
            y_pos = self.size[1] * 0.8
        return (x_pos, y_pos)
    

    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                self.story_progress = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            self.story_progress = 0

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(self.story_progress, f)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.story_progress = 0
        self.progress_path = RESOURCE_PATH / "story_progress.ini"
        self.load_progress()

        story_img = lambda s: tuple(
            RESOURCE_PATH / "story" / f"story_{i}.png"
            for i in range(1, s+1))
        
        super().__init__(pos, size, scale=(0.75, 0.75),
                         button_img=story_img(self.story_amount),
                         hovering_img=story_img(self.story_amount))

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        # 스토리 다음 버튼 = 돌아가기 버튼
        if index == self.story_amount:
            pygame.event.post(pygame.event.Event(EVENT_MAIN))
            return
        print(f"{index}번 스토리 시작")


class StoryMap:
    def __init__(self, pos, size):
        self.STORY_MENU = StoryMenu(pos, size)

    def draw(self, screen):
        self.STORY_MENU.draw(screen)

    def handle_event(self, event):
        self.STORY_MENU.handle_event(event)
    
    def resize(self, size):
        self.STORY_MENU.resize(size)