import pygame
from pathlib import Path

# 리소스 폴더 경로
resource_path = Path.cwd() / 'resources'

EVENT_QUIT_GAME = pygame.event.custom_type()

# 메인 메뉴
class Main_menu():
    
    # 가능한 메뉴 목록
    avail_menu = ['single', 'setting', 'exit']

    # 버튼이 있어야 할 위치 반환
    get_position = lambda self, index: (self.pos[0], self.pos[1]+self.size[1]*1.2*index)

    def __init__(self, pos=(0, 0), size=(150, 50)):
        self.menu = self.avail_menu
        self.max_menu = len(self.menu)
        self.button = []
        self.rect = []
        self.pos = (pos[0]-size[0]/2, pos[1])
        self.size = size
        for i in range(self.max_menu):
            # 각 버튼 별 이미지 조작
            self.button.append(pygame.transform.scale(pygame.image.load(resource_path / 'temp_image.png'), self.size))
            # 각 버튼 이벤트 처리용 Rect 생성
            self.rect.append(self.button[i].get_rect())
            (self.rect[i].x, self.rect[i].y) = self.get_position(i)

    # 스크린에 자신을 그리기
    def draw(self, screen):
        for i in range(self.max_menu):
            screen.blit(self.button[len(self.button)-1], self.get_position(i))
    
    # 이벤트 처리
    def handle_event(self, event):
        for i in range(self.max_menu):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect[i].collidepoint(event.pos):
                    if self.avail_menu[i] == 'exit':
                        pygame.event.post(pygame.event.Event(EVENT_QUIT_GAME)) # 게임 종료
                    elif self.avail_menu[i] == 'setting':
                        pass # 설정
                    elif self.avail_menu[i] == 'single':
                        pass # 싱글플레이
            elif event.type == pygame.MOUSEMOTION:
                if self.rect[i].collidepoint(event.pos):
                    print(f'{i} 번 버튼에 마우스 호버') # 올렸을 때, 임시 메시지