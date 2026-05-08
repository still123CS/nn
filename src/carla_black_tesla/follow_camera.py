import carla
import time

class FollowCamera:
    def __init__(self, world, vehicle):
        self.world = world
        self.vehicle = vehicle
        self.spectator = world.get_spectator()
        self.offset_x = -8.0
        self.offset_z = 5.0
        self.pitch_angle = -15.0
    
    def update(self):
        vehicle_transform = self.vehicle.get_transform()
        
        camera_location = vehicle_transform.location + carla.Location(
            x=self.offset_x,
            z=self.offset_z
        )
        
        camera_rotation = vehicle_transform.rotation
        camera_rotation.pitch = self.pitch_angle
        
        self.spectator.set_transform(carla.Transform(camera_location, camera_rotation))
    
    def run(self, update_interval=0.1):
        try:
            while True:
                self.update()
                time.sleep(update_interval)
        except KeyboardInterrupt:
            pass
