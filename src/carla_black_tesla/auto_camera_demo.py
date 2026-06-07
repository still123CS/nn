"""
CARLA - Auto camera tracking demo
"""
import carla
import sys
import time


class AutoCamera:
    """Automatically make your CARLA view follow the vehicle"""
    
    def __init__(self, world, vehicle):
        self.world = world
        self.vehicle = vehicle
        self.spectator = world.get_spectator()
        
    def follow_vehicle(self, mode="third_person"):
        """Update your view to follow the vehicle
        
        Args:
            mode: "third_person" (default), "first_person", "top_down", or "chase"
        """
        vehicle_transform = self.vehicle.get_transform()
        
        if mode == "third_person":
            spectator_location = (
                vehicle_transform.location + 
                vehicle_transform.get_forward_vector() * -6.0 + 
                carla.Location(z=3.5)
            )
            spectator_rotation = carla.Rotation(
                pitch=vehicle_transform.rotation.pitch - 12.0,
                yaw=vehicle_transform.rotation.yaw,
                roll=vehicle_transform.rotation.roll
            )
        elif mode == "first_person":
            spectator_location = (
                vehicle_transform.location + 
                vehicle_transform.get_forward_vector() * 1.5 + 
                carla.Location(z=1.3)
            )
            spectator_rotation = carla.Rotation(
                pitch=vehicle_transform.rotation.pitch,
                yaw=vehicle_transform.rotation.yaw,
                roll=vehicle_transform.rotation.roll
            )
        elif mode == "top_down":
            spectator_location = vehicle_transform.location + carla.Location(z=25.0)
            spectator_rotation = carla.Rotation(pitch=-90.0, yaw=vehicle_transform.rotation.yaw)
        elif mode == "chase":
            spectator_location = (
                vehicle_transform.location + 
                vehicle_transform.get_forward_vector() * -3.5 + 
                carla.Location(z=2.0)
            )
            spectator_rotation = carla.Rotation(
                pitch=vehicle_transform.rotation.pitch - 8.0,
                yaw=vehicle_transform.rotation.yaw,
                roll=vehicle_transform.rotation.roll
            )
        else:
            spectator_location = (
                vehicle_transform.location + 
                vehicle_transform.get_forward_vector() * -6.0 + 
                carla.Location(z=3.5)
            )
            spectator_rotation = carla.Rotation(
                pitch=vehicle_transform.rotation.pitch - 12.0,
                yaw=vehicle_transform.rotation.yaw,
                roll=vehicle_transform.rotation.roll
            )
        
        spectator_transform = carla.Transform(spectator_location, spectator_rotation)
        self.spectator.set_transform(spectator_transform)


def main():
    print("=" * 60)
    print("CARLA - Auto Camera Tracking Demo")
    print("=" * 60)
    
    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        print("[INFO] Connected to CARLA server successfully")
        
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        
        tesla_bp = blueprint_library.find("vehicle.tesla.model3")
        tesla_bp.set_attribute("color", "0, 0, 0")
        
        spawn_points = world.get_map().get_spawn_points()
        
        if len(spawn_points) == 0:
            print("[ERROR] No spawn points available on the map")
            return
        
        vehicle = None
        for i, spawn_point in enumerate(spawn_points[:5]):
            try:
                vehicle = world.spawn_actor(tesla_bp, spawn_point)
                print(f"[SUCCESS] Black Tesla Model 3 spawned at spawn point {i}!")
                break
            except RuntimeError as e:
                if "collision" in str(e).lower():
                    continue
                raise
        
        if vehicle is None:
            print("[ERROR] Failed to spawn vehicle")
            return
        
        vehicle.set_autopilot(True)
        print("[INFO] Autopilot enabled")
        
        auto_camera = AutoCamera(world, vehicle)
        print("[INFO] Auto camera tracking enabled - your view follows the car!")
        print("\n[INFO] Press Ctrl+C to stop and cleanup")
        
        try:
            while True:
                auto_camera.follow_vehicle(mode="third_person")
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\n[INFO] User interrupted the program")
        finally:
            print("[INFO] Cleaning up...")
            vehicle.destroy()
            print("[INFO] Vehicle destroyed successfully")
            
    except RuntimeError as e:
        print(f"[ERROR] Runtime error: {e}")
        print("[INFO] Make sure CARLA server (CarlaUE4.exe) is running")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
