import rasterio
import numpy as np
import glob

files = sorted(glob.glob(
"D:/hydrological-stress/hydrological_stress/stress_*.tif"
))

stack = []

for f in files:
    with rasterio.open(f) as src:
        stack.append(src.read(1))

stack = np.array(stack)

frequency = np.sum(stack,axis=0)

with rasterio.open(files[0]) as src:
    meta = src.meta

meta.update(dtype="float32")

with rasterio.open(
"D:/hydrological-stress/analysis_outputs/stress_frequency.tif",
"w",**meta) as dst:
    dst.write(frequency.astype("float32"),1)