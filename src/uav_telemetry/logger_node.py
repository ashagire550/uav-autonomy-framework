#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class LoggerNode(Node):

    def __init__(self):
        super().__init__('logger_node')

        # Subscribe to telemetry topic
        self.subscription = self.create_subscription(
            String,
            '/uav/status',
            self.status_callback,
            10
        )

        self.get_logger().info(
            'Logger Node Started'
        )

    def status_callback(self, msg):

        telemetry_data = msg.data

        self.get_logger().info(
            f'Received Telemetry: {telemetry_data}'
        )

        # Save telemetry to log file
        with open(
            'uav_telemetry.log',
            'a'
        ) as log_file:

            log_file.write(
                telemetry_data + '\n'
            )


def main(args=None):

    rclpy.init(args=args)

    node = LoggerNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
