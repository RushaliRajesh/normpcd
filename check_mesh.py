from natsort import natsorted
from glob import glob
import numpy as np
import open3d as o3d


# paths = natsorted(glob('ShapeNetCorev2/*/*/models/*.obj'))
# print(len(paths))
# c=0
# it=0
# for path in paths:
#     it=it+1
#     print("it: ",it) 
#     with open(path, 'r') as file:
#         for line in file:
#             tokens = line.strip().split()
#             for token in tokens:
#                 if token == 'v':
#                     has_vertices = True
#                 elif token == 'f':
#                     has_faces = True
#     if(has_vertices==0 or has_faces==0):
#         c=c+1
#         print(path)

# print(c)