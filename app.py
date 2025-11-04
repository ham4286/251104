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
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 성적 예측 시스템", page_icon="🎓", layout="centered")

st.title("🎓 AI 기반 학생 성적 예측 시스템")
st.write("학생의 학습 습관과 과목 점수를 기반으로 미래 점수를 예측합니다.")

# 1️⃣ CSV 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("student_exam_scores.csv")
    return df

df = load_data()
st.subheader("📊 데이터 미리보기")
st.dataframe(df.head())

# 2️⃣ 피처 선택
target_col = st.selectbox("🎯 예측할 점수(목표 변수)", [col for col in df.columns if df[col].dtype != 'object'])
feature_cols = st.multiselect("🧩 입력 변수 선택", [col for col in df.columns if col != target_col], default=[col for col in df.columns if col != target_col])

# 3️⃣ 모델 학습
if st.button("🔍 모델 학습 시작"):
    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.success(f"✅ 모델 학습 완료! R² Score: {r2:.3f}, MSE: {mse:.3f}")

    # 4️⃣ 실제 vs 예측 그래프
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.7)
    ax.set_xlabel("Actual")
    ax.set_ylabel("Predicted")
    ax.set_title("Actual vs Predicted Scores")
    st.pyplot(fig)

# 5️⃣ 예측 시뮬레이터
st.subheader("🎮 점수 향상 시뮬레이터")
st.write("아래에서 학생 정보를 입력하면 예측 점수를 확인할 수 있습니다.")

input_data = {}
for col in feature_cols:
    val = st.number_input(f"{col} 값 입력", float(df[col].min()), float(df[col].max()), float(df[col].mean()))
    input_data[col] = val

if st.button("🚀 점수 예측하기"):
    X_new = pd.DataFrame([input_data])
    pred = model.predict(X_new)[0]
    st.metric(label="📈 예측된 점수", value=f"{pred:.2f}")

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
