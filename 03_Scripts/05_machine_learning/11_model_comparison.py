# ======================================
# MODEL COMPARISON
# Random Forest vs Gradient Boosting
# Hydrological Stress Prediction
# ======================================

import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# ======================================
# PATHS
# ======================================

DATA_PATH = r"D:/hydrological-stress/ml_dataset/stress_dataset.csv"
OUTPUT_FOLDER = r"D:/hydrological-stress/ml_results/"


# ======================================
# LOAD DATA
# ======================================

data = pd.read_csv(DATA_PATH)

X = data[['PR_mean','ETP_mean','Balance_mean']]
y = data['stress_probability']


# ======================================
# TRAIN TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)


# ======================================
# MODELS
# ======================================

rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

gb = GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)


# ======================================
# TRAIN MODELS
# ======================================

rf.fit(X_train, y_train)
gb.fit(X_train, y_train)


# ======================================
# PREDICTIONS
# ======================================

rf_pred = rf.predict(X_test)
gb_pred = gb.predict(X_test)


# ======================================
# METRICS FUNCTION
# ======================================

def evaluate(y_true, y_pred):

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return rmse, mae, r2


rf_rmse, rf_mae, rf_r2 = evaluate(y_test, rf_pred)
gb_rmse, gb_mae, gb_r2 = evaluate(y_test, gb_pred)


# ======================================
# RESULTS TABLE
# ======================================

results = pd.DataFrame({

"Model": ["Random Forest","Gradient Boosting"],

"RMSE": [rf_rmse, gb_rmse],

"MAE": [rf_mae, gb_mae],

"R2": [rf_r2, gb_r2]

})

print("\nModel Comparison")
print(results)


# ======================================
# SAVE TABLE
# ======================================

results.to_csv(
OUTPUT_FOLDER + "model_comparison_metrics.csv",
index=False
)


# ======================================
# COMPARISON PLOT
# ======================================

plt.figure()

models = results["Model"]

plt.bar(models, results["R2"])

plt.title("Model Performance Comparison (R²)")
plt.ylabel("R² Score")

plt.savefig(
OUTPUT_FOLDER + "model_comparison_R2.png",
dpi=300,
bbox_inches="tight"
)


print("\nGenerated files:")
print("model_comparison_metrics.csv")
print("model_comparison_R2.png")