# ply_capture

## Usage

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
