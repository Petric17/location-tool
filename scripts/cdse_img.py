import os
import zipfile
import shutil

zip_path = r"C:\Users\petrica.s\geospatial_project\geo_work\data\raw\cdse_data\S2A_MSIL2A_20241128T092331_N0511_R093_T34TFT_20241128T122153.SAFE.zip"
output_dir = r"C:\Users\petrica.s\geospatial_project\geo_work\data\processed\cdse_img"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory at {output_dir}")

#Find the TCI (true color image) file in the zip

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    tci_path_in_zip = next((f for f in zip_ref.namelist() if 'TCI_10m.jp2' in f), None)
    
    if tci_path_in_zip:
        print(f"Found: {tci_path_in_zip}")
        
        # Extract the file to the output directory
        zip_ref.extract(tci_path_in_zip, path=output_dir)
        
        # Define where it landed and where we WANT it
        temp_extracted_path = os.path.join(output_dir, tci_path_in_zip)
        final_filename = os.path.basename(tci_path_in_zip)
        final_destination = os.path.join(output_dir, final_filename)
        
        if os.path.exists(temp_extracted_path):
            shutil.move(temp_extracted_path, final_destination)
            print(f"Moved: {final_destination}")
            
            top_level_folder = tci_path_in_zip.split('/')[0]
            shutil.rmtree(os.path.join(output_dir, top_level_folder), ignore_errors=True)
            print("cleaned up temporary folders.")
    else:
        print("TCI_10m.jp2 not found in the ZIP file.")


