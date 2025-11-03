import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MBTI 국가 분석", layout="centered")

st.markdown("### 🌟 ESFJ 유형 비율이 높은 국가 TOP 10")

# ✅ 파일 업로드 UI
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 상위 10개국
    top10_esfj = df.nlargest(10, "ESFJ")[["country", "ESFJ"]]

    # 그래프
    chart = (
        alt.Chart(top10_esfj)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("ESFJ:Q", title="비율"),
            y=alt.Y("country:N", sort="-x", title="국가"),
            color=alt.Color("ESFJ:Q", scale=alt.Scale(scheme="blues")),
            tooltip=["country", alt.Tooltip("ESFJ:Q", format=".2%")]
        )
        .properties(width=600, height=400)
    )

    st.altair_chart(chart, use_container_width=True)
    st.dataframe(top10_esfj.style.format({"ESFJ": "{:.2%}"}))

else:
    st.warning("⬆️ 위에서 CSV 파일을 업로드해주세요.")
