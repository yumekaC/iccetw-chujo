# Point Cloud Streaming

## Requirement
Unity version: 2019.4.17f1

code for rendering: https://github.com/keijiro/Pcx

## Usage
Capturing RGB-D images and convert to point cloud sequence on server side.

Downloading and Rendering point cloud sequence on client side.

### In server side

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

```
python3 ply_streamer.py
```

### In client side
In new Unity scene, create Resources folder in Assets folder and create new Material named MyDefault(.mat) in Resources folder.

Change to Shader: Point Cloud/Point in Inspector panel of MyDefault.mat.

Create Scripts folder in Assets folder. In Assets folder, create new two scripts named Live/Ondemand(.cs) and MyClass(.cs), and then replace code with the github code [Live.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/Live.cs)/[Ondemand.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/Ondemand.cs) and [MyClass.cs](https://github.com/yumekaC/iccetw-chujo/blob/main/source_code/Client/MyClass.cs). In Live.cs/Ondemand.cs, change from XXXX to the copied IP address (*).

Create new GameObject in Hierarchy and add code of Live.cs/Ondemand.cs by pushing Add Component button in Inspector panel.

Play the scene.

