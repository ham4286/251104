import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MBTI 국가별 분석", layout="centered")

st.markdown("## 🌎 국가별 MBTI 유형 분석 대시보드")
st.write("MBTI 유형을 선택하면 해당 유형 비율이 높은 상위 10개 국가를 확인할 수 있습니다.")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # 공백 제거

    # ✅ MBTI 열 자동 감지 (16개 유형 중 있는 것만)
    mbti_types = [
        "INTJ", "INTP", "INFJ", "INFP",
        "ISTJ", "ISTP", "ISFJ", "ISFP",
        "ENTJ", "ENTP", "ENFJ", "ENFP",
        "ESTJ", "ESTP", "ESFJ", "ESFP"
    ]
    available_types = [t for t in mbti_types if t in df.columns]

    if not available_types:
        st.error("❌ MBTI 관련 열이 CSV에 포함되어 있지 않습니다.")
        st.stop()

    # ✅ 국가 열 자동 탐색
    possible_country_cols = [col for col in df.columns if "country" in col.lower() or "국가" in col]
    if possible_country_cols:
        country_col = possible_country_cols[0]
    else:
        st.error("❌ 'country' 또는 '국가' 열을 찾을 수 없습니다.")
        st.stop()

    # ✅ 사용자 MBTI 선택
    selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요 👇", available_types, index=available_types.index("ESFJ") if "ESFJ" in available_types else 0)

    # ✅ 상위 10개국 추출
    top10 = df.nlargest(10, selected_type)[[country_col, selected_type]]

    # ✅ 그래프 생성
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X(f"{selected_type}:Q", title="비율"),
            y=alt.Y(f"{country_col}:N", sort="-x", title="국가"),
            color=alt.Color(f"{selected_type}:Q", scale=alt.Scale(scheme="blues")),
            tooltip=[country_col, alt.Tooltip(f"{selected_type}:Q", format=".2%")]
        )
        .properties(width=600, height=400, title=f"🌟 {selected_type} 유형 비율이 높은 국가 TOP 10")
    )

    # ✅ 출력
    st.altair_chart(chart, use_container_width=True)
    st.markdown("#### 📋 데이터 요약")
    st.dataframe(top10.style.format({selected_type: "{:.2%}"}))

else:
    st.warning("⬆️ 위에서 CSV 파일을 업로드해주세요.")
