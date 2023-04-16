import pygame, pickle, copy, setting
from constant import *
from button import Button
import random
from menu import Menu

# 키 입력을 위한 설정
class Setting_Key_Bundle(Menu):

     # 가능한 메뉴 목록
    avail_menu = ["up", "down", "left", "right", "enter", "pause"]
    display_name = ["위", "아래", "왼쪽", "오른쪽", "선택", "일시정지"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * (i+1)/7, self.size[1] * 0.7)

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    def __init__(self, pos, size):
        self.name = "keys"
        self.screen = None
        super().__init__(pos, size, scale=(0.6, 1.0))

    def init_draw(self):
        self.pos = self.pos_formula
        super().init_draw()
        for i in range(len(self.avail_menu)):
            self.button[i].ChangeText(
                f"{self.display_name[i]}: {pygame.key.name(setting.options[self.avail_menu[i]])}"
            )

    def draw(self, screen):
        # key_prompt를 위해 screen이 필요하지만, handle_event를 고칠 수는 없으므로.
        if self.screen is None:
            self.screen = screen

    def select_menu(self, index):
        key = self.avail_menu[index]

        # 키 설정 메시지 출력
        font = setting.get_font(70)
        text = font.render("바꿀 키를 입력해주세요.", True, "Black")
        pygame.draw.rect(self.screen, "White", text.get_rect(center=(self.size[0] / 2, self.size[1] / 2)))

        text_rect = text.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()

        # 사용자가 키를 입력할 때까지 대기
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # 입력된 키값 저장
                    try:
                        setting.apply_setting(key, event.key)
                        key_pressed = True
                    except ValueError:
                        text = font.render("중복된 키가 입력되었습니다. 다시 시도해 주세요.", True, "Black")
                        pygame.draw.rect(self.screen, "White", text.get_rect(center=(self.size[0] / 2, self.size[1] / 2)))
                        text_rect = text.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
                        self.screen.blit(text, text_rect)
                        pygame.display.update()
        self.button[index].ChangeText(
            f"{self.display_name[index]}: {pygame.key.name(setting.options[key])}"
        )


# 키 입력을 제외한 일반적인 설정
class Setting_Menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = []

    # 버튼이 있어야 할 위치 반환
    pos_formula = None

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    def __init__(self, pos, size, name):
        self.name = name
        if name == "resolution":
            self.avail_menu = list(str(value) for value in setting.resolution.values())
            self.pos_formula = lambda i: (
                self.size[0] * (7 + 6 * i) / 31,
                self.size[1] * 0.2,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.2)
            self.display_name = "해상도"
        elif name == "sound":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (9 + 14 * i) / 31,
                self.size[1] * 0.3,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.3)
            self.display_name = "전체 음량"
        elif name == "bgm":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (9 + 14 * i) / 31,
                self.size[1] * 0.4,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.4)
            self.display_name = "배경음악"
        elif name == "se":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (9 + 14 * i) / 31,
                self.size[1] * 0.5,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.5)
            self.display_name = "효과음"
        elif name == "colorblind":
            self.avail_menu = ["켜짐", "꺼짐"]
            self.pos_formula = lambda i: (
                self.size[0] * (9 + 14 * i) / 31,
                self.size[1] * 0.6,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.6)
            self.display_name = "색약 모드"
        elif name == "control":
            self.avail_menu = ["전체 초기화", "돌아가기"]
            self.pos_formula = lambda i: (
                self.size[0] * (9 + 14 * i) / 31,
                self.size[1] * 0.8,
            )
            self.name_formula = lambda: (self.size[0] * 0.1, self.size[1] * 0.8)
            self.display_name = ""

        super().__init__(pos, size, scale=((0.8, 1) if name == 'resolution' else (1, 1)))

    def init_draw(self):
        super().init_draw()

        self.name_pos = self.name_formula()
        self.NAME_TEXT = setting.get_font(45 * setting.get_screen_scale()).render(
            f"{self.display_name}: ", True, "Black"
        )
        self.NAME_RECT = self.NAME_TEXT.get_rect(center=self.name_pos)
    
    def draw(self, screen):
        if self.display_name != "":
            screen.blit(self.NAME_TEXT, self.NAME_RECT)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.name == "resolution":
            setting.apply_setting("resolution", index)
        if self.name in ("sound", "bgm", "se"):
            volume = int(self.avail_menu[index].split("%")[0])
            setting.apply_setting(self.name, setting.options[self.name]+volume)
        if self.name == "colorblind":
            setting.apply_setting(
                "colorblind", True if self.avail_menu[index] == "켜짐" else False
            )
        if self.name == "control":
            if index == 0:
                setting.reset_setting()
            else:
                pygame.event.post(pygame.event.Event(EVENT_CLOSE_OPTION))


