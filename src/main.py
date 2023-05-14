import sys, setting, pause, story_map, setting_menu, achievement, endgame
from main_menu import Main_menu, EVENT_QUIT_GAME, EVENT_START_SINGLE, EVENT_OPEN_OPTION
from single_lobby import SingleLobby
from multi_lobby import MultiLobby
from single import Single
from multi import Multi
from text_prompt import Text_Prompt
from constant import *

# pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)

setting_UI = None


def get_background(state, size):
    if state == "main_menu":
        return pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "main" / "main_background.png"), size
        )
    elif state == "story_map":
        try:
            path = (
                RESOURCE_PATH
                / "story"
                / f"story_background_{story_map.StoryMenu.story_progress+1}.png"
            )
        except FileNotFoundError:
            # 스토리를 다 깨면 +1번까지 열려있는 지도 = 없으므로 오류
            # 따라서, 다 열린 지도로 예외 처리
            path = (
                RESOURCE_PATH
                / "story"
                / f"story_background_{story_map.StoryMenu.story_amount}.png"
            )
        background = pygame.transform.scale(pygame.image.load(path), size)
        return background
    elif state == "single":
        return pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "single" / "single_background.png"), size
        )
    elif state == "single_lobby":
        return pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "single" / "single_robby_background.png"),
            size,
        )
    elif state == "multi":
        return pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "single" / "multi_background.png"),
            size,
        )
    elif state == "multi_lobby":
        return pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "single" / "multi_robby_background.png"),
            size,
        )


# 배경 음악 재생
def load_bgm(path, volume=1.0):
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # -1 = 무한 반복 재생


