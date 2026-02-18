import pygame

from scripts.utilities import image
from scripts.button import Button

class Menu:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.display = pygame.Surface((self.screen_size[0], self.screen_size[1]))
        self.clock = pygame.time.Clock()
        
        self.main_font = pygame.font.Font("assets/fonts/PermanentMarker-Regular.ttf", 80)
        self.secondary_font = pygame.font.Font("assets/fonts/Schoolbell-Regular.ttf", 40)
        
        self.confirm = False
        self.confirm_buttons = []
        self.quit_buttons()

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

            button = Button(button_rect, name, self.main_font, border_radius=150)
            self.buttons.append(button)
    
    def quit_buttons(self):
        pop_up_rect = pygame.Rect(0,0, 500, 250)
        pop_up_rect.center = (self.display.get_width() / 2, self.display.get_height() / 2)

        yes_button = Button((pop_up_rect.centerx - 110, pop_up_rect.centery + 50, 100, 50), "Yes",
                            self.secondary_font, border_radius=50)
        no_button = Button((pop_up_rect.centerx + 10, pop_up_rect.centery + 50, 100, 50), "No",
                            self.secondary_font, border_radius=50)
        
        self.confirm_buttons.append(yes_button)
        self.confirm_buttons.append(no_button)

    
    def quit(self):
        quit_screen_overlay = pygame.Surface(self.display.get_size())
        quit_screen_overlay.fill((0,0,0))
        quit_screen_overlay.set_alpha(200)

        bgr = pygame.transform.scale(image("background/bgr_menu.png"), self.display.get_size())
        sure_text = self.secondary_font.render("Are you sure?", True, (65, 65, 65))
        
        self.display.blit(bgr, (0, 0))
        self.display.blit(quit_screen_overlay, (0,0))

        pop_up_rect = pygame.Rect(0,0, 500, 250)
        pop_up_rect.center = (self.display.get_width() / 2, self.display.get_height() / 2)
        pygame.draw.rect(self.display, (55, 200, 100), pop_up_rect, border_radius=50)
        pygame.draw.rect(self.display, (100, 100, 100), pop_up_rect, 5 ,border_radius=50)
        sure_text_rect = sure_text.get_rect(center=(pop_up_rect.centerx, pop_up_rect.centery - 40))
        self.display.blit(sure_text, sure_text_rect)

        for button in self.confirm_buttons:
            button.draw(self.display)

    
    def run(self):
        bgr = pygame.transform.scale(image("background/bgr_game.png"), self.display.get_size())

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.confirm:
                            for button in self.confirm_buttons:
                                if button.rect.collidepoint(mouse_pos):
                                    if button.text == "Yes":
                                        return "quit"
                                    if button.text == "No":
                                        self.confirm = False
                        else:
                            for button in self.buttons:
                                if button.rect.collidepoint(mouse_pos):
                                    if button.text == "levels":
                                        return "levels"
                                    if button.text == "quit":
                                        self.confirm = True
                                    if button.text == "controls":
                                        return "controls"
                
            
            self.display.blit(bgr, (0, 0))

            for button in self.buttons:
                button.draw(self.display)

            if self.confirm:
                self.quit()
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Menu().run()