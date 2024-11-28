from setuptools import setup, find_packages

setup(
    name='GMI_ComputeEngine_ODPS',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "uplink",
        "requests",
        "dacite"
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)