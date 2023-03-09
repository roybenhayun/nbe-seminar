class PIDGains():
    """
    Struct to store values of PID gains. Used to transmit controller gain values while instantiating
    AngleLevel/AngleRate/Velocity/PositionControllerGains objects.

    Attributes:
        kP (float): Proportional gain
        kI (float): Integrator gain
        kD (float): Derivative gain
    """
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def to_list(self):
        return [self.kp, self.ki, self.kd]

class VelocityControllerGains():
    """
    Struct to contain controller gains used by velocity PID controller

    Attributes:
        x_gains (PIDGains): kP, kI, kD for X axis
        y_gains (PIDGains): kP, kI, kD for Y axis
        z_gains (PIDGains): kP, kI, kD for Z axis
    """
    def __init__(self, x_gains = PIDGains(0.2, 0, 0),
                       y_gains = PIDGains(0.2, 0, 0),
                       z_gains = PIDGains(2.0, 2.0, 0)):
        self.x_gains = x_gains
        self.y_gains = y_gains
        self.z_gains = z_gains

    def to_lists(self):
        return [self.x_gains.kp, self.y_gains.kp, self.z_gains.kp], [self.x_gains.ki, self.y_gains.ki, self.z_gains.ki], [self.x_gains.kd, self.y_gains.kd, self.z_gains.kd]
