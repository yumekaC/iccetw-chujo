import open3d as o3d
import numpy as np
import time
import json
import os
import glob
import csv

### setting
setting_path ="./setting.json"
with open (setting_path) as f:
    setting = json.load(f)

rs_config = setting['rs config file']
o3d_config = setting['o3d config file']
output_dirname = setting['output dir']
ply_dirname = setting['output ply dir']
bag_filename_base = setting['sequence name']
log_dirname = setting['log dir']
###

SAVE = True

def main():

    output_path, output_ply_path, output_proc_ply_path = create_output_directory()

    ### get number of ply frames
    num_ply = len(glob.glob(output_ply_path + '/*.ply'))
    #num_ply = 10

    logs = []

    for i in range(num_ply):

        ply_file_name = output_ply_path + "/" + str(i) + ".ply"

        pcd = prepare_pointcloud(ply_file_name)

        ts1 = time.time()
        outlier_cloud = plane_segmentation(pcd)
        ts2 = time.time()

        print ("{} {}sec".format(i, ts2-ts1))

        logs.append([i, ts2-ts1])

        if SAVE is True:
            output_file_name = os.path.join(output_proc_ply_path, str(i) + ".ply")
            o3d.io.write_point_cloud(output_file_name, outlier_cloud)

    csv_filename = os.path.join(log_dirname, bag_filename_base + "_log_plane.csv")
    write_to_csv(csv_filename, logs)

    #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])
    #o3d.visualization.draw_geometries([outlier_cloud])

    #print(outlier_cloud)


### parepare outout directory
def create_output_directory():

    #timestamp = datetime.datetime.now()
    #dt_str = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    #output_path = os.path.join(os.environ['HOME'], output_dirname, dt_str)
    output_path = os.path.join(os.environ['HOME'], output_dirname, bag_filename_base)

    if os.path.exists(output_path) == False:
        os.makedirs(output_path)

    ### for output ply sequence
    output_ply_path = os.path.join(os.environ['HOME'], output_dirname, bag_filename_base, ply_dirname)

    if os.path.exists(output_ply_path) == False:
        os.makedirs(output_ply_path)

    ### for processed ply sequence
    output_proc_ply_path = os.path.join(os.environ['HOME'], output_dirname, bag_filename_base, "proc_" + ply_dirname)

    if os.path.exists(output_proc_ply_path) == False:
        os.makedirs(output_proc_ply_path)

    print ("output path: {}".format(output_path))
    print ("output ply path: {}".format(output_ply_path))
    print ("output processed ply path: {}".format(output_proc_ply_path))

    return output_path, output_ply_path, output_proc_ply_path

def prepare_pointcloud(ply_file_name):

    pcd = o3d.io.read_point_cloud(ply_file_name)
    print (pcd)

    #t1 = time.time()
    R = pcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    pcd.rotate(R, center=(0,0,0))
    #t2 = time.time()

    return pcd

def plane_segmentation(pcd):

    plane_model, inliers = pcd.segment_plane(distance_threshold=0.02,
                                         ransac_n=3,
                                         num_iterations=1000)

    inlier_cloud = pcd.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_by_index(inliers, invert=True)

    return outlier_cloud

def write_to_csv(csv_filename, data):

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == '__main__':

    main()
