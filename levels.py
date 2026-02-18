import pygame
import os

from scripts.utilities import image
from scripts.button import Button

class Levels:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.clock = pygame.time.Clock()

        self.back_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 45)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", 50)
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.buttons = []
        self.buttons_rect()
    
    def buttons_rect(self):
        for level in range(len(os.listdir("assets/maps"))):
            gap = 40
            button_size = 100
            columns = 5
            grid_width = (columns * button_size) + ((columns - 1) * gap)
            start_x = (self.display.get_width() - grid_width) / 2
            start_y = 250
            column = level % columns
            row = level // columns
            button_x_position = start_x + column * (button_size + gap)
            button_y_position = start_y + row * (button_size + gap)

            button = Button((button_x_position, button_y_position, button_size, button_size),
                            f"{level+1}",self.secondary_font, border_radius=40)
            self.buttons.append(button)
        back_button = Button((10, 20, 150, 80), "back",self.back_font, border_radius=150)
        self.buttons.append(back_button)
    
    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())

        levels_text = self.main_font.render("levels", True, (65, 65, 65))
        levels_text_rect = levels_text.get_rect(center=(self.display.get_width() / 2, 100))
       
        while True:
            self.display.blit(bgr, (0, 0))
            self.display.blit(levels_text, levels_text_rect)
            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                button.draw(self.display)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.buttons:
                            button.sound(event)
                            if button.rect.collidepoint(mouse_pos):
                                if button.text == "back":
                                    return "menu"
                                else:
                                    return ("game", int(button.text) - 1)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Levels().run()