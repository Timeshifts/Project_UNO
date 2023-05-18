import sys, os

# src directory에서 import 가능하게 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pygame, unittest
import setting_menu, text_prompt, story_map
from constant import *

class SettingMenuTest(unittest.TestCase):

    KEY_EVENT = (pygame.event.Event(pygame.KEYDOWN, key=setting_menu.setting.options["up"]),
                 pygame.event.Event(pygame.KEYDOWN, key=setting_menu.setting.options["down"]),
                 pygame.event.Event(pygame.KEYDOWN, key=setting_menu.setting.options["left"]),
                 pygame.event.Event(pygame.KEYDOWN, key=setting_menu.setting.options["right"]),
                 pygame.event.Event(pygame.KEYDOWN, key=setting_menu.setting.options["enter"]),
                 pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F1),
                 pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
                 pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE))
    
    def test_setting_move(self):
        pygame.init()
        # 좌/우/상/하 이동
        setting_obj = setting_menu.Setting_UI()
        # MOUSEBUTTONDOWN은 dummy
        text_obj = text_prompt.Text_Prompt(done_event=pygame.MOUSEBUTTONDOWN)
        story_obj = story_map.StoryMenu()

        test_screen = pygame.surface.Surface((1920, 1080))

        self.assertEqual(text_obj.draw(test_screen), None)
        self.assertEqual(setting_obj.draw(test_screen), None)
        self.assertEqual(story_obj.draw(test_screen), None)

        for _ in range(20):

            self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[0]), None)
            self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[1]), None)
            self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[2]), None)
            self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[3]), None)

            self.assertEqual(text_obj.handle_event(self.KEY_EVENT[0]), None)
            self.assertEqual(text_obj.handle_event(self.KEY_EVENT[1]), None)
            self.assertEqual(text_obj.handle_event(self.KEY_EVENT[4]), None)
            self.assertEqual(text_obj.handle_event(self.KEY_EVENT[5]), None)
            self.assertEqual(text_obj.handle_event(self.KEY_EVENT[6]), None)

            self.assertEqual(story_obj.handle_event(self.KEY_EVENT[2]), None)
            self.assertEqual(story_obj.handle_event(self.KEY_EVENT[3]), None)

        pygame.quit()

    def test_select(self):
        pygame.init()
        size = (1920, 1080)
        setting_obj = setting_menu.Setting_UI()
        story_obj = story_map.StoryMenu()
        test_screen = pygame.display.set_mode(size)
        self.assertEqual(setting_obj.draw(test_screen), None)
        self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[1]), None)
        self.assertEqual(setting_obj.handle_event(self.KEY_EVENT[4]), None)

        self.assertEqual(story_obj.select_menu(0), None)
        self.assertEqual(story_obj.select_menu(story_obj.story_amount), None)
        self.assertEqual(story_obj.select_menu(story_obj.story_amount+2), None)
        pygame.quit()

if __name__ == "__main__":
    unittest.main()