import pygame, pickle, datetime, setting
from constant import *
from menu import Menu

# 업적 전체 리터럴, 추후 클래스에 들어갈 수 있습니다.
achievements = {
    0: {
    "icon": RESOURCE_PATH / "achievement" / "1.png",
    "name": "달인",
    "lore": "싱글 플레이어 모드에서 승리하세요."
    },
    1: {
    "icon": RESOURCE_PATH / "achievement" / "2.png",
    "name": "모험가",
    "lore": "공릉역 지역에서 승리하세요.",
    },
    2: {
    "icon": RESOURCE_PATH / "achievement" / "3.png",
    "name": "탐험가",
    "lore": "철길 지역에서 승리하세요."
    },
    3: {
    "icon": RESOURCE_PATH / "achievement" / "4.png",
    "name": "포식자",
    "lore": "쪼매떡 지역에서 승리하세요.",
    },
    4: {
    "icon": RESOURCE_PATH / "achievement" / "5.png",
    "name": "지배자",
    "lore": "미래관 지역에서 승리하세요.",
    },
    5: {
    "icon": RESOURCE_PATH / "achievement" / "6.png",
    "name": "압도",
    "lore": "싱글 플레이어 모드에서 10턴 안에 승리하세요."
    },
    6: {
    "icon": RESOURCE_PATH / "achievement" / "7.png",
    "name": "수학자",
    "lore": "기술카드를 사용하지 않고 승리하세요."
    },
    7: {
    "icon": RESOURCE_PATH / "achievement" / "8.png",
    "name": "사냥꾼",
    "lore": "다른 플레이어가 UNO를 선언한 뒤 승리하세요."
    },
    8: {
    "icon": RESOURCE_PATH / "achievement" / "9.png",
    "name": "전문가",
    "lore": "5명의 컴퓨터와 대전해 싱글 플레이어 모드에서 승리하세요."
    },
    9: {
    "icon": RESOURCE_PATH / "achievement" / "10.png",
    "name": "순수",
    "lore": "wild 카드를 사용하지 않고 승리하세요."
    },
    10: {
    "icon": RESOURCE_PATH / "achievement" / "11.png",
    "name": "전략가",
    "lore": "시간이 끝났을 때 가장 낮은 점수를 획득하여 승리하세요."
    }
}

# 달성 즉시 업적 확인 창
class AchievementIndicator():

    # 현재 몇 번째 칸에 업적이 보여지고 있는가?
    showing_count = []

    def __init__(self, id: int, gameobject: list, lifespan: int=180):
        for i in range(10):
            if i not in self.showing_count:
                self.showing_count.append(i)
                self.i = i
                break
        self.id = id
        self.gameobject = gameobject
        # 180프레임 = 렉 없을 때 3초
        self.lifespan = lifespan
        self.image = pygame.image.load(
            RESOURCE_PATH / "achievement" / f"name_{self.id+1}.png"
        )
        self.image = pygame.transform.scale(self.image,
                                            (300 * setting.get_screen_scale(),
                                            300 * setting.get_screen_scale()))

    def resize(self, size):
        pass
    
    def handle_event(self, event):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, 
                    (300 * self.i * setting.get_screen_scale(),
                     0))
        self.lifespan -= 1
        if self.lifespan < 0:
            self.showing_count.remove(self.i)
            self.gameobject.remove(self)

    

