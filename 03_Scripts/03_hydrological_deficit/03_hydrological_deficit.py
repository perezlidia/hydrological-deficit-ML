import rasterio
import numpy as np
import glob
import os

input_folder = r"D:/hydrological-stress/water_balance"
output_folder = r"D:/hydrological-stress/hydrological_stress"

os.makedirs(output_folder, exist_ok=True)

files = glob.glob(input_folder + "/balance_*.tif")

for f in files:

    year = os.path.basename(f).split("_")[1].split(".")[0]

    with rasterio.open(f) as src:

        data = src.read(1)

        stress = np.where(data < 0, 1, 0)

        meta = src.meta

    out = output_folder + f"/stress_{year}.tif"

    with rasterio.open(out,"w",**meta) as dst:
        dst.write(stress.astype("float32"),1)

    print("Stress map created:",year)