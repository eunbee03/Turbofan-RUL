# pages/pdf_report.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

# 한글 폰트 적용 (PDF 이미지 대응용)
import matplotlib
import matplotlib.font_manager as fm
font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우 기본 한글 폰트
font_prop = fm.FontProperties(fname=font_path).get_name()
matplotlib.rc('font', family=font_prop)
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="PDF 리포트 생성", layout="wide")
st.title("📝 예측 리포트 PDF 자동 생성기")

# 데이터 로드
@st.cache_data
def load_data():
    path = "rul_dashboard/data/rul_result_multi_model.csv"
    return pd.read_csv(path)

df = load_data()

# 엔진 선택
engine_id = st.selectbox("📌 리포트를 생성할 엔진을 선택하세요", df["engine_id"].unique())
engine_df = df[df["engine_id"] == engine_id]

# ✅ RMSE 계산 함수 변경
from sklearn.metrics import root_mean_squared_error
rmse_lr = root_mean_squared_error(df["true_rul"], df["predicted_rul_lr"])
rmse_xgb = root_mean_squared_error(df["true_rul"], df["predicted_rul_xgb"])

# 그래프 생성
fig, ax = plt.subplots()
ax.plot(engine_df["cycle"], engine_df["true_rul"], label="실제 RUL", color="black")
ax.plot(engine_df["cycle"], engine_df["predicted_rul_lr"], label="선형회귀", linestyle="--")
ax.plot(engine_df["cycle"], engine_df["predicted_rul_xgb"], label="XGBoost", linestyle=":")
ax.legend()
ax.set_title(f"Engine {engine_id} RUL 예측 비교")
ax.set_xlabel("Cycle")
ax.set_ylabel("RUL")

# 그래프 임시 이미지 저장
temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
fig.savefig(temp_image.name)

# PDF 생성 함수
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Engine {engine_id} 예측 리포트", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"선형회귀 RMSE: {rmse_lr:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"XGBoost RMSE: {rmse_xgb:.2f}", ln=True)

    pdf.ln(10)
    pdf.image(temp_image.name, x=10, w=180)

    output_path = os.path.join(tempfile.gettempdir(), f"engine_{engine_id}_report.pdf")
    pdf.output(output_path)
    return output_path

if st.button("📥 PDF 리포트 생성"):
    pdf_path = create_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button("📄 리포트 다운로드", f, file_name=f"Engine_{engine_id}_report.pdf")
