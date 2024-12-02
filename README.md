# Global_Mineral_Indices_Computing_Engine
## Overview
This project is a global-scale remote sensing data computing engine built on Alibaba Cloud's Apsara ODPS (Open Data Processing Service) which leverages ASTER L1T data to compute global mineral indices. The engine is designed to process and analyze vast amounts of remote sensing data, providing valuable insights into mineral resources worldwide.

Traditional mineral indices research has typically focused on local areas. However, when the spatial scale of study expands to a global scale, the massive amounts of remote sensing data bring new challenges regarding data storage and computation resources. Alibaba Cloud's ODPS (Open Data Processing Service) is a cloud-native big data computing service that has been upgraded to an integrated big data platform, addressing these challenges by integrating storage and computation resources. The development of a Global Mineral Indices Computing Engine based on the ODPS platform not only leverages Alibaba Cloud's advanced big data platform to address the storage and computational challenges of global-scale remote sensing data but also enhances the efficiency and accuracy of mineral indices research on a global scale.

## Get started with following steps
This guide will walk you through the steps to set up and utilize a computational pipeline for processing ASTER L1T data and performing advanced computations using ODPS (Online Data Processing Service). The process involves preparing your Python environment, installing necessary packages, transferring ASTER data into a structured table format, uploading this data to ODPS, performing computations, downloading the results, and converting the data into GeoTIFF files. We provide a comprehensive set of scripts and example data to facilitate this workflow.

