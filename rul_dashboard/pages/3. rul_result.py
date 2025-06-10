# pages/3. rul_result_xgb.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="RUL 예측 결과(XGBoost)", layout="wide")
st.title("📊 RUL 예측 결과 (XGBoost 기반)")
st.markdown("각 엔진별로 실제 RUL과 예측 RUL (XGBoost)을 비교합니다.")

# 📁 데이터 불러오기
@st.cache_data
def load_data():
    path = "rul_dashboard/rul_fd001_xgb_result.csv"
    return pd.read_csv(path)

df = load_data()

# ✅ 엔진 선택
unit_ids = df['unit'].unique()
selected_unit = st.selectbox("🔧 분석할 엔진을 선택하세요", unit_ids)

# ✅ 위험 기준 설정
threshold = st.slider("⚠️ 위험 기준 RUL (경고 기준)", min_value=10, max_value=50, value=30)

# ✅ 선택된 유닛 데이터
unit_df = df[df['unit'] == selected_unit]

# ✅ smoothing 적용 (이동 평균)
unit_df['smoothed_rul'] = unit_df['predicted_rul_xgb'].rolling(window=5, min_periods=1).mean()

# ✅ 시각화
st.markdown("### 📉 예측된 RUL vs 실제 RUL")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(unit_df['cycle'], unit_df['RUL'], label="실제 RUL", color='green')
ax.plot(unit_df['cycle'], unit_df['smoothed_rul'], label="예측 RUL (Smoothed)", color='orange', linestyle='--')
ax.axhline(y=threshold, color='red', linestyle='--', label=f"위험 기준 ({threshold})")
ax.set_xlabel("Cycle")
ax.set_ylabel("RUL")
ax.set_title(f"Engine {selected_unit} RUL 예측 결과")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ✅ 마지막 RUL 상태 체크
latest_pred = unit_df['predicted_rul_xgb'].iloc[-1]
if latest_pred < threshold:
    st.error(f"🚨 경고: 현재 예측 RUL이 {latest_pred:.2f}로 위험 기준({threshold}) 미만입니다!")
else:
    st.success(f"✅ 안전: 현재 예측 RUL은 {latest_pred:.2f}입니다.")

# 📋 상세 테이블
with st.expander("🔍 예측 상세 보기"):
    st.dataframe(unit_df[['cycle', 'RUL', 'predicted_rul_xgb']])
