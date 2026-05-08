import carla
import time

class SpeedController:
    def __init__(self, vehicle, max_speed_kmh=50):
        self.vehicle = vehicle
        self.max_speed_kmh = max_speed_kmh
        self.max_speed_ms = max_speed_kmh / 3.6
    
    def get_current_speed(self):
        velocity = self.vehicle.get_velocity()
        speed_ms = (velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5
        return speed_ms * 3.6
    
    def set_max_speed(self, max_speed_kmh):
        self.max_speed_kmh = max_speed_kmh
        self.max_speed_ms = max_speed_kmh / 3.6
    
    def control_speed(self):
        current_speed = self.vehicle.get_velocity()
        speed_ms = (current_speed.x**2 + current_speed.y**2 + current_speed.z**2) ** 0.5
        
        if speed_ms > self.max_speed_ms:
            control = self.vehicle.get_control()
            control.throttle = 0.0
            control.brake = 0.3
            self.vehicle.apply_control(control)
            return True
        else:
            return False
    
    def run(self, interval=0.1):
        try:
            while True:
                self.control_speed()
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
