import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import queue
import json
import os
import sys
import glob

FPS = 0/30

def main():

    if len(sys.argv) == 2:
        ply_dirname = sys.argv[1]
        rotate_flag = False
    elif len(sys.argv) == 3:
        ply_dirname = sys.argv[1]
        rotate_flag = True
    else:
        print ("please input ply directory (abs path) and rotation flag")
        print ("<example>")
        print ("*** <with rotation> ***")
        print ("python3 run.py ~/ply_dataset/test/ply true")
        print ("*** <w/o rortation> ***")
        print ("python3 run.py ~/ply_dateset/test/ply")
        sys.exit(1)

    ### get number of ply frames
    num_ply = len(glob.glob(ply_dirname + '/*.ply'))

    i = 0
    ply_file_name = ply_dirname + '/' + str(i) + ".ply"
    print ("read {}".format(ply_file_name))
    pcd = prepare_pointcloud(ply_file_name, rotate_flag)

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    i = i + 1

    while True:

        t2 = time.time()
        ply_file_name = ply_dirname + '/' + str(i) + ".ply"
        print ("read {}".format(ply_file_name))
        _pcd = prepare_pointcloud(ply_file_name, rotate_flag)
        t3 = time.time()

        print (i, t3-t2)

        vis.remove_geometry(pcd)
        vis.add_geometry(_pcd)
        vis.poll_events()
        vis.update_renderer()
        pcd = _pcd

        i = i + 1

        if i >= num_ply:
            break

    vis.destroy_window()

    #o3d.visualization.draw_geometries([pcd])
    #t3 = time.time()

    #print (t2-t1, t3-t2)

def prepare_pointcloud(ply_file_name, rotate_flag):

    pcd = o3d.io.read_point_cloud(ply_file_name)
    #print (pcd)

    #t1 = time.time()
    if rotate_flag is True:
        R = pcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
        pcd.rotate(R, center=(0,0,0))
    else:
        pass
    #t2 = time.time()

    time.sleep(FPS)

    return pcd

if __name__ == '__main__':

    main()
