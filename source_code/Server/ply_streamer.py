import json
import open3d as o3d
import time
import json
import os
import datetime
import threading
import queue
import numpy as np
import shutil
#from influxdb import InfluxDBClient

### params
ROOT_DIR = '/var/www/html'
#ROOT_DIR = os.environ['HOME']
MODE = "live"
voxel_size = 0.007#0.0075#0.01#0.015
FPS = 10#3#5#10
frame_skip = 30/FPS
plane_iteration = 20
#########


### setting for capturing pointcloud
setting_path ="./pcstreamer_setting.json"
with open (setting_path) as f:
    setting = json.load(f)

config_filename = setting['rs config file']
output_dirname = setting['output dir']
ply_dirname = setting['output ply dir']
bag_filename_base = setting['sequence name']
num_offset = int(setting['offset frames'])
plane_flag = setting['plane flag']

influxdb_ip = setting['influxdb ip']
influxdb_port = int(setting['influxdb port'])
influxdb_user = setting['influxdb user']
influxdb_pass = setting['influxdb pass']
influxdb_database = setting['influxdb database']
influxdb_mem_name = setting['influxdb mem name']
###


### fix params (L515)
depth_scale = 3999.999755859375
max_depth = 3.0

rs_queue = queue.Queue()
UTC = datetime.timezone.utc

### Connect InfluxDB
#influx_client = InfluxDBClient(influxdb_ip, influxdb_port, influxdb_user, influxdb_pass, influxdb_database)
#influx_client.create_database(influxdb_database)
###

def main():

    output_path, output_ply_path = create_output_directory()

    intrinsic_config = "./intrinsic.json"
    intrinsic = o3d.io.read_pinhole_camera_intrinsic(intrinsic_config)
 
    cam_thread = threading.Thread(target=cap_rgbd_rs, args=([output_path, num_offset]))
    cam_thread.setDaemon(True)
    cam_thread.start()

    main_thread(output_ply_path, intrinsic)


### parepare outout directory
def create_output_directory():

    #timestamp = datetime.datetime.now()
    #dt_str = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    output_path = os.path.join(ROOT_DIR, output_dirname, bag_filename_base)

    if os.path.exists(output_path) == True:
        shutil.rmtree(output_path)
    os.makedirs(output_path)

    ### for output ply sequence
    output_ply_path = os.path.join(ROOT_DIR, output_dirname, bag_filename_base, ply_dirname)

    if os.path.exists(output_ply_path) == True:
        shutil.rmtree(output_ply_path)
    os.makedirs(output_ply_path)

    print ("output path: {}".format(output_path))
    print ("output ply path: {}".format(output_ply_path))

    return output_path, output_ply_path


def main_thread(output_ply_path, intrinsic):

   frame_num = 0

   while True:
        if rs_queue.empty():
            pass
        else:
            rs_data = rs_queue.get()
            current_queue_size = rs_queue.qsize()
            pcd_thread = threading.Thread(target=create_pointcloud,
                                          args=([output_ply_path, intrinsic, rs_data, frame_num, current_queue_size]))
            pcd_thread.setDaemon(True)
            pcd_thread.start()
            
            frame_num += 1

