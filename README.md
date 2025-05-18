# Instructions to run:
Pre-requisites:
- npm, python3

Support:
- This application has been verified on mac exclusivley.
- This application has been verified on chrome exclusivley.

Running this application necessitates two terminals, one for the backend, the other for the frontend.

## Running the backend:
The backend server is pretty simple and made of three components:
- VideoStreamer: opencv powered class to caputre video from the host machine
- SmileDetector: opencv powered classifier class to process images and detect faces
- Server: flask powered backend hosting a video stream, and metadata

To run the backend, simply call the run_backend shell script provided in `adi_backend`. This script creates a python virtual environment, installs the prerequisites and kicks off the backend server.

```
ADI]$ ./adi_backend/run_backend.sh
```

If you have trouble running this script you may need to add executable permissions on your machine first:
```
ADI]$ chmod +x adi_backend/run_backend.sh
ADI]$ ./adi_backend/run_backend.sh 
```

When this server is exited nominally you will find all detected faces are captured in `adi_backend/detected_smiles.json`. This object will come in the following form:

```
{
    "image": {
        "width": $WIDTH_PX,
        "height": $HEIGHT_PX,
    },
    "smiles": {
        "$GPS_TIME": {
            "$ID": "(x, y)",
            ...
        }
        ...
    }
}
```


## Running the frontend:
The fronetend is a extremly barebones UI. To run this application simply call start with `npm`.

```
ADI]$ cd adi_smile_react_app
ADI]$ npm start
```

Access this application by visitng `http://localhost:3000/`.