import pygame
from button import Button
import setting
from constant import *
from menu import Menu

# 싱글플레이
class Rename(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["DONE", "CANCEL"]
    name = "My Name"

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (
        self.pos[0],
        self.pos[1] + self.size[1] * 1.2 * index,
    )

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)
        self.init_draw()

        self.prompt_text = setting.get_font(50).render("Enter New Name (max 8 chars):", True, "White")
        self.prompt_text_rect = self.prompt_text.get_rect(
            center=(self.size[0] / 2, self.size[1] * 0.15)
        )
        # 본인 이름 수정
        self.text_name = setting.get_font(50).render(self.name, True, "White")
        self.text_name_rect = self.text_name.get_rect(
            center=(self.size[0] / 2, self.size[1] * 0.3)
        )

    def resize(self, size):
        super().resize(size)

        self.text_name = setting.get_font(50).render(self.name, True, "White")
        self.text_name_rect = self.text_name.get_rect(
            center=(self.size[0] / 2, self.size[1] * 0.3)
        )

    # 스크린에 자신을 그리기
    def draw(self, screen):
        super().draw(screen)

        screen.blit(
            self.text_name,
            self.text_name_rect,
        )
        screen.blit(
            self.prompt_text,
            self.prompt_text_rect,
        )

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)

        if self.avail_menu[index] == "DONE":
            pygame.event.post(pygame.event.Event(EVENT_START_LOBBY, {"name": self.name}))
        elif self.avail_menu[index] == "CANCEL":
            # 싱글플레이 로비로 복귀
            pygame.event.post(pygame.event.Event(EVENT_START_LOBBY))  

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
                    if event.key == setting.options["enter"]:
                        # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                        if self.selected != -1:
                            self.select_menu(self.selected)
                    elif (event.key == setting.options["up"]):
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        self.highlight = self.selected
                    elif (event.key == setting.options["down"]):
                        # 선택을 하나 아래로 이동
                        self.selected = (
                            self.selected + 1
                            if self.selected < self.max_menu - 1
                            else self.max_menu - 1
                        )
                        self.highlight = self.selected
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.name) > 0:
                            self.name = self.name[:-1]
                            self.resize(self.size) # 입력 중인 이름 중앙으로 다시 가져오기
                    else:
                        if len(self.name) < 8:
                            if event.unicode != 0: # 글자가 없는(예: F1) 키 제외
                                self.name += event.unicode
                            self.resize(self.size) # 입력 중인 이름 중앙으로 다시 가져오기
                    self.text_name = setting.get_font(50).render(self.name, True, "BLACK")
                    self.text_name_rect.size = self.text_name.get_size()

            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False
