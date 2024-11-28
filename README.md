# Global_Mineral_Indices_Computing_Engine
## Overview
    This project is a global-scale remote sensing data computing engine built on Alibaba Cloud's Apsara ODPS (Open Data Processing Service) which leverages ASTER L1T data to compute global mineral indices. The engine is designed to process and analyze vast amounts of remote sensing data, providing valuable insights into mineral resources worldwide.

    Traditional mineral indices research has typically focused on local areas. However, when the spatial scale of study expands to a global scale, the massive amounts of remote sensing data present new challenges in terms of data storage and computation resources. Alibaba Cloud's ODPS (Open Data Processing Service) is a cloud-native big data computing service that has been upgraded to an integrated big data platform, addressing these challenges by integrating storage and computation resources. The development of a Global Mineral Indices Computing Engine based on the ODPS platform not only leverages Alibaba Cloud's advanced big data platform to address the storage and computational challenges of global-scale remote sensing data but also enhances the efficiency and accuracy of mineral indices research on a global scale.

## Get started with following steps
1. Prepare your Python enviroment

    First, you will need to set up a brand-new Python environment using conda and install the aster_core package. For detailed installation instructions and introductions to aster_core, you can refer to the [repository](https://github.com/datahub-zjlab/AsterL1T_SWIR-VNIR_pipeline) :

    ```bash
    conda create -n myenv python=3.10

    conda activate myenv

    conda install gdal>3.6 py6s

    pip install path/to/aster_core-0.0.2-py3-none-any.whl
    ```
    Then download the files from the aster_core/resource directory in the repository. Place these files in the corresponding directory where the aster_core package is installed.

2. Install GMI_ComputeEngine_ODPS

    After successfully instlled aster_core, you need to clone this repository and install it locally: 

    ```bash
    git clone https://github.com/datahub-zjlab/Global_Mineral_Indices_Computing_Engine.git

    cd Global_Mineral_Indices_Computing_Engine

    pip install .
    ```

3. Test GMI_ComputeEngine_ODPS in your Python enviroment

    ```bash
    python -c "import GMI_ComputeEngine_ODPS"
    ```
    If there are no error messages, GMI_ComputeEngine_ODPS has been successfully installed.

4. Transfer Aster L1t data into table with `Script1_transfer_aster_to_table.py` 

    Try to transfer the raster data and meta data of ASTER L1T hdf file as well as other auxiliary data like atmospheric correcion parameters and reflectance reference raster data into one row in a table.
    
    In this step, we will utilize `Script1_transfer_aster_to_table.py` to achieve the following:
    
    (1) Resample the ASTER L1T raster data from the UTM coordinate system to a customed standard tile (1024*1024) in the Web Mercator coordinate system with a resolution of 30 meters. Additionally, the raster data of the tile will be re-encoded from array type to binary type.

    (2) Calculate atmospheric correction parameters based on the provided AOD (Aerosol Optical Depth) and DEM (Digital Elevation Model) parameters.

    (3) In reference to the ASTER L1T raster data, resample the MODIS surface reflectance data to the tile and re-encode it into binary type.

    (4) Write all the aforementioned fields into a single row in a table.
    
    We have provided some demo data in the Google Drive folder accessible at this [link](https://drive.google.com/drive/folders/1yQ1_9ZQLKNLNPn-t6w2nS44n9toOW67X?). You can use the provided demo data to run the `Script1_transfer_aster_to_table.py` to obtain the corresponding table data, which will be stored in CSV format.

    ```bash
    conda activate myenv

    python Script1_transfer_aster_to_table.py AST_L1T_00309062006180242_20150516014601_17781.hdf GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv MCD19A2.A2006249.h08v05.061.2022278214439.hdf ASTGTMV003_N32W108_dem.tif,ASTGTMV003_N32W109_dem.tif --modis_ref_file modis_res-500_tilesize-256_x-260_y-526_dst-deshadow.tiff --tile_index_x 260 --tile_index_y 526
    ```

    After this step, you can obtain your table data (one row) stored in `GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv`.

5. Upload table into ODPS with `Script2_upload_table_to_odps.py`

6. Computing in ODPS with `Script3_computing.py`

7. Download table from ODPS with `Script4_download_table_from_odps.py`

8. Transfer table to GeoTiff file with `Script5_transfer_table_to_tif.py`

## Results
Typical result of output asterimage and mineralindices in South America:

<img src="./Results/OBJECT.2075.POINT.(-108.07,32.793)_Chino_dis20km_asterimage.png" alt="asterimage" width="300px" />
<img src="./Results/OBJECT.2075.POINT.(-108.07,32.793)_Chino_dis20km_linearstretch_groupindex.png" alt="mineralindices" width="300px" />