import pygame

class Button:
    def __init__(self, rect, text, font, 
                 text_color=(65, 65, 65), 
                 button_color=(55, 200, 100), 
                 hover_color=(35, 180, 75), 
                 border_color=(100, 100, 100), 
                 border_radius=150, border_width=5
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = border_width

        self.click_sound = pygame.mixer.Sound("assets/sound_effects/click.wav")
        self.click_sound.set_volume(0.1)

        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color 
        else: 
            current_color = self.button_color

        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, self.border_width, self.border_radius)
        surface.blit(self.text_surface, self.text_rect)

    def sound(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.click_sound.play()
