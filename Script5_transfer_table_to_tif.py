import os
import rasterio
import json
import argparse

import numpy as np
import pandas as pd

from aster_core.functional_group import functional_group_names

tile_size = 1024
default_dtype = np.int16

def save_to_geotif(data,meta,bands,path):
    data=np.asarray(data)
    data = data.astype(default_dtype)

    meta["dtype"] = rasterio.int16
    meta["count"] = data.shape[0]

    with rasterio.open(path, "w", **meta) as dest:
        dest.write(data)
        if bands is not None:
            for index in range(len(bands)):
                dest.set_band_description(index + 1, bands[index])

if __name__=="__main__":
    parser = argparse.ArgumentParser('Transfer table row to geoTIFF file.')
    parser.add_argument('csv_file', type=str, help='Path to the downloaded table.')
    parser.add_argument('save_path', type=str, default='./', help='Path to the output geoTIFF file.')
    parser.add_argument('label', type=str, default='MineralIndices', help='Data label to the output geoTIFF file, [ASTRef, MineralIndices]')
    args = parser.parse_args()

    csv_path = args.csv_file
    save_path = args.savepath
    label = args.label

    if label=='ASTRef':
        bands = ["vnir_swath_imagedata1", "vnir_swath_imagedata2", "vnir_swath_imagedata3",
                 "swir_swath_imagedata4", "swir_swath_imagedata5", "swir_swath_imagedata6",
                 "swir_swath_imagedata7", "swir_swath_imagedata8", "swir_swath_imagedata9"]
    elif label=='MineralIndices':
        bands = functional_group_names

    os.makedirs(save_path,exist_ok=True)

    df=pd.read_csv(csv_path)
    for row in df.iterrows():
        tile_index_x = row.tile_index_x
        tile_index_y = row.tile_index_y
        meta = json.loads(row.meta)

        path=os.path.join(save_path,f"Aster_{label}_{tile_index_x}-{tile_index_y}.tiff")
        
        data=[]
        for index in range(len(bands)):
            hex_string = row[bands[index]]
            byte_data = bytes.fromhex(hex_string)
            band_data = np.frombuffer(byte_data, dtype=default_dtype)
            data.append(band_data.reshape((tile_size,tile_size)))
            
        save_to_geotif(data,meta,bands,path)

