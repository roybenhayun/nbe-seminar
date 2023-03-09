import configurations
from decorators import timer


class CpuPidController:
    def __init__(self, kp, ki, kd) -> None:
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._integral = 0

    @staticmethod
    def __clamp(value, lower, upper):
        if value is None:
            return None
        elif (upper is not None) and (value > upper):
            return upper
        elif (lower is not None) and (value < lower):
            return lower
        return value

    #@timer
    def get_pid(self, error, last_error):
        dt = configurations.AIRSIM_SIMULATION_MS_PERIOD  # use AirSim time

        #P,D
        p = self._kp * error
        d = self._kd * (error - last_error) / dt
        #print(f"{self._kd} * ({error} - {self._lastError}) / {dt} = {d}")

        #I-path
        self._integral += self._ki * error * dt
        self._integral = CpuPidController.__clamp(self._integral, -30, 30)  # avoid integral windup
        i = self._integral

        u = CpuPidController.__clamp(p + i + d, -40, 40)  # avoid PID windup
        return u, p, i, d

