'''
main.py가 merge되어야 일시 정지를 메인 루프에 포함시킬 수 있습니다.
그 전에 미리 빼서 만들 수 있는 부분까지 만든 일시 정지 구현용 코드 블럭입니다.
'''

import pygame
from constant import *
from setting import Settings

event = pygame.event.Event()
paused = False

# 이벤트 처리 구간 - ESC 키를 눌러 일시정지 상태로 변경
if event.type == pygame.KEYDOWN:
    if event.key == Settings().settings['pause']:
        paused = not paused # paused를 toggle

# 일시 정지 루프
# 타이머를 제 방식대로 handle_event 함수를 받아 event-driven하게 처리한다면,
# 이 루프를 돌고 있을 때에는 타이머도 같이 멈출 것입니다.
while paused:
    # TODO: main 함수의 option 이벤트 처리, 게임 종료 메뉴 입장 이벤트 처리 가져오기
    
    # 게임 종료 메뉴의 루프
    while paused:
        # TODO: 시작 메뉴로 돌아가기와 프로그램 종료 중 선택하는 이벤트 처리 가져오기
        
        pass

# 시작 메뉴로 돌아가기 처리 블럭
if event.type == EVENT_START_MENU:
    pass