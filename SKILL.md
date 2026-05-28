# UAV Autonomy Skill

This skill allows an AI agent to interface with the UAV Autonomy Framework to execute missions, monitor telemetry, and manage vision-based tracking.

## Capabilities

- **Mission Orchestration**: Set waypoints, start/stop missions, and manage flight modes via ROS2/MAVSDK.
- **Perception Management**: Configure tracking parameters, select targets, and monitor detection streams.
- **Telemetry Analysis**: Analyze real-time flight data and adjust mission parameters dynamically.

## Usage Instructions

### 1. Initializing the Environment
Ensure the ROS2 workspace is sourced and the simulation is running:
```bash
source install/setup.bash
# Assuming a consolidated launch file exists
ros2 launch uav_launch simulation_launch.py
```

### 2. Setting a Tracking Target
To set a target for the perception node, publish to the `/detection/target_class` topic:
```bash
ros2 topic pub /detection/target_class std_msgs/msg/String "{data: 'person'}"
```

### 3. Monitoring Health
Check the `/uav/status` topic for heartbeats and error messages:
```bash
ros2 topic echo /uav/status
```

## Integration Patterns

Agents should use the `run_command` tool to interact with the framework's CLI or the `view_file` tool to inspect log nodes.
