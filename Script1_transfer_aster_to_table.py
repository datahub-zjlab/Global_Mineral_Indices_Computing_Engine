import os
import argparse
import numpy as np
import pandas as pd
from osgeo import gdal
from aster_core.global_grid import GlobalRasterGrid
from aster_core.hdf_utils import parse_meta, get_projection, get_transform, get_width_height
from aster_core.utils import geotransform_to_affine, affine_to_bbox, bbox2bbox
from aster_core.mosaic_tile import extract_granule,extract_geotif
from aster_core.odps import get_min_bounding_box, matrix_to_byte
from aster_core.atmospheric_correction import get_aod_from_tile_bbox,get_dem_from_tile_bbox,get_atmospheric_correction_parameters,calculate_atmospheric_correction_parameters

def get_bbox_from_aster(aster_file, dst_crs='epsg:3857'):
    """
    Get bounding box information from an ASTER HDF file and transform it to the target coordinate system.
    
    :param aster_file: Path to the ASTER HDF file.
    :param dst_crs: Target coordinate system, default is 'epsg:3857'.
    :return: Transformed bounding box.
    """
    ds = gdal.Open(aster_file)
    meta = ds.GetMetadata()
    meta_parser = parse_meta(meta)
    projection = get_projection(meta_parser)
    geotransform = get_transform(meta_parser, 'ImageData1')
    affine = geotransform_to_affine(geotransform)
    width, height = get_width_height(meta_parser, 'ImageData1')
    bbox = affine_to_bbox(affine, width, height)
    dst_bbox = bbox2bbox(bbox, projection, dst_crs)
    return dst_bbox

def process_tile(tile_index, aster_file, modis_ref_files, bands, aster_res, tile_size, granule_id, atmoshpheric_correction_paras):
    """
    Process a single tile from the ASTER HDF file.
    
    :param tile_index: Index of the tile to process.
    :param aster_file: Path to the ASTER HDF file.
    :param bands: List of bands to process.
    :param aster_res: ASTER data resolution.
    :param tile_size: Size of the tile.
    :param granule_id: ID of the granule.
    :return: Dictionary containing processed tile data.
    """
    global_grid = GlobalRasterGrid(resolution=aster_res, tile_size=tile_size)
    tile_bbox = global_grid.get_tile_bounds(tile_index)
    data, meta = extract_granule(aster_file, bands, tile_bbox, global_grid.tile_size, global_grid.projection)
    modis_ref_data = extract_geotif(modis_ref_files, tile_bbox, 256, global_grid.projection)
    result = {}

    if data is not None:
        zip_data, bounding_box_info = get_min_bounding_box(data)
        zip_data = zip_data.astype(np.uint8)
        min_row, min_col, max_row, max_col = bounding_box_info
        tile_index_x, tile_index_y = tile_index

        result['granule_id'] = granule_id
        result['min_row'] = min_row
        result['min_col'] = min_col
        result['max_row'] = max_row
        result['max_col'] = max_col
        result['tile_index_x'] = tile_index_x
        result['tile_index_y'] = tile_index_y
        result['tile_info'] = f'res-{aster_res}_tilesize-{tile_size}'
        result['meta'] = str(meta)
        result['atmoshpheric_correction_paras'] = str(atmoshpheric_correction_paras)

        for i, band in enumerate(bands):
            result[band.replace(':','_')] = matrix_to_byte(zip_data[i])
        for i in range(len(modis_ref_data)):
            result[f'modis_bands_{i}'] = matrix_to_byte(modis_ref_data[i])

    return result

def process_aster_file(aster_file, modis_aod_files, gdem_files, modis_ref_files, bands, tile_index, aster_res=30, tile_size=1024):
    """
    Process an ASTER HDF file, extract data, and compress it.
    
    :param aster_file: Path to the ASTER HDF file.
    :param bands: List of bands to process.
    :param aster_res: ASTER data resolution, default is 30.
    :param tile_size: Tile size, default is 1024.
    :return: List of result dictionaries containing compressed data.
    """
    global_grid = GlobalRasterGrid(resolution=aster_res, tile_size=tile_size)
    dst_bbox = get_bbox_from_aster(aster_file, dst_crs='epsg:3857')
    tile_index_list = global_grid.get_tile_list(dst_bbox)
    if not tile_index in tile_index_list:
        raise RuntimeError(f"Tile index: {tile_index} of global grid not in the area of this aster file!")

    granule_id = os.path.basename(aster_file).split('.')[0]

    hdf_ds = gdal.Open(aster_file)
    meta = hdf_ds.GetMetadata()

    result_list = []

    try:
        tile_bbox = global_grid.get_tile_bounds(tile_index)

        aod = get_aod_from_tile_bbox(modis_aod_files,tile_bbox,global_grid.projection)
        dem = get_dem_from_tile_bbox(gdem_files,tile_bbox,global_grid.projection)

        atmoshpheric_correction_paras = get_atmospheric_correction_parameters(meta,bands,aod,dem)

        result = process_tile(tile_index, aster_file, modis_ref_files, bands, aster_res, tile_size, granule_id, atmoshpheric_correction_paras)
        if result:
            result_list.append(result)
    except Exception as e:
        print(f"Tile processing failed for tile_index {tile_index}: {e}")

    return result_list

def hdf2tile_odps(aster_file,modis_aod_files,gdem_files,modis_ref_files,tile_index,output_csv):
    """
    Convert an ASTER HDF file to tiles and upload the data to ODPS.
    
    :param aster_file: Path to the ASTER HDF file.
    """
    bands = ['VNIR_Swath:ImageData1', 'VNIR_Swath:ImageData2', 'VNIR_Swath:ImageData3',
             'SWIR_Swath:ImageData4', 'SWIR_Swath:ImageData5', 'SWIR_Swath:ImageData6',
             'SWIR_Swath:ImageData7', 'SWIR_Swath:ImageData8', 'SWIR_Swath:ImageData9']
    
    try:
        result_list = process_aster_file(aster_file, modis_aod_files, gdem_files, modis_ref_files, bands, tile_index)
        if len(result_list) > 0:
            result_df = pd.DataFrame(result_list)
            result_df.to_csv(output_csv, index=False)
    except Exception as e:
        print(f"Error processing HDF file: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an ASTER HDF file.')
    parser.add_argument('aster_file', type=str, help='Path to the ASTER HDF file.')
    parser.add_argument('modis_aod_files', type=str, help='Path to the MODIS AOD HDF file.')
    parser.add_argument('gdem_files', type=str, help='Path to the ASTER GDEM file.')
    parser.add_argument('modis_ref_file', type=str, help='Path to the MODIS reflectance file.')
    parser.add_argument('tile_index_x', type=int, help='tile index x')
    parser.add_argument('tile_index_y', type=int, help='tile index y')
    parser.add_argument('csv_file,',type=str, help='Path to save output table.')

    args = parser.parse_args()
    aster_file = args.aster_file
    modis_aod_files = args.modis_files.split(',')
    gdem_files = args.gdem_files.split(',')
    modis_ref_file = args.modis_ref_file
    tile_index = (args.tile_index_x,args.tile_index_y)
    output_csv = args.csv_file

    hdf2tile_odps(aster_file,modis_aod_files,gdem_files,modis_ref_file,tile_index,output_csv)