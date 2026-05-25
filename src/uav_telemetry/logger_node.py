#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from mavsdk import System
import asyncio
import json
from datetime import datetime

class TelemetryLogger(Node):
    def __init__(self):
        super().__init__('uav_telemetry_logger')
        self.get_logger().info('📡 UAV Telemetry Logger Started')
        
        self.drone = System()
        self.log_file = f"flight_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    async def run(self):
        await self.drone.connect(system_address="udp://:14540")
        self.get_logger().info('✅ Connected to drone')

        async for state in self.drone.telemetry.position():
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "latitude": state.latitude_deg,
                "longitude": state.longitude_deg,
                "altitude": state.relative_altitude_m
            }
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_data) + '\n')
            self.get_logger().info(f"Logged position: {state.latitude_deg}, {state.longitude_deg}")

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
