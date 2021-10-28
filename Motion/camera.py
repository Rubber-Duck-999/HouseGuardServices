from time import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image
import cv2
import imutils
import logging
import datetime
import time


class ImageTaken(Exception):
    '''Exception to get out of capture'''


class Camera:
    def __init__(self):
        self.raw_capture = None
        self.min_frames = 8
        self.camera = None
        self.motion_counter = 0
        self.motion = False
        self.timestamp = None
        self.last_updated = None

    def reset(self):
        logging.info('reset()')
        self.raw_capture = None
        self.min_frames = 8
        self.camera = None
        self.motion_counter = 0
        self.motion = False
        self.timestamp = None
        self.last_updated = None

    def get_base_image(self):
        # initialize the camera and grab a reference to the raw camera capture
        logging.info('get_base_image()')
        try:
            logging.info("Starting up camera")
            self.camera = PiCamera()
            self.camera.resolution = [640, 480]
            self.camera.framerate = 8
            self.raw_capture = PiRGBArray(self.camera, size=[640, 480])
            time.sleep(10)
        except:
            logging.error("Camera failure")

    def check_motion(self, frame):
        '''Calcultes whether a motion has occurred'''
        logging.info('check_motion()')
        # check to see if the room is occupied
        if self.motion:
            # check to see if enough time has passed between uploads
            if (self.timestamp - self.last_updated).seconds >= 3:
                # increment the motion counter
                self.motion_counter = self.motion_counter + 1

                # check to see if the number of frames with consistent motion is
                # high enough
                if self.motion_counter >= 8:
                    # check to see if we should take pictures
                    logging.info("Motion detected")
                    image = "{}/img.jpg".format('/home/pi/Desktop/cam_images/')
                    logging.info("Creating file: {}".format(image))
                    cv2.imwrite(image, frame)
                    colorImage = Image.open(image)
                    transposed = colorImage.rotate(180)
                    transposed.save(image)
                    logging.info("Image created")
                    self.last_uploaded = self.timestamp
                    self.motion_counter = 0
                    self.camera.close()
        # otherwise, the room is not occupied
        else:
            logging.info('Resetting motion counter')
            self.motion_counter = 0

    def check_motion_capture(self):
        '''Calcultes whether a human or colour shade has drastically
        changed the raw image'''
        logging.info('check_motion_capture()')
        average_frame = None
        for capture in self.camera.capture_continuous(self.raw_capture, format="bgr", use_video_port=True):
            # resize the frame, convert it to grayscale, and blur it
            self.timestamp = datetime.datetime.now()
            frame = capture.array
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the average frame is None, initialize it
            if average_frame is None:
                logging.info("Starting background model")
                average_frame = gray.copy().astype("float")
                self.raw_capture.truncate(0)

            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(gray, average_frame, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(average_frame))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(
                thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            # loop over the contours
            for c in contours:
                # if the contour is large, use it
                if cv2.contourArea(c) >= 5000:
                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)
                    self.motion = True
            found = self.check_motion(frame)
            if found:
                self.camera.close()
            else:
                self.raw_capture.truncate(0)

    def run_capture(self):
        '''Setup for running capture'''
        logging.info('run_capture()')
        try:
            self.reset()
            self.get_base_image()
            self.check_motion_capture()
        except Exception as error:
            logging.error('Error found on camera capture: {}'.format(error))
