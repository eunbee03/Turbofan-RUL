import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- 데이터 불러오기 및 전처리 ---
@st.cache_data
def load_sensor_data(filepath):
    df = pd.read_csv(filepath, sep=" ", header=None)
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = ['engine_id', 'cycle'] + [f'sensor_{i}' for i in range(1, df.shape[1] - 1)]
    return df

# --- 분산 기준으로 센서 필터링 ---
def filter_low_variance_sensors(df, sensor_cols, threshold=1e-5):
    variances = df[sensor_cols].var()
    filtered = variances[variances > threshold].index.tolist()
    return filtered

# --- PCA 기반 중요 센서 추출 ---
def get_important_sensors_pca(df, sensor_cols, top_n=5):
    X = df[sensor_cols]
    X_std = StandardScaler().fit_transform(X)
    pca = PCA(n_components=5)
    pca.fit(X_std)
    contrib = np.mean(np.abs(pca.components_), axis=0)
    importance = pd.Series(contrib, index=sensor_cols).sort_values(ascending=False)
    return list(importance.head(top_n).index), importance

# --- 센서 그래프 출력 ---
def plot_sensor(ax, df, sensor):
    ax.plot(df['cycle'], df[sensor])
    ax.set_title(sensor, fontsize=10)
    ax.set_xlabel("Cycle", fontsize=8)
    ax.set_ylabel("Value", fontsize=8)
    ax.tick_params(axis='both', labelsize=6)

# --- Streamlit 설정 ---
st.set_page_config(page_title="PCA 센서 분석", layout="wide")
st.title("📊 PCA 기반 센서 중요도 분석")
st.markdown("##### 변동 없는 센서를 제거한 뒤, PCA로 중요 센서를 자동 추출합니다.")

# --- 데이터 로드 ---
file_path = "data/train_FD001.txt"
df = load_sensor_data(file_path)
sensor_cols_all = [col for col in df.columns if 'sensor' in col]

# --- 분산 필터링 ---
sensor_cols = filter_low_variance_sensors(df, sensor_cols_all)
removed_sensors = list(set(sensor_cols_all) - set(sensor_cols))
if removed_sensors:
    st.warning(f"⚠️ 변동 거의 없는 센서 제거됨: {', '.join(sorted(removed_sensors))}")

# --- 사용자 입력: 엔진 선택 ---
engine_id = st.selectbox("확인할 엔진 ID", df['engine_id'].unique())
engine_data = df[df['engine_id'] == engine_id]

# --- 중요 센서 추출 ---
important_sensors, pca_scores = get_important_sensors_pca(df, sensor_cols, top_n=5)
st.success(f"🔍 PCA 기준 중요 센서 TOP5: {', '.join(important_sensors)}")

# --- 중요 센서 시각화 ---
st.subheader("🔥 PCA 기준 중요 센서 시각화")
cols = st.columns(5)
for i, sensor in enumerate(important_sensors):
    with cols[i]:
        fig, ax = plt.subplots(figsize=(3, 2))
        plot_sensor(ax, engine_data, sensor)
        ax.set_title(f"⭐ {sensor}", fontsize=10, fontweight='bold')
        st.pyplot(fig)
        plt.close(fig)

# --- 전체 센서 시각화 ---
st.markdown("---")
st.subheader("📋 전체 센서 시각화 (유효 센서만)")
for i in range(0, len(sensor_cols), 5):
    cols = st.columns(5)
    for j in range(5):
        if i + j < len(sensor_cols):
            sensor = sensor_cols[i + j]
            with cols[j]:
                fig, ax = plt.subplots(figsize=(3, 2))
                plot_sensor(ax, engine_data, sensor)
                st.pyplot(fig)
                plt.close(fig)

# --- PCA 기여도 바 차트 ---
st.markdown("---")
st.subheader("📈 PCA 센서 기여도 (절댓값 기준)")
st.bar_chart(pca_scores.sort_values(ascending=False).head(10))
