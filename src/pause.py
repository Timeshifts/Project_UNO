'''
일시 정지 중에 메인 루프를 대체하여 작동하는 루프입니다.
'''

import pygame, sys
from constant import *
from setting import Settings
from button import *

settings = None
screen = None
pause_object = []
clock = pygame.time.Clock()

class Paused_Screen():
    
    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)
    
    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.pos = pos
        self.size = size
        self.init_draw()

    def init_draw(self):
        self.PAUSED_TEXT = self.get_font(45).render("게임 일시정지 중", True, "Black")
        self.PAUSED_RECT = self.PAUSED_TEXT.get_rect(center=(self.size[0] / 2, 260))

        self.options_back_hovered = False
        self.OPTIONS_BACK = Button(
            image=None,
            pos=(self.size[0] / 2, 460),
            text_input="BACK",
            font=self.get_font(75),
            base_color="Black",
            hovering_color="Green",
        )

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

    # 스크린에 자신을 그리기
    def draw(self, screen:pygame.Surface):
        screen.fill("white")
        
        screen.blit(self.PAUSED_TEXT, self.PAUSED_RECT)
        
        self.OPTIONS_BACK.forceChangeColor(self.options_back_hovered, screen)
        self.OPTIONS_BACK.update(screen)
    
    # 이벤트 처리
    def handle_event(self, event):
        pass
    

def init_pause(setting: Settings, main_screen: pygame.Surface):
    pause.settings = setting
    pause.screen = main_screen
    pause.pause_object = []

def pause():
    paused = True
    pause.pause_object.append(Paused_Screen((0, 0), pause.screen.get_size()))

    while paused:
        for event in pygame.event.get():
            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시, 메뉴에서 종료 선택 시 종료 처리
            if event.type in (pygame.QUIT, EVENT_QUIT_GAME):
                pause.settings.save_setting()
                pygame.quit()
                sys.exit(0)

            # 일시 정지 풀기
            if event.type == pygame.KEYDOWN:
                if event.key == pause.settings.settings["pause"]:
                    paused = False

            # 효과음
            if event.type == EVENT_PLAY_SE:
                se = pygame.mixer.Sound(event.path)
                se.set_volume(pause.settings.get_volume("se"))
                se.play()

            # 옵션 열기
            if event.type == EVENT_OPEN_OPTION:
                # 메인 메뉴 제거
                #if state == "main_menu": game_objects.remove(main_menu)
                # 설정을 게임 오브젝트에 넣어 표시되게 처리
                pause.pause_object.append(pause.settings)

            # 옵션 닫기
            if event.type == EVENT_CLOSE_OPTION:
                # 설정 제거
                pause.pause_object.remove(pause.settings)
                # 메인 메뉴로 복귀
                #if state == "main_menu": 
                #    game_objects.append(main_menu)
                #    main_menu.resize(size)

            # 해상도 변경 이벤트를 받아 화면 리사이징
            if event.type == EVENT_OPTION_CHANGED:
                if size != settings.settings['resolution']:
                    size = settings.resolution[settings.settings['resolution']]
                    pause.screen = pygame.display.set_mode(size)
                    for obj in pause.pause_object:
                        obj.resize(size)

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