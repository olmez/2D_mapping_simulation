from math import pi, cos, sin
import pygame

from Box2D import b2World, b2PolygonShape, b2Vec2, b2CircleShape

from renderer.renderer import Renderer
from utils.utils import matplotlib_rect_arg_to_Box2DPolygonShapeBox_arg
from simulator.lidar import Lidar, LidarCallback
from simulator.engine import Engine


class Simulator:
    def __init__(self, robot):
        self.world = b2World((0, 0), True)
        self.engine = Engine()
        self.lidar_sensor = Lidar()
        self.robot = robot
        
        self.time_step = 1 / 20
        self.box2d_iters = 2

    def user_interaction(self, robot_pos, measurements, agent_other, agent_requests):
        global up_pressed, down_pressed, right_pressed, left_pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                agent_requests.terminate = True

            if event.type == pygame.KEYDOWN:
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

        force = [0,0]

        if up_pressed:
            force[1] = force[1] + 100
        if down_pressed:
            force[1] = force[1] - 100
        if left_pressed:
            force[0] = force[0] - 100
        if right_pressed:
            force[0] = force[0] + 100

        self.robot.force = tuple(force)

        draw_collision(robot_pos,agent_other)

    def simulate(self):
        self.engine.initialize()
        t = 0


    def terminate(self):
        self.engine.quit()




def simulate(settings):

    world = b2World((0, 0), True)

    simulator_data = SimulatorData(settings.map_data)
    agent_requests = AgentRequests()

    agent_other = AgentOther()
    agent_other.simulator_data = simulator_data
    agent_other.simulator_settings = settings

    t = 0

    if settings.rendering_on:
        if not settings.renderer_settings:
            settings.renderer_settings = RendererSettings()

        settings.renderer_settings.map_size = settings.map_data.size
        settings.renderer_settings.fps = 1 / settings.time_step

        simulator_data.renderer = Renderer(settings.renderer_settings)
        agent_other.renderer = simulator_data.renderer

    map_width = settings.map_data.size[0]
    map_height = settings.map_data.size[1]

    obstacle = world.CreateStaticBody(
        position=(0, 0),
        shapes=[
            b2PolygonShape(box=matplotlib_rect_arg_to_Box2DPolygonShapeBox_arg(*i))
            for i in settings.map_data.obstacles
            + [
                ((-1.1, 0), 1, map_height),
                ((map_width + 0.1, 0), 1, map_height),
                ((0, -1.1), map_width, 1),
                ((0, map_height + 0.1), map_width, 1),
            ]
        ],
    )

    robot = world.CreateDynamicBody(
        position=tuple(settings.initial_pose),
        linearDamping=settings.damping,
        fixedRotation=True,
    )

    robot.CreateCircleFixture(
        radius=settings.radius, density=settings.density, friction=0
    )

    lidar_callback = LidarCallback()

    while True:

        agent_other.contacts = world.contacts

        if settings.rendering_on:
            for body in world.bodies:
                for fixture in body.fixtures:
                    if type(fixture.shape) == b2PolygonShape:
                        simulator_data.renderer.draw_polygon(
                            (255, 255, 255, 255),
                            [body.transform * v for v in fixture.shape.vertices],
                        )
                    elif type(fixture.shape) == b2CircleShape:
                        simulator_data.renderer.draw_circle(
                            settings.robot_color, robot.position, fixture.shape.radius
                        )

        if settings.laser_scanner_on:
            measurements = []

            for i in range(settings.laser_scanner_num_rays):
                lidar_callback.hit = None

                angle = 2 * pi / settings.laser_scanner_num_rays * i
                start_range = settings.radius + settings.laser_scanner_min_range

                point1 = b2Vec2((start_range * cos(angle), start_range * sin(angle)))
                point2 = settings.laser_scanner_max_range * point1
                point1 = point1 + robot.position
                point2 = point2 + robot.position
                world.RayCast(lidar_callback, point1, point2)

                if lidar_callback.hit:
                    measurements.append(((lidar_callback.hit), angle))
                    if settings.rendering_on:
                        point3 = tuple(lidar_callback.hit)
                        simulator_data.renderer.draw_line(
                            settings.laser_hit_color, point1, point3
                        )
                else:
                    if settings.rendering_on:
                        simulator_data.renderer.draw_line(
                            settings.laser_miss_color, point1, point2
                        )
                    if settings.laser_scanner_record_misses:
                        measurements.append((tuple(point2), angle))

            if settings.record_measurements:
                simulator_data.measurements_all.append(measurements)

        if settings.record_poses:
            simulator_data.pose_all.append(robot.position)

        if settings.record_time:
            simulator_data.t_all.append(t)

        settings.agent_function(
            robot.position, measurements, agent_other, agent_requests
        )

        if agent_requests.force:
            robot.ApplyForce(
                force=agent_requests.force, point=robot.position, wake=True
            )
        if agent_requests.velocity:
            robot.SetLinearVelocity(agent_requests.velocity)
        if agent_requests.terminate:
            break

        world.Step(settings.time_step, 2, settings.box2d_iters)

        if settings.rendering_on:
            simulator_data.renderer.flip_frame()

    simulator_data.renderer.quit()
