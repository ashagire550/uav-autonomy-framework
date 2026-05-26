#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2


class DetectionNode(Node):

    def __init__(self):
        super().__init__('detection_node')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            Image,
            '/detection/image',
            10
        )

        self.get_logger().info(
            'Detection Node Started'
        )

    def image_callback(self, msg):

        try:

            frame = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='bgr8'
            )

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            edges = cv2.Canny(
                gray,
                100,
                200
            )

            processed = cv2.cvtColor(
                edges,
                cv2.COLOR_GRAY2BGR
            )

            output_msg = self.bridge.cv2_to_imgmsg(
                processed,
                encoding='bgr8'
            )

            self.publisher.publish(output_msg)

        except Exception as e:

            self.get_logger().error(
                f'Error processing image: {str(e)}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = DetectionNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
