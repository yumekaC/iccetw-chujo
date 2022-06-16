import open3d as o3d
import time
import os
import numpy as np
import csv
import glob
import json

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
csv_filename = "log_all.csv"
csv_filename2 = "log_average.csv"

def main():

    output_path, output_ply_path, output_proc_ply_path = create_output_directory()

    ### get number of ply frames
    num_ply = len(glob.glob(output_ply_path + '/*.ply'))
    #num_ply = 10

    voxel_size = 0.001
    logs = []
    average_logs = []

    while True:

        _temp = str(round(voxel_size,3)).replace('.', '')
        output_voxel_path = os.path.join(output_path, _temp)
        if os.path.exists(output_voxel_path) == False:
            os.makedirs(output_voxel_path)

        _proc_time = 0
        _data_size = 0
        _num_points = 0

        for i in range(num_ply):
            
            ply_filename = os.path.join(output_proc_ply_path, str(i) + '.ply')

            pcd = o3d.io.read_point_cloud(ply_filename)
            #print (pcd)
 
            t1 = time.time()
            downpcd = pcd.voxel_down_sample(voxel_size)
            t2 = time.time()

            point_array = np.asarray(downpcd.points)

            output_filename = os.path.join(output_voxel_path, str(i)+'.ply')

            o3d.io.write_point_cloud(output_filename, downpcd, False, True)

            print ("frame_num, voxel_size, proc_time, # of points, file size {} {} {} {} {}"
                .format(i, voxel_size, t2-t1, len(point_array), os.path.getsize(output_filename)))

            logs.append([i, voxel_size, t2-t1, len(point_array), os.path.getsize(output_filename)])

            _proc_time = _proc_time + t2-t1
            _data_size = _data_size + os.path.getsize(output_filename)
            _num_points = _num_points + len(point_array)

        average_logs.append([voxel_size, _proc_time/num_ply, _data_size/num_ply, _num_points/num_ply])

        voxel_size = voxel_size + 0.001
        if voxel_size > 0.051:
            break

    log_all_file = os.path.join(log_dirname, bag_filename_base + '_log_voxel_all.csv')
    log_avg_file = os.path.join(log_dirname, bag_filename_base + '_log_voxel_avg.csv')

    write_to_csv(log_all_file, logs)
    write_to_csv(log_avg_file, average_logs)

    #o3d.visualization.draw_geometries([downpcd])

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

def write_to_csv(csv_filename, data):

    with open(csv_filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == '__main__':

    main()
