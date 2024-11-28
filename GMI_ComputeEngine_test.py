import GMI_ComputeEngine_ODPS as GMI_CE
from GMI_ComputeEngine_ODPS.computing.data_types import Column, ColumnType

# SET API KEY
GMI_CE.api_key = "NDUkMTczMjY5OTcwNyRqYXh5anBnbQ"
# GMI_CE.api_key ="MiQxNjkyMTU1Nzk3JGJxaXplaXRu"
GMI_CE.api_baseurl = "http://221.228.10.51:18080/platform/"

# 1. CREATE TABLE  FOR SOURCE DATA
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

source_table="demo_aster_global_tile_table_1"
result = GMI_CE.Computing.create_table(name=source_table,columns=columns)
print(result)
result = GMI_CE.Computing.upload_table_data(name="demo_aster_global_tile_table_1", append=True, csv_filepath="/data/gyw/GF_Preprocess/aster_core/GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv")
print(result)

# 2.Use functions

# 2.1 output="merge"/"color",input is the 9 channels of original remote sensing data for Aster.
# If the table to store the results does not exist, you must create it first. The following code is about how to use GMI_ComputeEngine to create a table.
source_table="demo_aster_global_tile_table"
results_table="demo_results_color"
output="color"
type="AC"
columns = [
    Column("tile_index_x", ColumnType.BIGINT),
    Column("tile_index_y", ColumnType.BIGINT),
    Column("meta", ColumnType.STRING),
    Column("code", ColumnType.STRING),
    Column("vnir_swath_imagedata1", ColumnType.STRING),
    Column("vnir_swath_imagedata2", ColumnType.STRING),
    Column("vnir_swath_imagedata3", ColumnType.STRING),
    Column("swir_swath_imagedata4", ColumnType.STRING),
    Column("swir_swath_imagedata5", ColumnType.STRING),
    Column("swir_swath_imagedata6", ColumnType.STRING),
    Column("swir_swath_imagedata7", ColumnType.STRING),
    Column("swir_swath_imagedata8", ColumnType.STRING),
    Column("swir_swath_imagedata9", ColumnType.STRING),
    Column("cloud_mask", ColumnType.STRING),
]

result = GMI_CE.Computing.create_table(name=results_table,columns=columns)
print(result)
# set odps.sql.python.version=cp37;
# Run the UDF you create to get the results of the preprocessed remote sensing images
SQL=f'''
insert overwrite table {results_table} 
select x as tile_index_x ,y as tile_index_y,results.meta as meta,results.code as code,
results.data[0],results.data[1],results.data[2],results.data[3],results.data[4],results.data[5], results.data[6],results.data[7],
results.data[8], results.data[9]
from (SELECT tile_index_x as x, tile_index_y as y,
GMI_ComputeEngine(
get_json_object(json_object('tile_info',tile_info,"granule_id",granule_id,"tile_index_x",tile_index_x,"tile_index_y",tile_index_y,
"min_row",min_row,"min_col",min_col,"max_row",max_row,"max_col",max_col,
"atmospheric_correction_paras",atmospheric_correction_paras,
"bands","VNIR_Swath_ImageData1-VNIR_Swath_ImageData2-VNIR_Swath_ImageData3-SWIR_Swath_ImageData4-SWIR_Swath_ImageData5-SWIR_Swath_ImageData6-SWIR_Swath_ImageData7-SWIR_Swath_ImageData8-SWIR_Swath_ImageData9",
"type","{type}","output",{output}), '$'),  meta,
array(VNIR_Swath_ImageData1,VNIR_Swath_ImageData2,VNIR_Swath_ImageData3,SWIR_Swath_ImageData4,SWIR_Swath_ImageData5,
SWIR_Swath_ImageData6,SWIR_Swath_ImageData7,SWIR_Swath_ImageData8,SWIR_Swath_ImageData9),
array(modis_VNIR_Swath_ImageData1,modis_VNIR_Swath_ImageData2,modis_VNIR_Swath_ImageData3,modis_VNIR_Swath_ImageData4,
modis_SWIR_Swath_ImageData5,modis_SWIR_Swath_ImageData6,modis_SWIR_Swath_ImageData7)) 
as results FROM {source_table} GROUP BY tile_index_x, tile_index_y);'''

job_id = GMI_CE.Computing.create_job(sql=SQL)
print(job_id)
status = GMI_CE.Computing.get_job_status(job_id=job_id)
print(status)

