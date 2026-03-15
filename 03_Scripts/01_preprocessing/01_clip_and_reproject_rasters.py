import os
import glob
import rasterio
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
import geopandas as gpd


# --------------------------------------------------
# FIX PROJ CONFLICT (PostGIS vs Rasterio)
# --------------------------------------------------

os.environ["PROJ_LIB"] = r"C:\Users\Lidia\AppData\Roaming\Python\Python312\site-packages\pyproj\proj_dir\share\proj"


# --------------------------------------------------
# PATHS
# --------------------------------------------------

etp_folder = r"D:/hydrological-stress/data_raw/evapotranspiration"
pr_folder  = r"D:/hydrological-stress/data_raw/precipitation"

clip_folder = r"D:/hydrological-stress/rasters_clipped"
output_folder = r"D:/hydrological-stress/rasters_lambert"

mask_path = r"D:/hydrological-stress/study_area/Area_base.shp"

os.makedirs(clip_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)


# --------------------------------------------------
# LOAD STUDY AREA
# --------------------------------------------------

gdf = gpd.read_file(mask_path)

print("Study area CRS:", gdf.crs)


# --------------------------------------------------
# COLLECT RASTERS
# --------------------------------------------------

rasters = []
rasters.extend(glob.glob(etp_folder + "/*.tif"))
rasters.extend(glob.glob(pr_folder + "/*.tif"))

print("Total rasters found:", len(rasters))


# --------------------------------------------------
# TARGET CRS (Lambert)
# --------------------------------------------------

dst_crs = "EPSG:5070"


# --------------------------------------------------
# PROCESS RASTERS
# --------------------------------------------------

for raster in rasters:

    name = os.path.basename(raster)

    # add prefix depending on folder
    if "evapotranspiration" in raster.lower():
        name = "ETP_" + name
    elif "precipitation" in raster.lower():
        name = "PR_" + name

    print("\nProcessing:", name)

    try:

        with rasterio.open(raster) as src:

            print("Raster CRS:", src.crs)

            if src.crs is None:
                print("WARNING: Raster has no CRS. Skipping.")
                continue

            # reproject shapefile to raster CRS
            gdf_proj = gdf.to_crs(src.crs)
            geoms = gdf_proj.geometry.values

            # -----------------------------
            # CLIP RASTER
            # -----------------------------

            clipped, transform = mask(src, geoms, crop=True)

            meta = src.meta.copy()
            meta.update({
                "height": clipped.shape[1],
                "width": clipped.shape[2],
                "transform": transform
            })

        clip_path = os.path.join(
            clip_folder,
            name.replace(".tif","_clip.tif")
        )

        with rasterio.open(clip_path,"w",**meta) as dst:
            dst.write(clipped)


        # -----------------------------
        # REPROJECT TO LAMBERT
        # -----------------------------

        with rasterio.open(clip_path) as src:

            transform, width, height = calculate_default_transform(
                src.crs,
                dst_crs,
                src.width,
                src.height,
                *src.bounds
            )

            kwargs = src.meta.copy()

            kwargs.update({
                "crs": dst_crs,
                "transform": transform,
                "width": width,
                "height": height
            })

            output_path = os.path.join(
                output_folder,
                name.replace(".tif","_lambert.tif")
            )

            with rasterio.open(output_path,"w",**kwargs) as dst:

                for i in range(1, src.count + 1):

                    reproject(
                        source=rasterio.band(src,i),
                        destination=rasterio.band(dst,i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.bilinear
                    )

    except Exception as e:

        print("Skipping raster due to error:")
        print(e)


print("\nPROCESS COMPLETED")