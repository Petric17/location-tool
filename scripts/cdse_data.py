import os
import requests

#Credentials and folder path

USERNAME = os.getenv(r"CDSE_USER")
PASSWORD = os.getenv(r"CDSE_PASS")

SAVE_PATH = r"C:\Users\petrica.s\geospatial_project\geo_work\data\raw\cdse_data"
folder_to_make = os.path.dirname(SAVE_PATH)
os.makedirs(folder_to_make, exist_ok=True)
print(f"Ensuring directory exists: {folder_to_make}")

#get the digital token for the CDSE API

def Get_Token(): 
    auth_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    data = {
        "client_id": "cdse-public",
        "username": USERNAME,
        "password": PASSWORD,
        "grant_type": "password"
    }
    response = requests.post(auth_url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

#download the data from the CDSE API

def download_data(product_id, product_name):
    token = Get_Token()
    download_url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream"
    }

    save_path = os.path.join(SAVE_PATH, f"{product_name}.zip")

    print(f"Downloading {product_name} to {save_path}")

    with requests.get(download_url, headers=headers, stream=True, allow_redirects=True) as r:
        if r.status_code == 401:
            print("Unauthorized. Refreshing token...")
            return
        
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    print(".", end="", flush=True)

   


#main search function

search_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
poly = "POLYGON((23.35 47.63, 23.45 47.63, 23.45 47.70, 23.35 47.70, 23.35 47.63))"
query_filter = (
    "Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/Value eq 'S2MSI2A') "
    "and ContentDate/Start gt 2023-06-01T00:00:00.000Z "
    f"and Intersects(footprint=geography'SRID=4326;{poly}')"
)

params = {"$filter": query_filter, "$top": 1}
print(f"Connecting to Copernicus...")
response = requests.get(search_url, params=params)

if response.status_code == 200:
    result = response.json().get("value", [])
    if result:
        target_product = result[0]
        download_data(target_product["Id"], target_product["Name"])
    else:
        print("No products found")

else:
    print(f"Error {response.status_code}: {response.text}")
