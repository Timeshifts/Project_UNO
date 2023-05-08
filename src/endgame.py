import setting
from constant import *

# 분리하지 않으면 업적 알리미가 뒤로 가서 검은 창에 가려지게 됩니다.
class EndGamePrompt():
    def __init__(self, pos, size, name, single, won, computer_count):
        self.pos = pos
        self.size = size
        self.single = single
        self.name = name
        self.computer_count = computer_count
        self.winner_name = ""

        if won:
            self.end_prompt = "승리하였습니다! 키보드/마우스로 시작 화면으로 돌아갑니다."
        else:
            self.end_prompt = "패배하였습니다. 키보드/마우스로 시작 화면으로 돌아갑니다."
    
    def handle_event(self, event):
        pass

    def resize(self, size):
        self.size = size

    def draw(self, screen):
        # 검은 배경 상자
        box = pygame.transform.scale(
            pygame.image.load(RESOURCE_PATH / "single" / "box.png"),
            (self.size[0], self.size[1]),
        )
        box_rect = box.get_rect(center=(self.size[0] / 2, self.size[1] / 2))
        screen.blit(box, box_rect)
        # 게임 승리/패배 표시
        prompt_text = setting.get_font(50).render(self.end_prompt, True, "White")
        prompt_text_rect = prompt_text.get_rect(center=(self.size[0] / 2, self.size[1] / 4))
        screen.blit(prompt_text, prompt_text_rect)
        # 승리자 표시
        if self.single.game.winner_index == 0:
            self.winner_name = self.name
        else:
            self.winner_name = f"Player_{self.single.game.winner_index}"
        winner = setting.get_font(50).render(
            f"승리자 : {self.winner_name}",
            True,
            "White",
        )
        winner_rect = winner.get_rect(
            center=(self.size[0] / 2, self.size[1] / 15 + self.size[1] / 3)
        )
        screen.blit(winner, winner_rect)
        # 시간이 다되어서 끝난 경우 점수 표시
        if self.single.game.is_someone_win == False:
            for i in range(self.computer_count + 1):
                if i == 0:
                    player_name = self.name
                else:
                    player_name = f"Player_{i}"
                score = setting.get_font(50).render(
                    f"{player_name}의 점수 : {self.single.game.player_score[i]}",
                    True,
                    "White",
                )
                score_rect = score.get_rect(
                    center=(self.size[0] / 2, self.size[1] * (i + 2) / 15 + self.size[1] / 3)
                )
                screen.blit(score, score_rect)