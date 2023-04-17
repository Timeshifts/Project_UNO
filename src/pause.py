import pygame, sys
from constant import *
import setting, setting_menu
from button import *
from menu import Menu

settings = None
screen = None
pause_object = []
clock = pygame.time.Clock()

# 일시정지 내부에서만 쓰이는 EVENT
EVENT_QUIT_MENU = pygame.event.custom_type()
EVENT_PAUSE_MENU = pygame.event.custom_type()
EVENT_RESUME = pygame.event.custom_type()

"""
일시 정지 중에 필요한 클래스 정의입니다.
일시 정지는 게임 진행 중에만 가능하게 할 예정이므로,
다른 상황에서 일시 정지 시 생기는 예외 상황은 오류가 아닙니다.
"""


class Quit_Menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["돌아가기", "시작 화면", "게임 종료"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * (5 + 10 * i) / 30, self.size[1] / 2)

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)

    def init_draw(self):
        super().init_draw()

        self.PAUSED_TEXT = setting.get_font(45).render("동작을 선택해 주세요.", True, "Black")
        self.PAUSED_RECT = self.PAUSED_TEXT.get_rect(center=(self.size[0] / 2, self.size[1] * 0.2))

    # 스크린에 자신을 그리기
    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.PAUSED_TEXT, self.PAUSED_RECT)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        if self.avail_menu[index] == "게임 종료":
            pygame.event.post(pygame.event.Event(EVENT_QUIT_GAME))  # 게임 종료
        elif self.avail_menu[index] == "돌아가기":
            pygame.event.post(pygame.event.Event(EVENT_PAUSE_MENU))  # 정지 메뉴로 복귀
        elif self.avail_menu[index] == "시작 화면":
            pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 시작 화면으로 복귀


class Paused_Menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["OPTIONS", "RESUME", "EXIT"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * (5 + 10 * i) / 30, self.size[1] / 2)

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)

    def init_draw(self):
        super().init_draw()

        self.PAUSED_TEXT = setting.get_font(45).render("Game is paused.", True, "Black")
        self.PAUSED_RECT = self.PAUSED_TEXT.get_rect(center=(self.size[0] / 2, self.size[1] * 0.2))

    # 스크린에 자신을 그리기
    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.PAUSED_TEXT, self.PAUSED_RECT)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        if self.avail_menu[index] == "EXIT":
            pygame.event.post(pygame.event.Event(EVENT_QUIT_MENU))  # 게임 종료 메뉴 호출
        elif self.avail_menu[index] == "OPTIONS":
            pygame.event.post(pygame.event.Event(EVENT_OPEN_OPTION))  # 옵션 열기
        elif self.avail_menu[index] == "RESUME":
            pygame.event.post(pygame.event.Event(EVENT_RESUME))  # 일시정지 해제


"""
일시 정지 중에 메인 루프를 대체하여 작동하는 루프입니다.
"""


def init_pause(settings: setting_menu.Setting_UI, main_screen: pygame.Surface):
    pause.settings = settings
    pause.screen = main_screen
    pause.pause_object = []


def pause(reset=True):
    paused = True
    paused_menu = Paused_Menu((0, 0), pause.screen.get_size())
    quit_menu = Quit_Menu((0, 0), pause.screen.get_size())
    if reset:
        pause.pause_object.append(paused_menu)
    size = pause.screen.get_size()

    # TODO: 임시
    for obj in pause_object:
        obj.resize(size)
    
    while paused:
        for event in pygame.event.get():
            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시, 메뉴에서 종료 선택 시 종료 처리
            if event.type in (pygame.QUIT, EVENT_QUIT_GAME):
                # 일시 정지를 풀고
                paused = False
                # Main 루프에서 이벤트를 처리하도록 다시 넘겨주기
                pygame.event.post(event)

            # 일시 정지 풀기
            if event.type == pygame.KEYDOWN:
                if event.key == setting.options["pause"]:
                    paused = False
                    # 실제로 설정이 바뀌지 않았을 수도 있으나,
                    # 설정 변경을 메인 루프에도 적용하기 위함.
                    pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))
            
            if event.type == EVENT_RESUME:
                paused = False
                pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

            # 효과음
            if event.type == EVENT_PLAY_SE:
                se = pygame.mixer.Sound(event.path)
                se.set_volume(setting.get_volume("se"))
                se.play()

            # 옵션 열기
            if event.type == EVENT_OPEN_OPTION:
                # 메인 일시정지 메뉴 제거
                pause.pause_object.remove(paused_menu)
                # 설정을 게임 오브젝트에 넣어 표시되게 처리
                pause.pause_object.append(pause.settings)

            # 일시정지 메뉴 -> 종료 메뉴
            if event.type == EVENT_QUIT_MENU:
                pause.pause_object.remove(paused_menu)
                # 메인 일시정지 메뉴로 복귀
                pause.pause_object.append(quit_menu)

            # 종료 메뉴 -> 일시정지 메뉴
            if event.type == EVENT_PAUSE_MENU:
                pause.pause_object.remove(quit_menu)
                # 메인 일시정지 메뉴로 복귀
                pause.pause_object.append(paused_menu)

            # 옵션 닫기
            if event.type == EVENT_CLOSE_OPTION:
                # 설정 제거
                pause.pause_object.remove(pause.settings)
                # 메인 일시정지 메뉴로 복귀
                pause.pause_object.append(paused_menu)
                paused_menu.resize(size)
                quit_menu.resize(size)

            # 시작 메뉴로 돌아가기
            if event.type == EVENT_MAIN:
                # 일시 정지를 풀고
                paused = False
                # Main 루프에서 이벤트를 처리하도록 다시 넘겨주기
                pygame.event.post(pygame.event.Event(EVENT_MAIN))

            # 해상도 변경 이벤트를 받아 화면 리사이징
            # 배경음악 음량 변경 즉시 적용
            if event.type == EVENT_OPTION_CHANGED:
                if size != setting.resolution[setting.options["resolution"]]:
                    size = setting.resolution[setting.options["resolution"]]
                    pause.screen = pygame.display.set_mode(size)
                    # TODO: 직접 setting을 뽑아올 수 있게 되면서,
                    # resize의 역할이 굉장히 애매해졌습니다.
                    # 조정이나 삭제가 이루어질 수도 있습니다.
                    for obj in pause.pause_object:
                        obj.resize(size)
                pygame.mixer.music.set_volume(setting.get_volume("bgm"))

            # 오브젝트별로 이벤트 처리
            for obj in pause.pause_object:
                obj.handle_event(event)

        # 기본 화면 표시
        pause.screen.fill("White")

        # 각각의 오브젝트 그리기
        for obj in pause.pause_object:
            obj.draw(pause.screen)

        # 화면 갱신, FPS 60
        pygame.display.flip()
        clock.tick(60)
