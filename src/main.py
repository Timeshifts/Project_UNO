import sys, setting
from button import Button
from pathlib import Path

# pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)


def get_font(size):  # 폰트 설정
    return pygame.font.Font(resource_path / "font.ttf", size)


def main():
    while True:
        # for event in pygame.event.get():
        #     # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시 종료 처리
        #     if event.type == pygame.QUIT:
        #         settings.save_setting()
        #         pygame.quit()
        #         sys.exit(0)

        # 기본 화면 표시
        screen.blit(background, (0, 0))
        # pygame.display.flip()

        # Frame Per Second - 우선 60으로 가정합니다.
        clock.tick(60)

        menu_mouse_pos = pygame.mouse.get_pos()
        # MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        # MENU_RECT = MENU_TEXT.get_rect(center=(width / 2, 100))

        # 메인메뉴 버튼 표시
        play_button = Button(
            image=pygame.image.load(resource_path / "main_button.png"),
            pos=(width / 2, height * 5 / 8),
            text_input="PLAY",
            font=get_font(50),
            base_color="#3a4aab",
            hovering_color="White",
        )
        options_button = Button(
            image=pygame.image.load(resource_path / "main_button.png"),
            pos=(width / 2, height * 6 / 8),
            text_input="OPTIONS",
            font=get_font(50),
            base_color="#3a4aab",
            hovering_color="White",
        )
        quit_button = Button(
            image=pygame.image.load(resource_path / "main_button.png"),
            pos=(width / 2, height * 7 / 8),
            text_input="QUIT",
            font=get_font(50),
            base_color="#3a4aab",
            hovering_color="White",
        )

        # screen.blit(MENU_TEXT, MENU_RECT)

        # 버튼 호버링
        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_pos, screen)
            button.update(screen)

        # 버튼 실행시 호출 함수
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# 게임 플레이 화면
def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        screen.fill("#526580")

        # 전체 타이머
        e_timer = get_font(45).render("entire timer", True, "White")
        e_timer_rect = e_timer.get_rect(center=(width * 2 / 20, height * 1 / 20))
        screen.blit(e_timer, e_timer_rect)

        # 플레이어 리스트 공간
        pygame.draw.rect(screen, (37, 37, 37), [width * 3 / 4, 0, width / 4, height])

        # 플레이어 리스트
        player_list = get_font(45).render("Player list", True, "White")
        player_list_rect = player_list.get_rect(center=(width * 7 / 8, height * 5 / 20))
        screen.blit(player_list, player_list_rect)

        # 플레이어 리스트 my
        player_list_my = get_font(60).render("Me", True, "White")
        player_list_my_rect = player_list_my.get_rect(
            center=(width * 13 / 16, height * 7 / 20)
        )
        screen.blit(player_list_my, player_list_my_rect)

        # 플레이어 리스트 my 남은 카드 개수
        player_list_my = get_font(60).render("rest", True, "White")
        player_list_my_rect = player_list_my.get_rect(
            center=(width * 15 / 16, height * 7 / 20)
        )
        screen.blit(player_list_my, player_list_my_rect)

        # 플레이어 리스트 플레이어 1
        player_list_p1 = get_font(60).render("P1", True, "White")
        player_list_p1_rect = player_list_p1.get_rect(
            center=(width * 13 / 16, height * 9 / 20)
        )
        screen.blit(player_list_p1, player_list_p1_rect)

        # 플레이어 리스트 플레이어 1 남은 카드 개수
        player_list_p1 = get_font(60).render("rest", True, "White")
        player_list_p1_rect = player_list_p1.get_rect(
            center=(width * 15 / 16, height * 9 / 20)
        )
        screen.blit(player_list_p1, player_list_p1_rect)

        # 플레이어 리스트 플레이어 2
        player_list_p2 = get_font(60).render("P2", True, "White")
        player_list_p2_rect = player_list_p2.get_rect(
            center=(width * 13 / 16, height * 11 / 20)
        )
        screen.blit(player_list_p2, player_list_p2_rect)

        # 플레이어 리스트 플레이어 2 남은 카드 개수
        player_list_p2 = get_font(60).render("rest", True, "White")
        player_list_p2_rect = player_list_p2.get_rect(
            center=(width * 15 / 16, height * 11 / 20)
        )
        screen.blit(player_list_p2, player_list_p2_rect)

        # 플레이어 리스트 플레이어 3
        player_list_p3 = get_font(60).render("P3", True, "White")
        player_list_p3_rect = player_list_p3.get_rect(
            center=(width * 13 / 16, height * 13 / 20)
        )
        screen.blit(player_list_p3, player_list_p3_rect)

        # 플레이어 리스트 플레이어 3 남은 카드 개수
        player_list_p3 = get_font(60).render("rest", True, "White")
        player_list_p3_rect = player_list_p3.get_rect(
            center=(width * 15 / 16, height * 13 / 20)
        )
        screen.blit(player_list_p3, player_list_p3_rect)

        # 플레이어 1 보드
        pygame.draw.rect(
            screen, (50, 50, 50), [width * 3 / 16, 0, width * 6 / 16, height / 8]
        )

        # 플레이어 1
        player_1 = get_font(45).render("P1", True, "White")
        player_1_rect = player_1.get_rect(center=(width * 7 / 32, height / 16))
        screen.blit(player_1, player_1_rect)

        # 플레이어 2 보드
        pygame.draw.rect(
            screen, (50, 50, 50), [0, height / 8, height / 8, width * 5 / 16]
        )

        # 플레이어 2
        player_2 = get_font(45).render("P2", True, "White")
        player_2_rect = player_2.get_rect(center=(height / 16, height * 5 / 32))
        screen.blit(player_2, player_2_rect)

        # 플레이어 3 보드
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            [width * 3 / 4 - height / 8, height / 8, height / 8, width * 5 / 16],
        )

        # 플레이어 3
        player_3 = get_font(45).render("P3", True, "White")
        player_3_rect = player_3.get_rect(
            center=(width * 3 / 4 - height / 16, height * 5 / 32)
        )
        screen.blit(player_3, player_3_rect)

        # 내 보드
        pygame.draw.rect(
            screen, (100, 100, 100), [0, height * 5 / 8, width * 3 / 4, height * 3 / 8]
        )

        # 내 보드 이름 표시
        my_board = get_font(45).render("My", True, "White")
        my_board_rect = my_board.get_rect(center=(width / 20, height * 11 / 16))
        screen.blit(my_board, my_board_rect)

        # 개인 타이머
        p_timer = get_font(45).render("personal timer", True, "White")
        p_timer_rect = p_timer.get_rect(center=(width * 4 / 20, height * 11 / 16))
        screen.blit(p_timer, p_timer_rect)

        # 우노버튼
        uno_button = Button(
            image=pygame.transform.scale(
                pygame.image.load(resource_path / "uno_button.png"), (150, 150)
            ),
            pos=(width * 13 / 20, height * 13 / 16),
            text_input="",
            font=get_font(0),
            base_color="White",
            hovering_color="Green",
        )

        # 덱
        draw_deck = Button(
            image=pygame.transform.scale(
                pygame.image.load(resource_path / "card/card_back.png"), (130, 182)
            ),
            pos=(width * 3 / 8 - 80, height * 9 / 20),
            text_input="",
            font=get_font(0),
            base_color="White",
            hovering_color="Green",
        )

        # 카드 놓을 자리
        put_card = Button(
            image=pygame.transform.scale(
                pygame.image.load(resource_path / "highlight.png"), (130, 182)
            ),
            pos=(width * 3 / 8 + 80, height * 9 / 20),
            text_input="",
            font=get_font(0),
            base_color="White",
            hovering_color="Green",
        )

        # 메인메뉴로 나가기
        PLAY_BACK = Button(
            image=None,
            pos=(width * 7 / 8, height * 2 / 20),
            text_input="MENU",
            font=get_font(75),
            base_color="White",
            hovering_color="Green",
        )

        for button in [uno_button, draw_deck, put_card, PLAY_BACK]:
            button.changeColor(play_mouse_pos, screen)
            button.update(screen)

        # QUIT 버튼 실행시 게임 종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(play_mouse_pos):
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if uno_button.checkForInput(play_mouse_pos):
                    main()

        pygame.display.update()


