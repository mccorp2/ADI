from smile_detector import SmileDetector
from video_steamer import VideoStreamer
from cv2 import imencode
import time
import json

from flask import Flask, render_template, Response
from flask_cors import CORS

streamer = VideoStreamer()
smile_detector = SmileDetector()

app = Flask(__name__)
CORS(app)

@app.route('/')
def proccess_stream(streamer):
    while True:
        frame = streamer.get_frame()
        processed_frame = smile_detector.process_frame(frame)
        ret, buffer = imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(proccess_stream(streamer),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/smiles')
def upload_smiles():
    """ Endpoint to upload image/smile metadata too. Returns a json object.
    
    Keys:
    - image: width, height
    - simles: index, coordinates
    """

    # Get image metadata
    image_metadata_dict = {"image": (streamer.frame_width, streamer.frame_height)}

    # Get smile data
    smile_coords = smile_detector.get_smile_coords()
    smile_coords_str = [f"({str(x)}, {str(y)})" for x, y in smile_coords]
    smile_dict = {"smiles": 
        {f" {index}:": value for index, value in enumerate(smile_coords_str)}
    }

    return json.dumps(image_metadata_dict | smile_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, threaded=True, use_reloader=False)
