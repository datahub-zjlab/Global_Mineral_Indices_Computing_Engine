import argparse
import GMI_ComputeEngine_ODPS as GMI_CE
from GMI_ComputeEngine_ODPS.computing.data_types import Column, ColumnType

# SET API KEY
GMI_CE.api_key = "NDUkMTczMjY5OTcwNyRqYXh5anBnbQ"
GMI_CE.api_baseurl = "http://221.228.10.51:18080/platform/"

# 1. Example column of ODPS table
columns = [
    Column(name='granule_id', type=ColumnType.STRING, comment='Unique identifier for each granule'),
    Column(name='min_row', type=ColumnType.BIGINT, comment='Minimum row index of the image data'),
    Column(name='min_col', type=ColumnType.BIGINT, comment='Minimum column index of the image data'),
    Column(name='max_row', type=ColumnType.BIGINT, comment='Maximum row index of the image data'),
    Column(name='max_col', type=ColumnType.BIGINT, comment='Maximum column index of the image data'),
    Column(name='tile_index_x', type=ColumnType.BIGINT, comment='Tile index on the X-axis'),
    Column(name='tile_index_y', type=ColumnType.BIGINT, comment='Tile index on the Y-axis'),
    Column(name='tile_info', type=ColumnType.STRING, comment='Additional information about the tile'),
    Column(name='meta', type=ColumnType.STRING, comment='Meta data'),
    Column(name='atmoshpheric_correction_paras', type=ColumnType.STRING, comment='Atmoshpheric correction parameters by 6S model'),
    Column(name='VNIR_Swath_ImageData1', type=ColumnType.STRING, comment='VNIR Swath image data for band 1'),
    Column(name='VNIR_Swath_ImageData2', type=ColumnType.STRING, comment='VNIR Swath image data for band 2'),
    Column(name='VNIR_Swath_ImageData3', type=ColumnType.STRING, comment='VNIR Swath image data for band 3'),
    Column(name='SWIR_Swath_ImageData4', type=ColumnType.STRING, comment='SWIR Swath image data for band 4'),
    Column(name='SWIR_Swath_ImageData5', type=ColumnType.STRING, comment='SWIR Swath image data for band 5'),
    Column(name='SWIR_Swath_ImageData6', type=ColumnType.STRING, comment='SWIR Swath image data for band 6'),
    Column(name='SWIR_Swath_ImageData7', type=ColumnType.STRING, comment='SWIR Swath image data for band 7'),
    Column(name='SWIR_Swath_ImageData8', type=ColumnType.STRING, comment='SWIR Swath image data for band 8'),
    Column(name='SWIR_Swath_ImageData9', type=ColumnType.STRING, comment='SWIR Swath image data for band 9'),
    Column(name='modis_vnir_swath_imagedata1', type=ColumnType.STRING, comment='VNIR Swath modis image data for band 1'),
    Column(name='modis_vnir_swath_imagedata2', type=ColumnType.STRING, comment='VNIR Swath modis image data for band 2'),
    Column(name='modis_vnir_swath_imagedata3', type=ColumnType.STRING, comment='VNIR Swath modis image data for band 3'),
    Column(name='modis_vnir_swath_imagedata4', type=ColumnType.STRING, comment='VNIR Swath modis image data for band 4'),
    Column(name='modis_swir_swath_imagedata5', type=ColumnType.STRING, comment='SWIR Swath modis image data for band 5'),
    Column(name='modis_swir_swath_imagedata6', type=ColumnType.STRING, comment='SWIR Swath modis image data for band 6'),
    Column(name='modis_swir_swath_imagedata7', type=ColumnType.STRING, comment='SWIR Swath modis image data for band 7'),
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload table to ODPS.')
    parser.add_argument('csv_file', type=str, help='Path to the output table to be uploaded.')
    parser.add_argument('source_table', type=str, help='Source table name in ODPS.')


    args = parser.parse_args()
    csv_path = args.csv_file
    source_table = args.source_table
    
    result = GMI_CE.Computing.create_table(name=source_table,columns=columns)
    result = GMI_CE.Computing.upload_table_data(name=source_table, append=True, csv_filepath=csv_path)
