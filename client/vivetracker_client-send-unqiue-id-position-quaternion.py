import openvr
import time
import sys
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client
import math

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

def convert_to_quaternion(pose_mat):
    # Per issue #2, adding a abs() so that sqrt only results in real numbers
    r_w = math.sqrt(abs(1+pose_mat[0][0]+pose_mat[1][1]+pose_mat[2][2]))/2
    r_x = (pose_mat[2][1]-pose_mat[1][2])/(4*r_w)
    r_y = (pose_mat[0][2]-pose_mat[2][0])/(4*r_w)
    r_z = (pose_mat[1][0]-pose_mat[0][1])/(4*r_w)

    x = pose_mat[0][3]
    y = pose_mat[1][3]
    z = pose_mat[2][3]
    return [x,y,z,r_w,r_x,r_y,r_z]

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

					# Get the position and quaternion from this matrix
					pq = convert_to_quaternion(m)
					# Extract position
					p = pq[:3]
					q = pq[3:]
					
					# Choose which values to send
					values = [p[0], p[1], p[2], q[1], q[2], q[3], q[0]]

					# Send this message with the header "vive"
					client.send_message("/"+str(serialNumberToUniqueID[serial]), values)

		print("\r{0}".format(start), end="")
		if sleep_time>0:
			time.sleep(sleep_time)
