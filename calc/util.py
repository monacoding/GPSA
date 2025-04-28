# calc/util.py

import math

# ✅ 레이놀즈수
def reynolds_number(rho, v, D, mu):
    return (rho * v * D) / mu

# ✅ 프란틀수
def prandtl_number(cp, mu, k):
    return (cp * mu) / k

# ✅ 단면적
def area(d):
    return math.pi * (d / 2) ** 2

# ✅ β 비율 (d/D)
def beta_ratio(d, D):
    return d / D

# ✅ CoolProp용 유체 스트링 생성
def make_fluid_string(components, mole_fractions):
    if len(components) == 1:
        return f"HEOS::{components[0]}"
    else:
        return "HEOS::" + '&'.join(
            [f"{comp}[{mf}]" for comp, mf in zip(components, mole_fractions)]
        )