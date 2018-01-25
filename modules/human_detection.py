#!/usr/bin/env python

"""
    Detection.

    The class is able to detect the
    presence of humans in the image
    feed of the robot.
"""

# import the necessary packages
from cv_bridge import CvBridge, CvBridgeError
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os

class HumanDetection:

    def __init__(self):
        """ Class constructor """

        self.bridge = CvBridge()

        # Define detection's target/s
        self.target = ["person"]

        # Bounding boxes colours
        self.colours = np.random.uniform(0, 255, size=(len(self.target), 3))

        # Load NN's serialised model
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe("/home/itaouil/tiago_ws/src/human_aware_robot_navigation/src/HARN/modules/MobileNetSSD_deploy.prototxt.txt",
                                            "/home/itaouil/tiago_ws/src/human_aware_robot_navigation/src/HARN/modules/MobileNetSSD_deploy.caffemodel")

    def detect(self, frame):
        """
            Returns the frame with recognitions.
        """

        # Save frame in memory
        print("PRINT: ", os.path.abspath(os.path.join(os.path.dirname( __file__ ))))
        cv2.imwrite(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'frame.png')), frame)

        # Resize image to be maximum 400px wide
        frame = imutils.resize(frame, width = 400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.8:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.target[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), self.colours[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colours[idx], 2)

        return frame
