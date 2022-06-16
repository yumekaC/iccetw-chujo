import json
import open3d as o3d
import glob
import os
import matplotlib.pyplot as plt

### setting
setting_path ="./setting.json"
with open (setting_path) as f:
    setting = json.load(f)

config_filename = setting['rs config file']
output_dirname = setting['output dir']
bag_filename_base = setting['sequence name']
num_offset = int(setting['offset frames'])
###

def main():

    output_path = create_output_directory()

    print ("extract bag file and save rgbd images")
    save_rgbd_frames(output_path)

    print ("remove first {} frames".format(num_offset))
    clean_images(output_path)    


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

def read_rs_config(config_filename):

    with open(config_filename) as cf:
        rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

    return rs_cfg

def read_bag_file(output_path):

    bag_filename = os.path.join(output_path, bag_filename_base + '.bag')

    bag_reader = o3d.t.io.RSBagReader()
    bag_reader.open(bag_filename)

    num_frames = 0

    ### read 1st frame
    im_rgbd = bag_reader.next_frame()
    num_frames += 1

    #show_frame(im_rgbd)

    ### continuous read frames
    while not bag_reader.is_eof():

        print("num frames: {}".format(num_frames))

        im_rbgd = bag_reader.next_frame()
        num_frames += 1

    bag_reader.close()

def show_frame(im_rgbd):

    plt.subplot(1, 2, 1)
    plt.imshow(im_rgbd.color)
    plt.subplot(1, 2, 2)
    plt.imshow(im_rgbd.depth)

    plt.show()

def save_rgbd_frames(output_path):

    bag_filename = os.path.join(output_path, bag_filename_base + '.bag')

    rgbd_video = o3d.t.io.RGBDVideoReader.create(bag_filename)
    rgbd_video.save_frames(output_path)

def clean_images(output_path):
    
    i = 0
    j = 0
    color_imgs = sorted(glob.glob(output_path+"/color/*.jpg"))
    for files in color_imgs:
        #print (files)
        if i < num_offset:
            os.remove(files)
        else:
            os.rename(files, output_path+"/color/"+ str(j) +".jpg")
            j += 1
        i += 1

    i = 0
    j = 0
    depth_imgs = sorted(glob.glob(output_path+"/depth/*.png"))
    for file in depth_imgs:
        if i < num_offset:
            os.remove(file)
        else:
            os.rename(file, output_path+"/depth/"+ str(j) +".png")
            j += 1
        i += 1


if __name__ == '__main__':

    main()
