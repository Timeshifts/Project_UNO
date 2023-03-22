import sys,setting
from pathlib import Path

#pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)

resource_path = None

# 메인 메뉴 - 추후 분리 예정
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
                    print(f'{i} 번 버튼에 마우스 클릭') # 눌렸을 때
            elif event.type == pygame.MOUSEMOTION:
                if self.rect[i].collidepoint(event.pos):
                    print(f'{i} 번 버튼에 마우스 호버') # 올렸을 때

def main():
    
    pygame.init()

    # 설정 불러오기
    settings = setting.Settings()
    
    # 기본 화면 설정 (기본 해상도 FHD)
    if settings.settings['resolution'] in settings.resolution.keys():
        size = width, height = settings.resolution[settings.settings['resolution']]
    else:
        # 지정된 해상도 범위 초과 시 초기화
        size = width, height = settings.settings['resolution'] = settings.default_setting['resolution']

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption('우노 게임')
    #pygame.display.set_icon(pygame.image.load(resource_path / '아이콘 파일 위치.png'))
    
    # 게임 오브젝트 배열
    game_objects = []

    # 메인 배경
    background = pygame.transform.scale(pygame.image.load(resource_path / 'main.png'), size)

    # 메인 메뉴 생성하여 게임 오브젝트에 추가
    main_menu = Main_menu((width/2, height/2+100), (400, 100))
    game_objects.append(main_menu)

    while True:

        for event in pygame.event.get():

            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시 종료 처리
            if event.type == pygame.QUIT:
                settings.save_setting()
                pygame.quit()
                sys.exit(0)

            # 오브젝트별로 이벤트 처리
            for obj in game_objects:
                obj.handle_event(event)

        # 기본 화면 표시
        screen.blit(background, (0, 0))

        # 각각의 오브젝트 그리기
        for obj in game_objects:
            obj.draw(screen)

        # 화면 갱신, FPS 60
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':

    if sys.version_info < (3, 8):
        print('[경고] Python 3.8 이상이 필요합니다.')
        sys.exit(1)

    if pygame.version.vernum < (2, 2, 0):
        print('[주의] Pygame 2.2.0 이상을 권장합니다.')

    # 리소스 폴더 경로
    resource_path = Path.cwd() / 'resources'

    main()