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

voxel_log = '_log_voxel_avg.csv'
frame_rate = 30
meta_filename = 'metadata.json'

### server info
server_ip = '133.9.96.57'
server_port = '33110'
server_protocol = 'http'

### buffer size
init_buffer = 30
min_buffer = 10
max_buffer = 100

def main():

    output_path, output_ply_path, output_proc_ply_path = create_output_directory()

    ### get number of ply frames
    num_frames = len(glob.glob(output_ply_path + '/*.ply'))

    ### proc: plane segment
    total_num_org, total_num_proc, total_data_org, total_data_proc = count_num_of_points(output_ply_path, output_proc_ply_path)

    log_filename = os.path.join(log_dirname, bag_filename_base + voxel_log)
    voxel_log_data = read_from_csv(log_filename)

    metadata = {}

    base_info = {'sequence_name': bag_filename_base,
                 'dir_name': {'root': output_dirname,
                              'org_ply': ply_dirname,
                              'proc_ply': 'proc'
                             },
                 'num_of_frames': num_frames,
                 'frame_rate': frame_rate,
                 'start_frame_num': 0,
                 'server_info': 'null',
                 'buffer_size': {'init': init_buffer,
                                 'max': max_buffer,
                                 'min': min_buffer
                                },
                 'representation': 'null'
                }
                 
    server_info = {'server_host': server_ip + ':' + server_port,
                   'server_protocol': server_protocol
                  }

    metadata = base_info
    metadata['server_info'] = server_info

    rep = []
    rep_id = 0
    voxel_size = 0

    init_rep = {'rep_id': rep_id,
                'voxel_size': voxel_size,
                'total_data_size': total_data_proc,
                'avg_data_size': round((total_data_proc/num_frames),2),
                'total_num_points': total_num_proc,
                'avg_num_points': round((total_num_proc/num_frames),2),
                'bitrate': round((total_data_proc*frame_rate)/num_frames,2)
                }

    rep.append(init_rep)

    for i in range(len(voxel_log_data)):

        rep_id = i + 1
        voxel_size = voxel_log_data[i][0]
        avg_data_proc = voxel_log_data[i][2]
        avg_num_proc = voxel_log_data[i][3]

        _rep = {'rep_id': rep_id,
                'voxel_size': round(voxel_size, 3),
                'total_data_size': round(avg_data_proc*num_frames,2),
                'avg_data_size': round(avg_data_proc,2),
                'total_num_points': round(avg_num_proc*num_frames,2),
                'avg_num_points': round(avg_num_proc,2),
                'bitrate': round((avg_data_proc*frame_rate),2)
               }

        rep.append(_rep)

    metadata['representation'] = rep

    print (json.dumps(metadata, indent=2))

    output_metadata = os.path.join(output_path, meta_filename)

    ### save metadata as a json file
    with open(output_metadata, 'w') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


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


def count_num_of_points(output_ply_path, output_proc_ply_path):

    _total_num_org = 0
    _total_num_proc = 0
    _total_data_org = 0
    _total_data_proc = 0

    num_ply = len(glob.glob(output_ply_path + '/*.ply'))

    for i in range(num_ply):

        org_ply = output_ply_path + '/' + str(i) + '.ply'
        proc_ply = output_proc_ply_path + '/' + str(i) + '.ply'

        org_pcd = o3d.io.read_point_cloud(org_ply)
        proc_pcd = o3d.io.read_point_cloud(proc_ply)

        org_pcd_array = np.asarray(org_pcd.points)
        proc_pcd_array = np.asarray(proc_pcd.points)

        _total_num_org = _total_num_org + len(org_pcd_array)
        _total_num_proc = _total_num_proc + len(proc_pcd_array)
        _total_data_org = _total_data_org + os.path.getsize(org_ply)
        _total_data_proc = _total_data_proc + os.path.getsize(proc_ply)

    return _total_num_org, _total_num_proc, _total_data_org, _total_data_proc


def read_from_csv(csv_filename):

    with open(csv_filename, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        data_list = [row for row in reader]

    return data_list

if __name__ == '__main__':

    main()
