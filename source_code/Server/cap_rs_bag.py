import open3d as o3d
import time
import json
import os
import datetime

### setting 
setting_path ="./setting.json"
with open (setting_path) as f:
    setting = json.load(f)

config_filename = setting['rs config file']
output_dirname = setting['output dir']
bag_filename_base = setting['sequence name']
NUM = int(setting['number of frames'])
###

def main():
    
    output_path = create_output_directory()
    cap_bag_rs(output_path)

### parepare outout directory
def create_output_directory():

    #timestamp = datetime.datetime.now()
    #dt_str = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    #output_path = os.path.join(os.environ['HOME'], output_dirname, dt_str)
    output_path = os.path.join(os.environ['HOME'], output_dirname, bag_filename_base)

    if os.path.exists(output_path) == False:
        os.makedirs(output_path)

    print ("output path: {}".format(output_path))

    return output_path

### capture bag file from realsense
def cap_bag_rs(output_path):

    t0 = time.time()

    with open(config_filename) as cf:
        rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

    rs = o3d.t.io.RealSenseSensor()

    bag_file_name = os.path.join(output_path, bag_filename_base +'.bag')

    rs.init_sensor(rs_cfg, 0, bag_file_name)
    rs.start_capture(True)

    t1 = time.time()
    for fid in range(NUM):
        im_rgbd = rs.capture_frame(True, True)
    t2 = time.time()

    print ("capture {} frames".format(NUM))
    print ("prepare camerae {}".format(t1-t0))
    print ("delay {}".format(t2-t1))

    rs.stop_capture()

if __name__ == '__main__':

    main()

