import pygame, pickle, datetime
from constant import *
from menu import Menu

# 업적 전체 리터럴, 추후 클래스에 들어갈 수 있습니다.
# 이름, 설명은 더미입니다. merge 이후 markdown을 읽어서 적용하겠습니다.
achievements = {
    0: {
    "icon": RESOURCE_PATH / "achievement" / "0.png",
    "name": "싱글 플레이어 승리",
    "lore": "싱글 플레이어 게임에서 1회 승리하였습니다."
    },
    1: {
    "icon": RESOURCE_PATH / "achievement" / "1.png",
    "name": "스토리 모드 A 지역 승리",
    "lore": "내부 체크용입니다.",
    },
    2: {
    "icon": RESOURCE_PATH / "achievement" / "2.png",
    "name": "스토리 모드 B 지역 승리",
    "lore": "내부 체크용입니다."
    },
    3: {
    "icon": RESOURCE_PATH / "achievement" / "3.png",
    "name": "스토리 모드 C 지역 승리",
    "lore": "내부 체크용입니다.",
    },
    4: {
    "icon": RESOURCE_PATH / "achievement" / "4.png",
    "name": "스토리 모드 D 지역 승리",
    "lore": "내부 체크용입니다.",
    },
    5: {
    "icon": RESOURCE_PATH / "achievement" / "5.png",
    "name": "싱글 플레이어 10턴안에 승리",
    "lore": "싱글 플레이어 게임을 10턴 이내에 승리하였습니다."
    },
    6: {
    "icon": RESOURCE_PATH / "achievement" / "6.png",
    "name": "기술카드 미사용 승리",
    "lore": "어떤 기술 카드도 사용하지 않고 게임에서 승리하였습니다."
    },
    7: {
    "icon": RESOURCE_PATH / "achievement" / "7.png",
    "name": "다른 플레이어 UNO 선언 뒤 승리",
    "lore": "다른 플레이어가 UNO를 선언한 상태에서 게임에서 승리하였습니다."
    },
    8: {
    "icon": RESOURCE_PATH / "achievement" / "8.png",
    "name": "멀티 플레이어 승리",
    "lore": "멀티 플레이어 게임에서 1회 승리하였습니다."
    },
    9: {
    "icon": RESOURCE_PATH / "achievement" / "9.png",
    "name": "와일드 카드 미사용 승리",
    "lore": "어떤 와일드 카드도 사용하지 않고 게임에서 승리하였습니다."
    },
    10: {
    "icon": RESOURCE_PATH / "achievement" / "10.png",
    "name": "시간 판정 승리",
    "lore": "턴 제한시간이 종료된 이후 게임 점수 판정에서 승리하였습니다."
    }
}

class AchievementMenu():

    # 달성한 업적 ({id: 시간}으로 저장)
    acquired = {}

    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                AchievementMenu.achi_progress = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            AchievementMenu.story_progress = []

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(AchievementMenu.achi_progress, f)

    # 업적을 달성 이벤트를 받아 처리하는 함수
    def acquire(self, achievement):
        
        # 이미 달성한 업적이면 무시
        if achievement in AchievementMenu.acquired:
            return
        
        # 현재 시각을 넣어서 저장
        achievement_dict = {achievement: datetime.datetime.now()}
        AchievementMenu.acquired.append(achievement_dict)

        # TODO: 게임 중 업적 창 띄워주기
        print(f"{achievement} 번 업적 {datetime.datetime.now()}에 달성")
    

    def __init__(self, pos=(0, 0), size=(150, 50)):
        AchievementMenu.achi_progress = []
        self.progress_path = RESOURCE_PATH / "achi_progress.ini"
        self.load_progress()
        
        self.resume_button = AchievementResume(pos, size)

    def draw(self, screen):
        screen.fill("white")

        self.resume_button.draw(screen)

    def handle_event(self, event):
        self.resume_button.handle_event(event)

    def resize(self, size):
        self.resume_button.resize(size)
        
# 돌아가기 버튼
class AchievementResume(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["돌아가기"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * 0.85, self.size[1] * 0.9)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.avail_menu[index] == "돌아가기":
            pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인
