
# 📁 calc/coolprop.py

import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np
import json
from CoolProp.CoolProp import PropsSI

# 물성 설명 로딩
with open('calc/property_map.json', 'r') as f:
    PROPERTY_MAP = json.load(f)

DEFAULT_PROPS = list(PROPERTY_MAP.keys())

# --------------------------------------------------
# 📦 유틸 함수
# --------------------------------------------------
def format_value(prop, value):
    if prop == "T":
        return value - 273.15, "°C"
    elif prop == "P":
        return value / 1e5 - 1, "barG"
    return value, PROPERTY_MAP.get(prop, {}).get("unit", "")

def make_fluid_string(components, mole_fractions):
    if len(components) == 1:
        return f"HEOS::{components[0]}"
    else:
        return "HEOS::" + '&'.join(
            [f"{comp}[{mf}]" for comp, mf in zip(components, mole_fractions)]
        )

# --------------------------------------------------
# ⚙️ 핵심 계산 함수
# --------------------------------------------------
def get_fluid_properties(components: list[str],
                         mole_fractions: list[float],
                         T_c: float,
                         P_bar: float,
                         props: list[str] = None) -> dict:
    try:
        print("📥 [DEBUG] Components:", components)
        print("📥 [DEBUG] Mole Fractions:", mole_fractions)

        if round(sum(mole_fractions), 5) != 1.0:
            return {"error": "몰분율의 합은 반드시 1.0이어야 합니다."}

        fluid = make_fluid_string(components, mole_fractions)
        T_K = T_c + 273.15
        P_Pa = P_bar * 1e5

        print(f"🧪 [DEBUG] Fluid: {fluid}")
        print(f"🌡️ [DEBUG] T(K): {T_K}, P(Pa): {P_Pa}")

        if props is None:
            props = DEFAULT_PROPS

        result = {}

        for prop in props:
            info = PROPERTY_MAP.get(prop, {"name": prop, "unit": ""})
            name = info["name"]
            unit = info.get("unit", "")

            try:
                value = PropsSI(prop, 'T', T_K, 'P', P_Pa, fluid)
                value, unit = format_value(prop, value)
                result[name] = {
                    "value": value,
                    "unit": unit
                }
            except Exception as prop_err:
                result[name] = {
                    "value": f"❌ 계산 불가: {str(prop_err).split(':')[0]}",
                    "unit": unit
                }

        # 📉 상다이어그램 이미지 생성 포함
        phase_img_path = "static/phase_diagram.png"
        generate_phase_diagram(fluid, T_K, P_Pa, save_path=phase_img_path)
        result["__phase_diagram__"] = {"image_path": phase_img_path}

        return result

    except Exception as e:
        print("💥 [DEBUG] Critical failure:", str(e))
        return {"error": f"계산 실패: {str(e)}"}

# --------------------------------------------------
# 📈 상다이어그램 생성 함수
# --------------------------------------------------
def generate_phase_diagram(fluid_string: str, T_input: float, P_input: float, save_path: str = "static/phase_diagram.png"):
    try:
        T_min = max(200, T_input * 0.5)
        T_max = T_input * 1.5
        Ts = np.linspace(T_min, T_max, 500)

        ps = CP.PropsSI('P', 'T', Ts, 'Q', 0, fluid_string)

        try:
            T_crit = CP.PropsSI("Tcrit", fluid_string)
            P_crit = CP.PropsSI("Pcrit", fluid_string)
        except:
            T_crit, P_crit = None, None

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(Ts, ps, 'orange', lw=2, label='Saturation curve')

        if T_crit and P_crit:
            ax.axvline(T_crit, color='blue', linestyle='dashed')
            ax.axhline(P_crit, color='blue', linestyle='dashed')

        ax.plot(T_input, P_input, 'ro', label='Your point')

        ax.set_yscale('log')
        ax.set_xlim(T_min, T_max)
        ax.set_ylim(1e3, 1e8)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Pressure [Pa]')
        ax.set_title('Phase Diagram')
        ax.legend()
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()

        plt.savefig(save_path)
        plt.close()
        return save_path
    except Exception as e:
        print(f"⚠️ Phase diagram generation failed: {e}")
        return None