def main():
    pygame.init()
    pygame.mixer.init()  # 음향 mixer 초기화

    # 설정 불러오기
    setting_UI = setting_menu.Setting_UI(pos=(100, 100))

    # 기본 화면 설정 (기본 해상도 FHD)
    if setting.options["resolution"] in setting.resolution.keys():
        size = width, height = setting.resolution[setting.options["resolution"]]
    else:
        # 지정된 해상도 범위 초과 시 초기화
        size = width, height = setting.options["resolution"] = setting.default_setting[
            "resolution"
        ]

    # 해상도에 맞추어 object들의 크기 재설정
    setting_UI.resize((width, height))
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption("우노 게임")
    pygame.display.set_icon(pygame.image.load(RESOURCE_PATH / "logo.png"))

    # 게임 오브젝트 배열
    game_objects = []
    game_objects.append

    # 상태 - 초기 화면인지, 로비인지, 게임 중인지 등등
    state = "main_menu"

    # 메인 배경과 음악
    background = get_background(state, size)
    load_bgm(RESOURCE_PATH / "sound" / "bg_main.mp3", setting.get_volume("bgm"))

    # 직접적으로 game_objects에 들어가는 objects는 여기서 미리 선언되어야
    # 넣고 뺄 때 문제가 생기지 않습니다.
    main_menu = Main_menu((width / 2, height / 2 + 100), size)
    game_objects.append(main_menu)  # 메인 메뉴 생성하여 게임 오브젝트에 추가
    single_lobby = SingleLobby(size, size)
    multi_lobby = MultiLobby(size, size)
    text_prompt = Text_Prompt(size, size, done_event=EVENT_START_LOBBY)
    story_object = story_map.StoryMap((0, 0), size)
    achi_object = achievement.AchievementMenu((0, 0), size)
    endgame_prompt = None

    # 싱글게임 진행 중인지 확인
    single_turn = 0

    while True:
        for event in pygame.event.get():
            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시, 메뉴에서 종료 선택 시 종료 처리
            if event.type in (pygame.QUIT, EVENT_QUIT_GAME):
                setting.save_setting()
                story_object.STORY_MENU.save_progress()
                achi_object.save_progress()
                pygame.quit()
                sys.exit(0)

            # 게임 종료 상황
            # 요구 사항 '플레이어가 마우스 클릭하거나 키를 누르면 시작 메뉴로'를 위해 필요합니다.
            if event.type == EVENT_END_GAME:
                # 게임 승리/패배 효과음 출력
                if event.player_win:
                    # if single.game.winner_index == 0:
                    pygame.event.post(
                        pygame.event.Event(
                            EVENT_PLAY_SE,
                            {"path": RESOURCE_PATH / "sound" / "victory.mp3"},
                        )
                    )
                else:
                    pygame.event.post(
                        pygame.event.Event(
                            EVENT_PLAY_SE,
                            {"path": RESOURCE_PATH / "sound" / "wild.mp3"},
                        )
                    )

                if endgame_prompt == None:
                    endgame_prompt = endgame.EndGamePrompt(
                        size, size, name, single, event.player_win, computer_count
                    )
                    game_objects.append(endgame_prompt)

                # 스토리 모드였다면 다음 지역 해금
                if "story_map" in event.dict.keys():
                    progress = story_map.StoryMenu.story_progress
                    if progress < event.story_map and event.player_win:
                        story_map.StoryMenu.story_progress = event.story_map
                        story_object.STORY_MENU.save_progress()
                    # 과 함께 업적 1~4 달성
                    pygame.event.post(
                        pygame.event.Event(
                            EVENT_ACQUIRE_ACHIEVEMENT, {"id": event.story_map}
                        )
                    )
                elif event.player_win:
                    # 업적 0: 싱글 플레이어 승리
                    pygame.event.post(
                        pygame.event.Event(EVENT_ACQUIRE_ACHIEVEMENT, {"id": 0})
                    )
                if event.player_win:
                    # 나머지 업적 flag를 읽어 업적 획득
                    for achi in single.game.achi_flag:
                        pygame.event.post(
                            pygame.event.Event(EVENT_ACQUIRE_ACHIEVEMENT, {"id": achi})
                        )
                state = "end_game"

            # 게임 종료 상황에
            if state == "end_game":
                # 플레이어가 마우스를 클릭하거나 아무 키나 누르면
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    # endgame_prompt는 지우고
                    game_objects.remove(endgame_prompt)
                    endgame_prompt = None
                    # 메인으로 돌아가기
                    pygame.event.post(pygame.event.Event(EVENT_MAIN))

            # 일시 정지
            if event.type == pygame.KEYDOWN:
                if event.key == setting.options["pause"] and state in (
                    "single_play" or "story_play"
                ):
                    single.game.paused = True
                    pause.init_pause(setting_UI, screen)
                    pause.pause()  # pause 상태에서의 루프

            # 효과음
            if event.type == EVENT_PLAY_SE:
                se = pygame.mixer.Sound(event.path)
                se.set_volume(setting.get_volume("se"))
                se.play()

            # 메인으로 복귀
            if event.type == EVENT_MAIN:
                if state == "single_lobby":  # 싱글 플레이 제거
                    game_objects.remove(single_lobby)
                elif state == "multi_lobby":  # 멑티 플레이 제거
                    game_objects.remove(multi_lobby)
                elif state == "story_map":  # 스토리 모드 제거
                    game_objects.remove(story_object)
                elif state == "achievement":  # 업적 메뉴 제거
                    game_objects.remove(achi_object)
                elif state in ("single", "multi", "end_game"): # single 혹은 multi 제거
                    if "single" in str(game_objects[0]):
                        game_objects.remove(single)
                        del single  # single 객체 삭제
                        single_turn = 0  # single 진행 X
                    elif "multi" in str(game_objects[0]):
                        game_objects.remove(multi)
                        del multi  # multi 객체 삭제

                # 메인 메뉴로 복귀
                game_objects.append(main_menu)
                main_menu.resize(size)
                # 메인 배경 및 음악
                state = "main_menu"
                background = get_background(state, size)
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_main.mp3", setting.get_volume("bgm")
                )

            # 게임 로비
            if event.type == EVENT_START_LOBBY:
                # 메인 메뉴 제거
                if state == "main_menu":
                    game_objects.remove(main_menu)
                elif state == "rename":
                    # 변경 창에서 바꾼 이름을 싱글 로비에 반영
                    if "input" in event.dict.keys():
                        single_lobby.name = event.input
                    game_objects.remove(text_prompt)
                state = "single_lobby"
                background = get_background(state, size)
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_game.mp3", setting.get_volume("bgm")
                )
                game_objects.append(single_lobby)
                single_lobby.resize(size)  # 임시
            elif event.type == EVENT_START_LOBBY_MULTI:
                # 메인 메뉴 제거, 멀티 로비 진입
                if state == "main_menu":
                    game_objects.remove(main_menu)
                elif state == "rename":
                    # 변경 창에서 바꾼 이름을 멀티 로비에 반영
                    if "input" in event.dict.keys():
                        multi_lobby.name = event.input
                        # TODO: 다른 플레이어에게 이름 변경 알리기
                    game_objects.remove(text_prompt)
                elif state == "passwd_change":
                    # 변경 창에서 바꾼 비밀번호를 멀티에 반영
                    if "input" in event.dict.keys():
                        multi_lobby.password = event.input
                        multi_lobby.mss.password(multi_lobby.password)  # 비밀번호를 서버에 적용
                    game_objects.remove(text_prompt)
                elif state == "ip_change":
                    # 변경 창에서 바꾼 ip를 멀티에 반영
                    if "input" in event.dict.keys():
                        multi_lobby.input_ip = event.input
                    game_objects.remove(text_prompt)
                state = "multi_lobby"
                background = get_background(state, size)
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_game.mp3", setting.get_volume("bgm")
                )
                game_objects.append(multi_lobby)
                multi_lobby.resize(size)  # 임시

            # 게임 시작
            if event.type == EVENT_START_SINGLE:
                # 스토리 모드 시작엔 index가 있는 event를 날려서
                if "index" in event.dict.keys():
                    single_lobby.name = "You"
                    if event.index == 0:
                        single_lobby.computer_chk = [2, 0, 0, 0, 0]
                    elif event.index == 1:
                        single_lobby.computer_chk = [1, 1, 1, 0, 0]
                    elif event.index == 2:
                        single_lobby.computer_chk = [1, 1, 0, 0, 0]
                    elif event.index == 3:
                        single_lobby.computer_chk = [1, 1, 1, 0, 0]
                    # 컴퓨터 개수
                    computer_count = single_lobby.computer_chk.count(1)
                    story_A_computer_count = single_lobby.computer_chk.count(2)
                    name = single_lobby.name
                    # 스토리 맵 제거
                    game_objects.remove(story_object)
                    state = "single"
                    background = get_background(state, size)
                    load_bgm(
                        RESOURCE_PATH / "sound" / "bg_story_game.mp3",
                        setting.get_volume("bgm"),
                    )
                    single = Single(
                        (width, height),
                        size,
                        computer_count,
                        story_A_computer_count,
                        name,
                        event.index,
                    )
                # 그게 없으면 일반 게임
                else:
                    # 컴퓨터 개수
                    computer_count = single_lobby.computer_chk.count(1)
                    story_A_computer_count = single_lobby.computer_chk.count(2)
                    name = single_lobby.name
                    # 게임 로비 제거
                    game_objects.remove(single_lobby)
                    state = "single"
                    background = get_background(state, size)
                    single = Single(
                        (width, height),
                        size,
                        computer_count,
                        story_A_computer_count,
                        name,
                    )

                game_objects.append(single)
                # single.name = name
                # single.computer_count = computer_count
                single_turn = 1
            elif event.type == EVENT_START_MULTI: # 멀티플레이 시작
                # 컴퓨터 개수
                computer_count = multi_lobby.other_chk.count(1)
                story_A_computer_count = multi_lobby.other_chk.count(2)
                player_count = multi_lobby.other_chk.count(3)
                name = multi_lobby.name
                # 게임 로비 제거
                game_objects.remove(multi_lobby)
                state = "multi"
                background = get_background(state, size)
                multi = Multi(
                    (width, height),
                    size,
                    computer_count,
                    story_A_computer_count,
                    player_count,
                    name,
                )
                game_objects.append(multi)

            # 접속 IP 입력 (클라이언트 측)
            if event.type == EVENT_OPEN_ENTER_IP:
                game_objects.remove(multi_lobby)
                text_prompt = Text_Prompt(
                    (width, height),
                    size,
                    prompt="Enter IP",
                    max_char=15,
                    done_event=EVENT_START_LOBBY_MULTI,
                    init_input=multi_lobby.input_ip,
                )
                state = "ip_change"

                text_prompt.resize(size)
                game_objects.append(text_prompt)
            elif event.type == EVENT_CLOSE_ENTER_IP:
                # IP 변경 제거
                game_objects.remove(text_prompt)

            # 비밀번호 입력 (클라이언트 측)
            if event.type == EVENT_OPEN_CLIENT_PASSWORD:
                game_objects.remove(multi_lobby)
                text_prompt = Text_Prompt(
                    (width, height),
                    size,
                    prompt="Enter password",
                    max_char=6,
                    done_event=EVENT_START_LOBBY_MULTI,
                    init_input=multi_lobby.password,
                )
                state = "passwd_change"

                text_prompt.resize(size)
                game_objects.append(text_prompt)
            elif event.type == EVENT_CLOSE_CLIENT_PASSWORD:
                # 비밀번호 변경 제거
                game_objects.remove(text_prompt)

            # 비밀번호 변경 (서버 측)
            if event.type == EVENT_OPEN_HOST_PASSWORD:
                game_objects.remove(multi_lobby)
                text_prompt = Text_Prompt(
                    (width, height),
                    size,
                    prompt="Enter password",
                    max_char=6,
                    done_event=EVENT_START_LOBBY_MULTI,
                    init_input=multi_lobby.password,
                )
                state = "passwd_change"

                text_prompt.resize(size)
                game_objects.append(text_prompt)
            elif event.type == EVENT_CLOSE_HOST_PASSWORD:
                # 비밀번호 변경 제거
                game_objects.remove(text_prompt)

            # 이름 변경 열기
            if event.type == EVENT_OPEN_RENAME:
                if state == "single_lobby":
                    game_objects.remove(single_lobby)
                    text_prompt = Text_Prompt(
                        (width, height),
                        size,
                        done_event=EVENT_START_LOBBY,
                        init_input=single_lobby.name,
                    )
                else:
                    game_objects.remove(multi_lobby)
                    text_prompt = Text_Prompt(
                        (width, height),
                        size,
                        done_event=EVENT_START_LOBBY_MULTI,
                        init_input=multi_lobby.name,
                    )
                state = "rename"

                text_prompt.resize(size)
                game_objects.append(text_prompt)
            elif event.type == EVENT_CLOSE_RENAME:
                # 이름 변경 제거
                game_objects.remove(text_prompt)

            # 스토리 모드
            if event.type == EVENT_OPEN_STORYMAP:
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                state = "story_map"
                background = get_background(state, size)
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_story_main.mp3",
                    setting.get_volume("bgm"),
                )
                story_object.resize(size)
                game_objects.append(story_object)

            # 업적 달성
            # 어디서든 업적 달성을 알릴 수 있도록 이벤트화
            if event.type == EVENT_ACQUIRE_ACHIEVEMENT:
                # 이미 달성한 업적이면 무시
                if event.id not in achi_object.acquired:
                    achi_object.acquire(event.id)
                    game_objects.append(
                        achievement.AchievementIndicator(event.id, game_objects)
                    )

            # 업적 열기
            if event.type == EVENT_OPEN_ACHIEVEMENT:
                # 메인 메뉴 제거
                if state == "main_menu":
                    game_objects.remove(main_menu)
                state = "achievement"
                game_objects.append(achi_object)
                achi_object.resize(size)

            # 옵션 열기
            if event.type == EVENT_OPEN_OPTION:
                # 메인 메뉴 제거
                if state == "main_menu":
                    game_objects.remove(main_menu)
                # 설정을 게임 오브젝트에 넣어 표시되게 처리
                game_objects.append(setting_UI)

            # 옵션 닫기
            if event.type == EVENT_CLOSE_OPTION:
                # 설정 제거
                game_objects.remove(setting_UI)
                # 메인 메뉴로 복귀
                if state == "main_menu":
                    game_objects.append(main_menu)
                    main_menu.resize(size)

            # 해상도 변경 이벤트를 받아 화면 리사이징
            # 배경음악 음량 변경 즉시 적용
            if event.type == EVENT_OPTION_CHANGED:
                if size != setting.resolution[setting.options["resolution"]]:
                    size = setting.resolution[setting.options["resolution"]]
                    screen = pygame.display.set_mode(size)
                    background = get_background(state, size)
                    for obj in game_objects:
                        obj.resize(size)
                # 일시 정지 이후 색약 모드 변경 결과 즉시 반영
                if state in ("single_play" or "story_play"):
                    # 과 함께 타이머 재작동
                    single.game.paused = False
                    single.update_card()
                    single.init_draw()
                pygame.mixer.music.set_volume(setting.get_volume("bgm"))

            # 오브젝트별로 이벤트 처리
            if state != "end_game":
                for obj in game_objects:
                    obj.handle_event(event)

        # 기본 화면 표시
        screen.blit(background, (0, 0))

        # 각각의 오브젝트 그리기
        for obj in game_objects:
            obj.draw(screen)

        # 화면 갱신, FPS 60
        pygame.display.flip()
        clock.tick(60)
        # print(clock.get_fps())

        # 싱글 게임 진행중 확인
        if single_turn == 1:
            single_turn = single.turn_start()
            if single_turn == 0:  # 싱글 게임 종료
                if single.game.winner_index == 0:  # 플레이어 승리한 경우
                    player_win = True
                else:  # 플레이어 패배한 경우
                    player_win = False
                pygame.event.post(
                    pygame.event.Event(EVENT_END_GAME, {"player_win": player_win})
                )


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("[경고] Python 3.8 이상이 필요합니다.")
        sys.exit(1)

    if pygame.version.vernum < (2, 2, 0):
        print("[주의] Pygame 2.2.0 이상을 권장합니다.")

    main()
