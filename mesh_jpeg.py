import numpy as np 
import open3d as o3d
import os
from natsort import natsorted
from glob import glob
from upsampling_mesh import meshify
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import RadiusNeighborsRegressor
import trimesh
import pdb

o3d.utility.set_verbosity_level(o3d.utility.VerbosityLevel.Error)

paths = natsorted(glob('ShapeNetCorev2/*/*/models/*.obj'))
print(paths[66])
print(paths[981])


# def delete_uv_coordinates(input_file, output_file):
#     with open(input_file, 'r') as infile:
#         lines = infile.readlines()

#     filtered_lines = [line for line in lines if not line.startswith('vt')]

#     output_dir = os.path.dirname(output_file)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     with open(output_file, 'w') as outfile:
#         outfile.writelines(filtered_lines)

# for ind,path in enumerate(paths):
#     # print(path[:-8]+'.obj')
#     out = 'update_shapenet/'+str(ind)+'.obj'
#     delete_uv_coordinates(path, out)

###########################################################################################
import os
import shutil

# def has_uv_coordinates(obj_file_path):
#     with open(obj_file_path, 'r') as obj_file:
#         for line in obj_file:
#             if line.startswith('vt'):
#                 return True
#     return False

# def move_folders_with_uv_coordinates(source_directory, destination_directory):
#     for root, dirs, files in os.walk(source_directory):
#         print("root: ", root)
#         print("dirs: ", dirs)
#         print("files: ", files)
#         print("------------------------------------------------------")
#         for dir_name in dirs:
#             folder_path = os.path.join(root, dir_name)
#             print(folder_path)
#             obj_files = [f for f in os.listdir(folder_path) if f.endswith('.obj')]
#             # if any(has_uv_coordinates(os.path.join(folder_path, obj_file)) for obj_file in obj_files):
#             #     destination_path = os.path.join(destination_directory, dir_name)
#             #     shutil.move(folder_path, destination_path)
#             #     print(f"Moved folder {dir_name} to {destination_path}")

# # Example usage
# source_directory_path = 'ShapeNetCorev2'
# destination_directory_path = 'messy_ones'
# move_folders_with_uv_coordinates(source_directory_path, destination_directory_path)

###########################################################################################


# import os
# import shutil

# source_dir = "ShapeNetCorev2"  # Path to the directory containing OBJ files
# target_dir = "uv_shapenet"  # Path to the destination directory

# def has_uv_coordinates(obj_file):
#     with open(obj_file, "r") as f:
#         for line in f:
#             if line.startswith("vt"):
#                 return True
#     return False

# for root, _, files in os.walk(source_dir):
#     for file in files:
#         if file.endswith(".obj"):
#             obj_file = os.path.join(root, file)
#             print(obj_file)
#             if has_uv_coordinates(obj_file):
#                 target_path = os.path.join(target_dir, os.path.relpath(root, source_dir))
#                 os.makedirs(target_path, exist_ok=True)  # Create target directory if it doesn't exist
#                 shutil.move(obj_file, os.path.join(target_path, file))
#                 print(f"Moved {obj_file} to {target_path}")

###########################################################################################
                
'''reversing'''

# import os
# import shutil

# source_dir = "uv_shapenet"  # Path to the directory containing moved OBJ files
# target_dir = "ShapeNetCorev2"  # Path to the original directory

# for root, _, files in os.walk(source_dir):
#     for file in files:
#         if file.endswith(".obj"):
#             obj_file = os.path.join(root, file)
#             original_path = os.path.join(target_dir, os.path.relpath(root, source_dir))
#             os.makedirs(original_path, exist_ok=True)  # Create original directory if it doesn't exist
#             shutil.move(obj_file, os.path.join(original_path, file))
#             print(f"Moved {obj_file} back to {original_path}")

# print("All files moved back to their original locations.")

###########################################################################################

# o3d.visualization.draw_geometries([mesh])
# ans = meshify([paths[982]])
# print(ans[0][0].shape)

# mesh = trimesh.load_mesh(paths[982])
# a= mesh.geometry[0]
# print(a.vertices)
# ind=0
# for path in paths:
#     mesh = o3d.io.read_triangle_mesh(path)
#     ind +=1
#     print(ind)