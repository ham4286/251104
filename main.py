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
    # 데이터 불러오기
    df = pd.read_csv(uploaded_file)

    # MBTI 유형 리스트 (Country 제외)
    mbti_types = [col for col in df.columns if col != "Country"]

    # 선택 위젯
    selected_type = st.selectbox("분석할 MBTI 유형을 선택하세요:", mbti_types, index=5)

    # 선택된 MBTI 유형 기준으로 정렬
    top10 = df.sort_values(by=selected_type, ascending=False).head(10)

    # 그래프 제목 표시
    st.subheader(f"🌟 {selected_type} 유형 비율이 높은 국가 TOP 10")

    # Altair 차트 생성
    chart = (
        alt.Chart(top10)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X(selected_type, title=f"{selected_type} 비율", scale=alt.Scale(domain=[0, top10[selected_type].max() * 1.1])),
            y=alt.Y("Country", sort='-x', title="국가"),
            color=alt.Color(selected_type, scale=alt.Scale(scheme="blues")),
            tooltip=["Country", f"{selected_type}"]
        )
        .properties(
            height=400,
            width=600
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    # 수치 데이터표 보기
    with st.expander("📋 수치 데이터 보기"):
        st.dataframe(top10.reset_index(drop=True))

else:
    st.info("⬆️ 먼저 `countriesMBTI_16types.csv` 파일을 업로드해주세요.")
