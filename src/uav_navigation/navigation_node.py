#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from mavsdk import System
import asyncio

class NavigationNode(Node):
    def __init__(self):
        super().__init__('uav_navigation_node')
        
        self.get_logger().info('🚀 UAV Navigation Node Started')
        
        # Publisher for goal pose (for simulation or ROS2 control)
        self.goal_publisher = self.create_publisher(PoseStamped, '/goal_pose', 10)
        
        # Timer to send waypoints periodically
        self.timer = self.create_timer(5.0, self.send_waypoint_callback)
        
        self.current_waypoint = 0
        self.waypoints = [
            (10.0, 0.0, 5.0),
            (10.0, 10.0, 5.0),
            (0.0, 10.0, 5.0),
            (0.0, 0.0, 5.0)
        ]

    def send_waypoint_callback(self):
        if self.current_waypoint < len(self.waypoints):
            x, y, z = self.waypoints[self.current_waypoint]
            self.send_waypoint(x, y, z)
            self.current_waypoint += 1
        else:
            self.get_logger().info('✅ Mission completed!')

    def send_waypoint(self, x: float, y: float, z: float):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        pose.pose.orientation.w = 1.0  # No rotation
        
        self.goal_publisher.publish(pose)
        self.get_logger().info(f'📍 Going to waypoint: ({x}, {y}, {z})')

def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down navigation node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
