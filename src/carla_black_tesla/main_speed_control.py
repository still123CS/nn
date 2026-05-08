import carla
import sys
import time

def main():
    print("=" * 60)
    print("CARLA - Black Tesla with Speed Control")
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
        max_speed_kmh = 50
        max_speed_ms = max_speed_kmh / 3.6
        print(f"[INFO] Autopilot enabled (max speed: {max_speed_kmh} km/h)")
        
        print("\n[INFO] Press Ctrl+C to stop")
        try:
            while True:
                velocity = vehicle.get_velocity()
                speed_ms = (velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5
                
                if speed_ms > max_speed_ms:
                    control = vehicle.get_control()
                    control.throttle = 0.0
                    control.brake = 0.3
                    vehicle.apply_control(control)
                
                speed_kmh = speed_ms * 3.6
                print(f"[INFO] Speed: {speed_kmh:.1f} km/h", end="\r")
                time.sleep(0.1)
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
