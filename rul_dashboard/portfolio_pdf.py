from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# 나눔고딕 같은 한글 폰트 파일 위치 지정
pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

c = canvas.Canvas("임태혁_프로젝트_요약.pdf", pagesize=A4)
width, height = A4
c.setFont("NanumGothic", 14)

lines = [
    "작성자: 임태혁",
    "▶ 프로젝트 개요",
    "NASA C-MAPSS 데이터를 활용하여 항공기 엔진의 RUL 예측 대시보드를 구현하였습니다.",
    "Streamlit을 기반으로 하며 센서 분석, 모델 성능 비교, 실시간 예측, PDF 생성 등을 포함합니다.",
    "▶ 사용 기술: Python, Streamlit, XGBoost, Scikit-learn, ngrok 등",
    "▶ 배포: ngrok, Streamlit Cloud 가능",
]

y = height - 40
for line in lines:
    c.drawString(40, y, line)
    y -= 20

c.save()
