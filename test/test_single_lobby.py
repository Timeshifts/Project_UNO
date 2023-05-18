import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame
import unittest
import single_lobby
from constant import *

class SingeLobbyTest(unittest.TestCase):

    def test_single_lobby(self):
        pygame.init()
        menu = single_lobby.SingleLobby()
        for event in range(menu.max_computer + menu.max_menu):
            self.assertEqual(menu.select_menu(event), None)
        pygame.quit()
    
if __name__ == "__main__":
    unittest.main()
