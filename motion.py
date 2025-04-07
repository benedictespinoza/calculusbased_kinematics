import machine
import time

PIR_PIN = 14
DETECTION_ZONE_WIDTH = 1.0
pir = machine.Pin(PIR_PIN, machine.Pin.IN)

def read_pir_sensor():
    """returns true if motion is detected, else false."""
    return pir.value() == 1

def measure_motion():
    """first waits for motion to be detected, then measures the duration of the motion, returns the time interval."""
    print("Waiting for motion...")
    while not read_pir_sensor():
        time.sleep(0.1)
    start_time = time.ticks_ms()
    print("Motion detected! Measuring duration...")
    while read_pir_sensor():
        time.sleep(0.1)
    stop_time = time.ticks_ms()
    time_interval = time.ticks_diff(stop_time, start_time) / 1000.0
    return time_interval

def simulate_velocity_profile(time_interval, num_samples=11):
    """simulates a triangular velocity profile over the motion interval. Returns lists of time samples and corresponding velocity samples."""

    T = time_interval
    times = []
    velocities = []
    for i in range(num_samples):
        t = T * i / (num_samples - 1)
        if t <= T / 2:
            v = 4 * DETECTION_ZONE_WIDTH * t / (T ** 2)
        else:
            v = 4 * DETECTION_ZONE_WIDTH * (T - t) / (T ** 2)
        times.append(t)
        velocities.append(v)
    return times, velocities

def calculate_kinematics(time_samples, velocity_samples):
    """calculates kinematic metrics. returns average velocity (m/s), displacement (m), and average acceleration (m/s²).
    for displacement, attempts to get best approximation using Simpson's rule."""

    n = len(time_samples)
    if n < 3 or len(velocity_samples) < 3:
        return 0, 0, 0
    total_time = time_samples[-1] - time_samples[0]
    if total_time <= 0:
        return 0, 0, 0
    if n % 2 == 1:
        h = (time_samples[-1] - time_samples[0]) / (n - 1)
        simpson_sum = velocity_samples[0] + velocity_samples[-1]
        for i in range(1, n - 1):
            coef = 4 if i % 2 == 1 else 2
            simpson_sum += coef * velocity_samples[i]
        displacement = (h / 3) * simpson_sum
    else:
        n_simpson = n - 1
        h_simpson = (time_samples[n_simpson - 1] - time_samples[0]) / (n_simpson - 1)
        simpson_sum = velocity_samples[0] + velocity_samples[n_simpson - 1]
        for i in range(1, n_simpson - 1):
            coef = 4 if i % 2 == 1 else 2
            simpson_sum += coef * velocity_samples[i]
        displacement_simpson = (h_simpson / 3) * simpson_sum
        h_last = time_samples[-1] - time_samples[-2]
        displacement_last = (velocity_samples[-2] + velocity_samples[-1]) * h_last / 2
        displacement = displacement_simpson + displacement_last
    avg_velocity = displacement / total_time
    avg_acceleration = (velocity_samples[-1] - velocity_samples[0]) / total_time
    return avg_velocity, displacement, avg_acceleration

def visualize_data(velocity, displacement, acceleration, time_interval):
    """Prints kinematic results: time interval, average velocity, displacement, and average acceleration."""
    print("\n--- Motion Analysis Results ---")
    print("Time Interval: {:.2f} s".format(time_interval))
    print("Average Velocity: {:.2f} m/s".format(velocity))
    print("Displacement: {:.2f} m".format(displacement))
    print("Average Acceleration: {:.2f} m/s²".format(acceleration))
    print("--------------------------------\n")

def main():
    print("Kinematic Physics Project with PIR Sensor on Raspberry Pi (MicroPython)")
    print("Press Ctrl+C to exit.\n")
    while True:
        try:
            t_interval = measure_motion()
            time_samples, velocity_samples = simulate_velocity_profile(t_interval)
            avg_velocity, displacement, avg_acceleration = calculate_kinematics(time_samples, velocity_samples)
            visualize_data(avg_velocity, displacement, avg_acceleration, t_interval)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
