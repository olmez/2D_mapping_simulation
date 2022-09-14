from Box2D import b2PolygonShape, b2Vec2, b2CircleShape

class Map:
    def __init__(self):
        self.window_size : tuple(int, int) = (400, 400)
        self.map_size = None
