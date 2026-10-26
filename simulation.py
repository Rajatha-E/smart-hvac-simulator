import time
import pandas as pd

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, setpoint, current_value, dt=1.0):
        error = setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        
        # Outputs a control value clamped between 0 and 100%
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        return max(0.0, min(100.0, output))

def run_simulation(target_temp=21.0, cycles=20):
    pid = PIDController(kp=2.0, ki=0.1, kd=0.05)
    current_temp = 28.0  # Starting room temp
    humidity = 60.0
    
    log_data = []
    
    print("====== SMART HVAC & THERMAL REGULATION SIMULATOR ======")
    for cycle in range(1, cycles + 1):
        # Compute PID output for compressor/fan load (0 to 100%)
        control_output = pid.compute(target_temp, current_temp)
        
        # Simulate physical temperature decay based on control output
        temp_drop = (control_output / 100.0) * 0.5
        current_temp = max(target_temp, current_temp - temp_drop + 0.05) # slight ambient drift
        humidity = max(40.0, humidity - (temp_drop * 0.2))
        
        fan_rpm = int(1800 + (control_output * 12))
        compressor_status = "HIGH" if control_output > 50 else ("ECO" if control_output > 0 else "OFF")
        
        # Log entry
        row = {
            "Cycle": cycle,
            "Temp": round(current_temp, 2),
            "Humidity": round(humidity, 2),
            "Fan": fan_rpm,
            "Compressor": compressor_status
        }
        log_data.append(row)
        print(f"[Cycle {cycle:02d}] Temp: {current_temp:.2f}°C | Humidity: {humidity:.2f}% | Fan: {fan_rpm} RPM | Compressor: {compressor_status}")
        
        time.sleep(0.1)
        
    # Save telemetry log
    df = pd.DataFrame(log_data)
    df.to_csv("hvac_telemetry_log.csv", index=False)
    print("\nSimulation complete. Telemetry logged to hvac_telemetry_log.csv")
    return df

if __name__ == "__main__":
    run_simulation()