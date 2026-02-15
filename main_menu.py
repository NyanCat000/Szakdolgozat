import sys
import pygame

from scripts.utilities import image
from levels import Levels

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.clock = pygame.time.Clock()
        
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", 40)
        self.buttons = []
        self.buttons_rect()
    
    def buttons_rect(self):
        button_names = ["levels", "options", "controls", "quit"]
        center_y = self.display.get_height() / 2 - 75
        y_offset = 150

        for i in range(len(button_names)):
            name = button_names[i]
            button_rect = pygame.Rect(0, 0, 450, 100)
            button_rect.centerx = self.display.get_width() / 2
            button_rect.centery = center_y + i * y_offset

            text = self.main_font.render(name, True, (65, 65, 65)) 
            text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - 8))

            self.buttons.append((name, button_rect, text, text_rect))
    
    def quit(self):
        quit_screen_overlay = pygame.Surface(self.display.get_size())
        quit_screen_overlay.fill((0,0,0))
        quit_screen_overlay.set_alpha(200)

        pop_up_rect = pygame.Rect(0,0, 500, 250)
        pop_up_rect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
        sure_text = self.secondary_font.render("Are you sure?", True, (65, 65, 65))
        sure_text_rect = sure_text.get_rect(center=(pop_up_rect.centerx, pop_up_rect.centery - 40))
        
        yes_button_rect = pygame.Rect(pop_up_rect.centerx - 110, pop_up_rect.centery + 50, 100, 50)
        no_button_rect = pygame.Rect(pop_up_rect.centerx + 10, pop_up_rect.centery + 50, 100, 50)
        yes_text = self.secondary_font.render("Yes", True, (65, 65, 65))
        no_text = self.secondary_font.render("No", True, (65, 65, 65))
        yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
        no_text_rect = no_text.get_rect(center=no_button_rect.center)

        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.display.blit(bgr, (0, 0))
            self.display.blit(quit_screen_overlay, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if yes_button_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                        if no_button_rect.collidepoint(mouse_pos):
                            return

            pygame.draw.rect(self.display, (55, 200, 100), pop_up_rect, border_radius=50)
            pygame.draw.rect(self.display, (100, 100, 100), pop_up_rect, 5 ,border_radius=50)

            button_color = (35, 180, 75)
            hover_color = (10, 150, 50)
            if yes_button_rect.collidepoint(mouse_pos):
                button_color = hover_color
            pygame.draw.rect(self.display, button_color, yes_button_rect,border_radius=50)
            pygame.draw.rect(self.display, (100, 100, 100), yes_button_rect, 5 ,border_radius=50)

            button_color = (35, 180, 75)
            hover_color = (10, 150, 50)
            if no_button_rect.collidepoint(mouse_pos):
                button_color = hover_color
            pygame.draw.rect(self.display, button_color, no_button_rect,border_radius=50)
            pygame.draw.rect(self.display, (100, 100, 100), no_button_rect, 5 ,border_radius=50)
            
            self.display.blit(sure_text, sure_text_rect)
            self.display.blit(yes_text, yes_text_rect)
            self.display.blit(no_text, no_text_rect)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
    
    def run(self):
        self.running = True
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())
        
        while self.running:
            self.display.blit(bgr, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for name, button_rect, text, text_rect in self.buttons:
                button_color = (55, 200, 100)
                hover_color = (35, 180, 75)
                if button_rect.collidepoint(mouse_pos):
                    button_color = hover_color
                pygame.draw.rect(self.display, button_color, button_rect,border_radius=150)
                pygame.draw.rect(self.display, (100, 100, 100), button_rect, 5 ,border_radius=150)
                self.display.blit(text, text_rect)
           
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for name, button_rect, text, text_rect in self.buttons:
                            if button_rect.collidepoint(mouse_pos):
                                if name == "levels":
                                    Levels().run()
                                if name == "quit":
                                    self.quit()
                    
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Menu().run()