To get started, follow the detailed steps outlined below. We have also made available a set of **demo data** (you can download from [Google Drive Link](https://drive.google.com/drive/folders/1yQ1_9ZQLKNLNPn-t6w2nS44n9toOW67X?)) and **ODPS Computing Resources** (you can access it through api_key provide in GMI_ComputeEngine_ODPS api) to help you through the process.
1. Prepare your Python enviroment

    First, you will need to set up a brand-new Python environment using conda and install the aster_core package. For detailed installation instructions and introductions to aster_core, you can refer to the [repository](https://github.com/datahub-zjlab/AsterL1T_SWIR-VNIR_pipeline) :

    ```bash
    conda create -n myenv python=3.10

    conda activate myenv

    conda install gdal>3.6 py6s

    pip install path/to/aster_core-0.0.2-py3-none-any.whl
    ```
    Then download the files from the aster_core/resource directory in the [repository](https://github.com/datahub-zjlab/AsterL1T_SWIR-VNIR_pipeline). Place these files in the corresponding directory where the aster_core package is installed.

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

    (3) In reference to the ASTER L1T raster data, resample the MODIS surface reflectance data used for color balancing to the tile and re-encode it into binary type.

    (4) Write all the aforementioned fields into a single row in a table.
    
    We have provided some demo data in the Google Drive folder accessible at this [Google Drive Link](https://drive.google.com/drive/folders/1yQ1_9ZQLKNLNPn-t6w2nS44n9toOW67X?). You can use the provided demo data to run the `Script1_transfer_aster_to_table.py` to obtain the corresponding table data, which will be stored in CSV format.

    ```bash
    conda activate myenv

    python Script1_transfer_aster_to_table.py AST_L1T_00309062006180242_20150516014601_17781.hdf GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv MCD19A2.A2006249.h08v05.061.2022278214439.hdf ASTGTMV003_N32W108_dem.tif,ASTGTMV003_N32W109_dem.tif --modis_ref_file modis_res-500_tilesize-256_x-260_y-526_dst-deshadow.tiff --tile_index_x 260 --tile_index_y 526
    ```

    After this step, you can obtain your table data (one row) stored in `GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv`.

5. Upload table into ODPS with `Script2_upload_table_to_odps.py`

    This guide will help you understand how to use `Script3_upload_to_odps.py` to upload data from a CSV file to an ODPS (Online Data Processing Service) table.

    The script performs the following actions:

    (1) Defines the structure of the ODPS table by specifying the columns and their data types, including identifiers, index information, tile metadata, atmospheric correction parameters, and image data for various bands.

    (2) Parses command line arguments to obtain the path to the CSV file and the name of the source table in ODPS.

    (3) Creates an ODPS table with the specified columns if it does not exist.

    (4) Uploads data from the CSV file to the specified ODPS table.

    To use this script, you will need a CSV file containing the data you wish to upload to ODPS. The CSV file should have columns that match the structure defined in the script.

    We have also provided demo table in the Google Drive folder accessible at this [link](https://drive.google.com/drive/folders/1yQ1_9ZQLKNLNPn-t6w2nS44n9toOW67X?) which store more rows (rasters) in the same tile region.

    Here's how you can run the `Script2_upload_table_to_odps.py`:

    ```bash
    python Script3_upload_to_odps.py path_to_your_csv_file.csv your_source_table_name
    ```

    Replace `path_to_your_csv_file.csv` with the actual path to your CSV file(`GMI_ComputeEngine_Demo_ASTER_Tiles_Table.csv`) and `your_source_table_name` with the name of the table in ODPS where you want to upload the data.

    After executing the script, the data from your CSV file will be uploaded to the specified ODPS table. If the table does not exist, it will be created with the column structure defined in the script.

6. Computing in ODPS with `Script3_computing.py`

    This guide will help you understand how to use `Script3_computing.py` to perform advanced computations on data stored in an ODPS (Online Data Processing Service) table.

    The script enables you to execute different computational methods on your data, including merging data, color balancing, and mineral indices calculation.

    Here's what you can achieve with `Script3_computing.py`:

    (1) **Mosaic Data**(mosaic): Perform DN to radiance conversion, atmospheric correction, and merge operations on your data.

    (2) **Color Balancing**(color_balancing): In addition to merging, apply color (spectral) transfer to your data.

    (3) **Mineral Indices Calculation**(mineral_indices): After merging and color balancing, calculate mineral indices for your data.

    To use this script, you will need to have data in an ODPS table and specify the source and results tables.

    Here's how you can run the `Script3_computing.py`:

    ```bash
    python Script3_computing.py your_source_table_name your_results_table_name --method your_selected_method
    ```

    Replace `your_source_table_name` with the name of the source table in ODPS, `your_results_table_name` with the name of the table where you want to store the results, and `your_selected_method` with the computing method you want to apply (merge, color_transfer, or mineral_indices).

    For example, if you want to perform mineral indices calculation:

    ```bash
    python Script3_computing.py source_table results_table --method mineral_indices
    ```

    After executing the script, the selected computation will be performed on your data, and the results will be stored in the specified results table.

7. Download table from ODPS with `Script4_download_table_from_odps.py`

    This guide will assist you in using `Script4_download_table_from_odps.py` to download data from an ODPS (Online Data Processing Service) table to your local machine.

    The script facilitates the following actions:

    (1) Download the contents of an ODPS table to a specified CSV file on your local system.

    To use this script, you will need the name of the results table in ODPS and a local path where you want to save the downloaded CSV file.

    Here's how you can execute the `Script4_download_table_from_odps.py`:

    ```bash
    python Script4_download_odps_to_local.py path_to_save_csv your_results_table_name
    ```

    Replace `path_to_save_csv` with the local path where you want to save the CSV file, and `your_results_table_name` with the name of the results table in ODPS from which you want to download the data.

    For example, if you want to download the data to a file named `downloaded_data.csv`:

    ```bash
    python Script4_download_odps_to_local.py downloaded_data.csv results_table
    ```

    After executing the script, the data from the specified ODPS table will be downloaded and saved as a CSV file at the specified local path.

8. Transfer table to GeoTiff file with `Script5_transfer_table_to_tif.py`
    This guide will help you understand how to use `Script5_convert_table_to_geotiff.py` to convert a table row containing raster data into a GeoTIFF file.

    The script performs the following actions:

    (1) Reads a CSV file containing raster data and metadata.

    (2) Based on the specified label, selects the appropriate bands to process.

    (3) Converts the hexadecimal string data from the CSV file into binary data, and then into a numpy array.

    (4) Saves the numpy array as a GeoTIFF file using the metadata from the CSV file.

    To use this script, you will need a CSV file containing raster data and metadata, and a local path where you want to save the GeoTIFF files.

    Here's how you can execute the `Script5_convert_table_to_geotiff.py`:

    ```bash
    python Script5_convert_table_to_geotiff.py path_to_your_csv_file --save_path path_to_save_geotiff --label your_data_label
    ```

    Replace `path_to_your_csv_file` with the path to your CSV file, `path_to_save_geotiff` with the local path where you want to save the GeoTIFF files, and `your_data_label` with the label of your data (`ASTRef` or `MineralIndices`).

    For example, if you want to convert data labeled as `MineralIndices` and save the GeoTIFF files in the current directory:

    ```bash
    python Script5_convert_table_to_geotiff.py downloaded_data.csv --save_path . --label MineralIndices
    ```

    After executing the script, the data from the CSV file will be converted into GeoTIFF files and saved at the specified local path.

    Note: The script assumes that the CSV file has a specific structure, with columns for tile indices, metadata, and hexadecimal string data for each band. Make sure your CSV file matches this structure.

**Note:**
If you face any issues or need further assistance, please verify the legitimacy of the URL and ensure your network settings allow access to the ODPS server.

## Detailed data processing steps

This section provides a detailed description of the data processing steps involved in `Script3_computing.py`, including the acquisition of atmospheric correction parameters and the color balancing process using MODIS reflectance. Additionally, it outlines the method for calculating mineral indices.

#### Atmospheric correction parameters acquisition

The atmospheric correction parameters are crucial for accurately processing remote sensing data. These parameters can be obtained using two primary methods:

1. Lookup Table (LUT) Based on 6S Model:
   - **Method:** This approach involves using a precomputed Look-Up Table (LUT) generated by the 6S radiative transfer model. The LUT contains precomputed atmospheric correction parameters for various atmospheric conditions, aerosol types, and solar geometries.
   - **Implementation:** The `Script1_transfer_aster_to_table.py` script can be configured to use this method by setting the `accuracy_ac_flag` to `False`. This flag instructs the script to retrieve the atmospheric correction parameters from the LUT based on the input AOD (Aerosol Optical Depth) and DEM (Digital Elevation Model) parameters.

2. Direct Calculation Using 6S Model:
   - **Method:** This method directly invokes the 6S radiative transfer model to compute the atmospheric correction parameters in real-time. This approach is more computationally intensive but provides more accurate results as it dynamically adjusts for the specific atmospheric conditions of the scene.
   - **Implementation:** To use this method, set the `accuracy_ac_flag` to `True` in the `Script1_transfer_aster_to_table.py` script. This flag instructs the script to call the 6S model directly for computing the atmospheric correction parameters.

#### Color balancing using MODIS reflectance

Color balancing is a critical step in harmonizing the spectral characteristics of different datasets. In this process, MODIS reflectance data is used as a reference to achieve consistent spectral properties across multiple datasets. The following steps outline the color balancing process:

1. Reference Data Selection:
   - **MODIS Reflectance:** The MODIS surface reflectance data (MOD09A1) is used as the reference dataset. This dataset provides high-quality, atmospherically corrected surface reflectance values.
   - **Note:** If the Modis reference data is not provided, the color balancing process will be skipped.

2. Tasseled Cap Transformation:
   - **Method:** The Tasseled Cap Transformation (TCT) is applied to the MODIS reflectance data to derive a set of orthogonal components that represent different physical properties of the land surface. These components are then used to guide the color balancing process.
   - **Implementation:** The TCT is applied to both the MODIS reflectance data and the ASTER L1T data. The resulting TCT components from the MODIS data are used to adjust the corresponding components in the ASTER data, ensuring that the spectral characteristics of the ASTER data match those of the MODIS data.

3. Spectral Harmonization:
   - **Process:** The adjusted TCT components are then transformed back into the original spectral space, resulting in ASTER data that has been spectrally harmonized with the MODIS data. This process ensures that the ASTER data can be directly compared and combined with the MODIS data for further analysis.

#### Mineral Indices Calculation

Mineral indices are calculated to identify and quantify the presence of specific minerals in the remote sensing data. The calculation methods for various mineral indices are detailed in the reference table `Mineral_Indices.csv`, which includes the following columns:

- **Index ID:** The ID of the mineral index.
- **Index Name:** The name of the mineral index.
- **Equation:** The mathematical formula used to calculate the index.

By following these steps, the `Script3_computing.py` script enables the accurate processing of ASTER L1T data, including atmospheric correction, spectral harmonization with MODIS data, and calculation of mineral indices, to facilitate advanced remote sensing analysis.

## Demo Data Sources and Licensing:
The demo data provided includes the following datasets:

- **ASTER L1T Data:**
  - **Source:** The ASTER L1T data is sourced from the [NASA Land Processes Distributed Active Archive Center (LP DAAC)](https://lpdaac.usgs.gov/).
  - **Licensing:** The data is distributed under the [NASA's Open Data Policy](https://www.nasa.gov/sites/default/files/atoms/files/nasa_open_data_policy.pdf), which allows for free and open access to the data for educational and scientific purposes.

- **MODIS MCD19A2 Data:**
  - **Source:** The MODIS MCD19A2 data is sourced from the [NASA Land Processes Distributed Active Archive Center (LP DAAC)](https://lpdaac.usgs.gov/).
  - **Licensing:** The data is distributed under the [NASA's Open Data Policy](https://www.nasa.gov/sites/default/files/atoms/files/nasa_open_data_policy.pdf), which allows for free and open access to the data for educational and scientific purposes.

- **MOD09A1 Data:**
  - **Source:** The MOD09A1 data is sourced from the [NASA Land Processes Distributed Active Archive Center (LP DAAC)](https://lpdaac.usgs.gov/).
  - **Licensing:** The data is distributed under the [NASA's Open Data Policy](https://www.nasa.gov/sites/default/files/atoms/files/nasa_open_data_policy.pdf), which allows for free and open access to the data for educational and scientific purposes.

- **ASTER GDEM v003 Data:**
  - **Source:** The ASTER GDEM v003 data is sourced from the [NASA Land Processes Distributed Active Archive Center (LP DAAC)](https://lpdaac.usgs.gov/).
  - **Licensing:** The data is distributed under the [NASA's Open Data Policy](https://www.nasa.gov/sites/default/files/atoms/files/nasa_open_data_policy.pdf), which allows for free and open access to the data for educational and scientific purposes.

Please ensure you comply with the licensing terms when using these datasets.

## Results
Typical result of output aster merged and color balancinged image and mineral indices (Alteration Mapping of Porphyry Copper Deposits) in South America:

<div style="display: flex; align-items: center;">
  <img src="./Results/OBJECT.2075.POINT.(-108.07,32.793)_Chino_dis20km_asterimage.png" alt="asterimage" width="250px" style="margin-right: 10px;" />
  <img src="./Results/OBJECT.2075.POINT.(-108.07,32.793)_Chino_dis20km_linearstretch_groupindex.png" alt="mineralindices" width="250px" />
</div>

## Reference
1. Wilson, R. T., 2012, Py6S: A Python interface to the 6S radiative transfer model, Computers and Geosciences, 51, p166-171

## Project Participants
- Research Center of Data Hub and Security, Zhejiang Lab ;  
- Yangjie, China University of Geosciences (Beijing); 
- Yunqi Academy of Engineering

## Contact us
For any questions or further assistance, please contact:

- **Chen Ziyang**  
  Email: [chenzy@zhejianglab.org](mailto:chenzy@zhejianglab.org)  
  Zhejiang Lab, CHINA
