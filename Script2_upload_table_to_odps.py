import os
import argparse
import pandas as pd
from odps import ODPS
from odps.models import TableSchema, Column
from aster_core.odps import upload_data_to_odps

# Set environment variables for ODPS authentication
os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'] = ""
os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'] = ""

# ODPS project and endpoint configuration
odps_project = "" 
odps_endpoint = ""

# Initialize ODPS client
o = ODPS(
    os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'),
    os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
    project=odps_project,
    endpoint=odps_endpoint
)


# ODPS table name
table_name = "demo_aster_global_tile_table"

# Create new table or not
create_table_flag = False


# Example for aster data table schema
columns = [
    Column(name='granule_id', type='string', comment='Unique identifier for each granule'),
    Column(name='min_row', type='bigint', comment='Minimum row index of the image data'),
    Column(name='min_col', type='bigint', comment='Minimum column index of the image data'),
    Column(name='max_row', type='bigint', comment='Maximum row index of the image data'),
    Column(name='max_col', type='bigint', comment='Maximum column index of the image data'),
    Column(name='tile_index_x', type='bigint', comment='Tile index on the X-axis'),
    Column(name='tile_index_y', type='bigint', comment='Tile index on the Y-axis'),
    Column(name='tile_info', type='string', comment='Additional information about the tile'),
    Column(name='meta', type='string', comment='Meta data'),
    Column(name='atmoshpheric_correction_paras', type='string', comment='Atmoshpheric correction parameters by 6S model'),
    Column(name='VNIR_Swath_ImageData1', type='binary', comment='VNIR Swath image data for band 1'),
    Column(name='VNIR_Swath_ImageData2', type='binary', comment='VNIR Swath image data for band 2'),
    Column(name='VNIR_Swath_ImageData3', type='binary', comment='VNIR Swath image data for band 3'),
    Column(name='SWIR_Swath_ImageData4', type='binary', comment='SWIR Swath image data for band 4'),
    Column(name='SWIR_Swath_ImageData5', type='binary', comment='SWIR Swath image data for band 5'),
    Column(name='SWIR_Swath_ImageData6', type='binary', comment='SWIR Swath image data for band 6'),
    Column(name='SWIR_Swath_ImageData7', type='binary', comment='SWIR Swath image data for band 7'),
    Column(name='SWIR_Swath_ImageData8', type='binary', comment='SWIR Swath image data for band 8'),
    Column(name='SWIR_Swath_ImageData9', type='binary', comment='SWIR Swath image data for band 9'),
    Column(name='modis_vnir_swath_imagedata1', type='binary', comment='VNIR Swath modis image data for band 1'),
    Column(name='modis_vnir_swath_imagedata2', type='binary', comment='VNIR Swath modis image data for band 2'),
    Column(name='modis_vnir_swath_imagedata3', type='binary', comment='VNIR Swath modis image data for band 3'),
    Column(name='modis_vnir_swath_imagedata4', type='binary', comment='VNIR Swath modis image data for band 4'),
    Column(name='modis_swir_swath_imagedata5', type='binary', comment='SWIR Swath modis image data for band 5'),
    Column(name='modis_swir_swath_imagedata6', type='binary', comment='SWIR Swath modis image data for band 6'),
    Column(name='modis_swir_swath_imagedata7', type='binary', comment='SWIR Swath modis image data for band 7'),
]

# Create new ODPS table with table schema
def create_table(table_name, columns):
    """
    Create a table in ODPS if it does not already exist.
    
    :param table_name: Name of the table to be created.
    :param columns: List of Column objects defining the table schema.
    """
    schema = TableSchema(columns=columns)
    o.create_table(table_name, schema, if_not_exists=True)
    print(f"Table {table_name} has been successfully created.")

# Create new table if flag is TRUE
if create_table_flag:
    create_table(table_name, columns)

# Retrieve existing tables
aster_global_tile_table = o.get_table(table_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an ASTER HDF file.')
    parser.add_argument('csv_file', type=str, help='Path to the output table to be uploaded.')


    args = parser.parse_args()
    output_csv = args.csv_file

    result_df = pd.read_csv(output_csv)

    result_list = [row.to_dict() for index, row in result_df.iterrows()]

    if len(result_list) > 0:
        upload_data_to_odps(result_list, aster_global_tile_table)