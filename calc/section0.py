#calc/secion0.py

from calc.coolprop import get_fluid_properties

def section0_calculation(form) :
    """
    Section 0: 구성성분 + 몰분율 + T, P + 물성치 선택 → 계산 실행
    - form: request.form (Flask의 POST 데이터)
    """
    
    try : 
        #1. 성분 및 몰분율 리스트 받아오기
        components = form.getlist("component")
        mole_fractions = [float(x) for x in form.getlist("mole_fraction")]
        
        #2. 온도, 업력
        T_c = float(form.get("T"))
        P_bar = float(form.get("P"))
        
        #3. 물성치 선택
        props = form.getlist("properties") 
        
        #. Coolporop 연동
        result = get_fluid_properties(components, mole_fractions, T_c, P_bar, props)
        
        return result
    except Exception as e:
        return {"error": f"입력 처리 중 오류 발생: {str(e)}"}