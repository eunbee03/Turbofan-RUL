# train_xgboost_rul_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import numpy as np

# 📁 파일 경로
input_path = "data/rul_fd001_pca_filtered.csv"
output_path = "data/rul_fd001_xgb_result.csv"

# 1. 데이터 불러오기
df = pd.read_csv(input_path)

# 2. RUL 생성 (최대 cycle - 현재 cycle)
df['max_cycle'] = df.groupby('unit')['cycle'].transform('max')
df['RUL'] = df['max_cycle'] - df['cycle']

# 3. 피처/타깃 설정
feature_cols = [col for col in df.columns if col.startswith('s')] + ['cycle']
X = df[feature_cols]
y = df['RUL']

# 4. 학습/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. XGBoost 모델 학습
model = XGBRegressor(n_estimators=200, max_depth=5, learning_rate=0.1)
model.fit(X_train, y_train)

# 6. 전체 데이터 예측
df['predicted_rul_xgb'] = model.predict(X)

# 7. RMSE 계산 (직접 제곱근)
mse = mean_squared_error(y, df['predicted_rul_xgb'])
rmse = np.sqrt(mse)
print(f"✅ 전체 RMSE: {rmse:.2f}")

# 8. 결과 저장
df.to_csv(output_path, index=False)
print(f"📁 예측 결과 저장 완료: {output_path}")
