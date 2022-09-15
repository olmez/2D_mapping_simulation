class Pose:
    def __init__(self):
        self.x : float = 10.0
        self.y : float = 10.0
        self.yaw : float = 0.0


class EnvironmentInteractions:
    def __init__(self):
        self.simulator_data = None
        self.simulator_settings = None
        self.contacts = None
        self.renderer = None

    
class UserInteractions:
    def __init__(self):
        self.force : float = 0.0
        self.velocity : float = 0.0
        self.terminate : bool = False
        self.probability : float = 0.9
