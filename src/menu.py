import pygame, setting
from button import Button
from constant import *


# 메인 메뉴
class Menu:
    # 가능한 메뉴 목록
    avail_menu = []

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    # 위치를 구하는 공식
    pos_formula = lambda self, i: (self.size[0] / 2, self.size[1] * (6 + i) / 10)

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "y"

    def __init__(self, pos=(0, 0), size=(150, 50), settings=None):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False
        self.settings = settings

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1
        self.init_draw()

    def init_draw(self):
        self.button = []
        self.rect = []

        for i in range(self.max_menu):
            # 버튼 삽입
            self.button.append(
                Button(
                    pygame.image.load(RESOURCE_PATH / "main" / "main_button.png"),
                    pygame.image.load(
                        RESOURCE_PATH / "main" / "main_button_highlight.png"
                    ),
                    pos=self.pos_formula(i),
                    text_input=self.menu[i],
                    font=self.get_font(50),
                    base_color="#3a4aab",
                    hovering_color="White",
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i].rect)

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

        for i in range(self.max_menu):
            self.button[i].resize(size)
            self.rect[i] = self.button[i].rect

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_menu):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeHighlight(True, screen)
            else:
                self.button[i].changeHighlight(False, screen)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        for i in range(self.max_menu):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect[i].collidepoint(event.pos):
                    self.select_menu(i)
                    break  # 한 번에 여러 개의 메뉴가 눌리지 않도록 처리
            elif event.type == pygame.MOUSEMOTION:
                if self.rect[i].collidepoint(event.pos):
                    # highlight 대상을 변경
                    self.highlight = i
                    # 키보드 선택 해제
                    self.selected = -1
            elif event.type == pygame.KEYDOWN:
                if self.pressed == False:
                    self.pressed = True
                    # 엔터 키가 눌렸을 때
                    if event.key == setting.options["enter"]:
                        # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                        if self.selected != -1:
                            self.select_menu(self.selected)
                    elif (
                        event.key
                        == setting.options["up" if self.axis == "y" else "left"]
                    ):
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif (
                        event.key
                        == setting.options["down" if self.axis == "y" else "right"]
                    ):
                        # 선택을 하나 아래로 이동
                        self.selected = (
                            self.selected + 1
                            if self.selected < self.max_menu - 1
                            else self.max_menu - 1
                        )
                        self.highlight = self.selected
            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False
