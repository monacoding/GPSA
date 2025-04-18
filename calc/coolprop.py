# 📁 calc/coolprop.py

import CoolProp.CoolProp as CP
import json
from CoolProp.CoolProp import PropsSI

# 물성 설명 로딩
with open('calc/property_map.json', 'r') as f:
    PROPERTY_MAP = json.load(f)

DEFAULT_PROPS = list(PROPERTY_MAP.keys())

# Property 계산 
def get_fluid_properties(components: list[str], 
                         mole_fractions: list[float],
                         T_c: float, 
                         P_bar: float, 
                         props: list[str] = None) -> dict:
    """
    단일 또는 혼합 유체의 PropsSI 기반 물성 계산

    :param components: ["Methane"] 또는 ["Methane", "Ethane"]
    :param mole_fractions: [1.0] 또는 [0.6, 0.4] (합이 1.0 이어야 함)
    :param T_c: 온도 (°C)
    :param P_bar: 압력 (bar)
    :param props: 계산할 물성 리스트. None이면 DEFAULT_PROPS 사용
    :return: {설명: 값} 또는 {"error": str}
    """
    try:
        
        if round(sum(mole_fractions), 5) != 1.0:
            return {"error": "몰분율의 합은 반드시 1.0이어야 합니다."}

        # CoolProp 혼합물 형식 문자열 생성
        fluid = f"{'&'.join(components)}[{ '&'.join(map(str, mole_fractions)) }]"

        # 단위 변환
        T_K = T_c + 273.15
        P_Pa = P_bar * 1e5

        if props is None:
            props = DEFAULT_PROPS

        result = {}
        for prop in props:
            value = PropsSI(prop, 'T', T_K, 'P', P_Pa, fluid)
            desc = PROPERTY_MAP.get(prop, prop)
            result[desc] = value

        return result

    except Exception as e:
        return {"error": f"계산 실패: {str(e)}"}