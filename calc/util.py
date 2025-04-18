# calc/util.py

def reynolds_number(rho, v, D, mu):
    return (rho * v * D) / mu

def prandtl_number(cp, mu, k):
    return (cp * mu) / k