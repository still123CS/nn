import carla
import sys
import time

def main():
    print("=" * 60)
    print("CARLA - Black Tesla Weather Control")
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

        weather_index = 0
        weather_list = [
            ("Clear Noon", {"sun_altitude_angle": 70, "cloudiness": 0, "precipitation": 0, "fog_distance": 0}),
            ("Cloudy", {"sun_altitude_angle": 50, "cloudiness": 50, "precipitation": 0, "fog_distance": 0}),
            ("Rain", {"sun_altitude_angle": 30, "cloudiness": 80, "precipitation": 50, "fog_distance": 0}),
            ("Heavy Rain", {"sun_altitude_angle": 20, "cloudiness": 100, "precipitation": 100, "fog_distance": 0}),
            ("Fog", {"sun_altitude_angle": 10, "cloudiness": 50, "precipitation": 0, "fog_distance": 30}),
            ("Sunset", {"sun_altitude_angle": -10, "cloudiness": 20, "precipitation": 0, "fog_distance": 0}),
        ]

        print("\n[INFO] Weather will change every 5 seconds:")
        for i, (name, _) in enumerate(weather_list):
            print(f"  {i + 1}. {name}")

        current = weather_list[0]
        weather = carla.WeatherParameters()
        weather.sun_altitude_angle = current[1]["sun_altitude_angle"]
        weather.cloudiness = current[1]["cloudiness"]
        weather.precipitation = current[1]["precipitation"]
        weather.fog_distance = current[1]["fog_distance"]
        world.set_weather(weather)
        print(f"\n[INFO] Current weather: {current[0]}")

        print("\n[INFO] Press Ctrl+C to stop")
        try:
            while True:
                weather_index = (weather_index + 1) % len(weather_list)
                name, params = weather_list[weather_index]

                weather = carla.WeatherParameters()
                weather.sun_altitude_angle = params["sun_altitude_angle"]
                weather.cloudiness = params["cloudiness"]
                weather.precipitation = params["precipitation"]
                weather.fog_distance = params["fog_distance"]
                world.set_weather(weather)

                print(f"\n[WEATHER] Changed to: {name}")

                velocity = vehicle.get_velocity()
                speed = ((velocity.x**2 + velocity.y**2 + velocity.z**2) ** 0.5) * 3.6
                print(f"[INFO] Speed: {speed:.1f} km/h", end="\r")

                time.sleep(5)

        except KeyboardInterrupt:
            print("\n[INFO] User interrupted")
        finally:
            if vehicle.is_alive:
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
