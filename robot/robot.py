from robot.data_structures import Pose  

class Robot:
    def __init__(self, world):
        self.world_robot_inside = world
        self.body = None
        self.radius : float = 1.0
        self.density : float = 1.0
        self.friction : float = 0.0
        self.color : (int, int, int, int) = (0, 0, 255, 255)
        

    def create_body(self):
        self.body = self.world_robot_inside.CreateDynamicBody(
                position = (Pose().x, Pose().y),
                linearDamping = 0,
                fixedRotation = True
            )
        self.body.CreateCircleFixture(
                radius = self.radius,
                density = self.density,
                friction = self.friction
            )

        
    def get_robot_position(self):
        return (self.body.position.x, self.body.position.y)


    def move_with_force(self, force):
        self.body.ApplyForce(force=force, point=self.get_robot_position(), wake=True)


    def move_with_velocity(self, velocity):
        self.body.SetLinearVelocity(velocity)