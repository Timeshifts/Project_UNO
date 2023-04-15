import pygame, pickle, setting
from constant import *
from menu import Menu

# 몇 번 스토리에 들어가려고 하는 중인지에 대한 정보 (확인 창에서 사용)
# 덤으로 -1일 경우에는 확인 창을 치우는 역할도 합니다.
enter_story = -1

# 2차 요구사항 - '대전을 시작할 것인지 묻는 창'
class StoryConfirm(Menu):
    stage_map = ("공릉역", "철길", "쪼매떡", "미래관")
    avail_menu = ("OK", "Cancel")
    axis = "x"
    pos_formula = lambda self, i: (self.size[0] * (0.35 + 0.3 * i), self.size[1] * 0.6)
    global enter_story

    def draw(self, screen):
        super().draw(screen)
        # 확인 메시지 출력
        font = setting.get_font(70)
        text = font.render(f"{self.stage_map[enter_story]}에서 스토리 대전을 시작하시겠습니까?", True, "Black")
        pygame.draw.rect(screen, "White", text.get_rect(center=(self.size[0] / 2, self.size[1] * 0.25)))

        text_rect = text.get_rect(center=(self.size[0] / 2, self.size[1] * 0.25))
        screen.blit(text, text_rect)
    
    # 메뉴 선택 시 처리
    def select_menu(self, index):
        global enter_story
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        # 스토리 다음 버튼 = 돌아가기 버튼
        if self.avail_menu[index] == "OK":
            print(f"{enter_story}번 스토리 시작")
        else:
            enter_story = -1


