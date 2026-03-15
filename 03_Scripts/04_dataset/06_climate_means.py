import rasterio
import numpy as np
import glob

def raster_mean(folder,pattern,output):

    files = sorted(glob.glob(folder + pattern))

    stack = []

    for f in files:
        with rasterio.open(f) as src:
            stack.append(src.read(1))

    stack = np.array(stack)

    mean = np.mean(stack,axis=0)

    with rasterio.open(files[0]) as src:
        meta = src.meta

    meta.update(dtype="float32")

    with rasterio.open(output,"w",**meta) as dst:
        dst.write(mean.astype("float32"),1)


raster_mean(
"D:/hydrological-stress/rasters_lambert/",
"PR_*_lambert.tif",
"D:/hydrological-stress/analysis_outputs/pr_mean.tif"
)

raster_mean(
"D:/hydrological-stress/rasters_lambert/",
"ETP_*_lambert.tif",
"D:/hydrological-stress/analysis_outputs/etp_mean.tif"
)

raster_mean(
"D:/hydrological-stress/water_balance/",
"balance_*.tif",
"D:/hydrological-stress/analysis_outputs/balance_mean.tif"
)