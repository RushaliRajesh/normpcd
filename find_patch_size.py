import numpy as np 
import open3d as o3d
import os
from natsort import natsorted
from glob import glob
from upsampling_mesh import meshify
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsRegressor

import pdb

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

paths = natsorted(glob('ShapeNetCorev2/*/*/models/*.obj'))

def find_r(points, k=2):
    nbrs = NearestNeighbors(n_neighbors=k, algorithm= 'kd_tree').fit(points)
    distances, indices = nbrs.kneighbors(points)
    print(distances, indices)
    distances = np.sum(distances, axis=1)
    r = np.mean(distances)
    return r

#this code is from creat_patches.py, i dont think its useful anyway.

# def find_r_dist(points, rad=1):
#     flag =0
#     neigh = NearestNeighbors(radius=rad)
#     neigh.fit(points)
#     distances, indices = neigh.radius_neighbors(points)
#     print(distances, indices.shape)

#     array_shapes = np.array([array.shape for array in distances])
#     distances = np.array([np.sum(data) for data in distances])

#     no_neigh = np.where(distances==0)
#     if len(no_neigh[0]) > 0:
#         flag =1
#     r = np.mean(distances)
#     return r, flag

def find_r_dist(points, rad=1):
    flag =0
    neigh = NearestNeighbors(radius=rad)
    neigh.fit(points)
    distances_ori, indices = neigh.radius_neighbors(points)
    print(distances_ori, indices.shape)
    print(type(distances_ori[0]), type(distances_ori), distances_ori.shape)
    array_shapes = np.array([array.shape for array in distances_ori])
    distances = np.array([np.sum(data) for data in distances_ori])

    print(array_shapes)

    no_neigh = np.where(distances==0)
    if len(no_neigh[0]) > 0:
        flag =1

    return distances_ori, indices, flag

# distances_ori, indices, flag = find_r_dist(points, radius_chosen)

def patching(points, normals, radius_chosen):
    # r = find_r(points, 10)
    r_rad = find_r_dist(points, radius_chosen)
    # print("r based on dist: ",r)
    print("mean dist based on radius: ",r_rad)
    # print("num of points within rad: ", len(points[0]))

# pdb.set_trace()

meshes= meshify(paths)
pcd_list = np.array(meshes[:,0])
normals_list = np.array(meshes[:,1])
print(pcd_list.shape, normals_list.shape)

params = [0.2, 0.3, 0.5, 1]
# for pcd, normals in zip(pcd_list, normals_list):
#     for par in params:
#         r, no_neigh = patching(pcd, normals, radius_chosen=par)
#         if no_neigh:
#             print("no neighbors found for a point")
#         print("done for radius: ", par)
#         print("-------------------\n")

