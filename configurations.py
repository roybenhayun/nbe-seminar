# 1. AirSim resolution is ~100ms (otherwise, will get same error as previous iteration and D-path will be 0)
# 2. Nengo min execution takes ~ 0.1secs
# 3. for reference, typical betaflight PID is 8Hz - 16Hz

AIRSIM_SIMULATION_MS_PERIOD = 0.1  #lower values makes drone fly less
NENGO_SIMULATION_MS_PERIOD = 0.1    #should allow Nengo sufficient compute time
