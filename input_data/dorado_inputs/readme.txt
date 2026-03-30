The dorado input files for each season "SC" and "FC" are too large for GitHub and are archived on NASA EarthData at https://doi.org/10.3334/ORNLDAAC/2306. 

Full citation: Wright, K. A., & Passalacqua, P. (2024). Delta-X: Calibrated ANUGA Hydrodynamic Outputs for the Atchafalaya Basin, MRD, LA (Version 1). 
ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/2306 Date Accessed: 2026-03-30

Note: You do not have to re-run `dorado_add_ROI.ipynb` to analyze the potential uptake results. The `dorado` results can be downloaded from Zenodo.

If you want to re-run `dorado`, download the hydrodynamic results within their respective seasonal folders in order to run `dorado_add_ROI.ipynb`. You should place the downloaded netcdf files in the following structure:

input_data/
    dorado_inputs/
    ├── FC/
    │   ├── Hydro_WLAD_20210819_DXF.nc
    │   ├── Hydro_WLAD_20210820_DXF.nc
    │   ├── Hydro_WLAD_20210821_DXF.nc
    │   ├── Hydro_WLAD_20210822_DXF.nc
    │   ├── Hydro_WLAD_20210823_DXF.nc
    │   ├── Hydro_WLAD_20210824_DXF.nc
    │   ├── Hydro_WLAD_20210825_DXF.nc
    │   ├── Hydro_WLAD_20210826_DXF.nc
    │   └── Hydro_WLAD_20210827_DXF.nc
    │  
    └── SC/
        ├── Hydro_WLAD_20210325_DXS.nc
        ├── Hydro_WLAD_20210326_DXS.nc
        ├── Hydro_WLAD_20210327_DXS.nc
        ├── Hydro_WLAD_20210328_DXS.nc
        ├── Hydro_WLAD_20210329_DXS.nc
        ├── Hydro_WLAD_20210330_DXS.nc
        ├── Hydro_WLAD_20210331_DXS.nc
        ├── Hydro_WLAD_20210401_DXS.nc
        └── Hydro_WLAD_20210402_DXS.nc