import pygame
from button import Button
import setting
from constant import *


# 싱글플레이
class Rename:
    # 가능한 메뉴 목록
    avail_menu = ["DONE", "CANCEL"]
    name = "ME"

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (
        self.pos[0],
        self.pos[1] + self.size[1] * 1.2 * index,
    )

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1
        self.init_draw()

        # 본인 이름 수정
        self.text_name = self.get_font(50).render(self.name, True, "White")
        self.text_name_rect = self.text_name.get_rect(
            center=(self.size[0] / 2, self.size[1] / 12)
        )

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
                    pos=(self.size[0] / 2, self.size[1] * (2 * i + 13) / 20),
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

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_menu):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeColor(True, screen)
            else:
                self.button[i].changeColor(False, screen)

        screen.blit(
            self.text_name,
            self.text_name_rect,
        )

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

        if self.avail_menu[index] == "DONE":
            pass
            # pygame.event.post(pygame.event.Event(EVENT_OPEN_OPTION))  # 옵션 열기
        elif self.avail_menu[index] == "CANCLE":
            pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인 메뉴

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
                    if event.key == Settings().settings["enter"]:
                        # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                        if self.selected != -1:
                            self.select_menu(self.selected)
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.name) > 0:
                            self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
                    self.text_name = self.get_font(50).render(self.name, True, "BLACK")
                    self.text_name_rect.size = self.text_name.get_size()

            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False
