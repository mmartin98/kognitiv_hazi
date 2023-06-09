#!/usr/bin/env python3

# Python package-ek
import cv2
import numpy as np

# ROS package-ek (python)
import rospy
from cv_bridge import CvBridge

# Uzenetek
from sensor_msgs.msg import Image

class LineDetector:
    def __init__(self):
        self.bridge = CvBridge()

        self.detection = Image()
        self.publisher = rospy.Publisher('line_follower', Image, queue_size=1)

    def read_image(self, message: Image):
        '''
        Beolvassa a ROS uzenetet es egy numpy tombbe konvertalja.
        Gauss-fele elmosast alkalmaz és az elmosodott kepet HSV formatumba alakitja.

        Bemenetek
        ---
            message: sensor_msgs.msg.Image
                Erzekelo kepuzenete
        '''

        self.image = self.bridge.imgmsg_to_cv2(message, desired_encoding='bgr8')
        self.blurred = cv2.GaussianBlur(self.image, ksize=(3, 3), sigmaX=.1, sigmaY=.1)
        self.blurred_hsv = cv2.cvtColor(self.blurred, cv2.COLOR_BGR2HSV)
        
        self.height, self.width, _ = self.image.shape

    def get_direction(self, message=None, line_color='red', tol=10):
        '''
        Egy kepuzenetet ha megadunk neki, akkor abbol megmondja az iranyt amit a robotnak kovetnie kell ahhoz, hogy a vonalat kovesse.
        Az iranyt legfokeppen a vonal szine alapjan szamitja ki.

        Bemenetek
        ---
            message: sensor_msgs.msg.Image
                Erzekelo kepuzenete

            line_color: str
                Vonal szine: "red" (piros) vagy "black" (fekete)
            
            tol: int, default = 10
                Megengedett tureshatar az irany kiszamitasahoz

        Kimenetek
        ---
            dir: int
                Az irany amit a robotnak kovetnie kell:
                    Megall (Stop) = 0; Egyenesen megy (Straight) = 1; Balra megy (Left) = 2; Jobbra megy (Right) = 3;
        '''
        
        if message:
            self.read_image(message)

        if line_color == 'red':
            lower = np.array([0, 100, 100])
            upper = np.array([10, 255, 255])

        if line_color == 'black':
            lower = np.array([0, 0, 0])
            upper = np.array([179, 20, 155])
        
        mask = cv2.inRange(self.blurred_hsv, lower, upper)

        search_y = int(self.height*2/5)
        mask[:search_y, ] = 0
        moments = cv2.moments(mask)

        try:
            cx = int(moments['m10']/moments['m00'])

            contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(max(contours, key=np.size))

            cv2.rectangle(self.image, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (79, 16, 41), 2)
            cv2.putText(self.image, 'Utvonalkereses', (rect_x - 2, rect_y - 8), cv2.FONT_HERSHEY_DUPLEX, .4, (79, 16, 41))

            self.detection = self.bridge.cv2_to_imgmsg(self.image, encoding='bgr8')
            self.publisher.publish(self.detection)


        except ZeroDivisionError:
            cv2.putText(self.image, '[WARNING] Nincs utvonal', (int(self.width/5), 20), cv2.FONT_HERSHEY_DUPLEX, .5, (0, 0, 255))
            
            self.detection = self.bridge.cv2_to_imgmsg(self.image, encoding='bgr8')
            self.publisher.publish(self.detection)


            rospy.logwarn('Nincs utvonal')
            return 0
        
        if cx > self.width/2 - tol and cx < self.width/2 + tol:
            return 1
        if cx < self.width/2 - tol:
            return 2
        if cx > self.width/2 + tol:
            return 3

if __name__ == '__main__':
    image_processor = LineDetector()