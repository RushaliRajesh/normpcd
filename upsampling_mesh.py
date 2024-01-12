from natsort import natsorted
from glob import glob
import numpy as np
import open3d as o3d
from sklearn.metrics.pairwise import cosine_similarity 
import time
from scipy.io import savemat
import pdb

def area_calc(x,y,z):
    #using cross product
    return 0.5 * np.linalg.norm(np.cross(x-y, x-z), axis=1)


def process_mesh(mesh, n):
    base_pcd = np.array(mesh.vertices)
    base_normals = np.array(mesh.vertex_normals)

    tri_x = base_pcd[np.array(mesh.triangles)[:,0]] 
    tri_y = base_pcd[np.array(mesh.triangles)[:,1]]
    tri_z = base_pcd[np.array(mesh.triangles)[:,2]]

    # print(tri_x.shape == tri_y.shape == tri_z.shape)


    norm_x = base_normals[np.array(mesh.triangles)[:,0]]
    norm_y = base_normals[np.array(mesh.triangles)[:,1]]
    norm_z = base_normals[np.array(mesh.triangles)[:,2]]

    # print(norm_x.shape == norm_y.shape == norm_z.shape)

    areas = area_calc(tri_x, tri_y, tri_z)
    probs = areas/areas.sum()

    # print(areas, probs)
    # print(areas.shape, probs.shape)

    # weighted indices for the triangles/faces not the vertices
    weighted_indices = np.random.choice(np.arange(areas.shape[0]), size=2048, p=probs)
    
    tri_x = tri_x[weighted_indices]
    tri_y = tri_y[weighted_indices]
    tri_z = tri_z[weighted_indices]

    norm_x = norm_x[weighted_indices]
    norm_y = norm_y[weighted_indices]
    norm_z = norm_z[weighted_indices]

    a = np.random.randint(1, 100, size=(n,1))
    b = np.random.randint(1, 100, size=(n,1))
    c = np.random.randint(1, 100, size=(n,1)) 

    sum = np.sum([a,b,c], axis=0)
    # print(sum.shape)
    a = a/sum
    b = b/sum
    c = c/sum

    # verify = np.sum([a,b,c], axis=0)
    # print(verify)

    sampled_pts = np.multiply(a, tri_x) + np.multiply(b, tri_y) + np.multiply(c, tri_z)
    sampled_norms = np.multiply(a, norm_x) + np.multiply(b, norm_y) + np.multiply(c, norm_z)
    same_norms = np.multiply(1/3, norm_x) + np.multiply(1/3, norm_y) + np.multiply(1/3, norm_z)

    sampled_pts= sampled_pts - np.mean(sampled_pts, axis=0)

    return sampled_pts, sampled_norms, same_norms


# def meshify(paths):
#     # print(len(paths))

#     #read all the meshes from paths
#     idx=1139
#     meshes = []
#     for path in paths[1139:]:
#         print(str(idx))                
#         mesh = o3d.io.read_triangle_mesh(path)
#         pcd, normals, same_norms = process_mesh(mesh, 2048)
#         meshes.append([pcd, normals, same_norms])
#         idx+=1
    
#     return meshes

def printy():
    print("hello")

def meshify(paths):
    meshes = []
    print("in meshify")
    for path in paths:             
        mesh = o3d.io.read_triangle_mesh(path)
        # print(path)
        # print(np.array(mesh.vertices).shape)
        if(np.array(mesh.vertices).shape[0]==0):
            print(path, " skipped")
            continue
        pcd, normals, same_norms = process_mesh(mesh, 2048)
        meshes.append([pcd, normals, same_norms])
    
    return meshes



def verification(points, normals):
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(np.asarray(points))
    pc.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))

    # comparision to our estimates using cosine similarity
    pc_normals = np.asarray(pc.normals)
    cos_sim = cosine_similarity(normals, pc_normals)
    print(cos_sim.shape)
    err = np.diag(cos_sim)
    print("avg cosine sim: ", np.mean(err))
    var = np.var(err)
    print("variance: ", var)
    print("std dev: ", np.sqrt(var))
    # print(err)

    dot_sim = np.dot(normals, pc_normals.T)
    dot_sim = np.diag(dot_sim)
    print("avg dot sim: ", np.mean(dot_sim))

    err = np.arccos(err) * 180/np.pi
    # print(err)
    print("cos angle: ", np.mean(err))

    
def visualization_pcd(points, normals=None, original=False):
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(np.asarray(points))
    
    if original:
        pc.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))
        # print("ori norm: ", np.asarray(pc.normals))
    else:
        pc.normals = o3d.utility.Vector3dVector(np.asarray(normals)*5)

    o3d.visualization.draw_geometries([pc], point_show_normal=True)
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    # vis.add_geometry(pc)
    # vis.capture_screen_image('cameraparams.png', point_show_normal=True)
    # time.sleep(1)
    # vis.destroy_window()


if __name__ == '__main__':
    paths = natsorted(glob('ShapeNetCorev2/*/*/models/*.obj'))
    # print(len(paths))
    # print(paths[0])
    pcd, normals, same_norm = meshify([paths[0]])
    # verification(pcd, normals)
    # visualization_pcd(pcd, normals)
    verification(pcd, same_norm)
    # visualization_pcd(pcd, same_norm)
    # visualization_pcd(pcd, original=True)
    mesh = o3d.io.read_triangle_mesh(paths[0])
    # visualization_pcd(np.array(mesh.vertices), np.array(mesh.vertex_normals), original=True)
    # visualization_pcd(np.array(mesh.vertices), np.array(mesh.vertex_normals))

    print(np.array(mesh.vertices)[:20,:])
    print(np.array(mesh.vertex_normals)[:20,:])

    # verification(mesh.vertices, mesh.vertex_normals)

    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(np.asarray(pcd))
    pc.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.2, max_nn=30))

    dict_sam = {}
    dict_sam['vertices'] = pcd
    dict_sam['normals'] = normals
    dict_sam['o3d_normals'] = np.asarray(pc.normals)
    dict_sam['mesh_vertices'] = np.array(mesh.vertices)
    dict_sam['mesh_normals'] = np.array(mesh.vertex_normals)
    dict_sam['same_normals'] = same_norm

    for i in dict_sam.keys():
        print(i, dict_sam[i].shape)

    savemat('sampled.mat', dict_sam)

