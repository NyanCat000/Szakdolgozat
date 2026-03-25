import pygame
import sys
import json

from menu import Menu
from game import Game
from levels import Levels
from controls import Controls
from settings import Settings

class Main:
    def __init__(self):
        pygame.init()
        ikon = pygame.image.load("assets/images/icon.ico")
        pygame.display.set_icon(ikon)
        self.screen = pygame.display.set_mode((0, 0))
        self.state = "menu"
        self.current_music = ""
        self.menu_volume = 0.05
        self.game_volume = 0.05

        self.new_game = False

        self.load()

    def music(self, path):
        if self.current_music != path:
            pygame.mixer.music.load(path)
            if "menu" in path:
                pygame.mixer.music.set_volume(self.menu_volume)
            else: pygame.mixer.music.set_volume(self.game_volume)
            pygame.mixer.music.play(-1)
            self.current_music = path

    def change_volume(self, name, volume):
        if name == "menu":
            self.menu_volume = volume
            if "menu" in self.current_music:
                pygame.mixer.music.set_volume(self.menu_volume)
        elif name == "game":
            self.game_volume = volume
            if "game" in self.current_music:
                pygame.mixer.music.set_volume(self.game_volume)

    def save(self):
        file = open("settings.json", "w")
        json.dump({"menu_volume": self.menu_volume, "game_volume": self.game_volume}, file)
        file.close()
        
    def load(self):
        file = open("settings.json", "r")
        settings_data = json.load(file)
        file.close()
        
        self.menu_volume = settings_data["menu_volume"]
        self.game_volume = settings_data["game_volume"]
    
    
    def run(self):
        while True:
            if self.state == "menu":
                self.music("assets/music/menu_music.wav")
                menu = Menu(self.screen)   
                action = menu.run() 
                if action == "levels":
                    self.state = "levels"
                elif action == "controls":
                    self.state = "controls"
                elif action == "settings":
                    self.state = "settings"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            elif self.state == "game":
                if not self.new_game:
                    self.new_game = True
                    game = Game(self.screen, start_level=level)
                self.music("assets/music/game_music.wav")
                action = game.run()
                if action == "menu":
                    self.new_game = False
                    self.state = "menu"
                elif action == "levels":
                    self.state = "levels"
                elif action == "controls_game":
                    self.state = "controls_game"
                elif action == "settings_game":
                    self.state = "settings_game"

            elif self.state == "levels":
                self.music("assets/music/menu_music.wav")
                levels = Levels(self.screen)
                action = levels.run()
                if action == "menu":
                    self.state = "menu"
                elif action[0] == "game":
                    level = action[1]
                    self.new_game = False
                    self.state = "game"
                
            elif self.state == "controls":
                self.music("assets/music/menu_music.wav")
                controls = Controls(self.screen)
                action = controls.run()
                if action == "menu":
                    self.state = "menu"
            elif self.state == "controls_game":
                self.music("assets/music/game_music.wav")
                controls = Controls(self.screen, "game")
                action = controls.run()
                if action == "game":
                    self.state = "game"

            elif self.state == "settings":
                self.music("assets/music/menu_music.wav")
                settings = Settings(self, self.screen)
                action = settings.run()
                if action == "menu":
                    self.state = "menu"
                if action == "save":
                    self.save()
            elif self.state == "settings_game":
                self.music("assets/music/game_music.wav")
                settings = Settings(self, self.screen, "game")
                action = settings.run()
                if action == "game":
                    self.state = "game"


if __name__ == "__main__":
    Main().run()