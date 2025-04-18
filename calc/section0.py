#calc/secion0.py

from calc.coolprop import get_fluid_properties

def section0_calculation(form):
    try:
        components = form.getlist("component")
        mole_fraction = [float(x) for x in form.getlist("mole_fraction")]
        T_c = float(form.get("T"))
        P_bar = float(form.get("P"))

        # 물성치 선택 없이 → 전체 default props
        result = get_fluid_properties(components, mole_fraction, T_c, P_bar)
        return result

    except Exception as e:
        return {"error": f"입력 처리 중 오류 발생: {str(e)}"}