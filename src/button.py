import pygame


class Button:
    def __init__(
        self, image, hovering_image, pos, text_input, font, base_color, hovering_color
    ):
        self.image = image
        self.hovering_image = hovering_image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        if self.hovering_image is None:
            self.hovering_image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # def changeColor(self, position, screen):
    #     if position[0] in range(self.rect.left, self.rect.right) and position[
    #         1
    #     ] in range(self.rect.top, self.rect.bottom):
    #         self.text = self.font.render(self.text_input, True, self.hovering_color)
    #         screen.blit(self.hovering_image, self.rect)
    #     else:
    #         self.text = self.font.render(self.text_input, True, self.base_color)

    def forceChangeColor(self, state, screen):
        if state:
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            screen.blit(self.image, self.rect)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            screen.blit(self.image, self.rect)

    def ChangeImage(self, change_image):
        self.image = change_image

    def ChangeText(self, change_text, change_base_color, change_hovering_color):
        self.text_input = change_text
        self.base_color, self.hovering_color = change_base_color, change_hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
