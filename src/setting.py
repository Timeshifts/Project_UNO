import pygame, pickle
from constant import *
from button import Button
import random
from menu import Menu

# 키 입력을 위한 설정
class Setting_Key(Button):

    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

    def __init__(self, key, size, settings):
        self.key = key
        self.settings = settings
        self.size = size
        self.highlighted = False
        self.screen = None
        if self.key == "up":
            self.pos_formula = lambda: (150, self.size[1]*0.7)
            self.display_name = "위"
        elif self.key == "down":
            self.pos_formula = lambda: (350, self.size[1]*0.7)
            self.display_name = "아래"
        elif self.key == "left":
            self.pos_formula = lambda: (550, self.size[1]*0.7)
            self.display_name = "왼쪽"
        elif self.key == "right":
            self.pos_formula = lambda: (750, self.size[1]*0.7)
            self.display_name = "오른쪽"
        elif self.key == "enter":
            self.pos_formula = lambda: (950, self.size[1]*0.7)
            self.display_name = "선택"
        elif self.key == "pause":
            self.pos_formula = lambda: (1150, self.size[1]*0.7)
            self.display_name = "일시정지"

        super().__init__(pygame.image.load(RESOURCE_PATH / "main_button.png"),
                        pos=self.pos_formula(),
                        text_input=f"{self.display_name}: {pygame.key.name(self.settings.settings[self.key])}",
                        font=self.get_font(30),
                        base_color="#3a4aab",
                        hovering_color="White",
                        size=(202, 104))
    
    def init_draw(self):
        self.pos=self.pos_formula

    def draw(self, screen):
        # key_prompt를 위해 screen이 필요하지만, handle_event를 고칠 수는 없으므로.
        if self.screen is None:
            self.screen = screen
        super().update(screen)
        super().forceChangeColor(self.highlighted, screen)

    def resize(self, size):
        self.size = size
        self.init_draw()

    def key_prompt(self):
        # 키 설정 메시지 출력
        font = self.get_font(70)
        text = font.render("바꿀 키를 입력해주세요.", True, "Black")
        text_rect = text.get_rect(center=(self.size[0]/2, self.size[1]/2))
        self.screen.blit(text, text_rect)
        pygame.display.update()

        # 사용자가 키를 입력할 때까지 대기
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # 입력된 키값 저장
                    try:
                        self.settings.apply_setting(self.key, event.key)
                        key_pressed = True
                    except ValueError:
                        pass
        self.text_input=f"{self.display_name}: {pygame.key.name(self.settings.settings[self.key])}"


    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.key_prompt()
        elif event.type == pygame.MOUSEMOTION:
            self.highlighted = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN:
            pass
        # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
        #elif event.type == pygame.KEYUP:
        #    self.pressed = False

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
            self.pos_formula = lambda i: (self.size[0] * (5 + 7*i) / 31, self.size[1] * 0.2)
            self.name_formula = lambda: (150, self.size[1] * 0.2)
            self.display_name = "해상도"
        if name == "sound":
            self.avail_menu = ["0%", "50%", "100%"]
            self.pos_formula = lambda i: (self.size[0] * (8 + 7*i) / 31, self.size[1] * 0.3)
            self.name_formula = lambda: (150, self.size[1] * 0.3)
            self.display_name = "전체 음량"
        if name == "bgm":
            self.avail_menu = ["0%", "50%", "100%"]
            self.pos_formula = lambda i: (self.size[0] * (8 + 7*i) / 31, self.size[1] * 0.4)
            self.name_formula = lambda: (150, self.size[1] * 0.4)
            self.display_name = "배경음악"
        if name == "se":
            self.avail_menu = ["0%", "50%", "100%"]
            self.pos_formula = lambda i: (self.size[0] * (8 + 7*i) / 31, self.size[1] * 0.5)
            self.name_formula = lambda: (150, self.size[1] * 0.5)
            self.display_name = "효과음"
        if name == "colorblind":
            self.avail_menu = ["켜짐", "꺼짐"]
            self.pos_formula = lambda i: (self.size[0] * (8 + 14*i) / 31, self.size[1] * 0.6)
            self.name_formula = lambda: (150, self.size[1] * 0.6)
            self.display_name = "색약 모드"

        super().__init__(pos, size, settings)

    def init_draw(self):
        super().init_draw()

        self.name_pos = self.name_formula()
        self.NAME_TEXT = self.get_font(30).render(f"{self.display_name}: ", True, "Black")
        self.NAME_RECT = self.NAME_TEXT.get_rect(center=self.name_pos)

    # 스크린에 자신을 그리기
    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.NAME_TEXT, self.NAME_RECT)
    
    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.name == "resolution":
            self.settings.apply_setting("resolution", index)
        if self.name in ("sound", "bgm", "se"):
            volume = int(self.avail_menu[index].split("%")[0])
            self.settings.apply_setting(self.name, volume)
        if self.name == "colorblind":
            self.settings.apply_setting("colorblind", True if self.avail_menu[index] == "켜짐" else False)

class Settings:
    # 가능한 해상도 목록
    resolution = {0: (1024, 576), 1: (1280, 720), 2: (1600, 900), 3: (1920, 1080)}
    
    # 폰트 설정
    get_font = lambda self, size: pygame.font.Font(RESOURCE_PATH / "font.ttf", size)

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
        self.init_draw()
        
    # init에서 draw 부분을 분리
    def init_draw(self):
        self.OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] / 2, 50))

        self.options_back_hovered = False
        self.OPTIONS_BACK = Button(
            image=None,
            pos=(self.size[0] / 2, self.size[1] - 100),
            text_input="BACK",
            font=self.get_font(75),
            base_color="Black",
            hovering_color="Green",
        )
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] / 2, 260))

        self.options_back_hovered = False
        self.OPTIONS_BACK = Button(
            image=None,
            hovering_image=None,
            pos=(self.size[0] / 2, 460),
            text_input="BACK",
            font=self.get_font(75),
            base_color="Black",
            hovering_color="Green",
        )

    # 볼륨 가져오기 (전체 음량 * 종류별 음량 = 실제 음량, 0~1 사이 값)
    get_volume = lambda self, type: self.settings["sound"] * self.settings[type] / 10000

        self.setting_menus = []
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "resolution", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "sound", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "bgm", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "se", self))
        self.setting_menus.append(Setting_Menu(self.pos, self.size, "colorblind", self))
        self.setting_menus.append(Setting_Key("up", self.size, self))
        self.setting_menus.append(Setting_Key("down", self.size, self))
        self.setting_menus.append(Setting_Key("left", self.size, self))
        self.setting_menus.append(Setting_Key("right", self.size, self))
        self.setting_menus.append(Setting_Key("enter", self.size, self))
        self.setting_menus.append(Setting_Key("pause", self.size, self))

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
        self.settings = Settings.default_setting

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

        screen.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)
        self.OPTIONS_BACK.forceChangeColor(self.options_back_hovered, screen)
        self.OPTIONS_BACK.update(screen)

        for obj in self.setting_menus:
            obj.draw(screen)
        
    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.options_back_hovered = self.OPTIONS_BACK.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.OPTIONS_BACK.rect.collidepoint(event.pos):
                pygame.event.post(pygame.event.Event(EVENT_CLOSE_OPTION))
        
        for obj in self.setting_menus:
            obj.handle_event(event)

    # 색맹 기능
    def is_blind(self, blind, ref_deck):
        self.apply_setting("colorblind", blind)
        for card in ref_deck:
            card.colorblind(self.settings["colorblind"])