class AchievementMenu():

    # 달성한 업적 ({id: 시간}으로 저장)
    acquired = {}

    pos_formula = lambda self, i: (self.size[0] * (i % 2) / 2,
                                   self.size[1] * (i // 2 / 6))
    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                AchievementMenu.acquired = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            AchievementMenu.story_progress = []

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(AchievementMenu.acquired, f)

    # 업적을 달성 이벤트를 받아 처리하는 함수
    def acquire(self, achievement, revoke=False):
        
        # 이미 달성한 업적이면 무시
        if achievement in AchievementMenu.acquired:
            return
        
        if revoke:
            # 업적 삭제
            del AchievementMenu.acquired[achievement]
        else:
            # 현재 시각을 넣어서 저장
            AchievementMenu.acquired[achievement] = datetime.datetime.now()
            self.save_progress()

        print(f"{achievement} 번 업적 {datetime.datetime.now()}에 달성")
    

    def __init__(self, pos=(0, 0), size=(150, 50)):
        AchievementMenu.achi_progress = []
        self.progress_path = RESOURCE_PATH / "achi_progress.ini"
        self.load_progress()
        
        self.pos = pos
        self.size = size
        self.resume_button = AchievementResume(pos, size)
        self.init_draw()

    def init_draw(self):
        self.resume_button.init_draw()

        self.max_achievements = len(achievements)
        self.icon_image = []
        for i in range(self.max_achievements):
            self.icon_image.append(
                pygame.transform.scale(
                    pygame.image.load(achievements[i]["icon"]),
                    (self.size[1] / 6 - 40 * setting.get_screen_scale(),
                    self.size[1] / 6 - 40 * setting.get_screen_scale())
                )
            )

    def draw(self, screen:pygame.Surface):
        screen.fill("white")

        middle = (lambda self, pos: 
                pos[0] + (self.size[0] / 4)
                + 70 * setting.get_screen_scale()
                - text.get_size()[0] / 2)
        
        for i in range(self.max_achievements):
            pos = self.pos_formula(i)
            
            # 배경 - 이미지로 교체 가능
            rect = pygame.rect.Rect(pos[0] + 10 * setting.get_screen_scale(),
                                    pos[1] + 10 * setting.get_screen_scale(),
                                    self.size[0] / 2 - 20 * setting.get_screen_scale(),
                                    self.size[1] / 6 - 20 * setting.get_screen_scale())
            pygame.draw.rect(screen, "#cccccc", rect)

            # 아이콘
            screen.blit(self.icon_image[i],
                        (pos[0] + 20 * setting.get_screen_scale(),
                        pos[1] + 20 * setting.get_screen_scale()))
            
            # 제목
            font = setting.get_font(50)
            text = font.render(achievements[i]["name"], True, "Black")
            screen.blit(
                text,
                (
                    middle(self, pos),
                    pos[1] + 25 * setting.get_screen_scale(),
                ),
            )

            # 설명
            font = setting.get_font(30)
            text = font.render(achievements[i]["lore"], True, "Black")
            screen.blit(
                text,
                (
                    middle(self, pos),
                    pos[1] + 85 * setting.get_screen_scale(),
                ),
            )

            # 달성일, 달성/미달성 여부
            font = setting.get_font(30)
            if i in self.acquired.keys():
                # acquired dict의 값 = 달성 일시
                text = f"달성일: {self.acquired[i].strftime('%Y-%m-%d %H:%M')}"
                color = "Black"
            else:
                text = f"달성일: 미달성"
                color = "Red"
            text = font.render(text, True, color)
            screen.blit(
                text,
                (
                    middle(self, pos),
                    pos[1] + 125 * setting.get_screen_scale(),
                ),
            )


        self.resume_button.draw(screen)

    def handle_event(self, event):
        self.resume_button.handle_event(event)

    def resize(self, size):
        self.size = size
        self.resume_button.resize(size)
        self.init_draw()
        
# 돌아가기 버튼
class AchievementResume(Menu):
    # 가능한 메뉴 목록
    avail_menu = ["돌아가기"]

    # 버튼이 있어야 할 위치 반환
    pos_formula = lambda self, i: (self.size[0] * 0.85, self.size[1] * 0.9)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        super().__init__(pos, size, showkey=False)

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        super().select_menu(index)
        if self.avail_menu[index] == "돌아가기":
            #########################
            # 디버그용 업적 획득 코드
            # "id": 3 부분을 바꿔 다른 업적으로
            # 변경할 수 있습니다.
            #########################
            #pygame.event.post(pygame.event.Event(
            #    EVENT_ACQUIRE_ACHIEVEMENT, {"id": 3}))
            pygame.event.post(pygame.event.Event(EVENT_MAIN))  # 메인
