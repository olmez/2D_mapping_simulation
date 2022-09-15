from math import pi, cos, sin
import pygame

from Box2D import b2World, b2PolygonShape, b2Vec2, b2CircleShape

from renderer.renderer import Renderer
from robot.robot import Robot
from simulator.lidar import Lidar, LidarCallback
from simulator.engine import Engine
from simulator.map import Map


class Simulator:
    def __init__(self):
        self.world = b2World((0, 0), True)
        self.map = Map(world=self.world)
        self.lidar = Lidar()
        self.lidar_callback = LidarCallback()
        self.robot = Robot(world=self.world)
        self.renderer = Renderer(simulator_map=self.map)
        self.engine = Engine(renderer=self.renderer)

        self.force_input = tuple([0,0])
        
        self.time_step = 1 / 30
        self.box2d_iters = 2

    def user_interaction(self):
        termination = False
        up_pressed = False
        down_pressed = False
        right_pressed = False
        left_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                termination = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up_pressed = True
                if event.key == pygame.K_DOWN:
                    down_pressed = True
                if event.key == pygame.K_RIGHT:
                    right_pressed = True
                if event.key == pygame.K_LEFT:
                    left_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    up_pressed = False
                if event.key == pygame.K_DOWN:
                    down_pressed = False
                if event.key == pygame.K_RIGHT:
                    right_pressed = False
                if event.key == pygame.K_LEFT:
                    left_pressed = False

        # force in X,Y
        force = [0,0]

        if up_pressed:
            force[1] = force[1] + 100
        if down_pressed:
            force[1] = force[1] - 100
        if left_pressed:
            force[0] = force[0] - 100
        if right_pressed:
            force[0] = force[0] + 100
       
        return tuple(force), termination


    def simulate(self):
        self.engine.initialize()
        self.robot.create_body()

        while(True):
            for body in self.world.bodies:
                for fixture in body.fixtures:
                    if type(fixture.shape) == b2PolygonShape:
                        self.renderer.draw_polygon((0, 0, 0, 255), [body.transform * v for v in fixture.shape.vertices])
                    elif type(fixture.shape) == b2CircleShape:
                        self.renderer.draw_circle(self.robot.color, self.robot.get_robot_position(), fixture.shape.radius)

            measurements = []

            for i in range(self.lidar.num_rays):
                self.lidar_callback.hit = None

                angle = 2 * pi / self.lidar.num_rays * i
                start_range = self.robot.radius + self.lidar.min_range

                lidar_start_point = b2Vec2((start_range * cos(angle), start_range * sin(angle)))
                lidar_end_point = self.lidar.max_range * lidar_start_point
                lidar_start_point = lidar_start_point + self.robot.get_robot_position()
                lidar_end_point = lidar_end_point + self.robot.get_robot_position()
                self.world.RayCast(self.lidar_callback, lidar_start_point, lidar_end_point)

                if self.lidar_callback.hit:
                    measurements.append(((self.lidar_callback.hit), angle))
                    lidar_hit_point = tuple(self.lidar_callback.hit)
                    self.renderer.draw_line(self.lidar.hit_color, lidar_start_point, lidar_hit_point)
                else:
                    self.renderer.draw_line(self.lidar.miss_color, lidar_start_point, lidar_end_point)

            force, termination = self.user_interaction()
            if termination:
                break

            self.robot.move_with_force(force = force)

            self.world.Step(self.time_step, self.box2d_iters, self.box2d_iters)
            self.engine.flip_frame()   
            self.renderer.fill_map_color(self.map.color)

        self.terminate()

    def terminate(self):
        self.engine.quit()
