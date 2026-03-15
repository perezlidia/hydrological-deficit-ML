# ======================================
# CROSS VALIDATION - ML MODELS
# ======================================

import pandas as pd
import numpy as np

from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


DATA_PATH = r"D:/hydrological-stress/ml_dataset/stress_dataset.csv"

data = pd.read_csv(DATA_PATH)

X = data[['PR_mean','ETP_mean','Balance_mean']]
y = data['stress_probability']


rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=10,
    random_state=42
)

gb = GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)

kfold = KFold(n_splits=5, shuffle=True, random_state=42)

rf_scores = cross_val_score(rf, X, y, scoring="r2", cv=kfold)
gb_scores = cross_val_score(gb, X, y, scoring="r2", cv=kfold)

print("Random Forest CV R2:", rf_scores.mean())
print("Gradient Boosting CV R2:", gb_scores.mean())