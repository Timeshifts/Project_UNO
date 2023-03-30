import pygame
from button import Button
from setting import Settings
from constant import *


# 싱글플레이
class Single:
    # 가능한 메뉴 목록
    my_card = ["blue_0", "green_5"]  # GameManager에서 self.hand 가져오기
    deck = "DECK"
    uno = "UNO"
    avail_menu = ["RESUME", "OPTIONS", "MAIN"]

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (
        self.pos[0],
        self.pos[1] + self.size[1] * 1.2 * index,
    )

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, pos=(0, 0), size=(150, 50), computer_count=1, name="ME"):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.computer_count = computer_count
        self.name = name
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
                self.button[i].forceChangeColor(True, screen)
            else:
                self.button[i].forceChangeColor(False, screen)

        for i in range(self.computer_count):
            # Player List 상자
            playlist_box = pygame.image.load(RESOURCE_PATH / "single" / "list.png")
            playlist_box_rect = playlist_box.get_rect(
                center=(self.size[0] * 7 / 8, self.size[1] * (2 * i + 3) / 12)
            )
            screen.blit(playlist_box, playlist_box_rect)
            # Player List 컴퓨터 이름
            font = self.get_font(50)
            playlist_player_name = font.render("Player_" + str(i + 1), True, "White")
            screen.blit(
                playlist_player_name,
                (
                    self.size[0] * (7 / 8 - 1 / 8) + 30,
                    self.size[1] * ((2 * i + 3) / 12 - 1 / 12) + 10,
                ),
            )
            # Player List 컴퓨터 카드
            for j in range(7):  # GameManager의 Computer(i)의 카드 개수
                card_x = 52
                card_y = 72.8
                playlist_player_card = pygame.image.load(
                    RESOURCE_PATH / "card" / "card_back.png"
                )
                playlist_player_card = pygame.transform.scale(
                    playlist_player_card, (card_x, card_y)
                )
                screen.blit(
                    playlist_player_card,
                    (
                        self.size[0] * (7 / 8 - 1 / 8) + 30 + j * card_x / 3,
                        self.size[1] * ((2 * i + 3) / 12 - 1 / 12) + 80,
                    ),
                )

        # 내 보드
        # 내 이름
        font = self.get_font(50)
        my_name = font.render(self.name, True, "White")
        screen.blit(
            my_name,
            (
                self.size[0] / 30,
                self.size[1] * 2 / 3,
            ),
        )
        # 내 카드
        for i in range(len(self.my_card)):
            card_x = 195
            card_y = 273
            playlist_player_card = pygame.image.load(
                str(RESOURCE_PATH / "card" / self.my_card[i]) + ".png"
            )
            playlist_player_card = pygame.transform.scale(
                playlist_player_card, (card_x, card_y)
            )
            screen.blit(
                playlist_player_card,
                (
                    self.size[0] / 30 + i * card_x / 3,
                    self.size[1] - card_y,
                ),
            )

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

        if self.avail_menu[index] == "RESUME":
            pass
        elif self.avail_menu[index] == "OPTIONS":
            pass
        elif self.avail_menu[index] == "MAIN":
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
                    elif event.key == Settings().settings["up"]:
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif event.key == Settings().settings["down"]:
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
