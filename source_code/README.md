# Point Cloud Streaming

## Requirement
Unity version: 2019.4.17f1

code for rendering: https://github.com/keijiro/Pcx

## Usage
Capturing RGB-D images and convert to point cloud sequence on server side.

Downloading and Rendering point cloud sequence on client side.

### In server side

### setting parameters

```
[setting.json]

{
  "sequence name": "greeting", # dataset name
  "number of frames": "10", # number of frames you want to capture
  "offset frames": "30", # offset frames (drop frames)
  "plane segmentation": "", # plane segmentation flag
  "output dir": "ply_dataset", # root directory for save all files
  "output ply dir": "ply", # directory name for save ply files
  "o3d config file": "o3d_config.json",
  "rs config file": "rs_config.json"
}
```

### capture bag file using RealSense L515
```bash
$python3 cap_ros_bag.py
```

### extract rgb and depth images from bag file
```bash
$python3 save_rgbd_img_from_bag.py
```

### create point cloud (ply file) from rgbd images
```bash
$python3 create_pointcloud_from_bag.py
```

### plane segmentation (crop background (e.g., wall)
```bash
$python3 plane_segmentation.py
```

This process takes approximately 3-5 sec per ply file

### voxel downsampling
```bash
$python3 voxel_down.py
```

### create metadata as a json file
```bash
$python3 create_metadata.py
```

### play ply sequence
```bash
$python3 play_ply.py <ply directory> <rotation flag>

[[example command]]
(with rotation)
$python3 play_ply.py ~/ply_dateset/test/ply true

(without rotation)
$python3 play_ply.py ~/ply_dataset/test/ply
(you don't need to specify 2nd argument)
```

Rotation: rotate 180 degree of ONLY x-axis

### show one ply file
```bash
$python3 show_ply.py <ply file (abs path)>

[[example command]]
$python3 show_ply.py ~/ply_dateset/test/ply/1.ply
```

### preparetion 
Create Apache server on sever machine.

Copy the published IP address (*) of the server. 

For only live streaming, prepare live.json

An example of live.json:
```
{
  "timestamp": "2022-04-17T02:33:24.734255Z",
  "mode": "live",
  "fps": 10,
  "voxel_size": 0.005,
  "plane_flag": "True",
  "plane_iteration": 20,
  "current_frame_num": 0
}
```

### In client side
In new Unity scene, create Resources folder in Assets folder and create new Material named MyDefault(.mat) in Resources folder.

Change to Shader: Point Cloud/Point in Inspector panel of MyDefault.mat.

Create Scripts folder in Assets folder. In Assets folder, create new two scripts named Live/Ondemand(.cs) and MyClass(.cs), and then replace code with the github code [Live.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/Live.cs)/[Ondemand.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/Ondemand.cs) and [MyClass.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/MyClass.cs). In Live.cs/Ondemand.cs, change from XXXX to the copied IP address (*).

Create new GameObject in Hierarchy and add code of Live.cs/Ondemand.cs by pushing Add Component button in Inspector panel.

Play the scene.

