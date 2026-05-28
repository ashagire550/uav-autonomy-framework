# UAV Autonomy Framework Expansion Plan

This plan outlines the steps to transform the current basic ROS2 framework into a production-grade autonomous UAV tracking and navigation system.

## User Review Required

> [!IMPORTANT]
> The current implementation has been upgraded to YOLOv8 for robust object detection and tracking. Future steps include integrating ESDF-based path planning.

## Proposed Changes

### Perception Layer (Implemented)
- **YOLOv8 Integration**: Real-time object detection and tracking using the `ultralytics` framework.
- **Metadata Output**: Publishing JSON-encoded detection data to `/detection/objects`.

### Navigation & Control Layer (Implemented)
- **PID-Based Target Following**: A P-controller that adjusts forward velocity and yaw rate based on target bounding box position and size.
- **MAVSDK Offboard Control**: Asynchronous integration with PX4 for velocity-based maneuvers.

### Documentation & Infrastructure (Implemented)
- **Gazebo Harmonic Support**: Utilizes `ros_gz_bridge` for seamless data flow.
- **Docker Environment**: A pre-configured Docker container with GUI support.

## Open Questions

- Should we focus on a specific target type (e.g., person, vehicle) for the final field tests?
- Are there specific flight constraints (max altitude/speed) for your testing area?

## Verification Plan

### Automated Tests
- `colcon build --packages-select uav_navigation uav_perception`
- `ros2 launch uav_navigation simulation_launch.py --use_sim_time:=true`
