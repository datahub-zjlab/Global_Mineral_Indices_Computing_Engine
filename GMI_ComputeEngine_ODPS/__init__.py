import os as __os
from GMI_ComputeEngine_ODPS.computing import Computing
from GMI_ComputeEngine_ODPS.storage import Storage
from GMI_ComputeEngine_ODPS.data import Data
from GMI_ComputeEngine_ODPS.computing.data_types import ColumnType, Column, JobStatus, ResourceType
from GMI_ComputeEngine_ODPS import method

api_key = "NDUkMTczMjY5OTcwNyRqYXh5anBnbQ"
api_baseurl = "http://221.228.10.51:18080/platform/"

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