class Setting_UI:

    # 가능한 메뉴 목록
    avail_menu = []

    def __init__(self, pos=(0, 0), size=(150, 50)):
        setting.options = setting.default_setting
        setting.load_setting()
        self.pos = pos
        self.size = size
        self.pressed = False

        # 현재 highlight된 위치의 index
        self.highlight = ("None", 0)
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = [0, -1]

        self.init_draw()

    # init에서 draw 부분을 분리
    def init_draw(self,):
        self.OPTIONS_TEXT = setting.get_font(45, True).render(
            "설정", True, "Black"
        )
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] / 2, 50))

        self.setting_menus = []
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "resolution"))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "sound"))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "bgm"))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "se"))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "colorblind"))
        self.setting_menus.append(Setting_Key_Bundle(self.pos, self.size))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "control")) # 초기화, 돌아가기

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size

        self.init_draw()
        
        for obj in self.setting_menus:
            obj.resize(size)

    # 스크린에 자신을 그리기
    def draw(self, screen: pygame.Surface):
        screen.fill("white")

        self.SOUND_TEXT = setting.get_font(45).render(
            f"{setting.options['sound']}%", True, "Black"
        )
        self.SOUND_RECT = self.SOUND_TEXT.get_rect(center=(self.size[0] / 2, self.size[1] * 0.3))
        self.BGM_TEXT = setting.get_font(45).render(
            f"{setting.options['bgm']}%", True, "Black"
        )
        self.BGM_RECT = self.BGM_TEXT.get_rect(center=(self.size[0] / 2, self.size[1] * 0.4))
        self.SE_TEXT = setting.get_font(45).render(
            f"{setting.options['se']}%", True, "Black"
        )
        self.SE_RECT = self.SE_TEXT.get_rect(center=(self.size[0] / 2, self.size[1] / 2))

        screen.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)
        screen.blit(self.SOUND_TEXT, self.SOUND_RECT)
        screen.blit(self.BGM_TEXT, self.BGM_RECT)
        screen.blit(self.SE_TEXT, self.SE_RECT)

        for menu in self.setting_menus:
            for i in range(menu.max_menu):
                menu.button[i].update(screen)
                if menu.name == self.highlight[0] and i == self.highlight[1]:
                    menu.button[i].changeHighlight(True, screen)
                else:
                    menu.button[i].changeHighlight(False, screen)

        for obj in self.setting_menus:
            obj.draw(screen)

    # 이벤트 처리
    # 키보드 처리를 해결하기 위해 모든 메뉴를 하나의 객체로 묶어버릴지,
    # 아니면 설정 객체에서 모든 이벤트를 처리할지 꽤 고민했습니다.
    # 일단 후자로 결정했습니다.
    def handle_event(self, event: pygame.event.Event):
        # 마우스 입력 = 모든 메뉴를 순회하여 기존 메뉴처럼 처리
        for menu in self.setting_menus:
            if event.type == pygame.MOUSEBUTTONDOWN:
                 for i in range(menu.max_menu):
                    if menu.rect[i].collidepoint(event.pos):
                        menu.select_menu(i)
                        break  # 한 번에 여러 개의 메뉴가 눌리지 않도록 처리
            elif event.type == pygame.MOUSEMOTION:
                for i in range(menu.max_menu):
                    if menu.rect[i].collidepoint(event.pos):
                        # highlight 대상을 변경
                        self.highlight = (menu.name, i)
                        # 키보드 선택 해제
                        self.selected = [0, -1]
        # 키보드 입력
        if event.type == pygame.KEYDOWN:
            if self.pressed == False:
                self.pressed = True
                # 엔터 키가 눌렸을 때
                if event.key == setting.options["enter"]:
                    # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                    if self.selected != -1:
                        self.setting_menus[self.selected[0]].select_menu(self.selected[1])
                elif (event.key == setting.options["left"]):
                    # 선택을 하나 위로 이동
                    if self.selected[1] > 0:
                        self.selected[1] -= 1
                    else:
                        # 해당 메뉴의 첫 선택으로 가면 이전 메뉴로 넘기기
                        self.selected[0] -= 1
                        if self.selected[0] == -1: self.selected[0] = len(self.setting_menus) - 1
                        self.selected[1] = self.setting_menus[self.selected[0]].max_menu - 1
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == setting.options["right"]):
                    # 선택을 하나 아래로 이동
                    if self.selected[1] < self.setting_menus[self.selected[0]].max_menu - 1:
                        self.selected[1] += 1
                    else:
                        # 해당 메뉴의 마지막 선택으로 가면 다음 메뉴로 넘기기
                        self.selected[0] += 1
                        if self.selected[0] == len(self.setting_menus) : self.selected[0] = 0
                        self.selected[1] = 0
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == setting.options["up"]):
                    # 메뉴를 하나 위로 이동
                    self.selected[0] -= 1
                    if self.selected[0] == -1: self.selected[0] = len(self.setting_menus) - 1
                    self.selected[1] = self.setting_menus[self.selected[0]].max_menu - 1
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == setting.options["down"]):
                    # 메뉴를 하나 아래로 이동
                    self.selected[0] += 1
                    if self.selected[0] == len(self.setting_menus) : self.selected[0] = 0
                    self.selected[1] = 0
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
        elif event.type == pygame.KEYUP:
            self.pressed = False

    # 색맹 기능
    def is_blind(self, blind, ref_deck):
        self.apply_setting("colorblind", blind)
        for card in ref_deck:
            card.colorblind(setting.options["colorblind"])
