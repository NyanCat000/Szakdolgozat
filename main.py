import pygame
import sys

from menu import Menu
from game import Game
from levels import Levels

class Main:
    def __init__(self):
        pygame.init()
        self.state = "menu"

    def run(self):
        while True:
            if self.state == "menu":
                menu = Menu()   
                action = menu.run() 
                if action == "levels":
                    self.state = "levels"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

            elif self.state == "game":
                game = Game(start_level=level)
                action = game.run()
                if action == "menu":
                    self.state = "menu"
                elif action == "levels":
                    self.state = "levels"

            elif self.state == "levels":
                levels = Levels()
                action = levels.run()
                if action == "menu":
                    self.state = "menu"
                elif action[0] == "game":
                    level = action[1]
                    self.state = "game"




if __name__ == "__main__":
    Main().run()