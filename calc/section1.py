# calc/section1.py

from calc.util import reynolds_number

def calculate_section1(params: dict):
    """
    params: {
        'rho': ..., 'v': ..., 'D': ..., 'mu': ...
    }
    """
    try:
        rho = float(params['rho'])
        v = float(params['v'])
        D = float(params['D'])
        mu = float(params['mu'])
        Re = reynolds_number(rho, v, D, mu)
        return {"Re": Re}
    except (KeyError, ValueError):
        return {"error": "입력값이 올바르지 않습니다."}