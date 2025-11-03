import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(page_title="MBTI 국가 분석", layout="centered")

# 제목
st.markdown("### 🌟 ESFJ 유형 비율이 높은 국가 TOP 10")

# CSV 불러오기
df = pd.read_csv("countriesMBTI_16types.csv")

# ESFJ 기준 상위 10개국 추출
top10_esfj = df.nlargest(10, "ESFJ")[["country", "ESFJ"]]

# 그래프
chart = (
    alt.Chart(top10_esfj)
    .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
    .encode(
        x=alt.X("ESFJ:Q", title="비율", scale=alt.Scale(domain=[0, top10_esfj["ESFJ"].max() * 1.1])),
        y=alt.Y("country:N", sort="-x", title="국가"),
        color=alt.Color("ESFJ:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["country", alt.Tooltip("ESFJ:Q", format=".2%")]
    )
    .properties(width=600, height=400)
)

# 시각화 출력
st.altair_chart(chart, use_container_width=True)

# 표로도 같이 보여줌
st.markdown("#### 📋 데이터 요약")
st.dataframe(top10_esfj.style.format({"ESFJ": "{:.2%}"}))
