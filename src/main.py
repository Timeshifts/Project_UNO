import sys, setting, pause, story_map, setting_menu# , GameManager
from main_menu import Main_menu, EVENT_QUIT_GAME, EVENT_START_SINGLE, EVENT_OPEN_OPTION
from single_lobby import SingleLobby, EVENT_MAIN
from single import Single, EVENT_MAIN
from rename import Rename
from constant import *

# pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)

setting_UI = None

def get_background(state, size):
    return pygame.transform.scale(
        pygame.image.load(RESOURCE_PATH / "main" / "main_background.png"), size
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
        size = width, height = setting.options[
            "resolution"
        ] = setting.default_setting["resolution"]

    # 해상도에 맞추어 object들의 크기 재설정
    setting_UI.resize((width, height))
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption("우노 게임")
    pygame.display.set_icon(pygame.image.load(RESOURCE_PATH / "logo.png"))

    # 게임 오브젝트 배열
    game_objects = []

    # 상태 - 초기 화면인지, 로비인지, 게임 중인지 등등
    state = "main_menu"

    # 일시정지 중인가?
    paused = False

    # 메인 배경과 음악
    background = get_background(state, size)
    load_bgm(RESOURCE_PATH / "sound" / "bg_main.mp3", setting.get_volume("bgm"))

    # 직접적으로 game_objects에 들어가는 objects는 여기서 미리 선언되어야
    # 넣고 뺄 때 문제가 생기지 않습니다.
    main_menu = Main_menu((width / 2, height / 2 + 100), size)
    game_objects.append(main_menu) # 메인 메뉴 생성하여 게임 오브젝트에 추가
    single_lobby = SingleLobby((width, height), size)
    single = Single((width, height), size, 1, "Test")
    rename = Rename((width, height), size)
    story_object = story_map.StoryMap((0, 0), size)

    while True:
        for event in pygame.event.get():
            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시, 메뉴에서 종료 선택 시 종료 처리
            if event.type in (pygame.QUIT, EVENT_QUIT_GAME):
                setting.save_setting()
                story_object.STORY_MENU.save_progress()
                pygame.quit()
                sys.exit(0)

            # 일시 정지
            if event.type == pygame.KEYDOWN:
                if event.key == setting.options["pause"]:
                    # TODO: 게임 중에만 일시정지가 작동하도록 제한
                    # and state in ("single_play" or "story_play")
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
                elif state == "single":
                    game_objects.remove(single)  # 스토리 모드 제거
                elif state == "story_map":
                    game_objects.remove(story_map)  # 스토리 모드 제거
                # 메인 메뉴로 복귀
                game_objects.append(main_menu)
                main_menu.resize(size)
                # 메인 배경 및 음악
                background = get_background(state, size)
                state = "main_menu"
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_main.mp3", setting.get_volume("bgm")
                )

            # 게임 로비
            if event.type == EVENT_START_LOBBY:
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                background = pygame.image.load(
                    RESOURCE_PATH / "single" / "single_robby_background.png"
                )
                state = "single_lobby"
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_game.mp3", setting.get_volume("bgm")
                )
                game_objects.append(single_lobby)

            # 게임 시작
            if event.type == EVENT_START_SINGLE:
                # 컴퓨터 개수
                computer_count = single_lobby.computer_chk.count(True)
                name = single_lobby.name
                # 게임 로비 제거
                game_objects.remove(single_lobby)
                background = pygame.image.load(
                    RESOURCE_PATH / "single" / "single_background.png"
                )
                state = "single"
                # load_bgm(
                #     RESOURCE_PATH / "sound" / "bg_game.mp3", setting_UI.get_volume("bgm")
                # )
                #
                game_objects.append(single)

            # 이름 변경 열기
            if event.type == EVENT_OPEN_RENAME:
                state = "rename"
                game_objects.remove(single_lobby)
                game_objects.append(rename)

            # 이름 변경 닫기
            if event.type == EVENT_CLOSE_RENAME:
                # 이름 변경 제거
                game_objects.remove(rename)

            # 스토리 모드
            if event.type == EVENT_START_STORY:
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                background = pygame.image.load(
                    RESOURCE_PATH / "story" / "story_background_1.png"
                )
                state = "story_map"
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_story_main.mp3",
                    setting.get_volume("bgm"),
                )
                game_objects.append(story_object)

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

            # 메인 메뉴로 복귀
            if event.type == EVENT_START_MENU:
                state = "main_menu"
                background = get_background(state, size)
                load_bgm(
                    RESOURCE_PATH / "sound" / "bg_main.mp3", setting.get_volume("bgm")
                )
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
                pygame.mixer.music.set_volume(setting.get_volume("bgm"))

            # 오브젝트별로 이벤트 처리
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


if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("[경고] Python 3.8 이상이 필요합니다.")
        sys.exit(1)

    if pygame.version.vernum < (2, 2, 0):
        print("[주의] Pygame 2.2.0 이상을 권장합니다.")

    main()
