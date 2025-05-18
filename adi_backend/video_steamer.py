""" To Do:
remove object detection from VideoStreamer class. Allow classifiers to be applied to a stream.



"""

from cv2 import (
    CAP_PROP_FRAME_WIDTH,
    CAP_PROP_FRAME_HEIGHT,
    VideoCapture,
    destroyAllWindows,
    imshow,
    waitKey,
    rectangle
)
import time

from smile_detector import SmileDetector

INFO="INFO"
WARNING="WARNING"
ERROR="ERROR"

def log(process, message, log_level=INFO):
    current_time=time.strftime('%H:%M:%S')
    print("{0} {1} {2}: {3}".format(log_level, current_time, process, message))

class VideoStreamer():
    def __init__(self):
        # https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
        self.camera = VideoCapture(0)
        self.frame_width = int(self.camera.get(CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(CAP_PROP_FRAME_HEIGHT))

    def log(self, message, log_level=INFO):
        log("video_streamer", message, log_level)

    def get_frame(self):
        """ Helper function to return all valid frames.
        Return:
        -frame: opencv image
        """

        status, frame = self.camera.read()
        if not status:
            raise Exception(
                "Failed to capture image."
            )

        return frame

    def check_interrupt(self):
        """ Allow case interupt for server
        """

        if waitKey(1) & 0xFF == ord('q'):
            raise KeyboardInterrupt(
                "Server recieved keyboard interrupt."
            )

    def __del__(self):
        """ Cleanup function performed on server shutdonw.
        Tasks: 
        - Release camera from program.
        - Close all windows opened.
        """

        self.log("Starting cleanup.")
        try:
            self.log("Releasing camera.")
            self.camera.release()
            
            self.log("Closing windows.")
            destroyAllWindows()
        except Exception as e:
            self.log(f"cleanup failed due to {e}.")

def debug_classifiers():
    """ Developer function to stream a video and optionally apply a classifier for
    general debugging purposes. Useful for paramaterizing classifiers.
    """

    streamer = VideoStreamer()
    streamer.log("Staring video capture.")

    smile_detector = SmileDetector()

    while True:
        streamer.check_interrupt()
        try:
            frame = streamer.get_frame()
            processed_frame = smile_detector.process_frame(frame)
            
            # Display the resulting frame
            imshow('frame', processed_frame)
        except Exception as err:
            streamer.log(err, log_level=WARNING)
            continue


if __name__ == "__main__":
    debug_classifiers()
