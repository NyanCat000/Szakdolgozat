import pygame
import sys

from menu import Menu
from game import Game
from levels import Levels

class Main:
    def __init__(self):
        pygame.init()
        self.state = "menu"
        self.current_music = None

    def music(self, path):
        if self.current_music != path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.05)
            pygame.mixer.music.play(-1)
            self.current_music = path
    
    def run(self):
        while True:
            if self.state == "menu":
                self.music("assets/music/menu_music.wav")
                menu = Menu()   
                action = menu.run() 
                if action == "levels":
                    self.state = "levels"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            elif self.state == "game":
                game = Game(start_level=level)
                self.music("assets/music/game_music.wav")
                action = game.run()
                if action == "menu":
                    self.state = "menu"
                elif action == "levels":
                    self.state = "levels"

            elif self.state == "levels":
                self.music("assets/music/menu_music.wav")
                levels = Levels()
                action = levels.run()
                if action == "menu":
                    self.state = "menu"
                elif action[0] == "game":
                    level = action[1]
                    self.state = "game"




if __name__ == "__main__":
    Main().run()