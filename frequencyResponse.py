import numpy as np
import matplotlib.pyplot as plt
import control
# Process Parameters
Kh = 3.5
theta_t = 22
theta_d = 2
# Transfer Function Process
num_p = np. array ([Kh])
den_p = np. array ([theta_t , 1])
Hp1 = control.tf(num_p , den_p)
#print ('Hp1(s) =', Hp1)
N = 5 # Time Delay - Order of the Approximation
[num_pade,den_pade] = control.pade(theta_d, N)
Hp_pade = control.tf(num_pade,den_pade);
#print ('Hp_pade(s) =', Hp_pade)
Hp = control.series(Hp1, Hp_pade);
#print ('Hp(s) =', Hp)
# Transfer Function PI Controller
Kp = 2
Ti = 16
num_c = np.array ([Kp*Ti, Kp])
den_c = np.array ([Ti , 0])
Hc = control.tf(num_c, den_c)
print ('Hc(s) =', Hc)
# The Loop Transfer function
L = control.series(Hc, Hp)
print ('L(s) =', L)
# Tracking transfer function
T = control.feedback(L,1)
print ('T(s) =', T)
# Sensitivity transfer function
S = 1 - T
print ('S(s) =', S)

# Step Response Feedback System (Tracking System)
t, y = control.step_response(T)
plt.figure(1)
plt.plot(t,y)
plt.title("Step Response Feedback System T(s)")
plt.grid()
# Bode Diagram with Stability Margins
plt.figure(2)
control.bode(L, dB=True, deg=True, margins=True)

# Poles and Zeros
plt.figure(3)
control.pzmap(T)
p = control.poles(T)
z = control.zeros(T)
print("poles = ", p)
# Calculating stability margins and crossover frequencies
gm , pm , w180 , wc = control.margin(L)
# Convert gm to Decibel
gmdb = 20 * np.log10(gm)
print("wc =", f'{wc:.2f}', "rad/s")
print("w180 =", f'{w180:.2f}', "rad/s")
print("GM =", f'{gm:.2f}')
print("GM =", f'{gmdb:.2f}', "dB")
print("PM =", f'{pm:.2f}', "deg")
# Find when Sysem is Marginally Stable (Kritical Gain - Kc)
Kc = Kp*gm
print("Kc=", f'{Kc:.2f}')
