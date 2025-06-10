# pages/4. model_summary.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="모델 성능 요약", layout="wide")
st.title("📊 모델 성능 종합 리포트")
st.markdown("예측 모델의 전반적인 성능을 요약하고, 오차 분포를 시각화합니다.")

# 📁 데이터 로딩
@st.cache_data
def load_rul_data():
    path = "data/rul_fd001_xgb_result.csv"  # ← 경로 확인 필요
    return pd.read_csv(path)

df = load_rul_data()

# 📊 예측 모델 선택
model_cols = [col for col in df.columns if col.startswith("predicted_rul")]
if not model_cols:
    st.error("❌ 예측 결과 컬럼이 존재하지 않습니다. predicted_rul_xxx 형태의 컬럼명을 확인하세요.")
    st.stop()

selected_model = st.selectbox("📊 비교할 예측 모델을 선택하세요", model_cols)

# 📈 오차 계산
df["오차"] = df[selected_model] - df["RUL"]

# ✅ RMSE 수동 계산
mse = mean_squared_error(df["RUL"], df[selected_model])
rmse = np.sqrt(mse)
st.metric("📌 전체 엔진 평균 RMSE", f"{rmse:.2f}")

# 📊 오차 분포 시각화
st.markdown("### 🧭 예측 오차 분포")
fig, ax = plt.subplots(figsize=(10, 4))  # 가로 10인치, 세로 4인치로 작게
ax.hist(df["오차"], bins=20, color="orange", edgecolor="black")
ax.set_xlabel("예측 오차 (예측 - 실제)")
ax.set_ylabel("엔진 수")
ax.set_title("예측 오차 분포")
st.pyplot(fig)

# 📋 엔진별 성능 테이블
st.markdown("### 📋 엔진별 예측 성능 요약")

df["절대오차"] = df["오차"].abs()
summary_df = df[["unit", "cycle", "RUL", selected_model, "오차", "절대오차"]].copy()
summary_df = summary_df.sort_values("절대오차", ascending=False)

st.dataframe(summary_df, use_container_width=True)
