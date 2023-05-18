import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame, time
import unittest, threading, setting
import setting_menu, pause, achievement
from constant import *
import main

EVENTS = (
    pygame.event.Event(EVENT_TURN_END),
    pygame.event.Event(EVENT_COMPUTER_THINK),
    pygame.event.Event(EVENT_OPEN_ACHIEVEMENT),
    pygame.event.Event(EVENT_MAIN),
    pygame.event.Event(EVENT_OPEN_OPTION),
    pygame.event.Event(EVENT_CLOSE_OPTION),
    pygame.event.Event(pause.EVENT_QUIT_MENU),
    pygame.event.Event(pause.EVENT_PAUSE_MENU),
    pygame.event.Event(EVENT_QUIT_GAME),
)

class PauseMainTest(unittest.TestCase):

    event_thread = None
    main_func = None

    # 테스트 중에 직접 GUI 조작은 불가능하므로,
    # 테스트를 위한 이벤트를 날리기 위한 비동기 스레드 생성
    def event_runner(self):
        time.sleep(0.2)
        for event in EVENTS:
            if isinstance(event, pygame.event.Event):
                pygame.event.post(event)
                time.sleep(0.05)

    # 메인 일시정지 화면 동작 검증
    def test_pause_main(self):
        setting.options["resolution"] = 3
        pygame.init()

        size = (1920, 1080)
        test_screen = pygame.display.set_mode(size)

        self.event_thread = threading.Thread(
                                target=self.event_runner
                            )
        self.event_thread.start()
        
        self.assertEqual(pause.init_pause(
            setting_menu.Setting_UI(size=size),
            test_screen,
            achievement.AchievementMenu(size=size)), None)

        self.assertEqual(pause.pause(), None)

        pygame.quit()

    def test_pause_select(self):
        setting.options["resolution"] = 3
        pygame.init()
        for i in range(len(pause.Paused_Menu.avail_menu)):
            self.assertEqual(pause.Paused_Menu().select_menu(i), None)
        pygame.quit()
    
if __name__ == "__main__":
    unittest.main()

