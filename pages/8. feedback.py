# pages/feedback.py

import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="피드백", layout="wide")
st.title("💬 사용자 피드백 수집")
st.markdown("Streamlit 대시보드 및 예측 리포트에 대한 여러분의 소중한 의견을 기다립니다.")

# 📋 피드백 폼
name = st.text_input("👤 이름 또는 닉네임", "")
satisfaction = st.slider("📊 대시보드 만족도 (1~5)", 1, 5, 3)
comment = st.text_area("📝 개선 의견 또는 자유 피드백")

submitted = st.button("📩 피드백 제출")

# 저장
if submitted:
    feedback = {
        "날짜": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "이름": name,
        "만족도": satisfaction,
        "피드백": comment
    }

    # 파일 저장 위치
    file_path = "feedback_results.csv"

    # 기존 파일 존재 시 이어쓰기
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df = pd.concat([df, pd.DataFrame([feedback])], ignore_index=True)
    else:
        df = pd.DataFrame([feedback])

    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    st.success("✅ 피드백이 성공적으로 제출되었습니다. 감사합니다!")

    # 제출 내용 요약 표시
    st.markdown("---")
    st.markdown("### 제출 요약")
    st.write(feedback)