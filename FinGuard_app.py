
import streamlit as st
import pandas as pd

st.set_page_config(page_title="FinGuard", layout="wide")

def make_risk_explanation(row):
    if row["RiskLevel"] == "정상":
        return "이상거래, 변동성, 공시 위험 신호가 낮은 상태입니다."
    elif row["RiskLevel"] == "관심":
        return "일부 이상거래 또는 변동성 신호가 관찰되어 모니터링이 필요합니다."
    elif row["RiskLevel"] == "주의":
        if row["Disclosure_Exists"] == 1:
            return "이상거래 신호와 함께 관련 공시가 확인되어 공시 내용 확인이 필요합니다."
        else:
            return "이상거래 신호가 높지만 관련 공시가 확인되지 않아 설명되지 않는 변동 가능성이 있습니다."
    else:
        if row["Disclosure_Exists"] == 1:
            return "강한 이상거래 및 변동성 신호와 위험 공시가 함께 관찰되어 높은 주의가 필요합니다."
        else:
            return "강한 이상거래 신호가 있으나 관련 공시가 확인되지 않아 설명되지 않는 고위험 변동으로 분류됩니다."

sample = pd.DataFrame([
    ["카카오","위험",92,1,"대기업"],
    ["우리기술투자","위험",89,1,"중소기업"],
    ["원익IPS","주의",71,0,"중견기업"],
    ["현대차","관심",55,1,"대기업"],
], columns=["Stock","RiskLevel","RiskScore","Disclosure_Exists","Size"])

sample["Explanation"] = sample.apply(make_risk_explanation, axis=1)

st.sidebar.title("🚨 FinGuard")
page = st.sidebar.radio(
    "메뉴",
    ["대시보드","종목 분석","기업 규모 비교"]
)

if page == "대시보드":
    st.title("🚨 FinGuard")
    st.subheader("금융 이상거래 탐지 플랫폼")

    c1,c2,c3 = st.columns(3)
    c1.metric("위험 종목", "4")
    c2.metric("관심 종목", "7")
    c3.metric("정상 종목", "15")

    st.markdown("### 위험 종목 TOP")
    st.dataframe(sample[["Stock","RiskLevel","RiskScore"]], use_container_width=True)

elif page == "종목 분석":
    stock = st.selectbox("종목 선택", sample["Stock"])
    row = sample[sample["Stock"] == stock].iloc[0]

    st.title(f"📈 {stock}")
    c1,c2,c3 = st.columns(3)
    c1.metric("위험등급", row["RiskLevel"])
    c2.metric("위험점수", row["RiskScore"])
    c3.metric("공시 여부", "있음" if row["Disclosure_Exists"] else "없음")

    st.markdown("### 🤖 AI 위험 해석")
    st.info(row["Explanation"])

    st.markdown("### 📰 공시/이벤트 분석")
    st.write("이상거래 발생일과 공시·뉴스를 연계하여 원인을 분석합니다.")

elif page == "기업 규모 비교":
    st.title("🏢 기업 규모별 비교")

    size_df = pd.DataFrame({
        "기업규모":["대기업","중견기업","중소기업"],
        "평균 이상거래 비율":[0.8,1.6,3.4]
    })

    st.bar_chart(size_df.set_index("기업규모"))
    st.dataframe(size_df, use_container_width=True)
