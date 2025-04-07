import machine
import time
import math

def read_pendulum_sensor():
    """
    placeholder, difficult to implement without a real sensor, PIR dificult to implement?
    """
    current_time = time.ticks_ms() / 1000.0  
    angle = 30 * math.sin(2 * math.pi * current_time / 2)
    return angle

def track_pendulum():
    """
    tracks a pendulum’s motion, calculates its period and maximum amplitude for each oscillation.
    """
    print("Tracking pendulum motion... Press Ctrl+C to exit.")
    equilibrium_threshold = 5   
    last_equilibrium_time = None
    current_max_amplitude = 0
    current_direction = None   
    try:
        while True:
            current_angle = read_pendulum_sensor()
            current_time = time.ticks_ms()  
            
            new_direction = 1 if current_angle >= 0 else -1
            
            if abs(current_angle) > current_max_amplitude:
                current_max_amplitude = abs(current_angle)
            
            if abs(current_angle) < equilibrium_threshold:
                if current_direction is None:
                    current_direction = new_direction
                    last_equilibrium_time = current_time
                elif new_direction != current_direction:
                    period = time.ticks_diff(current_time, last_equilibrium_time) / 1000.0
                    print("Period: {:.2f} s | Amplitude: {:.2f}°".format(period, current_max_amplitude))
                    
                    last_equilibrium_time = current_time
                    current_max_amplitude = 0
                    current_direction = new_direction
            
            time.sleep(0.05)  # sampling rate, variable

    except KeyboardInterrupt:
        print("Exiting pendulum tracking.")

def main():
    print("Kinematic Physics Project: Pendulum Tracking")
    print("This project measures the period and amplitude of a pendulum's motion in real time.")
    print("Press Ctrl+C to exit.\n")
    
    track_pendulum()

if __name__ == "__main__":
    main()
