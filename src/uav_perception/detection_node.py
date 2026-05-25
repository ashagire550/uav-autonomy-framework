#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2

class DetectionNode(Node):
    def __init__(self):
        super().__init__('uav_detection_node')
        self.get_logger().info('👁️ UAV Vision Detection Node Started')
        
        self.bridge = CvBridge()
        # Load YOLO model (nano model for faster performance)
        self.model = YOLO('yolov8n.pt')
        
        # Subscriber for raw camera images from drone/simulation
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        
        # Publisher for annotated images
        self.publisher = self.create_publisher(Image, '/detection/image_annotated', 10)

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Run YOLO detection
            results = self.model(cv_image, conf=0.5, verbose=False)
            
            # Draw bounding boxes and labels
            annotated_frame = results[0].plot()
            
            # Publish the annotated image
            annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, "bgr8")
            self.publisher.publish(annotated_msg)
            
            # Log detections
            num_detections = len(results[0].boxes)
            if num_detections > 0:
                self.get_logger().info(f'✅ Detected {num_detections} objects')
                
        except Exception as e:
            self.get_logger().error(f'Error processing image: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down detection node...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
