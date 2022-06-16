import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

def prepare_pointcloud(ply_file_name):

    pcd = o3d.io.read_point_cloud(ply_file_name)
    print (pcd)

    #t1 = time.time()
    R = pcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    pcd.rotate(R, center=(0,0,0))
    #t2 = time.time()

    return pcd

def main():

    if len(sys.argv) == 2:
        ply_file_name = sys.argv[1]

    else:
        print ("please input ply file name (abs path)")
        print ("<example>")
        print ("python3 run.py ~/ply_dataset/test/ply/1.ply")
        sys.exit(1)

    pcd = prepare_pointcloud(ply_file_name)

    o3d.visualization.draw_geometries([pcd])

    #print (t2-t1, t3-t2)

if __name__ == '__main__':

    main()
