# Increased Hydrological Connectivity Does Not Always Lead to Increased Nutrient Removal Potential in a Coastal River Delta Code Base

## Overview
This repository contains the code and data associated with the manuscript "Increased Hydrological Connectivity Does Not Always Lead to Increased Nutrient Removal Potential in a Coastal River Delta". 
The codebase is primarily written in Python, saved as jupyter notebook processing scripts for ease of use/explanation, and it uses a variety of scientific computing libraries.
The corresponding Zenodo for the large data files and output files published in the manuscript can be found here: 10.5281/zenodo.19337951.

## Organization
The repository is structured simply, with three folders: input_data, processing_scripts, and results. Much of the input data needed is too large for GitHub, and will need to be downloaded from Zenodo separately. 
Additionally, `dorado` is a particle tracking model that relies on a random-walk routing scheme, which means that each new `dorado` run could produce slightly different outputs with the same exact inputs.
For this reason, to replicate the results found in the manuscript, we recommend downloading the `dorado_results` from Zenodo, instead of re-running the `dorado` particle tracking with the `dorado_add_ROI.ipynb` script.
If you are not re-running `dorado`, you do not have to download the `ANUGA` hydrodynamic results that also accompany this dataset. 

## Recommended Order of Events
### 1. Clone this repository
git clone https://github.com/eghenson/delta-connectivity-denitrification.git

### 2. Clone the modified `dorado` repository
This project requires a modified version of `dorado` that will soon be merged with the main parent repo at passah20/dorado. Until the PR is merged into the main repo, install from this fork:
git clone https://github.com/eghenson/dorado.git
cd dorado
git checkout your-branch-name
pip install -e .

### 3. Create and activate the conda environment
conda env create -f `dorado_env.yml`
conda activate dorado_env

### 4. Download large data files
Both the `ANUGA` hydrodynamic outputs required to run `dorado` and the consequential `dorado` results are too large for GitHub.
Download them from Zenodo here: 10.5281/zenodo.19337951
Place them in the following structure:
results/dorado_results/FC_baseline/FC_wd.pkl
results/dorado_results/SC_baseline/SC_wd.pkl

### 5. Run the notebooks in order
1. processing_scripts/dorado_add_ROI.ipynb - this is optional. You can also just download the `dorado` results hosted here:

2. processing_scripts/post_process_walkdata.ipynb
-  The functions used to calculate the discharge used in the `post_process_walkdata.ipynb` script are available (along with the `discharge_env.yml`), but the outputs are already provided within this repo. 

## Data Citations:
The dorado input files for each season "SC" and "FC" are too large for GitHub and are archived on NASA EarthData at https://doi.org/10.3334/ORNLDAAC/2306 
and are also archived with this manuscript in the accompanying Zenodo (10.5281/zenodo.19337951).

Wright, K. A., & Passalacqua, P. (2024). Delta-X: Calibrated ANUGA Hydrodynamic Outputs for the Atchafalaya Basin, MRD, LA (Version 1). 
ORNL Distributed Active Archive Center. https://doi.org/10.3334/ORNLDAAC/2306 Date Accessed: 2026-03-30
