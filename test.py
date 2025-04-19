from calc.coolprop import get_fluid_properties

# 테스트용 데이터
def test_single_component():
    print("🧪 테스트: 단일 성분 Methane")
    components = ["Methane"]
    mole_fractions = [1.0]
    T = 25     # Celsius
    P = 1.0    # bar

    result = get_fluid_properties(components, mole_fractions, T, P)

    for prop, data in result.items():
        print(f"{prop:40} | {data['value']} {data['unit']}")

def test_multi_component():
    print("\n🧪 테스트: 혼합물 R32 + R125")
    components = ["R32", "R125"]
    mole_fractions = [0.7, 0.3]
    T = 25     # Celsius
    P = 1.0    # bar

    result = get_fluid_properties(components, mole_fractions, T, P)

    for prop, data in result.items():
        print(f"{prop:40} | {data['value']} {data['unit']}")

# 실행
if __name__ == "__main__":
    test_single_component()
    test_multi_component()