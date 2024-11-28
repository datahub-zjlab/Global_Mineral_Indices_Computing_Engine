import os as __os
from GMI_ComputeEngine_ODPS.computing import Computing
from GMI_ComputeEngine_ODPS.storage import Storage
from GMI_ComputeEngine_ODPS.data import Data
from GMI_ComputeEngine_ODPS.computing.data_types import ColumnType, Column, JobStatus, ResourceType
from GMI_ComputeEngine_ODPS import method

api_key = __os.getenv("GMI_ComputeEngine_APIKEY")
api_baseurl = __os.getenv("GMI_ComputeEngine_API_BASEURL", "https://www.citybrain.org/platform/")

__all__ = [
    "Computing",
    "Storage",
    "Data",
    "api_key",
    "api_baseurl",
    "ColumnType",
    "Column",
    "JobStatus",
    "ResourceType"
]
