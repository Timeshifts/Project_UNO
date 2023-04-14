import GameManager as GM
import pygame
from button import Button
from setting import Settings
from constant import *

clock = pygame.time.Clock()


class Single:
    # 가능한 메뉴 목록
    deck = "DECK"
    uno = "UNO"
    avail_menu = ["RESUME", "OPTIONS", "MAIN"]

    # 버튼이 있어야 할 위치 반환
    def get_position(self, index):
        return (
            self.pos[0],
            self.pos[1] + self.size[1] * 1.2 * index,
        )

    # 폰트 설정
    def get_font(self, size):
        return pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

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
        self.game_start()
        # self.turn_start()

    def update(self):
        self.hand_card = []  # 각자 소유한 카드
        for i in range(self.computer_count + 1):
            self.hand_card.append([])
            for j in range(len(self.game.players[i].hand)):
                self.hand_card[i].append(
                    f"{self.game.players[i].hand[j].color}_{self.game.players[i].hand[j].name}"
                )
        self.my_card = self.hand_card[0]  # 내가 소유한 카드
        self.game.grave_top_color
        self.game.grave_top.name
        self.game.turn

    def game_start(self):
        self.game = GM.Gm
        self.game.computer_count = self.computer_count
        self.game.start_cards_integer = 5
        self.game.game_start()

        self.update()
        print(f"내 카드 : {self.my_card}")
        print(f"{self.game.grave_top_color}_{self.game.grave_top.name}")  # 카드 묘지
        print(f"{self.game.turn}")

    def turn_start(self):
        self.game.turn_start()
        self.update()

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
        fontsize = 50
        font = self.get_font(fontsize)
        for i in range(self.max_menu):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeColor(True, screen)
            else:
                self.button[i].changeColor(False, screen)

        for i in range(self.computer_count):
            # Player List 상자
            playlist_box = pygame.image.load(RESOURCE_PATH / "single" / "list.png")
            playlist_box_rect = playlist_box.get_rect(
                center=(self.size[0] * 7 / 8, self.size[1] * (2 * i + 3) / 12)
            )
            screen.blit(playlist_box, playlist_box_rect)
            # Player List 컴퓨터 이름
            playlist_player_name = font.render("Player_" + str(i + 1), True, "White")
            screen.blit(
                playlist_player_name,
                (
                    self.size[0] * (7 / 8 - 1 / 8) + 30,
                    self.size[1] * ((2 * i + 3) / 12 - 1 / 12) + 10,
                ),
            )
            # Player List 컴퓨터 카드
            for j in range(len(self.hand_card[i])):  # GameManager의 Computer(i)의 카드 개수
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

        # 메인보드
        # 메인보드 컴퓨터 카드
        for i in range(self.computer_count):
            card_x = 87.75
            card_y = 122.85
            board_player_card = pygame.image.load(
                RESOURCE_PATH / "card" / "card_back.png"
            )
            board_player_card = pygame.transform.scale(
                board_player_card, (card_x, card_y)
            )
            screen.blit(
                board_player_card,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    - card_x / 2,
                    card_y * 2 / 3,
                ),
            )
        # 메인보드 컴퓨터 이름
        for i in range(self.computer_count):
            board_player_name = font.render("P" + str(i + 1), True, "White")
            screen.blit(
                board_player_name,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    - card_x / 2,
                    self.size[1] / 50,
                ),
            )
        # 메인보드 컴퓨터 카드 개수
        for i in range(self.computer_count):
            board_player_cardnum = font.render(
                f"{len(self.hand_card[i])}", True, "Black"
            )
            screen.blit(
                board_player_cardnum,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    - card_x / 6,
                    card_y * 5 / 3,
                ),
            )
        # 카드 덱
        deck_card_x = 130
        deck_card_y = 182
        deck_card = pygame.image.load(RESOURCE_PATH / "card" / "card_back.png")
        deck_card = pygame.transform.scale(deck_card, (deck_card_x, deck_card_y))
        screen.blit(
            deck_card,
            (
                self.size[0] * 3 / 8 - deck_card_x / 2 - deck_card_x * 2 / 3,
                self.size[1] / 2 - deck_card_y / 2,
            ),
        )
        # 카드 묘지
        grave_card_x = 130
        grave_card_y = 182
        grave_card = pygame.image.load(
            str(
                RESOURCE_PATH
                / "card"
                / f"{self.game.grave_top.color}_{self.game.grave_top.name}"
            )
            + ".png"
        )
        grave_card = pygame.transform.scale(grave_card, (grave_card_x, grave_card_y))
        screen.blit(
            grave_card,
            (
                self.size[0] * 3 / 8 - grave_card_x / 2 + grave_card_x * 2 / 3,
                self.size[1] / 2 - grave_card_y / 2,
            ),
        )
        # 카드 색상
        color_card_x = 80
        color_card_y = 80
        color_card = pygame.image.load(
            str(RESOURCE_PATH / "card" / f"{self.game.grave_top_color}") + ".png"
        )
        color_card = pygame.transform.scale(color_card, (color_card_x, color_card_y))
        screen.blit(
            color_card,
            (
                self.size[0] * 3 / 8 - color_card_x / 2 + grave_card_x * 11 / 6,
                self.size[1] / 2 - color_card_y / 2,
            ),
        )
        # 우노 버튼
        uno_x = 200
        uno_y = 200
        uno = pygame.image.load(str(RESOURCE_PATH / "single" / "uno_button.png"))
        uno = pygame.transform.scale(uno, (uno_x, uno_y))
        screen.blit(
            uno,
            (
                self.size[0] * 3 / 4 - uno_x - 20,
                self.size[1] * 3 / 4 - uno_y - 20,
            ),
        )

        # 내 보드
        # 내 이름
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
            card_x = 182
            card_y = 254.8
            playlist_player_card = pygame.image.load(
                str(RESOURCE_PATH / "card" / self.my_card[i]) + ".png"
            )
            playlist_player_card = pygame.transform.scale(
                playlist_player_card, (card_x, card_y)
            )
            screen.blit(
                playlist_player_card,
                (
                    self.size[0] / 30 + i * card_x / 2,
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
