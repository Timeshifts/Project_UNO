import pygame, pickle, copy
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

    def __init__(self, pos, size, settings):
        self.name = "keys"
        self.screen = None
        super().__init__(pos, size, settings)

    def init_draw(self):
        self.pos = self.pos_formula
        super().init_draw()
        for i in range(len(self.avail_menu)):
            self.button[i].ChangeText(
                f"{self.display_name[i]}: {pygame.key.name(self.settings.settings[self.avail_menu[i]])}"
            )

    def draw(self, screen):
        # key_prompt를 위해 screen이 필요하지만, handle_event를 고칠 수는 없으므로.
        if self.screen is None:
            self.screen = screen

    def resize(self, size):
        self.size = size
        self.init_draw()

    def select_menu(self, index):
        key = self.avail_menu[index]

        # 키 설정 메시지 출력
        font = self.get_font(70)
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
                        self.settings.apply_setting(key, event.key)
                        key_pressed = True
                    except ValueError:
                        text = font.render("중복된 키가 입력되었습니다. 다시 시도해 주세요.", True, "Black")
                        pygame.draw.rect(self.screen, "White", text.get_rect(center=(self.size[0] / 2, self.size[1] / 2)))
                        text_rect = text.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
                        self.screen.blit(text, text_rect)
                        pygame.display.update()
        self.button[index].ChangeText(
            f"{self.display_name[index]}: {pygame.key.name(self.settings.settings[key])}"
        )


