from flask import Blueprint, render_template, request
import math
import CoolProp.CoolProp as CP
from calc import section0, section3  # 물성 계산 모듈
section = Blueprint('section', __name__, template_folder='../templates')

@section.route('/section/0', methods=['GET', 'POST'])  # SECTION0 물성치 확인
def section0_route():
    result = None  # 계산 결과 초기화
    components = sorted(CP.FluidsList())  # 유체 리스트 생성
    
    if request.method == 'POST':
        """
        사용자가 데이터를 입력하고 [계산하기] 같은 버튼을 누르면, 
        HTML form이 POST 방식으로 전송됨
        이 조건이 계산 수행 조건임 
        """
        result = section0.section0_calculation(request.form)    
    return render_template('section0.html', result=result, components=components)

@section.route('/section/1')  # SECTION 1
def section1_route():
    return render_template('section1.html')

@section.route('/section/2')  # SECTION 2
def section2_route():
    return render_template('section2.html')

@section.route('/section/3')  # SECTION 3
def section3_route():
    return render_template('section3.html')

@section.route('/section/3-1')
def section3_1():
    return render_template("section3-1.html")

@section.route('/section/3-2', methods=['GET', 'POST'])
def section3_2_route():
    components = sorted(CP.FluidsList())
    result = None
    component_count = 1  # 기본 1개 성분

    if request.method == 'POST':
        try:
            # 1. 유체 정보
            component_list = request.form.getlist('component')
            mole_fractions = list(map(float, request.form.getlist('mole_fraction')))
            T = float(request.form['T'])  # °C
            P = float(request.form['P'])  # barG

            # 2. 유량 및 배관 정보
            mass_flow_rate_kg_h = float(request.form['mass_flow_rate'])  # kg/h
            delta_p_barG = float(request.form['delta_p'])  # barG
            D_mm = float(request.form['pipe_diameter'])  # mm

            # 변환
            mass_flow_rate_kg_s = mass_flow_rate_kg_h / 3600  # kg/h → kg/s
            delta_p_Pa = (delta_p_barG + 1.013) * 1e5  # barG → Pa
            D_m = D_mm / 1000  # mm → m

            # 물성치 계산
            rho, mu = section3.get_density_viscosity(component_list, mole_fractions, T, P)

            # 오리피스 직경 계산
            d_m = section3.orifice_diameter_newton(mass_flow_rate_kg_s, D_m, delta_p_Pa, rho, mu)

            beta = d_m / D_m
            Re_D = (4 * mass_flow_rate_kg_s) / (math.pi * d_m * mu)
            C = section3.discharge_coefficient(beta, Re_D)

            result = {
                "orifice_diameter_mm": d_m * 1000,  # m → mm
                "beta": beta,
                "discharge_coefficient": C,
                "reynolds_number": Re_D,
                "density": rho,
                "viscosity": mu,
            }

            component_count = len(component_list)

        except Exception as e:
            result = {"error": f"계산 실패: {str(e)}"}
            component_count = len(request.form.getlist('component'))

    return render_template(
        'section3-2.html',
        components=components,
        result=result,
        component_count=component_count
    )

@section.route('/section/4')
def section4():
    return render_template("section4.html")