# ======================================
# MACHINE LEARNING - GRADIENT BOOSTING
# Hydrological Stress Prediction
# ======================================

import pandas as pd
import numpy as np
import matplotlib

# avoid GUI backend errors
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# ======================================
# PATHS
# ======================================

DATA_PATH = r"D:/hydrological-stress/ml_dataset/stress_dataset.csv"
OUTPUT_FOLDER = r"D:/hydrological-stress/ml_results/"


# ======================================
# 1 LOAD DATA
# ======================================

data = pd.read_csv(DATA_PATH)

print("Dataset preview:")
print(data.head())

print("\nDataset shape:", data.shape)


# ======================================
# 2 MODEL VARIABLES
# ======================================

X = data[['PR_mean', 'ETP_mean', 'Balance_mean']]
y = data['stress_probability']


# ======================================
# 3 TRAIN / TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42
)


# ======================================
# 4 GRADIENT BOOSTING MODEL
# ======================================

gb_model = GradientBoostingRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)

gb_model.fit(X_train, y_train)


# ======================================
# 5 PREDICTION
# ======================================

y_pred = gb_model.predict(X_test)


# ======================================
# 6 MODEL EVALUATION
# ======================================

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\nModel Performance")
print("----------------------")
print("RMSE:", rmse)
print("MAE :", mae)
print("R²  :", r2)


# ======================================
# 7 VARIABLE IMPORTANCE
# ======================================

importances = gb_model.feature_importances_
features = X.columns

plt.figure()

plt.bar(features, importances)

plt.title("Variable Importance - Gradient Boosting")
plt.xlabel("Variables")
plt.ylabel("Importance")

plt.savefig(
OUTPUT_FOLDER + "GB_variable_importance.png",
dpi=300,
bbox_inches="tight"
)


# ======================================
# 8 OBSERVED VS PREDICTED
# ======================================

plt.figure()

plt.scatter(y_test, y_pred, alpha=0.4)

plt.xlabel("Observed Stress Probability")
plt.ylabel("Predicted Stress Probability")

plt.title("Observed vs Predicted Hydrological Stress")

plt.savefig(
OUTPUT_FOLDER + "GB_observed_vs_predicted.png",
dpi=300,
bbox_inches="tight"
)


# ======================================
# 9 SAVE RESULTS
# ======================================

results = pd.DataFrame({
"Observed": y_test,
"Predicted": y_pred
})

results.to_csv(
OUTPUT_FOLDER + "GB_results.csv",
index=False
)

print("\nGenerated files:")
print("GB_variable_importance.png")
print("GB_observed_vs_predicted.png")
print("GB_results.csv")