import pygame, pickle
from pathlib import Path
from constant import *
from button import Button
import random

class Settings:
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
        self.init_draw()
        
    # init에서 draw 부분을 분리
    def init_draw(self):
        self.OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
        self.OPTIONS_RECT = self.OPTIONS_TEXT.get_rect(center=(self.size[0] / 2, 260))

        self.options_back_hovered = False
        self.OPTIONS_BACK = Button(
            image=None,
            pos=(self.size[0] / 2, 460),
            text_input="BACK",
            font=self.get_font(75),
            base_color="Black",
            hovering_color="Green",
        )

    # 볼륨 가져오기 (전체 음량 * 종류별 음량 = 실제 음량)
    get_volume = lambda self, type: self.settings["sound"] * self.settings[type]

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
        if (value in (self.settings['up'],
                      self.settings['down'],
                      self.settings['left'],
                      self.settings['right'],
                      self.settings['enter'],
                      self.settings['pause'])
            and self.settings[key] != value):
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
    def draw(self, screen:pygame.Surface):
        screen.fill("white")
        
        screen.blit(self.OPTIONS_TEXT, self.OPTIONS_RECT)
        
        self.OPTIONS_BACK.forceChangeColor(self.options_back_hovered, screen)
        self.OPTIONS_BACK.update(screen)
        
    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.options_back_hovered = self.OPTIONS_BACK.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.OPTIONS_BACK.rect.collidepoint(event.pos):
                self.apply_setting('resolution', random.randint(0, 3))
                pygame.event.post(pygame.event.Event(EVENT_CLOSE_OPTION))

    # 색맹 기능
    def is_blind(self, blind, ref_deck):
        self.default_setting["colorblind"] = blind
        for card in ref_deck:
            card.colorblind(self.default_setting["colorblind"])
