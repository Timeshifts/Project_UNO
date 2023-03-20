import sys,setting
from pathlib import Path

#pygame 검사
try:
    import pygame
except ImportError:
    print("[경고] Pygame이 설치되어 있지 않습니다.")
    sys.exit(1)

resource_path = None

def main():
    
    pygame.init()

    # 설정 불러오기
    settings = setting.Settings()
    
    # 기본 화면 설정 (기본 해상도 FHD)
    size = width, height = settings.resolution[settings.settings['resolution']]
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    # 창 제목, 아이콘
    pygame.display.set_caption('우노 게임')
    #pygame.display.set_icon(pygame.image.load(resource_path / '아이콘 파일 위치.png'))
    
    # 메인 메뉴 배경
    background = pygame.transform.scale(pygame.image.load(resource_path / 'main.png'), size)

    while True:

        for event in pygame.event.get():

            # 사용자가 X 버튼을 누르는 등의 동작으로 창 종료 시 종료 처리
            if event.type == pygame.QUIT:
                settings.save_setting()
                pygame.quit()
                sys.exit(0)

        # 기본 화면 표시
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Frame Per Second - 우선 60으로 가정합니다.
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