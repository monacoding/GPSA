# 📁 calc/section3.py

import math
from calc.util import reynolds_number, area, beta_ratio, make_fluid_string
import CoolProp.CoolProp as CP

# ✅ CoolProp 기반 물성 계산
def get_density_viscosity(components, mole_fractions, T_C, P_barG):
    fluid = make_fluid_string(components, mole_fractions)
    T_K = T_C + 273.15
    P_Pa = (P_barG + 1.013) * 1e5  # barG → Pa 변환

    rho = CP.PropsSI('D', 'T', T_K, 'P', P_Pa, fluid)  # 밀도 [kg/m³]
    mu = CP.PropsSI('V', 'T', T_K, 'P', P_Pa, fluid)   # 점도 [Pa·s]
    return rho, mu

# ✅ 디스차지 계수 계산 (정식 식)
def discharge_coefficient(beta, Re_D):
    A = (19000 * beta / Re_D) ** 0.8
    C = (0.5961 
         + 0.0261 * beta**2 
         - 0.216 * beta**8 
         + 0.000521 * (10**6 / Re_D)**0.7 
         + (0.0188 + 0.0063*A) * beta**3.5 * (10**6 / Re_D)**0.3
         + (0.043 + 0.08 * math.exp(-10 * 2.2*beta))
         * (1 - 0.123 * math.exp(-7 * 0.5*(10**6/Re_D)))
         * (1 - 0.11 * math.exp(-12 * 0.5*(10**6/Re_D)))
    )
    return C

# ✅ 오리피스 직경 계산 (Newton-Raphson)
def orifice_diameter_newton(m_dot_target, D, delta_p, rho, mu, tol=1e-6, max_iter=50):
    d = D * 0.5  # 초기값: 내경의 절반
    for _ in range(max_iter):
        beta = d / D
        Re_D = (4 * m_dot_target) / (math.pi * d * mu)
        C = discharge_coefficient(beta, Re_D)
        A = math.pi * (d**2) / 4
        m_dot_calc = C * A * math.sqrt(2 * delta_p * rho / (1 - beta**4))
        
        f = m_dot_calc - m_dot_target
        df_dd = (
            (C * math.pi * d / 2) * math.sqrt(2 * delta_p * rho / (1 - beta**4))
            + (C * A * 2 * beta**3 / (D * (1 - beta**4)**1.5)) * math.sqrt(2 * delta_p * rho)
        )
        d_new = d - f / df_dd

        if abs(d_new - d) < tol:
            break
        d = d_new
    return d  # [m]