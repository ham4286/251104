import streamlit as st
import pandas as pd
import altair as alt

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI 국가별 분석 대시보드",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 MBTI 유형별 국가 TOP 10 분석")
st.markdown("""
이 앱은 국가별 MBTI 분포 데이터(`countriesMBTI_16types.csv`)를 기반으로  
**선택한 MBTI 유형이 높은 국가 TOP 10**을 시각적으로 보여줍니다.
""")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    # CSV 로드 및 열 이름 공백 제거
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # 공백 제거

    # 숫자형만 변환 시도 (Country 제외)
    for col in df.columns:
        if col != "Country":
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # MBTI 유형 리스트
    mbti_types = [col for col in df.columns if col != "Country"]

    # 분석할 유형 선택
    selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_types, index=mbti_types.index("ESFJ") if "ESFJ" in mbti_types else 0)

    # 상위 10개 국가 추출
    top10 = df.sort_values(by=selected_type, ascending=False).head(10)

    st.subheader(f"🌟 {selected_type} 유형 비율이 높은 국가 TOP 10")

    # Altair 그래프
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(selected_type, title=f"{selected_type} 비율", type="quantitative"),
            y=alt.Y("Country", sort='-x', title="국가", type="nominal"),
            color=alt.Color(selected_type, scale=alt.Scale(scheme="tealblues")),
            tooltip=["Country", alt.Tooltip(selected_type, format=".4f", title="비율")]
        )
        .properties(width=600, height=400)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # 표 보기
    with st.expander("📋 데이터 상세 보기"):
        st.dataframe(top10.reset_index(drop=True))

else:
    st.info("⬆️ 먼저 `countriesMBTI_16types.csv` 파일을 업로드해주세요.")
