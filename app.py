import streamlit as st
import pandas as pd
import time

st.title("🌡️ Smart HVAC & Thermal Regulation Dashboard")
st.write("Real-time telemetry and PID-controlled thermal regulation simulator.")

# Sidebar controls
target_temp = st.sidebar.slider("Target Temperature Setpoint (°C)", 15.0, 30.0, 21.0)
simulation_speed = st.sidebar.slider("Simulation Step Delay (s)", 0.05, 0.5, 0.1)

if st.button("🚀 Run Live Simulation"):
    metric_placeholder = st.empty()
    chart_placeholder = st.empty()
    
    current_temp = 28.0
    humidity = 60.0
    data = []
    
    for cycle in range(1, 25):
        # Quick simulation step for the dashboard UI
        current_temp = max(target_temp, current_temp - 0.3)
        humidity = max(40.0, humidity - 0.2)
        fan_rpm = 3000 if current_temp > target_temp else 1800
        
        data.append({"Cycle": cycle, "Temp": current_temp, "Humidity": humidity, "Fan RPM": fan_rpm})
        df = pd.DataFrame(data)
        
        # Update metrics and live charts on the page
        metric_placeholder.metric(
            label="Current Room Temperature", 
            value=f"{current_temp:.2f} °C", 
            delta=f"{target_temp - current_temp:.2f} °C to target"
        )
        chart_placeholder.line_chart(df.set_index("Cycle")[["Temp", "Humidity"]])
        
        time.sleep(simulation_speed)
    
    st.success("Simulation finished successfully!")