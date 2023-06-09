#!/usr/bin/env python3

# ROS package (python)
import rospy

# Uzenetek
from sensor_msgs.msg import Image

# Modul importalas
from motion import MotionPlanner
from detector import LineDetector

class Follower:
    def __init__(self):
        self.detector = LineDetector()
        self.motion_planner = MotionPlanner()

        rospy.init_node('line_follower')
        self.rate = rospy.Rate(30)
        self.subscriber = rospy.Subscriber('camera/image', Image, self.camera_callback)

    def run(self):
        while not rospy.is_shutdown():
            self.rate.sleep()
        

    def camera_callback(self, msg):
        direction = self.detector.get_direction(message=msg, line_color='red', tol=15)
        self.motion_planner.move(direction)

if __name__ == '__main__':
    follower = Follower()
    follower.run()