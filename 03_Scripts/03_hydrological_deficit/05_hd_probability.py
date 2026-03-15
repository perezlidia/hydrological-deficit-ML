import rasterio

years = 65

with rasterio.open(
"D:/hydrological-stress/analysis_outputs/stress_frequency.tif"
) as src:

    freq = src.read(1)
    meta = src.meta

prob = freq / years

meta.update(dtype="float32")

with rasterio.open(
"D:/hydrological-stress/analysis_outputs/stress_probability.tif",
"w",**meta) as dst:
    dst.write(prob.astype("float32"),1)