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

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.max_computer = len(self.computer)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False
        self.computer_chk = [True, False, False, False, False]

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1
        self.init_draw()

        # 본인 이름 수정
        self.text_name = self.get_font(50).render(self.name, True, "White")
        self.text_name_rect = self.text_name.get_rect(
            center=(self.size[0] / 2, self.size[1] / 3)
        )

    def init_draw(self):
        self.button = []
        self.rect = []

        for i in range(self.max_computer):
            # 버튼 삽입
            if self.computer_chk[i] == True:
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
                    pygame.image.load(RESOURCE_PATH / "single" / "list_hovering.png"),
                    pos=(self.size[0] * 7 / 8, self.size[1] * (2 * i + 3) / 12),
                    text_input=text,
                    font=self.get_font(50),
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
                    font=self.get_font(50),
                    base_color="#3a4aab",
                    hovering_color="White",
                )
            )
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i + self.max_computer].rect)
            # highlight용 오브젝트 생성
            # #############################
            # self.highlight_obj = pygame.transform.scale(
            #     pygame.image.load(RESOURCE_PATH / "highlight.png"), self.size
            # )
            # #############################

    def resize(self, size):
        pass

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_computer + self.max_menu):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeColor(True, screen)
            else:
                self.button[i].changeColor(False, screen)

        # Add a Player 텍스트
        font = self.get_font(50)
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

        if index < self.max_computer:
            if self.computer_chk[index] == True:
                self.button[index].ChangeImage(
                    pygame.image.load(RESOURCE_PATH / "single" / "list_unpicked.png")
                )
                self.button[index].ChangeText("+", "Black", "Black")
                self.computer_chk[index] = False
            else:
                self.button[index].ChangeImage(
                    pygame.image.load(RESOURCE_PATH / "single" / "list.png")
                )
                self.button[index].ChangeText(self.computer[index], "White", "White")
                self.computer_chk[index] = True
        else:
            index -= self.max_computer
            if self.avail_menu[index] == "RENAME":
                pygame.event.post(pygame.event.Event(EVENT_OPEN_RENAME))  # 이름 변경
            elif self.avail_menu[index] == "START":
                if self.computer_chk.count(True) == 0:
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
