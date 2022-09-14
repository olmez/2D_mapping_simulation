import pygame
from pygame.Rect import Rect


class Simulator:
    def __init__(self, screen_render):
        self.fps : int = 30
        self.screen_render : screen_render = ScreenRender()
        self.clock = pygame.time.Clock()


    def initialize(self):
        pygame.init()


    def flip_frame(self):
        pygame.display.flip()
        self.clock.tick(self.fps)
        self.screen_render.fill((0, 0, 0))


    def quit(self):
        pygame.quit()



class ScreenRender:
    def __init__(self):
        self.window_size : tuple(int, int) = (400, 400)
        self.map_size = None
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)
        self.screen.fill((0, 0, 0))

        self.screen_width = self.window_size[0]
        self.screen_height = self.window_size[1]
        self.scale_x = self.screen_width / self.map_size[0]
        self.scale_y = self.screen_height / self.map_size[1]


    def convert_world_point_to_pixel_point(self, point):
        return (
            round(self.scale_x * point[0]),
            round(self.screen_height - self.scale_y * point[1]),
        )


    def draw_polygon(self, color, vertices):
        pts = [self.convert_world_point_to_pixel_point(v) for v in vertices]
        pygame.draw.polygon(self.screen, color, pts)


    def draw_circle(self, color, position, radius, thickness=0):
        rad_x = round(self.scale_x * radius)
        rad_y = round(self.scale_y * radius)
        pos = self.convert_world_point_to_pixel_point(position)
        pygame.draw.ellipse(
            self.screen,
            color,
            Rect(pos[0] - rad_x, pos[1] - rad_y, 2 * rad_x, 2 * rad_y),
            thickness,
        )


    def draw_line(self, color, point1, point2, thickness=1):
        pygame.draw.line(
            self.screen,
            color,
            self.convert_world_point_to_pixel_point(point1),
            self.convert_world_point_to_pixel_point(point2),
            thickness,
        )


    def draw_rect(self, color, bottomleft, width, height, thickness=0):
        pygame.draw.rect(
            self.screen,
            color,
            Rect(
                *self.convert_world_point_to_pixel_point((bottomleft[0], bottomleft[1] + height)),
                int(self.scale_x * width),
                int(self.scale_y * height)
            ),
            thickness,
        )

