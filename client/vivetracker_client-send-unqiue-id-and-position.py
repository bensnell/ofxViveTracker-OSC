import openvr
import time
import sys
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

# Initialize OpenVR in the 
vr = openvr.init(openvr.VRApplication_Other)

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
parser.add_argument("--fps", type=int, default=60, help="Target FPS")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)
interval = 1.0/args.fps
 
print("OSC client is set to {0}:{1} at {2} fps".format(args.ip, args.port, args.fps))

# Create unique ID's (beginning at 0, 1, ...) for each new generic controller
serialNumberToUniqueID = {}

if interval:
	while(True):
		start = time.time()
		sleep_time = interval-(time.time()-start)
		poses = vr.getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount)
		for i in range(openvr.k_unMaxTrackedDeviceCount):
			if poses[i].bPoseIsValid:
				device_class = vr.getTrackedDeviceClass(i)

				# Only allow generic controllers to pass through
				if (device_class == 3):

					# Get the serial number
					serial = vr.getStringTrackedDeviceProperty(i, openvr.Prop_SerialNumber_String).decode('utf-8')
					# Create a unique ID for this device if it doesn't already exist
					if not serial in serialNumberToUniqueID:
						thisID = len(serialNumberToUniqueID)
						serialNumberToUniqueID[serial] = thisID

					# Get the full transformation matrix
					m = poses[i].mDeviceToAbsoluteTracking

					# Get the position from this matrix
					position = [m[0][3], m[1][3], m[2][3]]
					
					# Choose which values to send
					values = [serialNumberToUniqueID[serial], position[0], position[1], position[2] ]

					# Send this message with the header "vive"
					client.send_message("/vive", values)

		print("\r{0}".format(start), end="")
		if sleep_time>0:
			time.sleep(sleep_time)
