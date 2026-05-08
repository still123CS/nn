import carla
import sys
import time

def main():
    print("=" * 60)
    print("CARLA Spawn Tesla Vehicle")
    print("=" * 60)
    
    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        print("[INFO] Connected to CARLA server")
        
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        
        tesla_bp = blueprint_library.find("vehicle.tesla.model3")
        tesla_bp.set_attribute("color", "255, 255, 255")
        
        spawn_points = world.get_map().get_spawn_points()
        
        if len(spawn_points) == 0:
            print("[ERROR] No spawn points available")
            return
        
        vehicle = world.spawn_actor(tesla_bp, spawn_points[0])
        print(f"[SUCCESS] Tesla Model 3 spawned! ID: {vehicle.id}")
        print(f"[INFO] Location: ({spawn_points[0].location.x:.2f}, {spawn_points[0].location.y:.2f}, {spawn_points[0].location.z:.2f})")
        
        vehicle.set_autopilot(True)
        print("[INFO] Autopilot enabled")
        
        try:
            while True:
                location = vehicle.get_location()
                velocity = vehicle.get_velocity()
                speed = ((velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5) * 3.6
                print(f"[INFO] Speed: {speed:.1f} km/h | Location: ({location.x:.1f}, {location.y:.1f})", end="\r")
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[INFO] User interrupted")
        finally:
            vehicle.destroy()
            print("[INFO] Vehicle destroyed")
            
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        print("[INFO] Make sure CarlaUE4.exe is running")
        sys.exit(1)

if __name__ == "__main__":
    main()
