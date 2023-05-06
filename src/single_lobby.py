import pygame, setting
from button import Button
from constant import *


# 싱글플레이
class SingleLobby:
    # 가능한 메뉴 목록
    computer = ["1", "2", "3", "4", "5"]
    avail_menu = ["RENAME", "START", "BACK"]
    name = "My Name"

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (
        self.pos[0],
        self.pos[1] + self.size[1] * 1.2 * index,
    )

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.max_computer = len(self.computer)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False
        self.computer_chk = [1, 0, 0, 0, 0]  # 0: 없음, 1: 기본 컴퓨터, 2: A지역 컴퓨터

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1
        self.init_draw()

    def init_draw(self):
        self.button = []
        self.rect = []

        for i in range(self.max_computer):
            # 버튼 삽입
            if self.computer_chk[i] == 1:
                image = pygame.image.load(RESOURCE_PATH / "single" / "list.png")
                text = self.computer[i]
                color = "White"
            else:
                image = pygame.image.load(
                    RESOURCE_PATH / "single" / "list_unpicked.png"
                )
                text = "+"
                color = "Black"
            self.button.append(
                Button(
                    image,
                    image,
                    pos=(self.size[0] * 7 / 8, self.size[1] * (2 * i + 3) / 12),
                    text_input=text,
                    font=setting.get_font(50),
                    base_color=color,
                    hovering_color=color,
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i].rect)

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
                    font=setting.get_font(50),
                    base_color="#3a4aab",
                    hovering_color="White",
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i + self.max_computer].rect)

            # 본인 이름 수정
            self.text_name = setting.get_font(50).render(self.name, True, "White")
            self.text_name_rect = self.text_name.get_rect(
                center=(self.size[0] / 2, self.size[1] / 3)
            )

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_computer + self.max_menu):
            self.button[i].update(screen)
            # 컴퓨터 추가 영역 호버링 중지
            if i == self.highlight and i >= self.max_computer:
                self.button[i].changeHighlight(True, screen)
            else:
                if i >= self.max_computer:
                    self.button[i].changeHighlight(False, screen)

        # Add a Player 텍스트
        font = setting.get_font(50)
        text_player = font.render("Add a Player", True, "White")
        text_player_rect = text_player.get_rect(
            center=(self.size[0] * 7 / 8, self.size[1] / 12)
        )
        screen.blit(
            text_player,
            text_player_rect,
        )

        # 본인 이름 수정
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

        list_x = 480 * setting.get_screen_scale()
        list_y = 180 * setting.get_screen_scale()

        if index < self.max_computer:
            if self.computer_chk[index] == 1:
                self.button[index].ChangeImage(
                    pygame.transform.scale(
                        pygame.image.load(RESOURCE_PATH / "single" / "list_unpicked.png"),
                        (list_x, list_y)
                    )
                )
                self.button[index].ChangeText("+", "Black", "Black")
                self.computer_chk[index] = 0
            else:
                self.button[index].ChangeImage(
                    pygame.transform.scale(
                        pygame.image.load(RESOURCE_PATH / "single" / "list.png"),
                        (list_x, list_y)
                    )
                )
                self.button[index].ChangeText(self.computer[index], "White", "White")
                self.computer_chk[index] = 1
        else:
            index -= self.max_computer
            if self.avail_menu[index] == "RENAME":
                pygame.event.post(pygame.event.Event(EVENT_OPEN_RENAME))  # 이름 변경
            elif self.avail_menu[index] == "START":
                if self.computer_chk.count(0) == 5: # 모두 0인 경우
                    pass
                else:
                    pygame.event.post(pygame.event.Event(EVENT_START_SINGLE))  # 게임 시작
            elif self.avail_menu[index] == "BACK":
                pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인 메뉴

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        for i in range(self.max_computer + self.max_menu):
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
                    elif event.key == setting.options["up"]:
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif event.key == setting.options["down"]:
                        # 선택을 하나 아래로 이동
                        self.selected = (
                            self.selected + 1
                            if self.selected < self.max_computer + self.max_menu - 1
                            else self.max_computer + self.max_menu - 1
                        )
                        self.highlight = self.selected

            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False
