import rasterio
import pandas as pd
import numpy as np

raster = r"D:/hydrological-stress/analysis_outputs/stress_probability.tif"

with rasterio.open(raster) as src:

    data = src.read(1)
    transform = src.transform

rows,cols = np.where(~np.isnan(data))

xs,ys = rasterio.transform.xy(transform,rows,cols)

df = pd.DataFrame({
"x":xs,
"y":ys,
"stress_probability":data[rows,cols]
})

df.to_csv(
"D:/hydrological-stress/ml_dataset/stress_points.csv",
index=False
)