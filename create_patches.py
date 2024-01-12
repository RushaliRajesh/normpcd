import numpy as np 
import open3d as o3d
import os
from natsort import natsorted
from glob import glob
from upsampling_mesh import meshify
from sklearn.neighbors import NearestNeighbors
import ckwrap 
import matplotlib.pyplot as plt
from scipy.io import savemat

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

def find_neighs(points, k=2):
    nbrs = NearestNeighbors(n_neighbors=k, algorithm= 'kd_tree').fit(points)
    distances, indices = nbrs.kneighbors(points) 
    return distances, indices


def patching(points, normals, radius_chosen):
    dists_ori, indices_ori = find_neighs(points, k=500)
    dists_ori = dists_ori[:, 1:]
    indices_ori = indices_ori[:, 1:]
    # Apply ckmeans to all rows and extract labels using a lambda function:
    labels_per_row = np.apply_along_axis(lambda row: ckwrap.ckmeans(row, 5).labels, 1, dists_ori)

    # print("labels_arr shape: ",labels_per_row.shape)  # Now displays the actual labels for each row

    '''
    dists_array has 5 lists within, each list represents a cluster and has 2048 elements.
    '''
    dists_arrays = [[] for _ in np.unique(labels_per_row[0])]
    indices_arrays = [[]for _ in np.unique(labels_per_row[0])]
    for dist, ind, labels in zip(dists_ori, indices_ori, labels_per_row):
        # dist, ind, labels of shapes: (19,)
        for i in  np.unique(labels):
            temp_i = ind[np.where(labels == i)[0]]
            temp_d = dist[np.where(labels == i)[0]]
            dists_arrays[i].append(np.array([temp_d], dtype=object))
            indices_arrays[i].append(np.array([temp_i], dtype=object))
    return dists_arrays, indices_arrays


def visualize_clustered_points(dists_arrays):
    #visualising the clusters

    fig, ax = plt.subplots() 
    colors = ['blue', 'red', 'green', 'purple', 'orange']  
    for i, bucket in enumerate(dists_arrays):
        ax.plot(bucket[0], [i] * len(bucket[0]), '.', color=colors[i], markersize=10)

    plt.xlabel("Data Values")
    plt.ylabel("Cluster Labels")
    plt.title("Clustered Data")
    plt.grid(True)
    plt.show()




if __name__=='__main__':
    all = {'patches':[], 'norms':[]}
    pcd_list = np.load('pcd_list.npy')
    norm_list = np.load('normals_list.npy')
    for i, (pcd, norm) in enumerate(zip(pcd_list, norm_list)):
        dists_array, norms_array = patching(pcd, norm, 0.1)
        print(i, " done")
        all["patches"].append(dists_array)
        all["norms"].append(norms_array)
    savemat('patches.mat', all)
    
