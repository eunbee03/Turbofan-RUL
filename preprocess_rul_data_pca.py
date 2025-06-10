# preprocess_rul_data_pca.py

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 📌 경로 설정
input_path = "data/rul_result_real.csv"
output_path = "C:/Users/yimta/OneDrive/바탕 화면/Streamlit_prac/rul_dashboard/rul_result_pca_filtered.csv"

# 1. 데이터 불러오기
df = pd.read_csv(input_path)

# ✅ 여기 바로 아래에 삽입하세요!
print("✅ 전체 컬럼:", df.columns.tolist())

# 센서 컬럼 자동 인식: 's1' 또는 's_1' 또는 'sensor1' 등
sensor_cols = [col for col in df.columns if col.lower().startswith('s') and col != 'set']  # 'set'은 operational setting일 수 있음

# 확인
print("📌 센서 컬럼 목록:", sensor_cols)


# 3. 센서 데이터 정규화
X_scaled = StandardScaler().fit_transform(df[sensor_cols])

# 4. PCA 적용 (90% 분산 유지)
pca = PCA(n_components=0.9)
X_pca = pca.fit_transform(X_scaled)

# 5. 센서 기여도 계산
loadings = pd.DataFrame(pca.components_.T, index=sensor_cols)
sensor_scores = loadings.abs().sum(axis=1)
top_sensors = sensor_scores.sort_values(ascending=False).head(10).index.tolist()

print("✅ PCA 기반 중요 센서 선정:", top_sensors)

# 6. 선택된 센서만 남기기
df_filtered = df[top_sensors + ['engine_id', 'cycle', 'true_rul',
                                'predicted_rul_xgb', 'predicted_rul_lstm']]

# 7. cycle_ratio 추가
df_filtered['max_cycle'] = df_filtered.groupby('engine_id')['cycle'].transform('max')
df_filtered['cycle_ratio'] = df_filtered['cycle'] / df_filtered['max_cycle']

# 8. 저장
df_filtered.to_csv(output_path, index=False)
print(f"📁 저장 완료: {output_path}")
