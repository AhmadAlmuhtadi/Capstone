T1:
cd ~/ardupilot/ArduCopter ; ../Tools/autotest/sim_vehicle.py --map --console

mode GUIDED
arm throttle 
takeoff {meters}

T2: Just run gazebo and manually input the model or:
gazebo --verbose worlds/iris_arducopter_runway.world

T3:
roslaunch capstone_mavros capstone_mavros.launch 

udp://127.0.0.1:14551@14555

------------------------------------

Feb 26: Testing
T1:
sim_vehicle.py -v ArduCopter -f gazebo-iris -m --mav10 --out=udp:127.0.0.1:14550 --console -I1 –add-param-file=/home/ardupilot/Tools/autotest/default_params/gazebo-iris.parm -w
March17: sim_vehicle.py -v ArduCopter -f y6 -m --mav10 --out=udp:127.0.0.1:14550 --console -I1 

march1 edit: --mavproxy-args="--streamrate=50" removed


T2:
roslaunch capstone_mavros capstone_mavros.launch

T3: Not required
Downloads/QGroundControl.AppImage

T4: Just run gazebo and manually input the model or:
gazebo --verbose worlds/iris_arducopter_runway.world

T5:
rostopic echo /mavros/state


T3 commands:
rosservice call /mavros/set_mode "custom_mode: 'GUIDED'"

rosservice call /mavros/cmd/arming "value: true"

rosservice call /mavros/cmd/takeoff "{min_pitch: 0.0, yaw: 0.0, latitude: 0.0, longitude: 0.0, altitude: 5.0}


Run in terminal for takeoff:
rosservice call /mavros/cmd/takeoff "{min_pitch: 0.0, yaw: 0.0, latitude: 0.0, longitude: 0.0, altitude: 5.0}" 

/mavros/setpoint_position/local

rosrun capstone_mavros waypoint.py

rostopic pub /mavros/setpoint_position/local geometry_msgs/PoseStamped

Notes:
- To make file executable: chmod +x FILEPATH
- to restart after frame change in qground, go parameters, tools, reboot


Command lines to run March 25:


sim_vehicle.py -v ArduCopter -f gazebo-iris -m --mav10 --out=udp:127.0.0.1:14550 --console -I1
roslaunch ardu_urdf_sandbox mav.launch

To be able to publish messages run:

roslaunch capstone_mavros capstone_mavros.launch
rostopic pub /mavros/setpoint_position/local geometry_msgs/PoseStamped "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
pose:
  position:
    x: 0.0
    y: 1.0
    z: 0.8
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 0.0" 

rostopic pub /mavros/local_position/pose geometry_msgs/PoseStamped "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: ''
pose:
  position:
    x: 0.0
    y: 0.0
    z: 2.0
  orientation:
    x: 0.0
    y: 0.0
    z: -0.7
    w: -0.7"




To check with Dimitris: things i changed
- catkin_make mav_msgs error, check CMakeLists.txt

- AP:Prearm:Rangefinder 1: Not detected
  -fixed through qground control > top left > vehicle setup > safety

- Useless since we run gazebo-iris: 
  -ardupilot/tools/autotest/pysim/vehicleinfo.py
  -tried adding the line "external": True, to y6


    ardupilot/Tools/autotest/sim_vehicle.py -f gazebo-iris --console
  April 1 Run test for tricopter y6 terminal commands with full waypoint navigation: In that same order

  cd ~/ardupilot/ArduCopter
  ../Tools/autotest/sim_vehicle.py -f gazebo-iris --console 
  roslaunch ardu_urdf_sandbox mav.launch
  roslaunch capstone_mavros capstone_mavros.launch
  rosrun capstone_mavros waypoint.py


  rostopic list

  VICON updates:

  April 12: 
    Installed vrpn_client_ros successfully

    Steps:
    - Open vicon tracker 3.9 on PC for visuals. Select the correct drone as an object
    - On local laptop, run:
    roslaunch vrpn_client_ros sample.launch server:=192.168.1.2

    rostopic echo /vrpn_client_node/F550/pose

    rosrun logging_measurements vrpn_log_all


  IP 
    192.168.1.2


    April 14: Work on the NUC

    - Installed ros melodic
    - Installed vrpn-client-ros (shows in opt/ros/melodic/lib)
    - Installed mavros
    - Cloned RISC/Leader file to catkin_ws/src
    - 



    mono MissionPlanner.exe


    roslaunch mavros apm.launch fcu_url:="/dev/ttyACM1:57600"
    roslaunch mavros apm.launch fcu_url:="/dev/ttyACM1:921600"