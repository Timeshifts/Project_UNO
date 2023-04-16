import GameManager as GM
import pygame, setting
from button import Button
from constant import *

clock = pygame.time.Clock()


class Single:
    # 폰트 설정
    def get_font(self, size):
        return pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, pos=(0, 0), size=(150, 50), computer_count=1, name="ME"):
        # self.menu = self.avail_menu
        # self.max_menu = len(self.menu)
        self.computer_count = computer_count
        self.name = name
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False
        self.hand_card = []  # 각자 소유한 카드
        self.my_card = []  # 내가 소유한 카드
        self.max_card = 0  # 내가 소유한 카드 개수
        self.possible_cards_num = []  # 선택이 가능한 카드
        self.game_timer = 0
        self.first = 0
        self.is_turn_reversed = False  # 턴 방향

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1

        self.game_start()
        self.init_draw()

    def update_card(self):
        self.hand_card = []  # 각자 소유한 카드
        for i in range(self.computer_count + 1):
            self.hand_card.append([])
            for j in range(len(self.game.players[i].hand)):
                self.hand_card[i].append(
                    f"{self.game.players[i].hand[j].color}_{self.game.players[i].hand[j].name}"
                )
        self.my_card = self.hand_card[0]  # 내가 소유한 카드
        self.max_card = len(self.my_card)  # 내가 소유한 카드 개수
        self.game_timer = self.game.game_timer_integer
        self.is_turn_reversed = self.game.is_turn_reversed
        # self.init_draw()

    def game_start(self):
        self.game = GM.Gm
        self.game.computer_count = self.computer_count
        self.game.start_cards_integer = 5
        self.game.game_start()
        self.update_card()

    def turn_start(self):
        # self.game.turn_start()
        self.update_card()
        # self.init_draw()
        if self.game.turn == 0:  # 플레이어인 경우
            if self.first == 0:
                self.game.turn_start()
                # self.update_card()
                self.possible_cards_num = self.game.players[0].play()
                self.init_draw()
                self.first = 1
        else:  # 컴퓨터인 경우
            pygame.time.wait(2000)
            self.game.turn_start()
            self.update_card()
            self.first = 0
            self.game.players[self.game.turn].computer_play()
            self.game.turn_end()
            self.update_card()
            se_event = pygame.event.Event(
                EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
            )
            pygame.event.post(se_event)

        if self.game.end == 1:  # 게임 종료
            return 0
        else:
            return 1

    def init_draw(self):
        self.button = []
        self.rect = []

        # 내 카드
        card_x = 130
        card_y = 182
        for i in range(self.max_card):
            # 버튼 삽입
            if self.game.turn == 0:
                if i in self.possible_cards_num:
                    self.button.append(
                        Button(
                            pygame.transform.scale(
                                pygame.image.load(
                                    str(RESOURCE_PATH / "card" / self.my_card[i])
                                    + ".png"
                                ),
                                (card_x, card_y),
                            ),
                            pygame.transform.scale(
                                pygame.image.load(
                                    RESOURCE_PATH / "card" / "highlight.png"
                                ),
                                (card_x, card_y),
                            ),
                            pos=(
                                (i + 1.5) * card_x * 3 / 4,
                                self.size[1] - card_y,
                            ),
                            text_input="",
                            font=self.get_font(50),
                            base_color="Black",
                            hovering_color="Black",
                        )
                    )
                else:
                    self.button.append(
                        Button(
                            pygame.transform.scale(
                                pygame.image.load(
                                    str(RESOURCE_PATH / "card" / self.my_card[i])
                                    + ".png"
                                ),
                                (card_x, card_y),
                            ),
                            pygame.transform.scale(
                                pygame.image.load(
                                    RESOURCE_PATH / "card" / "shadow.png"
                                ),
                                (card_x, card_y),
                            ),
                            pos=(
                                (i + 1.5) * card_x * 3 / 4,
                                self.size[1] - card_y / 2,
                            ),
                            text_input="",
                            font=self.get_font(50),
                            base_color="Black",
                            hovering_color="Black",
                        )
                    )
            else:
                self.button.append(
                    Button(
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / "card" / self.my_card[i]) + ".png"
                            ),
                            (card_x, card_y),
                        ),
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / "card" / self.my_card[i]) + ".png"
                            ),
                            (card_x, card_y),
                        ),
                        pos=(
                            (i + 1.5) * card_x * 3 / 4,
                            self.size[1] - card_y / 2,
                        ),
                        text_input="",
                        font=self.get_font(50),
                        base_color="Black",
                        hovering_color="Black",
                    )
                )
            self.rect.append(self.button[i].rect)
        # 덱 버튼
        deck_card_x = 130
        deck_card_y = 182
        self.button.append(
            Button(
                pygame.transform.scale(
                    pygame.image.load(
                        str(RESOURCE_PATH / "card" / "card_back") + ".png"
                    ),
                    (deck_card_x, deck_card_y),
                ),
                pygame.transform.scale(
                    pygame.image.load(RESOURCE_PATH / "card" / "highlight.png"),
                    (deck_card_x, deck_card_y),
                ),
                pos=(
                    self.size[0] * 3 / 8 - deck_card_x * 2 / 3,
                    self.size[1] / 2,
                ),
                text_input="",
                font=self.get_font(50),
                base_color="Black",
                hovering_color="Black",
            )
        )
        self.rect.append(self.button[self.max_card].rect)
        # 우노 버튼
        uno_x = 200
        uno_y = 200
        self.button.append(
            Button(
                pygame.transform.scale(
                    pygame.image.load(RESOURCE_PATH / "single" / "uno_button.png"),
                    (uno_x, uno_y),
                ),
                pygame.transform.scale(
                    pygame.image.load(
                        RESOURCE_PATH / "single" / "uno_button_highlight.png"
                    ),
                    (uno_x, uno_y),
                ),
                pos=(
                    self.size[0] * 3 / 4 - uno_x / 2,
                    self.size[1] / 2,
                ),
                text_input="",
                font=self.get_font(50),
                base_color="Black",
                hovering_color="Black",
            )
        )
        # 각 버튼 이벤트 처리용 Rect 삽입
        self.rect.append(self.button[self.max_card + 1].rect)

    # 크기 변경에 맞춰 재조정
    # def resize(self, size):
    #     self.size = size
    #     self.init_draw()

    # 스크린에 자신을 그리기
    def draw(self, screen):
        fontsize = 50
        font = self.get_font(fontsize)
        for i in range(self.max_card + 2):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeHighlight1(True, screen)
            else:
                self.button[i].changeHighlight1(False, screen)

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
            for j in range(
                len(self.hand_card[i + 1])
            ):  # GameManager의 Computer(i)의 카드 개수
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
            color = "White"
            if self.game.turn == i + 1:
                color = "Blue"
            board_player_name = font.render("P" + str(i + 1), True, color)
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
                f"{len(self.hand_card[i+1])}", True, "Black"
            )
            screen.blit(
                board_player_cardnum,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    - card_x / 6,
                    card_y * 5 / 3,
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
                self.size[0] * 3 / 8 - color_card_x / 2 + grave_card_x * 5 / 3,
                self.size[1] / 2 - color_card_y / 2,
            ),
        )
        # 턴 방향
        rotation_x = 943
        rotation_y = 238
        if self.is_turn_reversed == False:
            rotation = pygame.image.load(RESOURCE_PATH / "single" / "rotation.png")
        else:
            rotation = pygame.image.load(
                RESOURCE_PATH / "single" / "rotation_reversed.png"
            )
        rotation = pygame.transform.scale(rotation, (rotation_x, rotation_y))
        screen.blit(
            rotation,
            (
                self.size[0] * 3 / 8 - rotation_x / 2,
                self.size[1] / 2 - rotation_y / 2,
            ),
        )
        # 내 보드
        # 내 이름
        color = "White"
        if self.game.turn == 0:
            color = "Blue"
        my_name = font.render(self.name, True, color)
        screen.blit(
            my_name,
            (
                self.size[0] / 30,
                self.size[1] * 2 / 3,
            ),
        )
        # 내 카드
        # for i in range(len(self.my_card)):
        #     card_x = 182
        #     card_y = 254.8
        #     playlist_player_card = pygame.image.load(
        #         str(RESOURCE_PATH / "card" / self.my_card[i]) + ".png"
        #     )
        #     playlist_player_card = pygame.transform.scale(
        #         playlist_player_card, (card_x, card_y)
        #     )
        #     screen.blit(
        #         playlist_player_card,
        #         (
        #             self.size[0] / 30 + i * card_x / 2,
        #             self.size[1] - card_y,
        #         ),
        #     )
        # 전체 타이머
        font = self.get_font(100)
        game_timer = font.render(f"{self.game_timer}", True, "White")
        screen.blit(
            game_timer,
            (
                self.size[0] * 61 / 80,
                self.size[1] / 24,
            ),
        )

    # 메뉴 선택 시 처리
    def select_card(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        print(f"---{index}---")

        if index in self.possible_cards_num:
            self.game.players[0].use_card(index)
            self.game.turn_end()
            self.update_card()
            self.init_draw()
        if index == self.max_card:  # 덱
            self.game.players[0].get_card()
            self.game.turn_end()
            self.update_card()
            self.init_draw()
        if index == self.max_card:  # 우노버튼
            self.game.players[0].press_uno()

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        if self.game.turn == 0:
            for i in range(self.max_card + 2):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect[i].collidepoint(event.pos):
                        self.select_card(i)
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
                                self.select_card(self.selected)
                        elif event.key == setting.options["left"]:
                            # 선택을 하나 왼쪽으로 이동
                            self.selected = (
                                self.selected - 1 if 0 < self.selected else 0
                            )
                            self.highlight = self.selected
                        elif event.key == setting.options["right"]:
                            # 선택을 하나 오른쪽으로 이동
                            self.selected = (
                                self.selected + 1
                                if self.selected < self.max_card + 1
                                else self.max_card + 1
                            )
                            self.highlight = self.selected

                # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
                elif event.type == pygame.KEYUP:
                    self.pressed = False
