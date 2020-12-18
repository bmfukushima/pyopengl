import pygame

class Input(object):
    def __init__(self):
        self.quit = False

    def update(self):
        # checks for user input events
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                self.quit = True