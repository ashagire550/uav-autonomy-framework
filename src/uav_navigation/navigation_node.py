#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityBodyYawspeed
import asyncio
import json
import threading

class NavigationNode(Node):
    def __init__(self):
        super().__init__('uav_navigation_node')
        
        self.get_logger().info('🚀 UAV Advanced Navigation Node Started')
        
        # Parameters
        self.declare_parameter('kp_velocity', 0.1)
        self.declare_parameter('kp_yaw', 0.005)
        self.declare_parameter('target_distance', 5.0) # Meters
        
        # MAVSDK System
        self.drone = System()
        self.connected = False
        
        # Subscriptions
        self.object_sub = self.create_subscription(String, '/detection/objects', self.object_callback, 10)
        
        # State
        self.target_locked = False
        self.target_bbox = None # [x1, y1, x2, y2]
        self.image_width = 640 # Default
        self.image_height = 480
        
        # Start MAVSDK loop in a separate thread
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_async_loop, daemon=True)
        self.thread.start()

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_mavsdk())

    async def run_mavsdk(self):
        self.get_logger().info('🔗 Connecting to UAV via MAVSDK...')
        # Default SITL address
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                self.get_logger().info('✅ UAV Connected!')
                self.connected = True
                break

        # Ensure we are in Offboard mode
        # Note: In a real scenario, we'd need to arm and takeoff first
        
        # Main Control Loop
        while rclpy.ok():
            if self.target_locked and self.target_bbox:
                await self.execute_follow_logic()
            await asyncio.sleep(0.05) # 20Hz control loop

    async def execute_follow_logic(self):
        """PID control to follow target based on bounding box"""
        if not self.connected:
            return

        x1, y1, x2, y2 = self.target_bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        
        # Errors
        error_x = center_x - (self.image_width / 2)
        
        # Calculate BBox height as a proxy for distance
        bbox_height = y2 - y1
        target_height = 150 # Target height in pixels at desired distance
        error_dist = target_height - bbox_height
        
        # PID gains (simplified P-gain)
        kp_v = self.get_parameter('kp_velocity').value
        kp_y = self.get_parameter('kp_yaw').value
        
        forward_vel = kp_v * error_dist
        yaw_rate = kp_y * error_x
        
        # Clamp values
        forward_vel = max(min(forward_vel, 2.0), -1.0) # Max 2m/s forward, 1m/s back
        yaw_rate = max(min(yaw_rate, 30.0), -30.0) # Max 30 deg/s
        
        try:
            await self.drone.offboard.set_velocity_body(
                VelocityBodyYawspeed(forward_vel, 0.0, 0.0, yaw_rate)
            )
        except OffboardError as e:
            self.get_logger().error(f'❌ Offboard error: {e._result.result}')

    def object_callback(self, msg):
        try:
            detections = json.loads(msg.data)
            # Focus on 'person' for tracking
            for det in detections:
                if det['name'] == 'person':
                    self.target_locked = True
                    self.target_bbox = det['bbox']
                    return
            
            # If no target found, stop moving
            if self.target_locked:
                self.target_locked = False
                # Optionally send zero velocity command here
        except Exception as e:
            self.get_logger().error(f'Error parsing detections: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = NavigationNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
