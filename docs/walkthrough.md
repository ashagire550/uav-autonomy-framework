# UAV Autonomy Framework: Final Implementation Walkthrough

The framework has been fully upgraded with advanced algorithms and simulation support for **ROS 2 Humble** and **Gazebo Harmonic**.

## 🚀 Implemented Features

### 1. Vision-Based Target Tracking (YOLOv8)
The perception layer now uses YOLOv8 to detect and track targets. The `detection_node.py` processes raw camera streams and publishes precise bounding box data.

![YOLOv8 Detection Overlay](./docs/assets/uav_hero.png)

### 2. Advanced Control (PID & MAVSDK)
The `navigation_node.py` implements a PID-based tracking algorithm. It dynamically calculates:
- **Yaw Rate**: To keep the target centered in the frame.
- **Forward Velocity**: To maintain a constant distance to the target using the bounding box size as a depth proxy.

### 3. Gazebo Harmonic & ROS 2 Humble Integration
I have configured the `ros_gz_bridge` to link the following Gazebo topics to ROS 2:
- `/camera/image` (Vision)
- `/scan` (Lidar/Obstacles)
- `/world/default/model/uav/pose` (Ground Truth State)

## 🛠 Testing instructions

### To build and run the simulation:
```bash
docker-compose up
```

### Manual check of detection output:
```bash
ros2 topic echo /detection/objects
```

## ✅ Project Status
The repository is now fully documented, algorithmically complete for basic tracking, and ready for advanced simulation testing.
