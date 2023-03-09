import airsim
from airsim.types import Vector3r

import configurations
from decorators import timer

start_position = {
    "x": -10,
    "y": 10,
    "z": -10
}

class SimDrone:
    def __init__(self, **kwargs) -> None:
        self._foo = None


class AirSimDrone(SimDrone):
    def __init__(self, conversion_function, **kwargs) -> None:
        super().__init__(**kwargs)
        self._conversion_function = conversion_function
        self._client = airsim.MultirotorClient()
        self._client.confirmConnection()
        pose = self._client.simGetVehiclePose()
        #print(f"pose 1: {pose}")
        self._client.enableApiControl(True)
        self._client.simPause(False)
        self._client.simSetVehiclePose(Vector3r(0,0,3), ignore_collision=True)
        #print(f"pose 2: {pose}")
        self._data = None

    def lift_off(self) -> int:
        self._client.armDisarm(True)
        self._client.takeoffAsync().join()
        self._client.moveToPositionAsync(start_position["x"], start_position["y"], start_position["z"], 5).join()
        return self.get_height()

    def get_height(self):
        return abs(self._client.simGetVehiclePose().position.z_val - start_position["z"])

    def log(self, key, val):
        self._client.simPrintLogMessage(key, val)

    @staticmethod
    def cpu_u_to_velocity(u) -> int:
        return u * -1 #-1 for AirSim direction on Z axis

    @staticmethod
    def snn_u_to_velocity(u) -> int:
        return u * -1 #-1 for AirSim direction on Z axis

    @timer
    def rc_command(self, u):
        """
        interprets a remote-control from the parameter U

        :param float u: PID output
        """
        self.log("PID: ", f"{u}")
        velocity = self._conversion_function(u)
        print(f"u: {u} , velocity: {velocity}")
        self.log("VELOCITY: ", f"{velocity}")
        self._client.simPause(False)
        self._client.moveByVelocityAsync(0, 0, velocity, configurations.AIRSIM_SIMULATION_MS_PERIOD).join()
        self._client.simPause(True)
        self.log("DIRECTION: ", "up" if u > 0 else "down")

    def close(self):
        self._client.enableApiControl(False)
        self._client.reset()


