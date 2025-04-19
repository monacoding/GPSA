#calc/secion0.py
import json
from calc.coolprop import get_fluid_properties
with open('calc/property_map.json', 'r') as f:
    PROPERTY_MAP = json.load(f)
    
    

def section0_calculation(form):
    try:
        components = form.getlist("component")
        mole_fractions = [float(x) for x in form.getlist("mole_fraction")]
        T_c = float(form.get("T"))
        P_bar = float(form.get("P"))

        return get_fluid_properties(components, mole_fractions, T_c, P_bar)

    except Exception as e:
        return {"error": f"입력 처리 중 오류 발생: {str(e)}"}