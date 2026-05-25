from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='uav_navigation',
            executable='navigation_node',
            name='navigation_node',
            output='screen'
        ),
        Node(
            package='uav_perception',
            executable='detection_node',
            name='detection_node',
            output='screen'
        ),
    ])
