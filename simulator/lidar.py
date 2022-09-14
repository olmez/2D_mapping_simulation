from Box2D import b2RayCastCallback

class Lidar:
    def __init__(self):
        self.min_range : float = 0
        self.max_range : float = 10
        self.num_rays : float = 50
        self.hit_color : (int, int, int, int) = (0, 255, 0, 255)
        self.miss_color : (int, int, int, int) = (255, 0, 255, 255)


class LidarCallback(b2RayCastCallback):
    def __init__(self, **kwargs):
        b2RayCastCallback.__init__(self)
        self.hit = None

    def ReportFixture(self, fixture, point, normal, fraction):
        self.hit = point
        return fraction
