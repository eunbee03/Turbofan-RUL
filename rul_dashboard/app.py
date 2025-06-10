# app.py

import streamlit as st

# 웹페이지 기본 설정
st.set_page_config(
    page_title="잔여수명 예측 대시보드",
    layout="wide"
)

# 메인 제목
st.title("✈️ 항공기 엔진 잔여수명 예측 프로젝트")

# 부제목
st.markdown("#### 🚀 NASA C-MAPSS 데이터 기반 예지보전 AI 모델링")

# 간략 소개
st.markdown("""
이 프로젝트는 항공기 엔진의 고장을 사전에 예측하여  
정비 효율성을 높이고 안전성을 향상시키기 위한 AI 기반 예지보전 시스템을 개발하는 것입니다.

**사용 데이터셋:** NASA C-MAPSS (FD001)  
**예측 대상:** Remaining Useful Life (RUL)  
**적용 기술:** LSTM, XGBoost, PCA, Streamlit 시각화
""")

# 팀원 소개
st.markdown("### 👨‍💻 팀원 소개")
st.markdown("""
- **팀장 심기원** – 발표, 전체 프로세스 관리  
- **개발팀장 임태혁** – 모델 구현, 파이프라인 설계  
- **분석팀장 이가은** – EDA, 모델 해석  
- **조원 이은비** – 데이터 정리, 시각화 보조
""")

# 이미지 넣기 (선택)
# st.image("assets/team_photo.png", width=500)

# 푸터
st.markdown("""
### 🎯 프로젝트 목적  
이 프로젝트는 **항공기 엔진의 잔여수명(RUL)을 정확히 예측하고**,  
예측 결과를 기반으로 **이상 징후 탐지, 모델 비교, 리포트 생성**까지 가능한  
**AI 기반 예지보전 통합 솔루션**을 구축하는 것을 목표로 합니다.

> 🚧 단순 예측이 아닌, 실제 운용 가능한 시각화/분석/리포트 기능까지 포함하는 완전한 대시보드 시스템입니다.
""")
