from nengo.utils.ensemble import tuning_curves
import matplotlib.pyplot as plt
import numpy as np
import nengo
from nengo.utils.matplotlib import rasterplot
import numpy as np
import matplotlib.pyplot as plt
from nengo.utils.ensemble import tuning_curves



def plot_results(setpoints, actuals, title, suptitle):
    plt.figure(figsize=(10, 4))
    plt.ylabel('Height')
    plt.xlabel("Samples")
    #plt.ylim((0, 50))

    plt.plot(setpoints, label='setpoint', color='r', linewidth=4)
    plt.plot(actuals, label='actual', color='g', linewidth=4)

    plt.legend()
    plt.title(title)
    plt.suptitle(suptitle)
    plt.savefig('output.png')
    plt.show()


def visualize_tuning_curves_basis_functions(model, x_ensemble, title=""):

    sim = nengo.Simulator(model, seed=4)
    #T = 1.0
    #sim.run(T)

    plt.plot(*tuning_curves(x_ensemble, sim))
    plt.xlabel('I')
    plt.ylabel('$a$ (Hz)');
    plt.title(f"Tuning Curves: {title}")
    plt.show()

    x, A = tuning_curves(x_ensemble, sim)

    Gamma = np.dot(A.T, A)
    U, S, V = np.linalg.svd(Gamma)
    chi = np.dot(A, U)

    for i in range(x_ensemble.n_neurons):
        plt.plot(x, chi[:, i], label='$\chi_%d$=%1.3g' % (i, S[i]), linewidth=3)
    plt.legend(loc='best')
    plt.title(f"Basis Functions: {title}")
    plt.show()

    plt.xlabel('neurons')
    plt.title(f"Variation Drop: {title}")
    plt.loglog(S, linewidth=4)
    plt.show()



def visualize_spikes_and_voltage(ens, sim, stim_p, spikes_p):
    plt.plot(*tuning_curves(ens, sim))
    # nengo.utils.matplotlib.plot_tuning_curves(ens, sim) #FIXME: module 'nengo.utils.matplotlib' has no attribute 'plot_tuning_curves'
    plt.xlabel('I')
    plt.ylabel('$a$ (Hz)');
    plt.suptitle("Two LIF neurons with the same intercept (0.5) and op-posing encoders")
    plt.title("tuning_curves")
    plt.show()

    t = sim.trange()
    plt.figure(figsize=(12, 6))
    plt.plot(t, sim.data[stim_p], 'r', linewidth=4)
    plt.ax = plt.gca()
    plt.ylabel("Output")
    plt.xlabel("Time");
    rasterplot(t, sim.data[spikes_p], ax=plt.ax.twinx(), use_eventplot=True)
    plt.ylabel("Neuron");

    plt.title("Two LIF neurons with the same intercept (0.5) and op-posing encoders")
    plt.show()


def visualize_stimulus_response(sim, stim_p, voltage_p, spikes_p):
    t = sim.trange()
    plt.figure(figsize=(10, 4))
    plt.plot(t, sim.data[stim_p], label='stimulus', color='r', linewidth=4)  # renders stimulus to ensemble
    plt.ax = plt.gca()
    plt.ax.plot(t, sim.data[voltage_p], 'g', label='v', color='g')  # renders neuron voltage
    #plt.ylim((-1, 2))
    plt.ylabel('Voltage')
    plt.xlabel("Time")

    rasterplot(t, sim.data[spikes_p], ax=plt.ax.twinx(), use_eventplot=True, color='b')  # renders which neurons fired
    #plt.ylim((-1, 2))

    plt.legend()
    plt.title("Response to Stimulus")
    plt.show()