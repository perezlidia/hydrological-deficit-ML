import rasterio
import numpy as np
import pandas as pd
import joblib
import os
import sys


# -------------------------------------------------
# PATHS
# -------------------------------------------------

PR_PATH = r"D:/hydrological-stress/rasters_lambert/PR_mean.tif"
ETP_PATH = r"D:/hydrological-stress/rasters_lambert/ETP_mean.tif"
BALANCE_PATH = r"D:/hydrological-stress/rasters_lambert/Balance_mean.tif"

MODEL_PATH = r"D:/hydrological-stress/ml_models/random_forest_model.joblib"

OUTPUT_PATH = r"D:/hydrological-stress/results/stress_prediction_map.tif"


# -------------------------------------------------
# CHECK MODEL
# -------------------------------------------------

if not os.path.exists(MODEL_PATH):

    print("ERROR: Model file not found")
    print(MODEL_PATH)
    sys.exit()

print("Loading ML model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully")


# -------------------------------------------------
# READ RASTERS
# -------------------------------------------------

print("Reading rasters...")

with rasterio.open(PR_PATH) as src:
    pr = src.read(1)
    meta = src.meta.copy()
    nodata = src.nodata

with rasterio.open(ETP_PATH) as src:
    etp = src.read(1)

with rasterio.open(BALANCE_PATH) as src:
    balance = src.read(1)

print("Rasters loaded")


# -------------------------------------------------
# CHECK RASTER DIMENSIONS
# -------------------------------------------------

if not (pr.shape == etp.shape == balance.shape):

    print("ERROR: Raster dimensions do not match")
    sys.exit()

rows, cols = pr.shape


# -------------------------------------------------
# STACK VARIABLES
# -------------------------------------------------

stack = np.stack([pr, etp, balance], axis=-1)

stack_2d = stack.reshape(rows * cols, 3)


# -------------------------------------------------
# HANDLE NODATA / NAN / INF
# -------------------------------------------------

mask_nan = np.any(np.isnan(stack_2d), axis=1)
mask_inf = np.any(np.isinf(stack_2d), axis=1)

if nodata is not None:
    mask_nodata = np.any(stack_2d == nodata, axis=1)
else:
    mask_nodata = np.zeros(stack_2d.shape[0], dtype=bool)

mask = mask_nan | mask_inf | mask_nodata

valid_pixels = stack_2d[~mask]

print("Valid pixels for prediction:", valid_pixels.shape[0])


# -------------------------------------------------
# CREATE DATAFRAME (fix sklearn warning)
# -------------------------------------------------

X_pred = pd.DataFrame(
    valid_pixels,
    columns=['PR_mean', 'ETP_mean', 'Balance_mean']
)


# -------------------------------------------------
# PREDICT
# -------------------------------------------------

print("Predicting stress probability...")

predictions = model.predict(X_pred)


# -------------------------------------------------
# REBUILD FULL MAP
# -------------------------------------------------

full_predictions = np.full(stack_2d.shape[0], np.nan)

full_predictions[~mask] = predictions

prediction_map = full_predictions.reshape(rows, cols)


# -------------------------------------------------
# SAVE OUTPUT RASTER
# -------------------------------------------------

meta.update(
    dtype=rasterio.float32,
    count=1
)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("Saving prediction raster...")

with rasterio.open(OUTPUT_PATH, "w", **meta) as dst:
    dst.write(prediction_map.astype(rasterio.float32), 1)


print("\nStress prediction map saved at:")
print(OUTPUT_PATH)