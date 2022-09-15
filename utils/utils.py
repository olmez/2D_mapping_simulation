def rect2box2Dpolygon(xy, width, height, angle=0.0):
    return width/2, height/2, (xy[0] + width/2, xy[1] + height/2), angle