#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import json

class DetectionNode(Node):

    def __init__(self):
        super().__init__('uav_detection_node')
        
        # Initialize YOLOv8 model (Nano version for real-time performance)
        self.model = YOLO('yolov8n.pt')
        self.bridge = CvBridge()

        # Subscriptions
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Publishers
        self.image_publisher = self.create_publisher(
            Image,
            '/detection/image',
            10
        )
        self.object_publisher = self.create_publisher(
            String,
            '/detection/objects',
            10
        )

        self.get_logger().info('🔍 YOLOv8 Detection Node Started')

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Run YOLOv8 inference
            results = self.model(frame, verbose=False)
            
            # Process detections
            detections = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    # Get box coordinates, confidence, and class
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    name = self.model.names[cls]
                    
                    detections.append({
                        'name': name,
                        'confidence': conf,
                        'bbox': [float(x1), float(y1), float(x2), float(y2)]
                    })

                    # Draw bounding box on frame
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f'{name} {conf:.2f}', (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Publish processed image
            output_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.image_publisher.publish(output_msg)

            # Publish detection metadata as JSON string
            if detections:
                meta_msg = String()
                meta_msg.data = json.dumps(detections)
                self.object_publisher.publish(meta_msg)

        except Exception as e:
            self.get_logger().error(f'❌ Error in detection callback: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
