from cv2 import (
    CAP_PROP_FRAME_WIDTH,
    CAP_PROP_FRAME_HEIGHT,
    VideoCapture,
    destroyAllWindows,
    imshow,
    waitKey,
)
import time

INFO="INFO"
WARNING="WARNING"
ERROR="ERROR"

class video_streamer():
    def __init__(self):
        # https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
        self.camera = VideoCapture(0)
        self.frame_width = int(self.camera.get(CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.camera.get(CAP_PROP_FRAME_HEIGHT))
    
    def log(self, message, log_level=INFO):
        current_time=time.strftime('%H:%M:%S')
        print("{0} {1} video_streamer: {2}".format(log_level, current_time, message))
    
    def stream(self):
        self.log("Staring video capture.")
        while True:
            self.check_interrupt()
            try:
                frame = self.get_frame()
            except Exception as err:
                self.log(err, log_level=WARNING)
                continue
            
            # Display the resulting frame
            imshow('frame', frame)

    def get_frame(self):
        # Grab camera frame
        status, frame = self.camera.read()
        if not status:
            raise Exception(
                "Failed to capture image."
            )

        return frame

    def check_interrupt(self):
        # Press 'q' to exit
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


if __name__ == "__main__":
    streamer = video_streamer()
    streamer.stream()
    
    
