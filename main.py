import sys
import pygame

from settings import *


class Main:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stock Sim")

    def run(self):
        while True:
            self.window.fill(Color.BLACK.value)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()



if __name__ == '__main__':
    main = Main()
    main.run()
