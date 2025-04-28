from calc.section3 import orifice_diameter_newton

target_m_dot = 1.5  # kg/s
D = 0.1             # 관 지름 100 mm
delta_p = 50000     # 차압 50 kPa
rho = 800           # 밀도 800 kg/m3
mu = 0.001          # 점도 0.001 Pa.s

d = orifice_diameter_newton(target_m_dot, D, delta_p, rho, mu)
print(f"계산된 오리피스 지름: {d*1000:.2f} mm")