# 게임 설정화면
def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(width / 2, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(width / 2, 460),
            text_input="BACK",
            font=get_font(75),
            base_color="Black",
            hovering_color="Green",
        )

        OPTIONS_BACK.changeColor(options_mouse_pos, screen)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(options_mouse_pos):
                    main()

        pygame.display.update()


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("[경고] Python 3.8 이상이 필요합니다.")
        sys.exit(1)

    if pygame.version.vernum < (2, 2, 0):
        print("[주의] Pygame 2.2.0 이상을 권장합니다.")

    # 리소스 폴더 경로
    resource_path = Path.cwd() / "UNO/resources"

    pygame.init()

    # 설정 불러오기
    settings = setting.Settings()

    # 기본 화면 설정 (기본 해상도 FHD)
    if settings.settings["resolution"] in settings.resolution.keys():
        size = width, height = settings.resolution[settings.settings["resolution"]]
    else:
        # 지정된 해상도 범위 초과 시 초기화
        size = width, height = settings.settings[
            "resolution"
        ] = settings.default_setting["resolution"]

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption("우노 게임")
    pygame.display.set_icon(pygame.image.load(resource_path / "logo.png"))

    # 메인 메뉴 배경
    background = pygame.transform.scale(
        pygame.image.load(resource_path / "main.png"), size
    )

    main()
