import os
import glob
import rasterio
import numpy as np

workspace = r"D:/hydrological-stress/rasters_lambert"
output_folder = r"D:/hydrological-stress/water_balance"

os.makedirs(output_folder, exist_ok=True)

pr_rasters = glob.glob(workspace + "/PR_*_lambert.tif")

for pr in pr_rasters:

    year = os.path.basename(pr).split("_")[1]

    etp = workspace + f"/ETP_{year}_lambert.tif"

    if os.path.exists(etp):

        with rasterio.open(pr) as pr_src, rasterio.open(etp) as etp_src:

            pr_data = pr_src.read(1)
            etp_data = etp_src.read(1)

            balance = pr_data - etp_data

            meta = pr_src.meta

        out = output_folder + f"/balance_{year}.tif"

        with rasterio.open(out,"w",**meta) as dst:
            dst.write(balance.astype("float32"),1)

        print("Balance created:",year)