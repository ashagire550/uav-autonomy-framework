import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # ROS-GZ Bridge (Gazebo Harmonic)
    # This bridge connects Gazebo topics to ROS2 topics
    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Format: /gazebo/topic@ros_msg_type[gz_msg_type
            '/camera/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/world/default/model/uav/pose@geometry_msgs/msg/Pose[gz.msgs.Pose',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    # uav_perception node
    detection_node = Node(
        package='uav_perception',
        executable='detection_node.py',
        name='uav_detection_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # uav_navigation node
    navigation_node = Node(
        package='uav_navigation',
        executable='navigation_node.py',
        name='uav_navigation_node',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'kp_velocity': 0.1},
            {'kp_yaw': 0.005}
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'
        ),
        gz_bridge,
        detection_node,
        navigation_node
    ])
