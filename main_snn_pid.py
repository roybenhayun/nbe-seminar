import setup_path
import airsim
from gains import PIDGains, VelocityControllerGains
from simulator_drone import *

import time
import numpy as np

from snn_pid import model, probes, p_ensemble, integrator, d_ensemble, radius, gains, n_neurons
from snn_pid_controller import SnnPidController, scale_factor
from visualization import plot_results, visualize_tuning_curves_basis_functions, visualize_stimulus_response

from decorators import timer


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
    drone = AirSimDrone(AirSimDrone.snn_u_to_velocity)
    drone.log("BEGIN: ", f"before lift off..")

    # adjust AirSim inner-loop PID
    pidGains = VelocityControllerGains(z_gains=PIDGains(10, 10, 10))
    drone._client.setVelocityControllerGains(pidGains)

    pid_controller = SnnPidController()  # IMPL-NOTE: Gains defines in snn_pid.py for NengoGUI
    height = drone.lift_off()
    drone.log("BEGIN: ", f"start height {height}")

    time.sleep(3)
    run_simulation(drone, pid_controller)

    drone.close()

    print(f"setpoints.size: {setpoints.size}, actuals.size: {actuals.size}")
    plot_results(setpoints, actuals,
                 suptitle="SNN-PID",
                 title=f"{gains} [AirSim\\Nengo period: {configurations.AIRSIM_SIMULATION_MS_PERIOD}, {configurations.NENGO_SIMULATION_MS_PERIOD}; scale: {scale_factor}; radius: {radius}; neurons: {n_neurons}]")

    #post_run_render(pid_controller)


def post_run_render(pid_controller):
    visualize_stimulus_response(pid_controller._sim, probes["stimulus"], probes["spikes_P"], probes["voltage_P"])
    visualize_stimulus_response(pid_controller._sim, probes["stimulus"], probes["spikes_I"], probes["voltage_I"])
    visualize_stimulus_response(pid_controller._sim, probes["stimulus"], probes["spikes_D"], probes["voltage_D"])


def pre_run_render():
    #visualize Tuning Curves, Basis Functions
    visualize_tuning_curves_basis_functions(model, p_ensemble, title="P-term ensemble")
    visualize_tuning_curves_basis_functions(model, integrator.ensemble, title="I-term ensemble")
    visualize_tuning_curves_basis_functions(model, d_ensemble, title="D-term ensemble")
    pass

if __name__ == '__main__':
    #pre_run_render()
    run_main()



