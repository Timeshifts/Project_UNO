import pygame, pickle
from pathlib import Path

class Settings:
    default_keyset = { 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'enter': pygame.K_KP_ENTER }
    # 싱글톤 객체 생성
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.settings = Settings.default_keyset
        self.setting_path = Path.cwd() / 'resources' / 'settings.ini'
        self.load_setting()

    # 파일에 저장된 설정 불러오기
    def load_setting(self):
        try:
            with open(self.setting_path, 'rb') as f:
                self.settings = pickle.load(f)
        # 파일이 없을 시 기본 설정 불러오기
        except FileNotFoundError:
            self.reset_setting()
    
    # 파일에 설정 저장하기
    def save_setting(self):
        with open(self.setting_path, 'wb') as f:
            pickle.dump(self.settings, f)

    # 설정 초기화하기
    def reset_setting(self):
        self.settings = Settings.default_keyset
    
    def apply_setting(self):
        pass