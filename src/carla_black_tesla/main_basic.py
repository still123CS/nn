import carla
import sys
import time

def main():
    print("=" * 60)
    print("CARLA - Black Tesla Basic Version")
    print("=" * 60)
    
    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        print("[INFO] Connected to CARLA server")
        
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        
        tesla_bp = blueprint_library.find("vehicle.tesla.model3")
        tesla_bp.set_attribute("color", "0, 0, 0")
        
        spawn_points = world.get_map().get_spawn_points()
        
        vehicle = None
        for i, spawn_point in enumerate(spawn_points[:5]):
            try:
                vehicle = world.spawn_actor(tesla_bp, spawn_point)
                print(f"[SUCCESS] Black Tesla spawned at point {i}!")
                break
            except RuntimeError as e:
                if "collision" in str(e).lower():
                    continue
                else:
                    raise
        
        if vehicle is None:
            print("[ERROR] Failed to spawn vehicle")
            return
        
        vehicle.set_autopilot(True)
        print("[INFO] Autopilot enabled")
        
        print("\n[INFO] Press Ctrl+C to stop")
        try:
            while True:
                velocity = vehicle.get_velocity()
                speed = ((velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5) * 3.6
                print(f"[INFO] Speed: {speed:.1f} km/h", end="\r")
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
