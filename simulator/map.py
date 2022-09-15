from Box2D import b2PolygonShape
from utils.utils import rect2box2Dpolygon

class Map:
    def __init__(self, world):
        self.size = (100, 100)
        self.color = (220, 220, 220)
        self.obstacles_as_rects = [ ((30, 50), 10, 10), 
                                    ((30, 70), 30, 10),
                                    ((80, 10), 10, 30),
                                    ((0 , 10), 10, 30), 
                                    ((5 , 85), 70,  5),
                                    ((90, 60), 10, 30),
                                    ((40, 10), 50,  5)]
        self.static_shapes = world.CreateStaticBody(
            position = (0,0),
            shapes = [b2PolygonShape(box=rect2box2Dpolygon(*i)) for i in self.obstacles_as_rects])