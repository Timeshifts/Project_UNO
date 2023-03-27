import pygame
from button import Button
from setting import Settings
from constant import *

# 메인 메뉴
class Main_menu():
    
    # 가능한 메뉴 목록
    avail_menu = ['single', 'setting', 'exit']

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (self.pos[0], self.pos[1]+self.size[1]*1.2*index)

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.button = []
        self.rect = []
        self.pos = pos
        self.size = size
        self.pressed = False

        # 현재 highlight된 위치의 index
        self.highlight = 0
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = -1

        for i in range(self.max_menu):
            # 버튼 삽입
            self.button.append(Button(pygame.image.load(RESOURCE_PATH / "main_button.png"),
                                pos=(self.size[0] / 2, self.size[1] * (5 + i) / 8),
                                text_input=self.menu[i],
                                font=self.get_font(50),
                                base_color="#3a4aab",
                                hovering_color="White"))
            # 각 버튼 이벤트 처리용 Rect 삽입
            self.rect.append(self.button[i].rect)
            # highlight용 오브젝트 생성
            self.highlight_obj = pygame.transform.scale(pygame.image.load(RESOURCE_PATH / 'highlight.png'), self.size)

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_menu):
            self.button[i].update(screen)
            if i == self.highlight:
                self.button[i].forceChangeColor(True, screen)
            else:
                self.button[i].forceChangeColor(False, screen)
    
    # 메뉴 선택 시 처리
    def select_menu(self, index):
        if self.avail_menu[index] == 'exit':
            pygame.event.post(pygame.event.Event(EVENT_QUIT_GAME)) # 게임 종료
        elif self.avail_menu[index] == 'setting':
            pygame.event.post(pygame.event.Event(EVENT_OPEN_OPTION)) # 옵션 열기
        elif self.avail_menu[index] == 'single':
            pygame.event.post(pygame.event.Event(EVENT_START_SINGLE)) # 싱글플레이

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        for i in range(self.max_menu):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect[i].collidepoint(event.pos):
                    self.select_menu(i)     
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
                    if event.key == Settings().settings['enter']:
                        # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                        if self.selected != -1: self.select_menu(self.selected)
                    elif event.key == Settings().settings['up']:
                        # 선택을 하나 위로 이동
                        self.selected = self.selected-1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif event.key == Settings().settings['down']:
                        # 선택을 하나 아래로 이동
                        self.selected = self.selected+1 if self.selected < self.max_menu-1 else self.max_menu-1
                        self.highlight = self.selected
            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False