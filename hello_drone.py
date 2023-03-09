import time

import setup_path
print("installed setup_path")
import airsim
from airsim.utils import to_eularian_angles
print("installed airsim")

import numpy as np
import os
import tempfile
import pprint
import cv2


def print_airim_info(client):
    print("-------------------------------------------------")

    drone_state =
    print("state: %s" % pprint.pformat(drone_state))
    state = {}
    state["position"] = drone_state.kinematics_estimated.position
    state["velocity"] = drone_state.kinematics_estimated.linear_velocity
    state['orientation'] = to_eularian_angles(drone_state.kinematics_estimated.orientation)

    print("-------------------------------------------------")

    print("imu_data: %s" % pprint.pformat(client.getImuData()))

    print("-------------------------------------------------")

    print("barometer_data: %s" % pprint.pformat(client.getBarometerData()))

    print("-------------------------------------------------")

    print("magnetometer_data: %s" % pprint.pformat(client.getMagnetometerData()))

    print("-------------------------------------------------")

    print("gps_data: %s" % pprint.pformat(client.getGpsData()))

    print("-------------------------------------------------")

    print("home_pt: %s" % pprint.pformat(client.getHomeGeoPoint()))

    print("-------------------------------------------------")

    print("listVehicles: %s" % pprint.pformat(client.listVehicles()))

    print("-------------------------------------------------")

    print("kinematics: %s" % pprint.pformat(client.simGetGroundTruthKinematics()))

    print("-------------------------------------------------")

    print("pose: %s" % pprint.pformat(client.simGetVehiclePose()))

    print("-------------------------------------------------")

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print_airim_info(client)

client.simPrintLogMessage("State: ", "taking off..")
client.armDisarm(True)
client.takeoffAsync().join()

start_position = {
    "x": -10,
    "y": 10,
    "z": -10
}

client.simPrintLogMessage("State: ", "to position")
client.moveToPositionAsync(start_position["x"], start_position["y"], start_position["z"], 5).join()
client.simPrintLogMessage("State: ", "at position")


max_iteration = 5
angle = 1
max_turns = 1
sleep_secs = 2
duration = 1.5
throttle = 1.0

client.simPrintLogMessage("State: ", "test 1")
iteration = 0
client.moveByRollPitchYawThrottleAsync(angle, 0, 0, throttle, 100)
while iteration < 100:
    print("eularian angles: %s" % pprint.pformat(to_eularian_angles(client.getMultirotorState().kinematics_estimated.orientation)))
    time.sleep(1)

client.simPrintLogMessage("State: ", "test 2")
iteration = 0
while iteration < max_iteration:
    iteration += 1
    client.simPrintLogMessage("Iteration: ", f"{iteration}")

    client.moveToPositionAsync(start_position["x"], start_position["y"], start_position["z"], 5).join()
    time.sleep(sleep_secs)
    left_turns = 0
    while left_turns < max_turns:
        client.simPrintLogMessage("Left: ", f"{left_turns}")
        #moveByRollPitchYawZAsync() #radians, in the body frame
        client.moveByRollPitchYawThrottleAsync(angle, 0, 0, throttle, duration) #in body frame: radians in SimpleFlight, degrees in PX4
        client.simPrintLogMessage("sleep: ON")
        time.sleep(sleep_secs)
        client.simPrintLogMessage("sleep: OFF")
        left_turns += 1

    client.moveToPositionAsync(start_position["x"], start_position["y"], start_position["z"], 5).join()
    time.sleep(sleep_secs)
    right_turns = 0
    while right_turns < max_turns:
        client.simPrintLogMessage("Right: ", f"{right_turns}")
        client.moveByRollPitchYawThrottleAsync(-angle, 0, 0, throttle, duration)
        client.simPrintLogMessage("sleep: ON")
        time.sleep(sleep_secs)
        client.simPrintLogMessage("sleep: OFF")
        right_turns += 1


client.reset()
client.armDisarm(False)

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
