import pygame, copy, pickle

from constant import *

# 설정 경로
setting_path = RESOURCE_PATH / "settings.ini"

# 가능한 해상도 목록
resolution = {0: (1024, 576), 1: (1280, 720), 2: (1600, 900), 3: (1920, 1080)}

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



# 현재 설정: 이전 코드가 적절한 수정 없이 논리적 오류를
# 일으키는 것을 방지하기 위해 일부러 options로 명명했습니다.
# 설정을 읽어야 할 때가 있다면, 이 dict를 읽어서 사용하면 됩니다.
options = copy.deepcopy(default_setting)

# 볼륨 가져오기 (전체 음량 * 종류별 음량 = 실제 음량, 0~1 사이 값)
get_volume = lambda type: options["sound"] * options[type] / 10000

# 스크린이 1920 * 1080 대비 얼마나 줄었나를 실수(0-1)로 반환합니다.
# 1920 * 1080 크기에서 1.0이 반환됩니다.
get_screen_scale = lambda: resolution[options['resolution']][0] / 1920

# 스크린 size tuple을 (1920, 1080)과 같이 반환합니다.
get_screen_size = lambda: resolution[options['resolution']]

# 폰트를 하나만 쓰므로 여기에 몰아도 됩니다.
# scale이 True이면 화면 크기에 따라 폰트 사이즈가 자동으로 조정됩니다.
def get_font(size, scale=True): 
    return pygame.font.Font(RESOURCE_PATH / "font.ttf",
        int(size * get_screen_scale()) if scale else size)



# 파일에 저장된 설정 불러오기
def load_setting():
    global options
    try:
        with open(setting_path, "rb") as f:
            options = pickle.load(f)

            # 버전이 다를 시 기본 설정 덮어쓰기
            if default_setting["version"] != options["version"]:
                reset_setting()

    # 파일이 없을 시 기본 설정 불러오기
    except FileNotFoundError:
        reset_setting()

# 파일에 설정 저장하기
def save_setting():
    global options
    with open(setting_path, "wb") as f:
        pickle.dump(options, f)

# 설정 초기화하기
def reset_setting():
    global options
    # 깊은 복사
    options = copy.deepcopy(default_setting)
    pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

# 설정 적용하기
def apply_setting( key: str, value):
    global options
    # 이미 사용중인 키 등록 시 예외 처리
    if (
        value
        in (
            options["up"],
            options["down"],
            options["left"],
            options["right"],
            options["enter"],
            options["pause"],
        )
        and options[key] != value
    ):
        raise ValueError("중복된 키가 입력되었습니다.")

    # 음량 0% 미만, 100% 초과 방지
    if key in ("sound", "bgm", "se"):
        if value < 0: value = 0
        if value > 100: value = 100

    # 해당 설정 적용
    options[key] = value
    save_setting()

    # 설정 변경에 대한 이벤트 발생
    pygame.event.post(pygame.event.Event(EVENT_OPTION_CHANGED))