# 2.2 output="fg",input is the 9 channels of original remote sensing data for Aster.
# Create a table to store functional groups if not exists.
source_table="demo_aster_global_tile_table"
results_table="demo_results_fg"
output="fg"
type="AC"
columns = [
    Column("tile_index_x", ColumnType.BIGINT),
    Column("tile_index_y", ColumnType.BIGINT),
    Column("meta", ColumnType.STRING),
    Column("code", ColumnType.STRING),
    Column("ferric_iron", ColumnType.STRING),
    Column("ferrous_iron", ColumnType.STRING),
    Column("laterite", ColumnType.STRING),
    Column("gosson", ColumnType.STRING),
    Column("ferrous_silicates", ColumnType.STRING),
    Column("ferric_oxdes", ColumnType.STRING),
    Column("carbonate_chlorite_epidote", ColumnType.STRING),
    Column("mg_oh_alteration", ColumnType.STRING),
    Column("amphibole_mgoh", ColumnType.STRING),
    Column("amphibole", ColumnType.STRING),
    Column("dolomit", ColumnType.STRING),
    Column("sericite_muscovite_illite_smectite", ColumnType.STRING),
    Column("alunite_kaolinite_pyrophyllite", ColumnType.STRING),
    Column("phengitic", ColumnType.STRING),
    Column("muscovite", ColumnType.STRING),
    Column("kaolinite", ColumnType.STRING),
    Column("clay", ColumnType.STRING),
    Column("kaolinite_argillic", ColumnType.STRING),
    Column("alunite_advanced_argillic", ColumnType.STRING),
    Column("al_oh_alteration", ColumnType.STRING),
    Column("calcite", ColumnType.STRING),
    Column("ndwi", ColumnType.STRING),
    Column("ndvi", ColumnType.STRING),
    Column("cloud_mask", ColumnType.STRING),
]
result = GMI_CE.Computing.create_table(name=results_table,columns=columns)
print(result)

# Run the UDF you create to get the results of functional groups
SQL=f'''set odps.sql.python.version=cp37;
insert overwrite table {results_table}
select x as tile_index_x ,y as tile_index_y,results.meta as meta,results.code as code,
results.data[0],results.data[1],results.data[2],results.data[3],results.data[4],results.data[5], results.data[6],results.data[7],
results.data[8], results.data[9],results.data[10],results.data[11],results.data[12],results.data[13],results.data[14],results.data[15],
results.data[16], results.data[17],results.data[18],results.data[19],results.data[20],results.data[21],results.data[22],results.data[23]
from (
SELECT tile_index_x as x, tile_index_y as y,
GMI_ComputeEngine(
get_json_object(json_object('tile_info',tile_info,"granule_id",granule_id,"tile_index_x",tile_index_x,"tile_index_y",tile_index_y,
"min_row",min_row,"min_col",min_col,"max_row",max_row,"max_col",max_col,
"atmospheric_correction_paras",atmospheric_correction_paras,
"bands","VNIR_Swath_ImageData1-VNIR_Swath_ImageData2-VNIR_Swath_ImageData3-SWIR_Swath_ImageData4-SWIR_Swath_ImageData5-SWIR_Swath_ImageData6-SWIR_Swath_ImageData7-SWIR_Swath_ImageData8-SWIR_Swath_ImageData9",
"type","{type}","output",{output}), '$'),  meta,
array(VNIR_Swath_ImageData1,VNIR_Swath_ImageData2,VNIR_Swath_ImageData3,SWIR_Swath_ImageData4,SWIR_Swath_ImageData5,
SWIR_Swath_ImageData6,SWIR_Swath_ImageData7,SWIR_Swath_ImageData8,SWIR_Swath_ImageData9),
array(modis_VNIR_Swath_ImageData1,modis_VNIR_Swath_ImageData2,modis_VNIR_Swath_ImageData3,modis_VNIR_Swath_ImageData4,
modis_SWIR_Swath_ImageData5,modis_SWIR_Swath_ImageData6,modis_SWIR_Swath_ImageData7))
as results FROM {source_table} GROUP BY tile_index_x, tile_index_y);'''

job_id = GMI_CE.Computing.create_job(sql=SQL)
print(job_id)
status = GMI_CE.Computing.get_job_status(job_id=job_id)
print(status)

# 3.Download results
GMI_CE.Data.download(data_address="demo_results_color", save_file="test.csv")