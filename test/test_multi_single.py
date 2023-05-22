import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame
import unittest, setting
import Multi_single
from card import Card
import Multi_GameManager
from constant import *

single_object = None
TEST_REFERANCE_DICT = {"index": 0, 
                       "turn": 0, 
                       "players": [Multi_GameManager.User(True),
                                    Multi_GameManager.User(True)], 
                       "computer_count": 0, 
                       "story_A_computer_count": 0, 
                       "ref_deck": [Card("1", "blue"), Card("1", "blue")], 
                       "deck": [Card("1", "blue"), Card("1", "blue")]}

class DummyQueue():
    def empty():
        return True

class DummyClient():
    uno_queue = DummyQueue

class Test(unittest.TestCase):

    def test_game_start(self):
        pygame.init()
        test_screen = pygame.display.set_mode((1920, 1080))
        #시작 테스트
        single_object = Multi_single.Multi_Single(client=DummyClient(), dict=TEST_REFERANCE_DICT)
        self.assertIn(single_object.turn_start(), (0, 1))
        self.assertEqual(single_object.draw(test_screen), None)
        pygame.quit()

    def test_event(self):
        pygame.init()
        single_object = Multi_single.Multi_Single(client=DummyClient(), dict=TEST_REFERANCE_DICT)
        single_object.client = DummyClient()
        single_object.game.turn = 0
        self.assertEqual(single_object.handle_event(
            pygame.event.Event(EVENT_TURN_END, option=0)
        ), None)
        self.assertEqual(single_object.handle_event(
            pygame.event.Event(EVENT_TURN_END, option=1)
        ), None)
        single_object.game.turn = 0
        for _ in range(20):
            self.assertEqual(single_object.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=setting.options["right"])
            ), None)
            self.assertEqual(single_object.handle_event(
                pygame.event.Event(pygame.KEYDOWN, key=setting.options["left"])
            ), None)
        
        self.assertEqual(single_object.handle_event(
            pygame.event.Event(pygame.KEYDOWN, key=setting.options["enter"])
        ), None)

        pygame.quit()

if __name__ == "__main__":
    unittest.main()