def create_pointcloud(output_ply_path, intrinsic, rs_data, frame_num, current_queue_size):

    t1 = time.time()

    ### convert t.geometry.RGBDImage to geometry.RGBDImage
    _rs_data = o3d.t.geometry.RGBDImage.to_legacy(rs_data)

    ### create rgbd iamges from rgb and depth images
    im_rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
                _rs_data.color,
                _rs_data.depth,
                depth_scale,
                depth_trunc=max_depth,
                convert_rgb_to_intensity=False)
    t2 = time.time()

    ### create pointcloud from rgbd image
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(im_rgbd, intrinsic)
    t3 = time.time()

    ### voxel downsampling
    downpcd = pcd.voxel_down_sample(voxel_size)
    t4 = time.time()

    ### rotate ply pointcloud
    R = downpcd.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    downpcd.rotate(R, center=(0,0,0))
    t5 = time.time()

    ### plane segmentation
    #if plane_flag == "True" || plane_flag == "true":
    if plane_flag == "True" or plane_flag == "true":
        plane_pcd = plane_segmentation(downpcd, plane_iteration)
        
    else:
        plane_pcd = downpcd
    t6 = time.time()

    ### write as a ply file
    o3d.io.write_point_cloud(output_ply_path + '/' + str(frame_num) + '.ply', plane_pcd, False, True)
    t7 = time.time()

    ### output latest mpd file
    create_mpd_file(output_ply_path, frame_num)

    log = {'timestamp': get_current_time(UTC),
           'frame num': str(frame_num),
           'data size': os.path.getsize(output_ply_path + '/' + str(frame_num) + '.ply'),
           'voxel size': voxel_size,
           'frame rate': FPS,
           'queue size': current_queue_size,
           'plane flag': plane_flag,
           'plane iteration': plane_iteration,
           'process time': {'create rgbd image': t2-t1,
                            'create pointcloud': t3-t2,
                            'voxel downsampling': t4-t3,
                            'rotation': t5-t4,
                            'plane': t6-t5,
                            'write': t7-t6,
                            'total': t7-t1,
                            }
          }
    #t8 = time.time()

    print ("{} frame, queue: {} proc: {} sec".format(str(frame_num), current_queue_size, (t7-t1)))
    print (json.dumps(log, indent=2))

    #log_thread = threading.Thread(target=write_to_influxdb, args=([log]))
    #log_thread.setDaemon(True)
    #log_thread.run()


### plane segmentation
def plane_segmentation(pcd, itera):

    plane_model, inliers = pcd.segment_plane(distance_threshold=0.02,
                                         ransac_n=3,
                                         num_iterations=itera)

    inlier_cloud = pcd.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])
    outlier_cloud = pcd.select_by_index(inliers, invert=True)

    return outlier_cloud

### capture bag file from realsense
def cap_rgbd_rs(output_path, offset_num):

    print("start capure rgbd from realsense")

    with open(config_filename) as cf:
        rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

    rs = o3d.t.io.RealSenseSensor()

    bag_file_name = os.path.join(output_path, bag_filename_base +'.bag')

    rs.init_sensor(rs_cfg, 0, bag_file_name)
    rs.start_capture(True)

    counter = 1
    frame_id = 1

    while True:
        im_rgbd = rs.capture_frame(True, True)

        if counter >= num_offset:
            if frame_id == 1:
                rs_queue.put(im_rgbd)
            elif frame_id % frame_skip == 0:
                rs_queue.put(im_rgbd)
            else:
                pass
            frame_id += 1
                    
        counter += 1

    rs.stop_capture()


def write_to_influxdb(log):

    data_to_db = [{"measurement": influxdb_mem_name,
                   "tags": {"id": log['frame num'],
                            "voxel size": log['voxel size'],
                            "frame rate": log['frame rate'],
                            "plane flag": log['plane flag'],
                            "plane iteration": log['plane iteration'],
                            "type": "log"},
                   "time": log['timestamp'],
                   "fields": {"data size": float(log['data size'] / (1000*1000)),
                              "queue size": int(log['queue size']),
                              "create rgbd image": float(log['process time']['create rgbd image']),
                              "create pointcloud": float(log['process time']['create pointcloud']),
                              "voxel downsampling": float(log['process time']['voxel downsampling']),
                              "rotation": float(log['process time']['rotation']),
                              "plane segmentation": float(log['process time']['plane']),
                              "write to disk": float(log['process time']['write']),
                              "total process time": float(log['process time']['total'])
                              }
                   }]
    #influx_client.write_points(data_to_db)


def create_mpd_file(output_dir, frame_num):

    mpd = {"timestamp": get_current_time(UTC),
           "mode": MODE,
           "fps": FPS,
           "voxel_size": voxel_size,
           "plane_flag": plane_flag,
           "plane_iteration": plane_iteration,
           "current_frame_num" : frame_num}

    output_mpd = os.path.join(output_dir, 'live.json')

    with open(output_mpd, 'w') as f:
        json.dump(mpd, f, ensure_ascii=False, indent=2)



def get_current_time(UTC):

    timestamp = datetime.datetime.now(UTC)
    str_ts = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return str_ts

if __name__ == '__main__':

    main()
