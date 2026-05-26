import zipfile
import os
import shutil


zip_path = r"C:\Users\petrica.s\geospatial_project\geo_work\data\raw\cdse_data\S2A_MSIL2A_20241128T092331_N0511_R093_T34TFT_20241128T122153.SAFE.zip"
output_dir = r"C:\Users\petrica.s\geospatial_project\geo_work\data\processed\nir_band"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#Bands to find 

bands_to_find = ["B08_10m.jp2", "B04_10m.jp2"]

with zipfile.ZipFile(zip_path, 'r') as z:
    all_files = z.namelist()
    
    for band_name in bands_to_find:
        match = next((f for f in all_files if band_name in f), None)
        if match:
             #Extract the file to the output directory
             z.extract(match, path=output_dir)
             print(f"Extracted {match} to {output_dir}")
        else:
            print(f"Band {band_name} not found in the ZIP file.")

print(f"All bands extracted to {output_dir}")

