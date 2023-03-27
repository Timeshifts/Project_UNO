import pygame, pickle
from pathlib import Path
from constant import *


class Settings:
    # 가능한 해상도 목록
    resolution = {0: (1024, 576), 1: (1280, 720), 2: (1600, 900), 3: (1920, 1080)}

    # 기본 설정
    default_setting = {
        "version": 3,
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "enter": pygame.K_RETURN,
        'pause': pygame.K_ESCAPE,
        "colorblind": False,
        "resolution": 3,
    }

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.settings = Settings.default_setting
        self.setting_path = RESOURCE_PATH / "settings.ini"
        self.load_setting()
        self.pos = pos
        self.size = size
        self.background = pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "temp_image.png"), self.size
        )

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
        pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

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

        # 설정 변경에 대한 이벤트 발생
        pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))
        

    # 자기 자신 = 설정 창의 크기 재설정 -> 추후 바뀔 가능성 높음
    def resize(self, size):
        self.size = size
        self.background = pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "temp_image.png"), self.size
        )

    # 스크린에 자신을 그리기
    def draw(self, screen):
        screen.blit(self.background, self.pos)

    # 이벤트 처리
    def handle_event(self, event: pygame.event.Event):
        pass
