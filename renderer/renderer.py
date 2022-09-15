import pygame


class Renderer:
    def __init__(self):
        self.window_size = (500, 500)
        self.map_size = (100, 100)
        self.display = pygame.display.set_mode(self.window_size, 0, 32)
        self.display.fill((255, 255, 255))

        self.screen_width = self.window_size[0]
        self.screen_height = self.window_size[1]
        self.scale_x = self.screen_width / self.map_size[0]
        self.scale_y = self.screen_height / self.map_size[1]


    def __convert_world_point_to_pixel_point(self, point):
        return (
            round(self.scale_x * point[0]),
            round(self.screen_height - self.scale_y * point[1]),
        )


    def draw_polygon(self, color, vertices):
        pts = [self.__convert_world_point_to_pixel_point(v) for v in vertices]
        pygame.draw.polygon(self.display, color, pts)


    def draw_circle(self, color, position, radius, thickness=0):
        rad_x = round(self.scale_x * radius)
        rad_y = round(self.scale_y * radius)
        pos = self.__convert_world_point_to_pixel_point(position)
        pygame.draw.ellipse(
            self.display,
            color,
            pygame.Rect(pos[0] - rad_x, pos[1] - rad_y, 2 * rad_x, 2 * rad_y),
            thickness,
        )


    def draw_line(self, color, point1, point2, thickness=1):
        pygame.draw.line(
            self.display,
            color,
            self.__convert_world_point_to_pixel_point(point1),
            self.__convert_world_point_to_pixel_point(point2),
            thickness,
        )


    def draw_rect(self, color, bottomleft, width, height, thickness=0):
        pygame.draw.rect(
            self.display,
            color,
            pygame.Rect(
                *self.__convert_world_point_to_pixel_point((bottomleft[0], bottomleft[1] + height)),
                int(self.scale_x * width),
                int(self.scale_y * height)
            ),
            thickness,
        )

