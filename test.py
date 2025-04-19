from calc.coolprop import generate_phase_diagram

fluid = "HEOS::Water"
T_K = 300.0
P_Pa = 1e5

# 실행 및 HTML로 저장해서 확인
img_base64 = generate_phase_diagram(fluid, T_K, P_Pa)

with open("phase_test.html", "w") as f:
    f.write(f'<img src="{img_base64}" alt="Diagram" style="max-width:100%;">')

print("✅ HTML 파일 생성 완료: phase_test.html")