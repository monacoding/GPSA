# 📁 calc/coolprop.py
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 방지
import matplotlib.pyplot as plt
import numpy as np
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI
import base64
from io import BytesIO
import json

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
        return value / 1e5 - 1.013, "barG"
    return value, PROPERTY_MAP.get(prop, {}).get("unit", "")

def make_fluid_string(components, mole_fractions):
    if len(components) == 1:
        return f"HEOS::{components[0]}"
    else:
        return "HEOS::" + '&'.join(
            [f"{comp}[{mf}]" for comp, mf in zip(components, mole_fractions)]
        )

# --------------------------------------------------
# ⚙️ 물성치 계산 함수
# --------------------------------------------------
def get_fluid_properties(components, mole_fractions, T_c, P_bar, props=None):
    try:
        if round(sum(mole_fractions), 5) != 1.0:
            return {"error": "몰분율의 합은 반드시 1.0이어야 합니다."}

        fluid = make_fluid_string(components, mole_fractions)
        T_K = T_c + 273.15
        P_Pa = (P_bar + 1.013) * 1e5  # barG → Pa

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
                result[name] = {"value": value, "unit": unit}
            except Exception as prop_err:
                result[name] = {
                    "value": f"❌ 계산 불가: {str(prop_err).split(':')[0]}",
                    "unit": unit
                }

        # 📈 상다이어그램 생성 (내부에서 fluid, T_K, P_Pa 사용)
        image_base64 = _generate_phase_diagram_internal(fluid, T_K, P_Pa)
        if image_base64:
            result["__phase_diagram__"] = {"image_base64": image_base64}

        return result

    except Exception as e:
        return {"error": f"계산 실패: {str(e)}"}

# --------------------------------------------------
# 📈 상다이어그램 내부 전용 함수
# --------------------------------------------------
def _generate_phase_diagram_internal(fluid_string, T_K, P_Pa):
    try:
        T_min = max(200, T_K * 0.5)
        T_max = T_K * 1.5
        Ts = np.linspace(T_min, T_max, 500)

        ps = CP.PropsSI('P', 'T', Ts, 'Q', 0, fluid_string)
        ps_barG = ps / 1e5 - 1.013
        Ts_C = Ts - 273.15

        # 👉 유효한 데이터만 남기기
        valid = ~np.isnan(ps_barG)
        ps_barG = ps_barG[valid]
        Ts_C = Ts_C[valid]

        if len(ps_barG) == 0 or len(Ts_C) == 0:
            raise ValueError("유효한 상곡선 데이터가 없습니다.")

        # 임계점
        try:
            T_crit = CP.PropsSI("Tcrit", fluid_string) - 273.15
            P_crit = CP.PropsSI("Pcrit", fluid_string) / 1e5 - 1.013
        except:
            T_crit, P_crit = None, None

        T_C = T_K - 273.15
        P_barG = P_Pa / 1e5 - 1.013

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot(Ts_C, ps_barG, 'orange', lw=2, label='Saturation curve')

        if T_crit and P_crit:
            ax.axvline(T_crit, color='blue', linestyle='dashed')
            ax.axhline(P_crit, color='blue', linestyle='dashed')

        ax.plot(T_C, P_barG, 'ro', label='Your point')
        ax.set_yscale('linear')
        ax.set_xlim(min(Ts_C), max(Ts_C))
        ax.set_ylim(min(ps_barG), max(ps_barG))
        ax.set_xlabel('Temperature [°C]')
        ax.set_ylabel('Pressure [barG]')
        ax.set_title('Phase Diagram')
        ax.legend()
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        return f"data:image/png;base64,{base64.b64encode(buf.read()).decode('utf-8')}"

    except Exception as e:
        print("⚠️ Phase diagram 오류:", str(e))
        return None