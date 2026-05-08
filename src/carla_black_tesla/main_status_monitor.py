import carla
import sys
import time

def main():
    print("=" * 60)
    print("CARLA - Black Tesla Status Monitor")
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
        print("[INFO] Status monitor enabled")
        
        print("\n" + "=" * 60)
        try:
            while True:
                location = vehicle.get_location()
                velocity = vehicle.get_velocity()
                acceleration = vehicle.get_acceleration()
                control = vehicle.get_control()
                
                speed = ((velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5) * 3.6
                
                print("\033[H\033[J", end="")
                print("=" * 60)
                print("CARLA - Black Tesla Status Monitor")
                print("=" * 60)
                print(f"[LOCATION] X: {location.x:>6.1f}  Y: {location.y:>6.1f}  Z: {location.z:>6.1f}")
                print(f"[VELOCITY] X: {velocity.x:>6.2f}  Y: {velocity.y:>6.2f}  Z: {velocity.z:>6.2f}")
                print(f"[SPEED]    {speed:>6.1f} km/h")
                print("-" * 60)
                print(f"[CONTROL] Throttle: {control.throttle:>5.2f}")
                print(f"          Brake:    {control.brake:>5.2f}")
                print(f"          Steer:    {control.steer:>5.2f}")
                print(f"          Reverse:  {control.reverse}")
                print(f"          Handbrake:{control.hand_brake}")
                print("-" * 60)
                print(f"[ACCEL]    X: {acceleration.x:>6.2f}  Y: {acceleration.y:>6.2f}  Z: {acceleration.z:>6.2f}")
                print("=" * 60)
                print("Press Ctrl+C to exit")
                
                time.sleep(0.2)
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
