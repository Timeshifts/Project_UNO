import GameManager as GM
import pygame, setting
import threading, time
import random
from button import Button
from constant import *

clock = pygame.time.Clock()


class Single:
    def __init__(
        self, pos=(0, 0), size=(150, 50), computer_count=1, name="ME", story=-1
    ):
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
        self.game_timer = 0  # 전체 타이머
        self.turn_timer = 0  # 턴 타이머
        self.set_first = 0  # 내 턴일때 화면 갱신 한번만 하는 용도
        self.set_again = 0  # 컴퓨터 턴일때 화면 갱신 하는 용도
        self.is_turn_reversed = False  # 턴 방향
        self.effect = 0  # 애니메이션
        self.computer_think_thread = None  # 컴퓨터 비동기 처리용 스레드
        self.count = 0  # 애니메이션 횟수
        self.effect_index = 0  # 내는 카드 번호
        self.story = story  # 스토리 모드 (-1이면 스토리 아님)

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1

        self.game_start()
        self.init_draw()

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

        for i in range(len(self.button)):
            self.button[i].resize(size)
            self.rect[i] = self.button[i].rect

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
        self.game_timer = self.game.game_timer_integer  # 게임 타이머 갱신
        self.turn_timer = self.game.turn_timer_integer  # 턴 타이머 갱신
        self.is_turn_reversed = self.game.is_turn_reversed
        self.init_draw()

    def game_start(self):
        # Gm 역시 single처럼 게임 재시작시 변경되도록 처리
        GM.Gm = GM.GameManager()
        self.game = GM.Gm
        self.game.story = self.story
        self.game.computer_count = self.computer_count
        self.game.start_cards_integer = 5
        self.game.game_start()
        self.update_card()

    def turn_start(self):
        if self.game.end == 1:  # 게임 종료
            return 0
        else:
            self.update_card()
            if self.game.turn == 0:  # 플레이어인 경우
                self.possible_cards_num = self.game.players[0].play()
                if self.game.timer_zero == True:  # 턴 타이머 종료된 경우
                    if self.game.no_act == False:
                        self.game.players[0].get_card()
                    self.game.turn_end(option=2)
                if self.set_first == 0:
                    self.game.turn_start()
                    self.init_draw()
                    self.set_first = 1
            else:  # 컴퓨터인 경우
                if self.set_first == 0:
                    # pygame.time.wait(1000)
                    # self.game.turn_start()
                    # self.update_card()
                    # self.effect = self.game.players[self.game.turn].computer_play()
                    # self.set_first = 1

                    # 컴퓨터 비동기 대기 - 컴퓨터 턴에 일시 정지 문제가 생기지 않도록 하기 위함.
                    # race condition 방지를 위해 이벤트로 복잡하게 구현되긴 했습니다.
                    if self.computer_think_thread is None:
                        self.game.turn_timer_end = False
                        self.game.turn_count_down()
                        self.computer_think_thread = threading.Thread(
                            target=self.computer_wait
                        )
                        self.computer_think_thread.start()
                        # 나머지는 바로 밑 computer_act 함수로 이동
                else:
                    self.game.turn_end()
            return 1

    def computer_act(self):
        self.computer_think_thread = None
        self.game.turn_start()
        self.update_card()
        # self.set_first == 0
        self.effect = self.game.players[self.game.turn].computer_play()
        self.set_first = 1

    def computer_wait(self):
        time.sleep(random.randint(1, 3))
        pygame.event.post(pygame.event.Event(EVENT_COMPUTER_THINK))

    def init_draw(self):
        self.button = []
        self.rect = []
        # 색약 모드 적용을 위한 폴더명
        card_folder = "card_colorblind" if setting.options["colorblind"] else "card"
        # wild 색 선택 버튼
        color_num = 0
        if self.game.wild == True:
            color_num = 4
            card_color = ["blue", "green", "red", "yellow"]
            for i in range(4):
                color_x = 100
                color_y = 100
                self.button.append(
                    Button(
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / card_folder / f"{card_color[i]}")
                                + ".png"
                            ),
                            (color_x, color_y),
                        ),
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / card_folder / f"{card_color[i]}")
                                + ".png"
                            ),
                            (color_x, color_y),
                        ),
                        pos=(
                            self.size[0] * (i * 2 + 3) / 16,
                            self.size[1] * 3 / 4 - color_y,
                        ),
                        text_input="",
                        font=setting.get_font(50),
                        base_color="Black",
                        hovering_color="Black",
                    )
                )
                self.rect.append(self.button[i].rect)
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
                                    str(RESOURCE_PATH / card_folder / self.my_card[i])
                                    + ".png"
                                ),
                                (card_x, card_y),
                            ),
                            pygame.transform.scale(
                                pygame.image.load(
                                    RESOURCE_PATH / card_folder / "highlight.png"
                                ),
                                (card_x, card_y),
                            ),
                            pos=(
                                (i + 1.5) * card_x * setting.get_screen_scale() * 3 / 4,
                                self.size[1] - card_y * setting.get_screen_scale(),
                            ),
                            text_input="",
                            font=setting.get_font(50),
                            base_color="Black",
                            hovering_color="Black",
                        )
                    )
                else:
                    self.button.append(
                        Button(
                            pygame.transform.scale(
                                pygame.image.load(
                                    str(RESOURCE_PATH / card_folder / self.my_card[i])
                                    + ".png"
                                ),
                                (card_x, card_y),
                            ),
                            pygame.transform.scale(
                                pygame.image.load(
                                    RESOURCE_PATH / card_folder / "shadow.png"
                                ),
                                (card_x, card_y),
                            ),
                            pos=(
                                (i + 1.5) * card_x * setting.get_screen_scale() * 3 / 4,
                                self.size[1] - card_y * setting.get_screen_scale() / 2,
                            ),
                            text_input="",
                            font=setting.get_font(50),
                            base_color="Black",
                            hovering_color="Black",
                        )
                    )
            else:
                self.button.append(
                    Button(
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / card_folder / self.my_card[i])
                                + ".png"
                            ),
                            (card_x, card_y),
                        ),
                        pygame.transform.scale(
                            pygame.image.load(
                                str(RESOURCE_PATH / card_folder / self.my_card[i])
                                + ".png"
                            ),
                            (card_x, card_y),
                        ),
                        pos=(
                            (i + 1.5) * card_x * setting.get_screen_scale() * 3 / 4,
                            self.size[1] - card_y * setting.get_screen_scale() / 2,
                        ),
                        text_input="",
                        font=setting.get_font(50),
                        base_color="Black",
                        hovering_color="Black",
                    )
                )
            self.rect.append(self.button[i + color_num].rect)
        # 덱 버튼
        deck_card_x = 130
        deck_card_y = 182
        self.button.append(
            Button(
                pygame.transform.scale(
                    pygame.image.load(
                        str(RESOURCE_PATH / card_folder / "card_back") + ".png"
                    ),
                    (deck_card_x, deck_card_y),
                ),
                pygame.transform.scale(
                    pygame.image.load(RESOURCE_PATH / card_folder / "highlight.png"),
                    (deck_card_x, deck_card_y),
                ),
                pos=(
                    self.size[0] * 3 / 8
                    - deck_card_x * setting.get_screen_scale() * 2 / 3,
                    self.size[1] / 2,
                ),
                text_input="",
                font=setting.get_font(50),
                base_color="Black",
                hovering_color="Black",
            )
        )
        self.rect.append(self.button[self.max_card + color_num].rect)
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
                    self.size[0] * 3 / 4 - uno_x * setting.get_screen_scale() / 2,
                    self.size[1] / 2,
                ),
                text_input="",
                font=setting.get_font(50),
                base_color="Black",
                hovering_color="Black",
            )
        )
        self.rect.append(self.button[self.max_card + 1 + color_num].rect)

    # 스크린에 자신을 그리기
    def draw(self, screen):
        # 색약 모드 적용을 위한 폴더명
        card_folder = "card_colorblind" if setting.options["colorblind"] else "card"

        fontsize = 50
        font = setting.get_font(fontsize)
        for i in range(self.max_card + 2):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].changeHighlight1(True, screen)
            else:
                self.button[i].changeHighlight1(False, screen)

        # ESC 문구
        ESC = pygame.key.name(setting.options["pause"])
        if ESC == "escape":
            ESC = "Esc"
        ESC_text = font.render((ESC), True, "White")
        screen.blit(
            ESC_text,
            (
                self.size[0] * 47 / 50,
                self.size[1] / 50,
            ),
        )
        for i in range(self.computer_count):
            # Player List 상자
            playlist_x = 480 * setting.get_screen_scale()
            playlist_y = 180 * setting.get_screen_scale()
            playlist_box = pygame.image.load(RESOURCE_PATH / "single" / "list.png")
            playlist_box = pygame.transform.scale(
                playlist_box, (playlist_x, playlist_y)
            )
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
                card_x = 52 * setting.get_screen_scale()
                card_y = 72.8 * setting.get_screen_scale()
                playlist_player_card = pygame.image.load(
                    RESOURCE_PATH / card_folder / "card_back.png"
                )
                playlist_player_card = pygame.transform.scale(
                    playlist_player_card, (card_x, card_y)
                )
                screen.blit(
                    playlist_player_card,
                    (
                        self.size[0] * (7 / 8 - 1 / 8) + 30 + j * card_x / 3,
                        self.size[1] * ((2 * i + 3) / 12 - 1 / 12)
                        + 80 * setting.get_screen_scale(),
                    ),
                )

        # 메인보드
        # 메인보드 컴퓨터 카드
        for i in range(self.computer_count):
            card_x = 87.75 * setting.get_screen_scale()
            card_y = 122.85 * setting.get_screen_scale()
            card_pos_x = (
                self.size[0] * 3 / 4 * (self.game.turn) / (self.computer_count + 1)
                - card_x / 2
            )
            card_pos_y = card_y * 2 / 3
            board_player_card = pygame.image.load(
                RESOURCE_PATH / card_folder / "card_back.png"
            )
            board_player_card = pygame.transform.scale(
                board_player_card, (card_x, card_y)
            )
            screen.blit(
                board_player_card,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    - card_x / 2,
                    card_pos_y,
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
        # 메인보드 컴퓨터 타이머
        for i in range(self.computer_count):
            if self.game.turn == i + 1:
                turn_timer = font.render(f"{self.turn_timer}", True, "White")
            else:
                turn_timer = font.render("15", True, "White")
            screen.blit(
                turn_timer,
                (
                    self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                    + card_x / 2,
                    card_y * 2 / 3,
                ),
            )
        # 메인보드 컴퓨터 쉴드
        for i in range(self.computer_count):
            if self.game.players[i + 1].defence_int > 0:
                shield_x = 49 * setting.get_screen_scale()
                shield_y = 53 * setting.get_screen_scale()
                shield = pygame.image.load(RESOURCE_PATH / "single" / "shield.png")
                shield = pygame.transform.scale(shield, (shield_x, shield_y))
                screen.blit(
                    shield,
                    (
                        self.size[0] * 3 / 4 * (i + 1) / (self.computer_count + 1)
                        + card_x / 2,
                        card_y * 5 / 3 - shield_y,
                    ),
                )
        # 카드 덱
        deck_card_x = 130 * setting.get_screen_scale()
        deck_card_y = 182 * setting.get_screen_scale()
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
        grave_card_x = 130 * setting.get_screen_scale()
        grave_card_y = 182 * setting.get_screen_scale()
        grave_card_pos_x = (
            self.size[0] * 3 / 8 - grave_card_x / 2 + grave_card_x * 2 / 3
        )
        grave_card_pos_y = self.size[1] / 2 - grave_card_y / 2
        grave_card = pygame.image.load(
            str(
                RESOURCE_PATH
                / card_folder
                / f"{self.game.grave_top.color}_{self.game.grave_top.name}"
            )
            + ".png"
        )
        grave_card = pygame.transform.scale(grave_card, (grave_card_x, grave_card_y))
        screen.blit(
            grave_card,
            (
                grave_card_pos_x,
                grave_card_pos_y,
            ),
        )
        # 카드 색상
        color_card_x = 80 * setting.get_screen_scale()
        color_card_y = 80 * setting.get_screen_scale()
        color_card = pygame.image.load(
            str(RESOURCE_PATH / card_folder / f"{self.game.grave_top_color}") + ".png"
        )
        color_card = pygame.transform.scale(color_card, (color_card_x, color_card_y))
        screen.blit(
            color_card,
            (
                self.size[0] * 3 / 8 - color_card_x / 2 + grave_card_x * 5 / 3,
                self.size[1] / 2 - color_card_y / 2,
            ),
        )
        # 우노 성공할 경우
        if self.game.players[0].is_uno == True:
            uno_x = 400 * setting.get_screen_scale()
            uno_y = 300 * setting.get_screen_scale()
            uno = pygame.transform.scale(
                pygame.image.load(RESOURCE_PATH / "single" / "uno_effect.png"),
                (uno_x, uno_y),
            )
            screen.blit(
                uno,
                (
                    self.size[0] * 3 / 4 - uno_x * 5 / 7 * setting.get_screen_scale(),
                    self.size[1] / 2 - uno_y / 2,
                ),
            )
        # 턴 방향
        rotation_x = 943 * setting.get_screen_scale()
        rotation_y = 238 * setting.get_screen_scale()
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
        # 내 쉴드
        if self.game.players[0].defence_int > 0:
            shield_x = 49 * setting.get_screen_scale()
            shield_y = 53 * setting.get_screen_scale()
            shield = pygame.image.load(RESOURCE_PATH / "single" / "shield.png")
            shield = pygame.transform.scale(shield, (shield_x, shield_y))
            screen.blit(
                shield,
                (
                    0,
                    self.size[1] * 2 / 3,
                ),
            )
        # 전체 타이머
        font = setting.get_font(100)
        game_timer = font.render(f"{self.game_timer}", True, "White")
        screen.blit(
            game_timer,
            (
                self.size[0] * 61 / 80,
                self.size[1] / 24,
            ),
        )
        # 턴 타이머
        font = setting.get_font(50)
        if self.game.turn == 0:
            turn_timer = font.render(f"{self.turn_timer}", True, "White")
        else:
            turn_timer = font.render("15", True, "White")
        screen.blit(
            turn_timer,
            (
                self.size[0] / 150,
                self.size[1] * 3 / 4,
            ),
        )
        # 애니메이션
        if self.effect == "get":  # 컴퓨터 카드 가져올때
            get_card_x = 130 * setting.get_screen_scale()
            get_card_y = 182 * setting.get_screen_scale()
            get_card = pygame.image.load(
                RESOURCE_PATH / card_folder / "card_back_effect.png"
            )
            get_card = pygame.transform.scale(get_card, (get_card_x, get_card_y))
            screen.blit(
                get_card,
                (
                    self.size[0] * 3 / 8 - get_card_x / 2 - get_card_x * 2 / 3,
                    self.size[1] / 2 - get_card_y,
                ),
            )
            self.effect = 0
        elif self.effect == "get_my":  # 플레이어가 카드 가져올때
            get_card_x = 130 * setting.get_screen_scale()
            get_card_y = 182 * setting.get_screen_scale()
            get_card = pygame.image.load(
                RESOURCE_PATH / card_folder / "card_back_effect.png"
            )
            get_card = pygame.transform.scale(get_card, (get_card_x, get_card_y))
            screen.blit(
                get_card,
                (
                    self.size[0] * 3 / 8 - get_card_x / 2 - get_card_x * 2 / 3,
                    self.size[1] / 2 + get_card_y / 2,
                ),
            )
            self.effect = 0
        elif self.effect != 0:
            max_count = 2  # 효과 보여주는 횟수
            if self.game.turn == 0:  # 플레이어가 카드 낼때
                give_card_x = 130 * setting.get_screen_scale()
                give_card_y = 182 * setting.get_screen_scale()
                give_x = (
                    self.effect_index
                    * give_card_x
                    * setting.get_screen_scale()
                    * 3
                    / 4,
                )
                give_y = self.size[1] - give_card_y * setting.get_screen_scale() / 2
                give_card = pygame.image.load(
                    RESOURCE_PATH / card_folder / f"{self.effect}.png"
                )
                give_card = pygame.transform.scale(
                    give_card, (give_card_x, give_card_y)
                )
                screen.blit(
                    give_card,
                    (
                        give_x[0]
                        + (grave_card_pos_x - give_x[0]) * self.count / max_count,
                        give_y + (grave_card_pos_y - give_y) * self.count / max_count,
                    ),
                )
                self.count += 1
                if self.count == max_count:
                    self.effect = 0
                    self.count = 0
            else:  # 컴퓨터 카드 낼때
                i == self.game.turn
                give_card_x = 130 * setting.get_screen_scale()
                give_card_y = 182 * setting.get_screen_scale()
                give_card = pygame.image.load(
                    RESOURCE_PATH / card_folder / f"{self.effect}.png"
                )
                give_card = pygame.transform.scale(
                    give_card, (give_card_x, give_card_y)
                )
                screen.blit(
                    give_card,
                    (
                        card_pos_x
                        + (grave_card_pos_x - card_pos_x) * self.count / max_count,
                        card_pos_y
                        + (grave_card_pos_y - card_pos_y) * self.count / max_count,
                    ),
                )
                self.count += 1
                if self.count == max_count:
                    self.effect = 0
                    self.count = 0

    # 메뉴 선택 시 처리
    def select_card(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

        if self.game.wild == True:
            if index in range(4):
                card_color = ["blue", "green", "red", "yellow"]
                self.game.grave_top_color = card_color[index]
                if self.game.wild_card == "wild_four":
                    target = 0
                    if self.game.is_turn_reversed == False:
                        target = (self.game.turn + 1) % self.game.player_num
                    else:
                        target = (self.game.turn - 1) % self.game.player_num
                    self.game.attack(4, target)
                    self.game.wild = False
                    self.game.turn_end(option=1)
                # elif self.game.wild_card == "wild_target":
                #     self.game.attack(2, random.randint(0, self.game.player_num - 1))
                #     self.game.wild = False
                #     self.game.turn_end(option=1)
                else:
                    self.game.wild = False
                    self.game.turn_end(option=1)
        else:
            if index in self.possible_cards_num:
                self.effect = self.hand_card[0][index]
                self.effect_index = index
                if self.game.players[0].use_card(index) == "wild":
                    self.update_card()
                    self.init_draw()
                    self.highlight = 0
                    self.game.turn_timer_end = True
                else:
                    self.game.turn_end(option=1)
            if index == self.max_card:  # 덱
                self.game.players[0].get_card()
                self.effect = "get_my"
                self.game.turn_end()
            if index == self.max_card + 1:  # 우노버튼
                self.game.players[0].press_uno()

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        self.color = 0
        if self.game.wild == True:
            self.color = 4
        # 턴 종료 대기 완료
        if event.type == EVENT_TURN_END:
            self.game.turn_end_act()
            if event.option == 2:
                # print("옵션 2")
                self.turn_start()
            if event.option == 1:
                self.update_card()
                self.init_draw()
                self.highlight = 0
            if self.game.turn != 0 and self.set_first != 0:
                self.update_card()
                se_event = pygame.event.Event(
                    EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "select.mp3"}
                )
                pygame.event.post(se_event)
                self.set_first = 0
            else:
                self.update_card()
                self.init_draw()
                self.highlight = 0
                self.set_first = 0
            self.game.no_act = False
            self.turn_start()
        # 컴퓨터 비동기 대기 완료
        if event.type == EVENT_COMPUTER_THINK:
            self.computer_act()
        if self.game.turn == 0:
            # 겹친 구간에서 위에 있는 카드가 선택되게 하기 위한 조정
            for i in range(self.max_card + 1, -1, -1):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect[i].collidepoint(event.pos):
                        self.select_card(i)
                        break  # 한 번에 여러 개의 메뉴가 눌리지 않도록 처리
                elif event.type == pygame.MOUSEMOTION:
                    if self.rect[i].collidepoint(event.pos):
                        # 2차 요구사항 - 카드 선택을 위한 효과음 추가
                        if i != self.highlight:
                            pygame.event.post(
                                pygame.event.Event(
                                    EVENT_PLAY_SE,
                                    {"path": RESOURCE_PATH / "sound" / "select.mp3"},
                                )
                            )
                        # highlight 대상을 변경
                        self.highlight = i
                        # 키보드 선택 해제
                        self.selected = -1
                        return  # 겹친 구간에서 카드 여러 개 선택 방지
                elif event.type == pygame.KEYDOWN:
                    if self.pressed == False:
                        self.pressed = True
                        # 엔터 키가 눌렸을 때
                        if event.key == setting.options["enter"]:
                            # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                            if self.selected != -1:
                                self.select_card(self.selected)
                        elif event.key == setting.options["left"]:
                            # 2차 요구사항 - 카드 선택을 위한 효과음 추가
                            pygame.event.post(
                                pygame.event.Event(
                                    EVENT_PLAY_SE,
                                    {"path": RESOURCE_PATH / "sound" / "select.mp3"},
                                )
                            )
                            # 선택을 하나 왼쪽으로 이동
                            self.selected = (
                                self.selected - 1 if 0 < self.selected else 0
                            )
                            self.highlight = self.selected
                        elif event.key == setting.options["right"]:
                            # 2차 요구사항 - 카드 선택을 위한 효과음 추가
                            pygame.event.post(
                                pygame.event.Event(
                                    EVENT_PLAY_SE,
                                    {"path": RESOURCE_PATH / "sound" / "select.mp3"},
                                )
                            )
                            # 선택을 하나 오른쪽으로 이동
                            self.selected = (
                                self.selected + 1
                                if self.selected < self.max_card + 1 + self.color
                                else self.max_card + 1 + self.color
                            )
                            self.highlight = self.selected

                # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
                elif event.type == pygame.KEYUP:
                    self.pressed = False
