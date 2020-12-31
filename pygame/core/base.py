import sys
import pygame
from core.input import Input


class Base(object):
    def __init__(self):

        # initialize pygame
        pygame.init()

        # initialize default attrs
        screen_size = (512, 512)
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL

        # create drawing window
        self.screen = pygame.display.set_mode(screen_size, display_flags)

        # Set title text
        pygame.display.set_caption("Set Caption")

        # determines if main loop is active
        self.running = True

        # time related data/ops
        self.clock = pygame.time.Clock()

        # mange user input
        self.input = Input()

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        self.initialize()

        # main loop
        while self.running:
            ## process input
            self.input.update()
            if self.input.quit:
                self.running = False

            ## update
            self.update()

            ## render

            # display image
            pygame.display.flip()

            # set max frame rate
            self.clock.tick(60)

        # quit
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pass
