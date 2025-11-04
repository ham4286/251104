import streamlit as st
import numpy as np
import sympy as sp
import altair as alt

# 🧠 페이지 설정
st.set_page_config(page_title="AI 수식 그래프 시각화기", page_icon="📈", layout="centered")

st.title("📈 AI 수식 그래프 시각화기")
st.caption("입력한 수학식을 자동으로 그래프로 시각화하고, 미분·적분 결과도 보여줍니다 💡")

# ✍️ 사용자 입력
expr_input = st.text_input("수식을 입력하세요 (예: sin(x), x**2 + 3*x - 4)", "sin(x)")
x = sp.Symbol("x")

try:
    # 🔍 수식 파싱
    expr = sp.sympify(expr_input)

    # 🧮 함수 평가용 NumPy 함수 변환
    f = sp.lambdify(x, expr, modules=["numpy"])

    # 📊 x 범위와 y 계산
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f(x_vals)

    # 📉 Altair 그래프 시각화
    chart_data = {"x": x_vals, "y": y_vals}
    chart = (
        alt.Chart(alt.Data(values=[{"x": float(x), "y": float(y)} for x, y in zip(x_vals, y_vals)]))
        .mark_line(color="#1f77b4", strokeWidth=3)
        .encode(x="x:Q", y="y:Q")
        .properties(width=700, height=400, title=f"y = {expr_input}")
    )

    st.altair_chart(chart, use_container_width=True)

    # 🧩 추가 기능: 미분 & 적분
    st.markdown("### 🔹 미분 결과")
    derivative = sp.diff(expr, x)
    st.latex(f"f'(x) = {sp.latex(derivative)}")

    st.markdown("### 🔹 적분 결과")
    integral = sp.integrate(expr, x)
    st.latex(f"∫f(x)dx = {sp.latex(integral)}")

except Exception as e:
    st.error("⚠️ 수식을 인식할 수 없습니다. 예: sin(x), x**2 + 3*x - 4 형태로 입력하세요.")
