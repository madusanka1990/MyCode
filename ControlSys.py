# Air Heater System
import numpy as np
import time
import matplotlib.pyplot as plt
from opcua import Client

# Model Parameters
Kh = 3.5
theta_t = 22
theta_d = 2
Tenv = 21.5
# Simulation Parameters
Ts = 0.1 # Sampling Time

# PI Controller Settings
Kp = 0.1
Ti = 30


r = np.array([28.0])
e = np.array([0])
u = np.array([0])
t = np.array([0])
T = np.array([Tenv,Tenv])
Total_Time = 0

#OPC UA Server Simulator from Integration Objects
url = "opc.tcp://Niroshan:49580"

client = Client(url)
client.connect()

# Simulation
for k in range(1,200):
# Controller
    Total_Time = Total_Time + Ts
    t = np.append(t,Total_Time)
    r = np.append(r,28.0)
    e = np.append(e,r[k] - T[k])
    uk = u[k-1] + Kp*(e[k] - e[k-1]) + (Kp/Ti)*e[k] #PI Controller
    u = np.append(u,uk)
    
    if u[k]>5:
        u[k] = 5
    if u[k]<0:
        u[k] = 0
# Process Model
    Tk = T[k] + (Ts/theta_t) * (-T[k] + Kh*u[max(0,int(k-theta_d/Ts))] + Tenv)
    T = np.append(T,Tk)
    print("t = %2.1f, u = %3.2f, T = %3.1f" %(t[k], u[k], T[k+1]))
    
    plt.figure(figsize=(6, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(t,u, '-o', markersize=1, color='red')
    plt.ylim(0, 5)
    plt.title("Control Voltage")
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    
    plt.subplot(2, 1, 2)
    plt.plot(t,T[1:], '*-', label='Output Temperature', markersize=1, color='blue')
    plt.plot(t,r, '*-', label='Set Point',markersize=1, color='green')
    plt.ylim(20, 32)
    plt.title("Temperature")
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [C]')
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()
    
    if k%10==0:
        node1 = client.get_node("ns=2;s=Process Data.FilteredTemperature")
        node1.set_data_value(T[-1])
        node2 = client.get_node("ns=2;s=Process Data.ControlVoltage")
        node2.set_data_value(u[-1])        
        node3 = client.get_node("ns=2;s=Process Data.SetPoint")
        node3.set_data_value(r[-1])
        node4 = client.get_node("ns=2;s=Process Data.AmbientTemperature")
        node4.set_data_value(Tenv)
    time.sleep(Ts)
    
client.disconnect()   
    