# 키 입력을 제외한 일반적인 설정
class Setting_Menu(Menu):
    # 가능한 메뉴 목록
    avail_menu = []

    # 버튼이 있어야 할 위치 반환
    pos_formula = None

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    def __init__(self, pos, size, name, settings):
        self.name = name
        if name == "resolution":
            self.avail_menu = list(str(value) for value in settings.resolution.values())
            self.pos_formula = lambda i: (
                self.size[0] * (5 + 7 * i) / 31,
                self.size[1] * 0.2,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.2)
            self.display_name = "해상도"
        elif name == "sound":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (8 + 14 * i) / 31,
                self.size[1] * 0.3,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.3)
            self.display_name = "전체 음량"
        elif name == "bgm":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (8 + 14 * i) / 31,
                self.size[1] * 0.4,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.4)
            self.display_name = "배경음악"
        elif name == "se":
            self.avail_menu = ["-10%", "+10%"]
            self.pos_formula = lambda i: (
                self.size[0] * (8 + 14 * i) / 31,
                self.size[1] * 0.5,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.5)
            self.display_name = "효과음"
        elif name == "colorblind":
            self.avail_menu = ["켜짐", "꺼짐"]
            self.pos_formula = lambda i: (
                self.size[0] * (8 + 14 * i) / 31,
                self.size[1] * 0.6,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.6)
            self.display_name = "색약 모드"
        elif name == "control":
            self.avail_menu = ["전체 초기화", "돌아가기"]
            self.pos_formula = lambda i: (
                self.size[0] * (8 + 14 * i) / 31,
                self.size[1] * 0.8,
            )
            self.name_formula = lambda: (150, self.size[1] * 0.8)
            self.display_name = ""

        super().__init__(pos, size, settings)

    def init_draw(self):
        super().init_draw()

        self.name_pos = self.name_formula()
        self.NAME_TEXT = self.get_font(30).render(
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
            self.settings.apply_setting("resolution", index)
        if self.name in ("sound", "bgm", "se"):
            volume = int(self.avail_menu[index].split("%")[0])
            self.settings.apply_setting(self.name, self.settings.settings[self.name]+volume)
        if self.name == "colorblind":
            self.settings.apply_setting(
                "colorblind", True if self.avail_menu[index] == "켜짐" else False
            )
        if self.name == "control":
            if index == 0:
                self.settings.reset_setting()
            else:
                pygame.event.post(pygame.event.Event(EVENT_CLOSE_OPTION))


class Settings:

    # 가능한 메뉴 목록
    avail_menu = []

    # 가능한 해상도 목록
    resolution = {0: (1024, 576), 1: (1280, 720), 2: (1600, 900), 3: (1920, 1080)}

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    # 기본 설정
    default_setting = {
        "version": 4,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "enter": pygame.K_RETURN,
        "pause": pygame.K_ESCAPE,
        "sound": 100,
        "bgm": 100,
        "se": 100,
        "colorblind": False,
        "resolution": 3,
    }

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.settings = Settings.default_setting
        self.setting_path = RESOURCE_PATH / "settings.ini"
        self.load_setting()
        self.pos = pos
        self.size = size
        self.pressed = False

        # 현재 highlight된 위치의 index
        self.highlight = ("None", 0)
        # 현재 선택된 대상, -1일 경우 마우스 조작 중
        self.selected = [0, -1]

        self.init_draw()

    # init에서 draw 부분을 분리
    def init_draw(self):
        self.OPTIONS_TEXT = self.get_font(45).render(
            "This is the OPTIONS screen.", True, "Black"
        )
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] / 2, 50))

        self.setting_menus = []
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "resolution", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "sound", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "bgm", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "se", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "colorblind", self))
        self.setting_menus.append(Setting_Key_Bundle(self.pos, self.size, self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "control", self)) # 초기화, 돌아가기

    # 볼륨 가져오기 (전체 음량 * 종류별 음량 = 실제 음량, 0~1 사이 값)
    get_volume = lambda self, type: self.settings["sound"] * self.settings[type] / 10000

    # 파일에 저장된 설정 불러오기
    def load_setting(self):
        try:
            with open(self.setting_path, "rb") as f:
                self.settings = pickle.load(f)

                # 버전이 다를 시 기본 설정 덮어쓰기
                if self.default_setting["version"] != self.settings["version"]:
                    self.reset_setting()

        # 파일이 없을 시 기본 설정 불러오기
        except FileNotFoundError:
            self.reset_setting()

    # 파일에 설정 저장하기
    def save_setting(self):
        with open(self.setting_path, "wb") as f:
            pickle.dump(self.settings, f)

    # 설정 초기화하기
    def reset_setting(self):
        # 깊은 복사
        self.settings = copy.deepcopy(self.default_setting)
        pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

    # 설정 적용하기
    def apply_setting(self, key: str, value):
        # 이미 사용중인 키 등록 시 예외 처리
        if (
            value
            in (
                self.settings["up"],
                self.settings["down"],
                self.settings["left"],
                self.settings["right"],
                self.settings["enter"],
                self.settings["pause"],
            )
            and self.settings[key] != value
        ):
            raise ValueError("중복된 키가 입력되었습니다.")

        # 음량 0% 미만, 100% 초과 방지
        if key in ("sound", "bgm", "se"):
            if value < 0: value = 0
            if value > 100: value = 100

        # 해당 설정 적용
        self.settings[key] = value
        self.save_setting()

        # 설정 변경에 대한 이벤트 발생
        pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

    # 크기 변경에 맞춰 재조정
    def resize(self, size):
        self.size = size
        self.init_draw()

    # 스크린에 자신을 그리기
    def draw(self, screen: pygame.Surface):
        screen.fill("white")

        self.SOUND_TEXT = self.get_font(45).render(
            f"{self.settings['sound']}%", True, "Black"
        )
        self.SOUND_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] * 0.6, self.size[1] * 0.3))
        self.BGM_TEXT = self.get_font(45).render(
            f"{self.settings['bgm']}%", True, "Black"
        )
        self.BGM_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] * 0.6, self.size[1] * 0.4))
        self.SE_TEXT = self.get_font(45).render(
            f"{self.settings['se']}%", True, "Black"
        )
        self.SE_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] * 0.6, self.size[1] * 0.5))

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
                if event.key == self.settings["enter"]:
                    # 키보드로 선택한 것이 있다면 그 메뉴를 선택
                    if self.selected != -1:
                        self.setting_menus[self.selected[0]].select_menu(self.selected[1])
                elif (event.key == self.settings["left"]):
                    # 선택을 하나 위로 이동
                    if self.selected[1] > 0:
                        self.selected[1] -= 1
                    else:
                        # 해당 메뉴의 첫 선택으로 가면 이전 메뉴로 넘기기
                        self.selected[0] -= 1
                        if self.selected[0] == -1: self.selected[0] = len(self.setting_menus) - 1
                        self.selected[1] = self.setting_menus[self.selected[0]].max_menu - 1
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == self.settings["right"]):
                    # 선택을 하나 아래로 이동
                    if self.selected[1] < self.setting_menus[self.selected[0]].max_menu - 1:
                        self.selected[1] += 1
                    else:
                        # 해당 메뉴의 마지막 선택으로 가면 다음 메뉴로 넘기기
                        self.selected[0] += 1
                        if self.selected[0] == len(self.setting_menus) : self.selected[0] = 0
                        self.selected[1] = 0
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == self.settings["up"]):
                    # 메뉴를 하나 위로 이동
                    self.selected[0] -= 1
                    if self.selected[0] == -1: self.selected[0] = len(self.setting_menus) - 1
                    self.selected[1] = self.setting_menus[self.selected[0]].max_menu - 1
                    self.highlight = (self.setting_menus[self.selected[0]].name, self.selected[1])
                elif (event.key == self.settings["down"]):
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
            card.colorblind(self.settings["colorblind"])
