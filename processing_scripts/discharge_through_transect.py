#!/usr/bin/env python
"""
Python script to calculate the discharge through a provided transect
This uses unstructured ANUGA hydrodynamic outputs - ymom and xmom
Ran in WSL linux with accompanying .yml file

"""
## Some dependencies, specifically the ANUGA ones, require a very particular environment setup to run - worth noting!
import matplotlib.pyplot as plt
import pandas as pd
import anuga
import anuga.shallow_water.sww_interrogate as test
import numpy as np
import xarray as xr
import os
import anuga.utilities.log as log
from anuga.abstract_2d_finite_volumes.neighbour_mesh import segment_midpoints
from matplotlib.path import Path
import sys
from scipy.spatial import cKDTree

# -------------- Inputs --------------
# Season and folder location where hydrodynamic outputs are stored- User would have to change these!!!
scenario = "FC"  # 'FC' or 'SC' for fall or spring seasons
foldername = f"/mnt/ANUGA_outputs/{scenario}"
outfolder  = f"./Discharge_calculations"

# List of transects, each defined by two endpoints
transects = [[[652384.34,3269959.74], [652676.54, 3269894.26]]] # Seeding for dorado simulations
             # [[653831.01, 3298120.48], [654811.01, 3298120.48]]] # DS of Inlet for ANUGA model - to test
    # [[653808.0,3298573.0],[654788.0,3298573.0]]  # Inlet of ANUGA model - to test

# Get all .nc files in the folder (ANUGA outputs)
filename = [
    os.path.join(foldername, f)
    for f in os.listdir(foldername)
    if f.endswith('.nc')
]

ds = xr.open_dataset(filename[0])
print(f"Dataset loaded from {filename[0]}")
print(f"-------------- Looking at dataset attributes-----------------", ds)
print(ds.attrs)

def get_mesh_and_quantities_from_netcdf(ds, quantities=None, verbose=False):
    """
    Extract mesh and quantities from an already-open ANUGA NetCDF xarray.Dataset.

    Parameters:
        ds         - xarray.Dataset from xr.open_dataset(...)
        quantities - list of variable names to extract
                     default: ['topo', 'stage', 'xmom', 'ymom']
        verbose    - print progress if True

    Returns:
        mesh       - ANUGA Mesh object
        quantities - dict of arrays (shape: [time, volumes] or [volumes])
        time       - array of time in seconds since model start
    """
    import numpy as np
    from anuga.abstract_2d_finite_volumes.neighbour_mesh import Mesh

    # Use time as-is if already float
    time = ds['time'].values
    if np.issubdtype(time.dtype, np.datetime64):
        time = (time - time[0]) / np.timedelta64(1, 's')  # convert to seconds
    else:
        time = time.astype(np.float64)

    # Node coordinates
    x = ds['x'].values
    y = ds['y'].values
    nodes = np.column_stack((x, y))  # shape: (nodes, 2)

    # Triangle connectivity
    triangles = ds['mesh'].values.T  # shape: (volumes, 3)

    if verbose:
        print(f"Building ANUGA Mesh from {len(nodes)} nodes and {len(triangles)} triangles")

    # Build mesh object
    mesh = Mesh(nodes.tolist(), triangles.tolist())

    # Default quantities
    if quantities is None:
        quantities = ['depth', 'stage', 'xmom', 'ymom']

    # Load quantities
    qdict = {}
    for name in quantities:
        if verbose:
            print(f"Loading quantity: {name}")
        qdict[name] = ds[name].values  # shape: (time, volumes) or (volumes,)

    return mesh, qdict, time

def compute_centroids(mesh):
    """
    Compute centroids of triangular elements in an ANUGA Mesh.

    Parameters:
        mesh - an ANUGA Mesh object with .nodes and .triangles

    Returns:
        centroids - (num_triangles, 2) array of [x, y] centroid coordinates
    """
    triangles = np.array(mesh.triangles)      # (num_triangles, 3)
    nodes = np.array(mesh.nodes)              # (num_nodes, 2)
    triangle_coords = nodes[triangles]        # (num_triangles, 3, 2)
    centroids = triangle_coords.mean(axis=1)  # (num_triangles, 2)
    return centroids

# Here is the main function, where we precompute transect geometry based on the ANUGA grid because this geometry is constant throughout the model
# Only need to do this once and then loop through the daily model outputs
def precompute_transect_geometry(ds, polyline, verbose=False):
    mesh, _, _ = get_mesh_and_quantities_from_netcdf(ds, quantities=[], verbose=True)
    centroids = compute_centroids(mesh)

    segments = mesh.get_intersecting_segments(polyline, verbose=verbose)
    midpoints = segment_midpoints(segments)

    tree = cKDTree(centroids)
    _, nearest_indices = tree.query(midpoints)

    normals = np.array([seg.normal for seg in segments])
    lengths = np.array([seg.length for seg in segments])

    return {
        "nearest_indices": nearest_indices,
        "normals": normals,
        "lengths": lengths
    }

# Compute geometry with the first file (aka first day of simulation)
ds0 = xr.open_dataset(filename[0])
geom = precompute_transect_geometry(ds0, transects[0], verbose=True)
t0 = ds0['time'].values[0]   # numpy.datetime64-- start time
ds0.close()

# ----------- Function to compute normal flux --------------
def compute_transect_flux(ds, geom):
    uh = ds['xmom'].values    # (time, volumes)
    vh = ds['ymom'].values

    idx = geom["nearest_indices"]
    normals = geom["normals"]
    lengths = geom["lengths"]

    uh_sel = uh[:, idx]
    vh_sel = vh[:, idx]

    normal_flux = uh_sel * normals[:, 0] + vh_sel * normals[:, 1]
    Q = np.sum(normal_flux * lengths, axis=1)

    return Q

# --------- Compute the transect fluxes -------------
all_time = []
all_Q = []

filenames = sorted(filename)
for i, fpath in enumerate(filenames):
    print(f"🔄 Processing {i+1}/{len(filenames)}: {os.path.basename(fpath)}")

    with xr.open_dataset(fpath) as ds:
        raw_time = ds['time'].values # datetime64[ns]
        # convert to hours since simulation start
        t_hours = (raw_time - t0) / np.timedelta64(1, 'h')

        # compute fluxes
        Q = compute_transect_flux(ds, geom)

        all_time.extend(t_hours)
        all_Q.extend(Q)

print("Finished all files")

# ------------ Plot and save results --------------
plt.figure(figsize=(10, 5))
plt.plot(all_time, all_Q, lw=1.5)
plt.xlabel("Time [hours]")
plt.ylabel("Discharge [m³/s]")
plt.title("Hydrograph Across Seeding Transect")
plt.grid(True)
plt.tight_layout()
plt.show()
plt.savefig(f"Transect_Hydrograph_{scenario}")

# Save as npy array
np.savez(
    os.path.join(outfolder, f"discharge_results_{scenario}.npz"),
    time=np.array(all_time),
    Q=np.array(all_Q)
)
# Also save as CSV
df = pd.DataFrame({
    'time_hours': all_time,
    'discharge_m3s': all_Q
})
df.to_csv(
    os.path.join(outfolder, f"discharge_results_{scenario}.csv"),
    index=False
)
print(f"Saved Discharge Results for", {scenario})

