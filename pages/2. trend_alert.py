# pages/2. trend_alert.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="RUL 트렌드 경고 (초고속)", layout="wide")
st.title("⚡ 초고속 RUL 트렌드 애니메이션")
st.markdown("예측 RUL을 매우 빠르게 반복 출력하며 경고 여부를 실시간으로 확인합니다.")

@st.cache_data
def load_data():
    return pd.read_csv("data/rul_fd001_xgb_result.csv")

df = load_data()

unit_ids = df["unit"].unique()
selected_unit = st.selectbox("🎯 엔진 선택", unit_ids)
threshold = 30  # 고정 경고 기준

# 데이터 준비
unit_df = df[df["unit"] == selected_unit].copy()
unit_df["smoothed_rul"] = unit_df["predicted_rul_xgb"].rolling(window=5, min_periods=1).mean()

# UI 요소
stop_button = st.button("🛑 정지")
plot_placeholder = st.empty()
status_placeholder = st.empty()

# 반복 애니메이션 (step=8, sleep=0.001)
STEP_SIZE = 8
SLEEP_TIME = 0.001

while True:
    for i in range(5, len(unit_df) + 1, STEP_SIZE):
        if stop_button:
            status_placeholder.info("🛑 애니메이션 중지됨.")
            st.stop()

        partial_df = unit_df.iloc[:i]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(partial_df["cycle"], partial_df["smoothed_rul"], label="예측 RUL (Smoothed)", color='orange')
        ax.axhline(y=threshold, color='red', linestyle='--', label=f"위험 기준 {threshold}")
        ax.set_xlim(0, unit_df["cycle"].max())
        ax.set_ylim(0, unit_df["smoothed_rul"].max() + 10)
        ax.set_xlabel("Cycle")
        ax.set_ylabel("예측 RUL")
        ax.set_title(f"Engine {selected_unit} - Cycle {partial_df['cycle'].iloc[-1]}")
        ax.legend()
        ax.grid(True)

        plot_placeholder.pyplot(fig)
        time.sleep(SLEEP_TIME)
