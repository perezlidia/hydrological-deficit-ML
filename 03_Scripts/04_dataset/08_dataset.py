import rasterio
import pandas as pd

points = pd.read_csv(r"D:\outputs\stress_points.csv")

rasters = {
"PR_mean": r"D:\outputs\PR_mean.tif",
"ETP_mean": r"D:\outputs\ETP_mean.tif",
"Balance_me": r"D:\outputs\Balance_mean.tif"
}

for var, path in rasters.items():

    values = []

    with rasterio.open(path) as src:

        for x,y in zip(points.x, points.y):
            row,col = src.index(x,y)
            val = src.read(1)[row,col]
            values.append(val)

    points[var] = values

points.to_csv(
r"D:\outputs\stress_prob.csv",
index=False
)