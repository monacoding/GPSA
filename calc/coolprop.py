# 📁 calc/coolprop.py

import CoolProp.CoolProp as CP
import json
from CoolProp.CoolProp import PropsSI

# 물성 설명 로딩
with open('calc/property_map.json', 'r') as f:
    PROPERTY_MAP = json.load(f)

DEFAULT_PROPS = list(PROPERTY_MAP.keys())

# Property 계산 
# 📁 calc/coolprop.py

def get_fluid_properties(components: list[str],
                         mole_fractions: list[float],
                         T_c: float,
                         P_bar: float,
                         props: list[str] = None) -> dict:

    try:
        if round(sum(mole_fractions), 5) != 1.0:
            return {"error": "몰분율의 합은 반드시 1.0이어야 합니다."}

        fluid = f"{'&'.join(components)}[{ '&'.join(map(str, mole_fractions)) }]"
        T_K = T_c + 273.15
        P_Pa = P_bar * 1e5

        if props is None:
            props = list(PROPERTY_MAP.keys())

        result = {}

        for prop in props:
            info = PROPERTY_MAP.get(prop, {"name": prop, "unit": ""})
            name = info["name"]
            unit = info.get("unit", "")
            
            try:
                value = PropsSI(prop, 'T', T_K, 'P', P_Pa, fluid)
                result[name] = {
                    "value" :value,
                    "unit" : unit
                }
            except Exception as prop_err:
                result[name] = {
                    "value" : f"❌ 계산 불가: {str(prop_err).split(':')[0]}",
                    "unit" : unit }

        return result

    except Exception as e:
        return {"error": f"계산 실패: {str(e)}"}