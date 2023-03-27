import sys, setting #, GameManager
from main_menu import Main_menu, EVENT_QUIT_GAME, EVENT_START_SINGLE, EVENT_OPEN_OPTION
from constant import *

# pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)

settings = None


def main():
    pygame.init()

    # 설정 불러오기
    settings = setting.Settings(pos=(100, 100))

    # 기본 화면 설정 (기본 해상도 FHD)
    if settings.settings["resolution"] in settings.resolution.keys():
        size = width, height = settings.resolution[settings.settings["resolution"]]
    else:
        # 지정된 해상도 범위 초과 시 초기화
        size = width, height = settings.settings[
            "resolution"
        ] = settings.default_setting["resolution"]

    # 해상도에 맞추어 object들의 크기 재설정
    settings.resize((width - 200, height - 200))
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption("우노 게임")
    # pygame.display.set_icon(pygame.image.load(RESOURCE_PATH / '아이콘 파일 위치.png'))

    # 게임 오브젝트 배열
    game_objects = []

    # 메인 배경
    background = pygame.transform.scale(
        pygame.image.load(RESOURCE_PATH / "main.png"), size
    )

    # 메인 메뉴 생성하여 게임 오브젝트에 추가
    main_menu = Main_menu((width / 2, height / 2 + 100), size)
    game_objects.append(main_menu)

    while True:
        for event in pygame.event.get():
            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시, 메뉴에서 종료 선택 시 종료 처리
            if event.type in (pygame.QUIT, EVENT_QUIT_GAME):
                settings.save_setting()
                pygame.quit()
                sys.exit(0)

            # 게임 시작
            if event.type == EVENT_START_SINGLE:
                
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                background.fill("#526580")
                # GameManager.GameManager().game_start() 게임 시작 처리

            # 스토리 모드
            if event.type == EVENT_START_STORY:
                
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                background.fill("#526580")
                # GameManager.GameManager().game_start() 게임 시작 처리

            # 옵션 열기
            if event.type == EVENT_OPEN_OPTION:
                # 메인 메뉴 제거
                game_objects.remove(main_menu)
                # 설정을 게임 오브젝트에 넣어 표시되게 처리
                game_objects.append(settings)

            # 해상도 변경 이벤트를 받아 화면 리사이징
            if event.type == EVENT_OPTION_CHANGED:
                if size != settings.settings['resolution']:
                    size = settings.settings['resolution']
                    screen = pygame.display.set_mode(size)

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
