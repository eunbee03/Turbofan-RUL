# pages/model_comparison.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import root_mean_squared_error  # ✅ 변경된 부분

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="모델 비교", layout="wide")
st.title("🆚 예측 모델 성능 비교")
st.markdown("여러 예측 모델의 RUL 결과를 비교하여 가장 정확한 모델을 평가합니다.")

# 📁 데이터 로딩
@st.cache_data
def load_data():
    path = "rul_result_multi_model.csv"
    return pd.read_csv(path)

df = load_data()

# ✅ 비교할 모델 선택
model_cols = [col for col in df.columns if col.startswith("predicted_rul_")]
model1 = st.selectbox("🔵 모델 1 선택", model_cols)
model2 = st.selectbox("🟢 모델 2 선택", model_cols, index=1 if len(model_cols) > 1 else 0)

# 엔진 선택
engine_ids = df["engine_id"].unique()
selected_engine = st.selectbox("🔧 비교할 엔진 선택", engine_ids)

engine_df = df[df["engine_id"] == selected_engine]

# 📊 비교 그래프
st.markdown("### 📈 RUL 예측 비교")

fig, ax = plt.subplots()
ax.plot(engine_df["cycle"], engine_df["true_rul"], label="실제 RUL", color="black")
ax.plot(engine_df["cycle"], engine_df[model1], label=model1, linestyle="--")
ax.plot(engine_df["cycle"], engine_df[model2], label=model2, linestyle=":")
ax.set_xlabel("Cycle")
ax.set_ylabel("RUL")
ax.set_title(f"Engine {selected_engine} 예측 비교")
ax.legend()
st.pyplot(fig)

# 📊 성능 비교 지표 (✅ RMSE 계산 방식 변경)
rmse1 = root_mean_squared_error(engine_df["true_rul"], engine_df[model1])
rmse2 = root_mean_squared_error(engine_df["true_rul"], engine_df[model2])

st.metric(f"📊 {model1} RMSE", f"{rmse1:.2f}")
st.metric(f"📊 {model2} RMSE", f"{rmse2:.2f}")

# 🔍 데이터 테이블 보기
with st.expander("🔎 비교 테이블 보기"):

    # ✅ 중복 모델 선택 방지 및 충돌 방지 코드
    if model1 == model2:
        st.warning("⚠️ 두 모델이 동일합니다. 다른 모델을 선택해주세요.")
    else:
        cols = ["engine_id", "cycle", "true_rul", model1, model2]
        cols = list(dict.fromkeys(cols))  # 중복 제거
        st.dataframe(engine_df[cols])