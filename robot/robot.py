from robot.data_structures import Pose  

class Robot:
    def __init__(self, world):
        self.world_robot_inside = world
        self.dynamic_body = None
        self.radius : float = 0.0
        self.density : float = 1.0
        self.friction : float = 0.0
        self.robot_color : (int, int, int, int) = (255, 0, 0, 255)
        self.pose : Pose = Pose()
        

    def create_dynamic_body(self):
        self.dynamic_body = self.world_robot_inside.CreateDynamicBody(
                position = self.get_robot_position(),
                linearDamping = 0,
                fixedRotation = True
            )


    def create_rigid_body(self):
        self.dynamic_body.CreateCircleFixture(
                radius = self.radius,
                density = self.density,
                friction = self.friction
            )

        
    def get_robot_position(self):
        return tuple(self.pose.x, self.pose.y)


    def move_with_force(self, force):
        self.dynamic_body.ApplyForce(force=force, point=self.get_robot_position(), wake=True)


    def move_with_velocity(self, velocity):
        self.dynamic_body.SetLinearVelocity(velocity)