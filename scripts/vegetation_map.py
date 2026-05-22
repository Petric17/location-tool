#required libraries

import geopandas as gpd
from pystac_client import Client
import odc.stac 
import matplotlib.pyplot as plt
import os


#load the Cicarlau boundary data

boundary = gpd.read_file(r'C:\Users\petrica.s\geospatial_project\geo_work\data\raw\UAT\uat_boundary.gpkg')
boundary_4326 = boundary.to_crs(epsg=4326)
bbox = boundary_4326.total_bounds

#Connect to the Copernicus stac API 

print(f"Searching for Sentinel-2 data...")

client = Client.open("https://earth-search.aws.element84.com/v1")

#search for the NDVI data

search = client.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2024-06-01/2024-09-30",
    query={"eo:cloud_cover": {"lt": 5}}
)
items = list(search.items())

#Load the data

data = odc.stac.load(
    items[:1],  
    bands=["red", "nir"], 
    resolution=10,
    geopolygon=boundary_4326.geometry.iloc[0],
    chunks={}
)

#Calculate the NDVI

red = data.red.astype(float)
nir = data.nir.astype(float)
ndvi = (nir - red) / (nir + red)

#Visualise 

fig, ax = plt.subplots(figsize=(12, 10))
im = ndvi.isel(time=0).plot(ax=ax, cmap="RdYlGn", vmin=0, vmax=1, add_colorbar=True)
boundary_4326.boundary.plot(ax=ax, color="black", linewidth=2)

plt.title("Harta de Sănătate a Vegetatiei (NDVI) - Cicârlău (2024)", fontsize=16)
plt.axis("off")

#Save the figure
output_folder = r'C:\Users\petrica.s\geospatial_project\geo_work\Maps'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Save high resolution png
output_PATH = os.path.join(output_folder, 'cicarlau_ndvi_map.png')
plt.savefig(output_PATH, dpi=300, bbox_inches='tight')
print(f"Vegetation map saved to {output_PATH}")