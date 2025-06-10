# preprocess_train_fd001_pca.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. 파일 경로
input_path = "data/train_FD001.txt"
output_path = "data/rul_fd001_pca_filtered.csv"

# 2. 컬럼 이름 지정 (C-MAPSS FD001 기준: 3 + 21 = 24 열)
column_names = ['unit', 'cycle'] + [f'op_setting_{i}' for i in range(1, 4)] + [f's{i}' for i in range(1, 22)]

# 3. 데이터 불러오기
df = pd.read_csv(input_path, sep=r"\s+", header=None, names=column_names)

# 4. 센서 컬럼 추출
sensor_cols = [col for col in df.columns if col.startswith('s')]
print("📌 센서 컬럼 수:", len(sensor_cols))

# 5. 표준화
X_scaled = StandardScaler().fit_transform(df[sensor_cols])

# 6. PCA (분산 90% 유지)
pca = PCA(n_components=0.9)
X_pca = pca.fit_transform(X_scaled)

# 7. 중요 센서 추출
loadings = pd.DataFrame(pca.components_.T, index=sensor_cols)
sensor_scores = loadings.abs().sum(axis=1)
top_sensors = sensor_scores.sort_values(ascending=False).head(10).index.tolist()
print("✅ PCA로 선정된 중요 센서:", top_sensors)

# 8. 필요한 컬럼만 저장
df_filtered = df[['unit', 'cycle'] + top_sensors]
df_filtered.to_csv(output_path, index=False)
print(f"📁 저장 완료: {output_path}")
