# pages/live_predict.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="실시간 RUL 예측", layout="wide")
st.title("🔮 실시간 잔여수명(RUL) 예측")
st.markdown("센서값을 입력하면 현재 상태에서의 RUL(잔여 수명)을 예측합니다.")

# ✅ 예측 모델 로드 (여기선 샘플 더미 모델 사용)
@st.cache_resource
def load_model():
    # 실제 모델이 있다면 joblib.load("model.pkl") 등으로 교체
    return lambda x: 130 - np.mean(x) * 5 + np.random.randint(-3, 3)  # 더미 함수

model = load_model()

# ✅ 수동 입력 모드
st.subheader("🧪 센서값 수동 입력")

sensor_inputs = {}
sensor_list = [f"sensor_{i}" for i in range(1, 6)]  # 예시로 5개만 사용
cols = st.columns(len(sensor_list))

for i, sensor in enumerate(sensor_list):
    sensor_inputs[sensor] = cols[i].number_input(sensor, value=50.0, min_value=0.0, max_value=100.0)

if st.button("🔍 예측 실행"):
    input_array = np.array(list(sensor_inputs.values())).reshape(1, -1)
    predicted_rul = model(input_array[0])
    st.success(f"📈 예측된 RUL: `{predicted_rul:.2f}` cycles")

# ✅ CSV 업로드 예측
st.subheader("📁 CSV 업로드 예측")
uploaded_file = st.file_uploader("CSV 파일 업로드 (센서값 포함)", type="csv")

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.dataframe(data.head())

        if st.button("📊 일괄 예측"):
            results = []
            for _, row in data.iterrows():
                result = model(row.values)
                results.append(result)

            data["predicted_rul"] = results
            st.success("예측 완료!")
            st.dataframe(data)

            # 다운로드 링크 제공
            csv = data.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 결과 다운로드", csv, file_name="rul_predictions.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ CSV 처리 오류: {e}")