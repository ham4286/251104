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

# 1️⃣ CSV 업로드
uploaded_file = st.file_uploader("📂 학생 성적 데이터 파일 업로드 (.csv)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 데이터 미리보기")
    st.dataframe(df.head())

    # object 타입 컬럼을 자동 인코딩 (문자열 → 숫자)
    df_encoded = df.copy()
    for col in df_encoded.select_dtypes(include=["object"]).columns:
        df_encoded[col] = df_encoded[col].astype("category").cat.codes

    st.info("문자열 컬럼이 자동으로 숫자로 변환되었습니다. (예: 성별 → 0/1)")

    # 2️⃣ 피처 선택
    target_col = st.selectbox("🎯 예측할 점수(목표 변수)", df_encoded.columns)
    feature_cols = st.multiselect(
        "🧩 입력 변수 선택",
        [col for col in df_encoded.columns if col != target_col],
        default=[col for col in df_encoded.columns if col != target_col]
    )

    if len(feature_cols) == 0:
        st.warning("⚠️ 하나 이상의 입력 변수를 선택하세요.")
    else:
        # 3️⃣ 모델 학습
        if st.button("🔍 모델 학습 시작"):
            X = df_encoded[feature_cols]
            y = df_encoded[target_col]

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

            st.session_state.model = model
            st.session_state.features = feature_cols
            st.session_state.data = df_encoded

        # 5️⃣ 예측 시뮬레이터
        if "model" in st.session_state:
            st.subheader("🎮 점수 향상 시뮬레이터")
            st.write("학생 정보를 입력하면 예측 점수를 확인할 수 있습니다.")

            input_data = {}
            for col in st.session_state.features:
                val = st.number_input(
                    f"{col} 값 입력",
                    float(df_encoded[col].min()),
                    float(df_encoded[col].max()),
                    float(df_encoded[col].mean())
                )
                input_data[col] = val

            if st.button("🚀 점수 예측하기"):
                X_new = pd.DataFrame([input_data])
                pred = st.session_state.model.predict(X_new)[0]
                st.metric(label="📈 예측된 점수", value=f"{pred:.2f}")
else:
    st.info("👆 CSV 파일을 먼저 업로드하세요.")
