import nengo

from configurations import AIRSIM_SIMULATION_MS_PERIOD

n_neurons = 250
tau_i = 0.1


model = nengo.Network(label="SNN-PID", seed=10)

#
# Pseudo API
#

pid_output_val = {
    "last": -1
}
def node_output_func(t, x):
    print(f"{t}: {x}")
    pid_output_val["last"] = x
    return x

p_ensemble = None
integrator = None
d_ensemble = None

gains = [14.0, 5.0, 1.0]
Kp = gains[0]
Ki = gains[1]
Kd = gains[2]

radius = 1

probes = {
}

stimulus_value = {
    "n_err": 30,
    "n_last_error": 30
}

def get_stimulus(t):
    return [stimulus_value["n_err"], stimulus_value["n_last_error"]]

#
# Nengo model
#

with model:
    # stim, in, out
    stim = nengo.Node(get_stimulus) #[error, last_error]
    error_input = nengo.Node(size_in=2, label="PID input")
    pid_output = nengo.Node(output=node_output_func, size_in=1, size_out=1, label="PID output")
    nengo.Connection(stim, error_input)


    # P path
    p_ensemble = nengo.Ensemble(n_neurons=n_neurons, dimensions=1, radius=radius, label="P-path")
    nengo.Connection(error_input[0], p_ensemble, synapse=0.005)
    nengo.Connection(p_ensemble, pid_output, transform=Kp, label="Kp")

    # I path
    integrator = nengo.networks.Integrator(tau_i, n_neurons=n_neurons, dimensions=1, label="I-path")
    integrator.ensemble.radius = radius * 2
    nengo.Connection(error_input[0], integrator.input)
    nengo.Connection(integrator.output, pid_output, transform=Ki, label="Ki", synapse=0.1)

    # D path
    d_ensemble = nengo.Ensemble(n_neurons=n_neurons, dimensions=1, radius=radius, label="D-path")
    nengo.Connection(error_input[0], d_ensemble, transform=1 / AIRSIM_SIMULATION_MS_PERIOD, synapse=0.5)
    nengo.Connection(error_input[1], d_ensemble, transform=-1 / AIRSIM_SIMULATION_MS_PERIOD, synapse=0.5)
    nengo.Connection(d_ensemble, pid_output, transform=Kd, label="Kd")

    probes["stimulus"] = nengo.Probe(stim)
    probes["pid_output"] = nengo.Probe(pid_output)
    probes["p_term"] = nengo.Probe(p_ensemble)
    probes["i_term"] = nengo.Probe(integrator.ensemble)
    probes["d_term"] = nengo.Probe(d_ensemble)

    probes["spikes_P"] = nengo.Probe(p_ensemble.neurons, 'output')
    probes["voltage_P"] = nengo.Probe(p_ensemble.neurons, 'voltage')
    probes["spikes_I"] = nengo.Probe(integrator.ensemble.neurons, 'output')
    probes["voltage_I"] = nengo.Probe(integrator.ensemble.neurons, 'voltage')
    probes["spikes_D"] = nengo.Probe(d_ensemble.neurons, 'output')
    probes["voltage_D"] = nengo.Probe(d_ensemble.neurons, 'voltage')

