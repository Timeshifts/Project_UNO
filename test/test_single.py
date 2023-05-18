import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame
import unittest, setting
import single, story_map
from constant import *

single_object = None

class Test(unittest.TestCase):

    def test_game_start(self):
        pygame.init()
        # 각 story별로 시작 테스트
        for i in range(-1, story_map.StoryMenu.story_amount):
            single_object = single.Single(computer_count=3, story=i)
            self.assertEqual(single_object.game_start(), None)
            self.assertIn(single_object.turn_start(), (0, 1))
        pygame.quit()
    
    def test_game_feature(self):
        pygame.init()
        single_object = single.Single(computer_count=3, story=-1)
        test_screen = pygame.surface.Surface((1920, 1080))
        single_object.game.players[0].defence_int = 1
        self.assertEqual(single_object.draw(test_screen), None)
        self.assertEqual(single_object.resize((1920, 1080)), None)
        # 플레이어의 턴으로 만들기
        single_object.game.turn_count = 0
        self.assertEqual(single_object.select_card(0), None)
        # 와일드카드 색상 선택
        single_object.game.wild = True
        self.assertEqual(single_object.select_card(0), None)
        # 일반 카드 선택
        single_object.game.turn_count = 0
        self.assertEqual(single_object.select_card(0), None)
        # 컴퓨터 턴 비동기 종료
        single_object.game.turn_count = 1
        self.assertEqual(pygame.event.post(pygame.event.Event(
            EVENT_TURN_END)), True)
        
        pygame.quit()

    def test_animation(self):
        ANIMATION = ("get", "get_my", 0, "red_skip", "red_again", "red_pick", "wild_four")

        pygame.init()
        single_object = single.Single(computer_count=3, story=-1)
        test_screen = pygame.surface.Surface((1920, 1080))
        single_object.game.turn = 1
        for anim in ANIMATION:
            single_object.effect = anim
            self.assertEqual(single_object.draw(test_screen), None)
        single_object.game.turn = 0
        for anim in ANIMATION:
            single_object.effect = anim
            self.assertEqual(single_object.draw(test_screen), None)
        # 우노 이펙트
        single_object.effect = 0
        single_object.game.players[0].is_uno = True
        self.assertEqual(single_object.draw(test_screen), None)
        pygame.quit()

    def test_event(self):
        pygame.init()
        single_object = single.Single(computer_count=3, story=-1)
        test_screen = pygame.surface.Surface((1920, 1080))
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