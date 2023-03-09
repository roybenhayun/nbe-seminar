import setup_path
import airsim

import numpy as np
from simulator_drone import *
from cpu_pid import *
import time

from visualization import plot_results
from gains import PIDGains, VelocityControllerGains

num_points = 200
setpoints = np.ones(num_points) * 30
actuals = np.zeros(num_points)
print(f"num_points.size: {num_points}")

@timer
def run_simulation(drone, pid_controller):
    last_error = 0
    for sample_idx, sp in enumerate(setpoints):
        drone.log("SP: ", f"{sp}")
        actuals[sample_idx] = drone.get_height()
        err = sp - actuals[sample_idx]
        drone.log("ACTUAL: ", f"{actuals[sample_idx]}")
        drone.log("ERROR: ", f"{err}")
        if abs(actuals[sample_idx] - sp) < 2:
            print(f"-------------------\nreach {sp} at {sample_idx}-------------------\n")
        u, p, i, d = pid_controller.get_pid(err, last_error)
        last_error = err
        print(f"[{sample_idx}] height: {actuals[sample_idx]}, err:{err}, P:{p}, I:{i}, D:{d}, PID: {u}")
        drone.rc_command(u)


@timer
def run_main():
    drone = AirSimDrone(AirSimDrone.cpu_u_to_velocity)
    drone.log("BEGIN: ", f"before lift off..")

    # adjust AirSim inner-loop PID
    pidGains = VelocityControllerGains(z_gains=PIDGains(10, 10, 10))
    drone._client.setVelocityControllerGains(pidGains)

    pid_controller = CpuPidController(kp=1.1, ki=0.9, kd=1.2)
    height = drone.lift_off()
    drone.log("BEGIN: ", f"start at {height}")

    time.sleep(3)
    run_simulation(drone, pid_controller)

    drone.close()

    print(f"setpoints.size: {setpoints.size}, actuals.size: {actuals.size}")
    plot_results(setpoints, actuals,
                 suptitle="CPU-PID",
                 title=f"[{pid_controller._kp}, {pid_controller._ki}, {pid_controller._kd}] [AirSim period: {configurations.AIRSIM_SIMULATION_MS_PERIOD}]")

if __name__ == '__main__':
    run_main()