# ofxViveTracker-OSC
This addon utilizes a python script (in the folder "client") to send OSC messages from the Vive system to the OF Application. 

The scripts "vivetracker_client-send-unqiue-id-and-position.py" and "vivetracker_client-send-unqiue-id-position-quaternion.py" can be used to send position or position and quaternions for generic trackers (pucks) with unique ID's over OSC.

### How to Use
- Tested on Windows 10 only.
- Setup HTC Vive.
- Install [Anaconda Package](https://www.continuum.io/downloads) for Python 3.6
  - Although this addon does not depend on [triad_openvr](https://github.com/TriadSemi/triad_openvr), [this instruction](http://www.roadtovr.com/how-to-use-the-htc-vive-tracker-without-a-vive-headset/) is also applicable to disable HMD requirement, 
```
pip install pyopenvr
pip install python-osc
```
- Run Anaconda Prompt and go to ```ofxViveTracker-OSC/client``` directory, then
```
python vivetracker_osc.py --host [HOST] --port [PORT] --fps [FPS]
```

### Tested Environment
- OF0.9.8 + VS2015 on Windows 10
