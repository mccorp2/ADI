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

class VideoStreamer():
    def __init__(self):
        # https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
        self.camera = VideoCapture(0)
        self.frame_width = int(self.camera.get(CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(CAP_PROP_FRAME_HEIGHT))
        self.smile_detector = SmileDetector()
    
    def log(self, message, log_level=INFO):
        current_time=time.strftime('%H:%M:%S')
        print("{0} {1} video_streamer: {2}".format(log_level, current_time, message))
    
    def debug_stream(self):
        """ Developer function to stream a video and optionally apply a classifier for
        general debugging purposes. Useful for paramaterizing classifiers.
        """
        self.log("Staring video capture.")
        while True:
            self.check_interrupt()
            try:
                frame = self.get_frame()
                smile_rectangles = self.smile_detector.find_smiles(frame)
                processed_frame = overlay_rectangles(frame, smile_rectangles)
                
                # Display the resulting frame
                imshow('frame', processed_frame)
            except Exception as err:
                self.log(err, log_level=WARNING)
                continue

    def get_frame(self):
        """ Helper function to return all valid frames.

        return:
            frame: opencv image
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
        self.log("Starting cleanup.")
        try:
            self.log("Releasing camera.")
            self.camera.release()
            
            self.log("Closing windows.")
            destroyAllWindows()
        except Exception as e:
            self.log(f"cleanup failed due to {e}.")

def overlay_rectangles(image, rectangles):
        for (x, y, w, h) in rectangles: 
            rectangle(image, (x, y), ((x + w), (y + h)), (0, 0, 255), 2) 
        return image


if __name__ == "__main__":
    streamer = VideoStreamer()
    streamer.debug_stream()
