import numpy as np 
import open3d as o3d
import os
from natsort import natsorted
from glob import glob
from upsampling_mesh import meshify
from sklearn.neighbors import NearestNeighbors
import pdb

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

def find_r_dist(points, rad=1):
    flag =0
    neigh = NearestNeighbors(radius=rad)
    neigh.fit(points)
    distances_ori, indices = neigh.radius_neighbors(points)
    pdb.set_trace()
    print(distances_ori, indices.shape)
    print(type(distances_ori[0]), type(distances_ori), distances_ori.shape)
    array_shapes = np.array([array.shape for array in distances_ori])
    distances = np.array([np.sum(data) for data in distances_ori])

    print(array_shapes)

    no_neigh = np.where(distances==0)
    if len(no_neigh[0]) > 0:
        flag =1

    return distances_ori, indices, flag

def patching(points, normals, radius_chosen):
    distances_ori, indices, flag = find_r_dist(points, radius_chosen)

    return distances_ori, indices, flag

pcd_list = np.load('pcd_list.npy')

dists, indices, no_neigh = find_r_dist(pcd_list[10], rad=0.1)
