import pygame

class Engine:
    def __init__(self, renderer):
        self.fps : int = 30
        self.display = renderer.display
        self.clock = pygame.time.Clock()


    def initialize(self):
        pygame.init()


    def flip_frame(self):
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.display.fill((255, 255, 255))


    def quit(self):
        pygame.quit()

