from time import time
import numpy as np

import nengo

from snn_pid import model, probes, pid_output_val

from decorators import timer

from configurations import NENGO_SIMULATION_MS_PERIOD

from snn_pid import stimulus_value


def set_inputs(err, last_error):
    stimulus_value['n_err'] = err
    stimulus_value['n_last_error'] = last_error
    print(f"err: {stimulus_value['n_err']}, {stimulus_value['n_last_error']}")


scale_factor = 35


class SnnPidController:

    def __init__(self) -> None:
        self._snn = model
        self._sim = nengo.Simulator(model, dt=0.01, seed=10)  # dt 1ms is enough, constant seed to ease the evaluation
        self._integral = 0
        self._t1 = None

    @timer
    def __execute_nengo(self):
        """
        Utility function with sole purpose to allow profiling the execution time of Nengo in isolation
        """
        self._sim.run(NENGO_SIMULATION_MS_PERIOD) #run Nengo same duration as AirSim

    @staticmethod
    def __clamp(value, lower, upper):
        if value is None:
            return None
        elif (upper is not None) and (value > upper):
            return upper
        elif (lower is not None) and (value < lower):
            return lower
        return value

    @timer
    def get_pid(self, err, last_error):
        set_inputs(err/scale_factor, last_error/scale_factor)
        self.__execute_nengo()
        # u = np.average(self._sim.data[probes["pid_output"]][-5:]) * scale_factor
        # p = np.average(self._sim.data[probes["p_term"]][-5:]) * scale_factor
        # i = np.average(self._sim.data[probes["i_term"]][-5:]) * scale_factor
        # d = np.average(self._sim.data[probes["d_term"]][-5:]) * scale_factor
        # return u, p, i, d
        u = pid_output_val["last"][0] * scale_factor
        u = SnnPidController.__clamp(u, -40, 40)  # avoid PID windup
        return u, -1, -1, -1

    def close(self):
        self._sim.close()
