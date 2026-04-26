import pybullet as p

def add_light_marker(position, color=(1, 1, 0, 1), radius=0.1):
    visual_shape_id = p.createVisualShape(
        shapeType=p.GEOM_SPHERE,
        radius=radius,
        rgbaColor=color
    )
    body_id = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=-1,
        baseVisualShapeIndex=visual_shape_id,
        basePosition=position
    )
    return body_id

def set_marker_color(marker_id, color):
    import pybullet as p
    p.changeVisualShape(marker_id, -1, rgbaColor=color)