class StoryMenu(Menu):
    # 현재 몇 개의 스토리?
    story_amount = 4

    # 스토리 진행도 (몇 번 스토리까지 클리어?)
    story_progress = 0

    # x축 정렬 메뉴? y축 정렬 메뉴?
    axis = "x"

    # 가능한 메뉴 목록
    avail_menu = ("", "", "", "", "돌아가기")

    # 2차 요구사항 - '지도 화면에서는 각 지역별 특색을 선택시 미리 확인할 수 있어야 합니다.'
    local_rule = ("첫 분배 시 컴퓨터가 기술 카드를 50% 더 높은 확률로 받게 됩니다. 컴퓨터가 기술카드를 조합하여 2장 이상의 카드를 한번에 내는 콤보를 사용합니다.",
                  "2명의 컴퓨터 플레이어와 대전하여, 첫 카드를 제외한 모든 카드가 같은 수만큼 플레이어들에게 분배됩니다.",
                  "1명의 컴퓨터 플레이어와 대전하여, 매 5턴마다 낼 수 있는 카드의 색상이 무작위로 변경됩니다.",
                  "3명의 컴퓨터 플레이어와 대전하여, 매 20턴마다 플레이어들이 손에 든 카드가 서로 뒤바뀝니다.",
                  "" ) # 돌아가기 버튼 오류 방지 placeholder

    # 버튼이 있어야 할 위치 반환
    def pos_formula(self, i):
        if i == 0:
            return (self.size[0] * 0.1, self.size[1] * 0.7)
        elif i == 1:
            return (self.size[0] * 0.4, self.size[1] * 0.28)
        elif i == 2:
            return (self.size[0] * 0.6, self.size[1] * 0.6)
        elif i == 3:
            return (self.size[0] * 0.9, self.size[1] * 0.2)
        else:
            return (self.size[0] * 0.5, self.size[1] * 0.8)
    
    
    def draw(self, screen):
        super().draw(screen)

        # 꼼수: 안 열린 버튼 shadow로 덮어씌우기
        shadow_x = 374 * 0.75 * setting.get_screen_scale()
        shadow_y = 374 * 0.75 * setting.get_screen_scale()
        shadow_image = pygame.image.load(RESOURCE_PATH / "story" / "story_shadow.png")
        shadow_image = pygame.transform.scale(shadow_image, (shadow_x, shadow_y))
        for i in range(self.story_amount):
            if i > StoryMenu.story_progress:
                screen.blit(shadow_image, 
                            (self.pos_formula(i)[0] - shadow_x / 2,
                            self.pos_formula(i)[1] - shadow_y / 2))
        
        # 특색 표시
        font = setting.get_font(30)
        local_rule_id = self.highlight if self.selected == -1 else self.selected
        local_rule_text = f"특색: {self.local_rule[local_rule_id]}"
        if local_rule_text == "특색: ": local_rule_text = ""
        local_rule_text = font.render(local_rule_text, True, "White")
        local_rule_rect = local_rule_text.get_rect(center=(self.size[0] / 2, self.size[1] * 0.05))
        screen.blit(local_rule_text, local_rule_rect)

    # 파일에 저장된 진행도 불러오기
    def load_progress(self):
        try:
            with open(self.progress_path, "rb") as f:
                StoryMenu.story_progress = pickle.load(f)

        # 파일이 없을 시 진행도 초기화
        except FileNotFoundError:
            StoryMenu.story_progress = 0

    # 파일에 진행도 저장하기
    def save_progress(self):
        with open(self.progress_path, "wb") as f:
            pickle.dump(StoryMenu.story_progress, f)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        # ############################
        # 높은 단계의 스토리를 테스트를 위해 들어가려면
        # load_progress()를 주석처리한 뒤 story_progress = 0을 높이면 됩니다.
        # ############################
        StoryMenu.story_progress = 0
        self.progress_path = RESOURCE_PATH / "story_progress.ini"
        self.load_progress()

        story_img = lambda s: tuple(
            RESOURCE_PATH / "story" / f"story_{i}.png"
            for i in range(1, s+1))
        
        super().__init__(pos, size, scale=(0.75, 0.75),
                         button_img=story_img(self.story_amount),
                         hovering_img=RESOURCE_PATH / "main" / "main_button_highlight.png")

    # 메뉴 선택 시 처리
    def select_menu(self, index):
        se_event = pygame.event.Event(
            EVENT_PLAY_SE, {"path": RESOURCE_PATH / "sound" / "button.mp3"}
        )
        pygame.event.post(se_event)
        # 스토리 다음 버튼 = 돌아가기 버튼
        if index == self.story_amount:
            pygame.event.post(pygame.event.Event(EVENT_MAIN))
            return
        global enter_story
        # 진입 불가 스토리는 확인 창 없이 return
        if index > StoryMenu.story_progress: return
        enter_story = index

    # 이벤트 처리 - 미개방 지역 선택을 방지하기 위해 재정의
    def handle_event(self, event: pygame.event.Event):
        # 스토리 확인 창이 나오는 중에는 스토리 선택은 작동하지 않게 처리
        global enter_story
        if enter_story != -1: return
        for i in range(self.max_menu):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect[i].collidepoint(event.pos):
                    self.select_menu(i)
                    break  # 한 번에 여러 개의 메뉴가 눌리지 않도록 처리
            elif event.type == pygame.MOUSEMOTION:
                if self.rect[i].collidepoint(event.pos):
                    # 해금되지 않은 스토리에는 반응하지 않되, '돌아가기'에는 반응
                    if (i <= StoryMenu.story_progress) or i == self.max_menu -1:
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
                    elif (
                        event.key
                        == setting.options["up" if self.axis == "y" else "left"]
                    ):
                        # 선택을 하나 위로 이동
                        self.selected = self.selected - 1 if 0 < self.selected else 0
                        # 돌아가기에서 미해금 스토리로 이동 시, (예: 돌아가기 -> 5번)
                        # 해금된 가장 마지막 스토리로 이동 (예: 5번 -> 3번)
                        if self.selected > StoryMenu.story_progress:
                            self.selected = StoryMenu.story_progress
                        self.highlight = self.selected
                    elif (
                        event.key
                        == setting.options["down" if self.axis == "y" else "right"]
                    ):
                        # 선택을 하나 아래로 이동
                        self.selected = (
                            self.selected + 1
                            if self.selected < self.max_menu - 1
                            else self.max_menu - 1
                        )
                        # 해금된 마지막 스토리에서 미해금으로 이동 시, (예: 3번 -> 4번)
                        # 돌아가기로 이동 (예: 4번 -> 돌아가기)
                        if self.selected > StoryMenu.story_progress:
                            self.selected = self.max_menu -1
                        self.highlight = self.selected
            # 버튼이 누르고 있어도 계속 동작하지 않게 뗄 때까지는 작동 방지
            elif event.type == pygame.KEYUP:
                self.pressed = False


class StoryMap:
    global enter_story

    def __init__(self, pos, size):
        
        self.STORY_MENU = StoryMenu(pos, size)
        self.STORY_CONFIRM = StoryConfirm(pos, size)

    def draw(self, screen):
        if enter_story == -1:
            self.STORY_MENU.draw(screen)
        else:
            self.STORY_CONFIRM.draw(screen)

    def handle_event(self, event):
        if enter_story == -1:
            self.STORY_MENU.handle_event(event)
        else:
            self.STORY_CONFIRM.handle_event(event)
    
    def resize(self, size):
        self.STORY_MENU.resize(size)
        self.STORY_CONFIRM.resize(size)