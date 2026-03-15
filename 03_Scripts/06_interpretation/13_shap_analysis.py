import matplotlib
matplotlib.use("Agg")

import shap
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.ensemble import RandomForestRegressor


# -----------------------------
# PATHS
# -----------------------------

DATA_PATH = r"D:/hydrological-stress/ml_dataset/stress_dataset.csv"
OUTPUT_FOLDER = r"D:/hydrological-stress/ml_results"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# LOAD DATA
# -----------------------------

data = pd.read_csv(DATA_PATH)

X = data[['PR_mean','ETP_mean','Balance_mean']]
y = data['stress_probability']


# -----------------------------
# TRAIN MODEL
# -----------------------------

model = RandomForestRegressor(
    n_estimators=500,
    max_depth=10,
    random_state=42
)

model.fit(X,y)


# -----------------------------
# SHAP ANALYSIS
# -----------------------------

explainer = shap.Explainer(model, X)
shap_values = explainer(X)


# -----------------------------
# SHAP SUMMARY PLOT
# -----------------------------

shap.summary_plot(
    shap_values,
    X,
    show=False
)

output_path = os.path.join(
    OUTPUT_FOLDER,
    "shap_summary.png"
)

plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.close()


print("SHAP plot saved in:")
print(output_path)