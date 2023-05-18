import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame, time
import unittest, threading
import setting, main_menu
from constant import *
import main

EVENTS = (
    pygame.event.Event(EVENT_START_LOBBY),
    pygame.event.Event(EVENT_OPEN_RENAME),
    pygame.event.Event(EVENT_START_LOBBY, name="Test"),
    pygame.event.Event(EVENT_START_SINGLE),
    pygame.event.Event(EVENT_MAIN),
    pygame.event.Event(EVENT_OPEN_STORYMAP),
    pygame.event.Event(EVENT_START_SINGLE, index=1),
    pygame.event.Event(EVENT_START_LOBBY_MULTI),
    # 추후 멀티플레이 동작 추가
    pygame.event.Event(EVENT_MAIN),
    pygame.event.Event(EVENT_OPEN_ACHIEVEMENT),
    pygame.event.Event(EVENT_MAIN),
    pygame.event.Event(EVENT_OPEN_OPTION),
    0,
    pygame.event.Event(EVENT_OPTION_CHANGED),
    pygame.event.Event(EVENT_CLOSE_OPTION),
    3,
    pygame.event.Event(EVENT_QUIT_GAME)
)

class MainTest(unittest.TestCase):

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

    # 메인 화면 동작 검증
    def test_main(self):
        setting.options["resolution"] = 3

        self.event_thread = threading.Thread(
                                target=self.event_runner
                            )
        self.event_thread.start()
        
        with self.assertRaises(SystemExit) as cm:
            self.main_func = main.main()
        
        # code 0의 정상 종료시 test 통과
        self.assertEqual(cm.exception.code, 0)

    def test_background(self):
        
        BACKGROUND_STATES = ("main_menu", "story_map", "single", "single_lobby", "multi_lobby")

        for background in BACKGROUND_STATES:
            self.assertIsInstance(
                main.get_background(
                background, (1920, 1080)),
                pygame.surface.Surface)
            
    def test_bgm(self):
        pygame.init()
        main.load_bgm(RESOURCE_PATH / "sound" / "bg_game.mp3")
        pygame.quit()

    def test_main_menu(self):
        pygame.init()
        menu = main_menu.Main_menu()
        for event in range(len(menu.avail_menu)):
            self.assertEqual(menu.select_menu(event), None)
        pygame.quit()
    
if __name__ == "__main__":
    unittest.main()

