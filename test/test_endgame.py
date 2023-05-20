import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame
import unittest
import endgame, single
from constant import *

class MultiLobbyTest(unittest.TestCase):

    def test_endgame(self):
        pygame.init()
        end_obj = endgame.EndGamePrompt((150, 150), (150, 150), "abc",
                                        single.Single(computer_count=3)
                                        , True, 3)
        end_obj = endgame.EndGamePrompt((150, 150), (150, 150), "abc",
                                        single.Single(computer_count=3)
                                        , False, 3)
        
        end_obj.single.game.player_score = (10, 20, 30, 40)

        test_screen = pygame.display.set_mode((1920, 1080))
        self.assertEqual(end_obj.draw(test_screen), None)

        pygame.quit()
    
if __name__ == "__main__":
    unittest.main()
