import carla
import sys
import time
import math

def main():
    print("=" * 60)
    print("CARLA - Black Tesla with Follow Camera")
    print("=" * 60)

    try:
        client = carla.Client("localhost", 2000)
        client.set_timeout(10.0)
        print("[INFO] Connected to CARLA server")

        world = client.get_world()
        blueprint_library = world.get_blueprint_library()
        spectator = world.get_spectator()

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
        print("[INFO] Follow camera enabled")

        print("\n[INFO] Press Ctrl+C to stop")
        try:
            last_time = time.time()
            while True:
                current_time = time.time()
                if current_time - last_time < 0.02:
                    continue
                last_time = current_time

                if not vehicle.is_alive:
                    print("\n[ERROR] Vehicle is not alive")
                    break

                vehicle_transform = vehicle.get_transform()
                vehicle_location = vehicle_transform.location
                yaw_deg = vehicle_transform.rotation.yaw
                yaw_rad = math.radians(yaw_deg)

                camera_offset_x = -8.0
                camera_offset_z = 5.0

                camera_x = vehicle_location.x + camera_offset_x * math.cos(yaw_rad)
                camera_y = vehicle_location.y + camera_offset_x * math.sin(yaw_rad)
                camera_z = vehicle_location.z + camera_offset_z

                camera_location = carla.Location(x=camera_x, y=camera_y, z=camera_z)
                camera_rotation = carla.Rotation(pitch=-15.0, yaw=yaw_deg, roll=0.0)

                spectator.set_transform(carla.Transform(camera_location, camera_rotation))

        except KeyboardInterrupt:
            print("\n[INFO] User interrupted")
        finally:
            if vehicle and vehicle.is_alive:
                vehicle.destroy()
                print("[INFO] Vehicle destroyed")

    except RuntimeError as e:
        print(f"[ERROR] {e}")
        print("[INFO] Make sure CarlaUE4.exe is running")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
