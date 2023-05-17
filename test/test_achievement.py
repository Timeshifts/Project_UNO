import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame, unittest
import achievement, setting
from constant import *

class AchievementTest(unittest.TestCase):

    def test_achievement(self):
        pygame.init()
        achi_object = achievement.AchievementMenu((1920, 1080), (1920, 1080))
        achi_object.acquired = {}
        test_screen = pygame.Surface((1920, 1080))
        self.assertEqual(achi_object.draw(test_screen), None)
        self.assertEqual(achi_object.acquire(0, False), None)
        self.assertEqual(achi_object.acquire(0, False), None)
        self.assertEqual(achi_object.acquire(0, True), None)
        pygame.quit()
    
    def test_achieve_indicator(self):
        pygame.init()
        test_screen = pygame.Surface((1920, 1080))
        achi_indi = achievement.AchievementIndicator(0, [], lifespan=1)
        achi_indi.gameobject.append(achi_indi)
        self.assertEqual(achi_indi.draw(test_screen), None)
        pygame.quit()



if __name__ == "__main__":
    unittest.main()