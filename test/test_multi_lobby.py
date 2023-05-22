import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame
import unittest
import multi_lobby
from constant import *

class MultiLobbyTest(unittest.TestCase):

    def test_multi_lobby(self):
        STATES = ("client_or_server", "client_connection", "client_password", "client_connected", "server_connected")
        pygame.init()
        menu = multi_lobby.MultiLobby()

        for event in range(menu.max_other + menu.max_menu):
                self.assertEqual(menu.select_menu(event), None)

        test_screen = pygame.display.set_mode((1920, 1080))
        for state in STATES:
            menu.state = state
            menu.password = "1234"
            if menu.max_other != 0:
                menu.other_chk[0] = 1
                menu.other_chk[1] = 2
                menu.other_chk[2] = 3
                menu.other_chk[3] = 4
            self.assertEqual(menu.draw(test_screen), None)

        pygame.quit()
    
if __name__ == "__main__":
    unittest.main()
