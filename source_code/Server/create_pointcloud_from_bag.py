import json
import open3d as o3d
import time
import os
import datetime
import glob
import csv
import matplotlib.pyplot as plt

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

def main():

    output_path, output_ply_path = create_output_directory()
    ### get number of frames
    num_frames = len(glob.glob(output_path + '/color/*.jpg'))

    intrinsic_config = output_path + "/intrinsic.json"

    with open(o3d_config) as json_file:
        config = json.load(json_file)

    with open(intrinsic_config) as json_file:
        config2 = json.load(json_file)

    intrinsic = o3d.io.read_pinhole_camera_intrinsic(intrinsic_config)

    depth_scale = config2['depth_scale']
    max_depth = config['max_depth']

    logs = []
    
    for i in range(num_frames):
        t1 = time.time()
        create_pointcloud(output_path, output_ply_path, i, intrinsic, depth_scale, max_depth)
        t2 = time.time()

        print ("{} frame proc time: {}sec".format(i, t2-t1))

        logs.append([i, t2-t1])

    csv_filename = os.path.join(log_dirname, bag_filename_base + "_log_create_pointcloud.csv")
    write_to_csv(csv_filename, logs)

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

    print ("output path: {}".format(output_path))
    print ("output ply path: {}".format(output_ply_path))

    return output_path, output_ply_path

def read_rs_config(rs_config):

    with open(rs_config) as cf:
        rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

    return rs_cfg

def create_pointcloud(output_path, output_ply_path, frame_num, intrinsic, depth_scale, max_depth):

    #intrinsic_config = output_path + "/intrinsic.json"

    #with open(o3d_config) as json_file:
    #    config = json.load(json_file)

    #with open(intrinsic_config) as json_file:
    #    config2 = json.load(json_file)

    #im_rgbd = read_rgbd_image(output_path + "/color/" + str(frame_num) + ".jpg", 
    #                          output_path + "/depth/" + str(frame_num) + ".png", 
    #                          False, 
    #                          config2["depth_scale"], 
    #                          config["max_depth"])

    im_rgbd = read_rgbd_image(output_path + "/color/" + str(frame_num) + ".jpg", 
                              output_path + "/depth/" + str(frame_num) + ".png", 
                              False, 
                              depth_scale, 
                              max_depth)
 
    #intrinsic = o3d.io.read_pinhole_camera_intrinsic(intrinsic_config)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
            im_rgbd, intrinsic)
    
    #o3d.io.write_point_cloud(output_ply_path + '/' + str(frame_num) + ".ply", pcd, False, True)
    o3d.io.write_point_cloud(output_ply_path + '/' + str(frame_num) + ".ply", pcd, True, True)

def read_rgbd_image(color_file, depth_file, convert_rgb_to_intensity, depth_scale, depth_trunc):

    color = o3d.io.read_image(color_file)
    depth = o3d.io.read_image(depth_file)
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color,
        depth,
        depth_scale,
        depth_trunc,
        convert_rgb_to_intensity=convert_rgb_to_intensity)
    return rgbd_image


def write_to_csv(csv_filename, data):

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == '__main__':

    main()
