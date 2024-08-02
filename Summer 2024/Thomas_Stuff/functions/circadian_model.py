import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.signal import lombscargle

# -- LIGHT INTENSITY FUNCTIONS --

def LD(t, intensity, off_time=12, daylength=24):
    """
    Light intensity as a function of t. Default: 12hrs light, 12hrs dark.

    Parameters:
    t: float
        Input time (hrs)
    intensity: float
        Return value when light is on; 0 is returned when light is off
    off_time: float
        Time at which the lights turn off (hrs); must be less than daylength
    daylength: float
        Length of each ZT day (hrs)

    Returns:
    intensity: float
        Light intensity at time t
    """
    time = t % daylength
    is_light = time < off_time
    
    return is_light * intensity


def LD_pulse(t, intensity, pulse_day, pulse_time, pulse_length=2, off_time=12, daylength=24):
    """
    Light intensity as a function of t, with a pulse at the specified time. Default: 12hrs light, 12hrs dark;
    

    Parameters:
    t: float
        Input time (hrs)
    intensity: float
        Return value when light is on; 0 is returned when light is off
    off_time: float
        Time at which the lights turn off (hrs); must be less than daylength
    daylength: float
        Length of each ZT day (hrs)
    pulse_day: int
        Day of the simulation on which to add the pulse
    pulse_time: float
        ZT time of the start of the pulse (hrs)
    pulse_length: float 
        Length of the pulse (hrs)

    Returns:
    intensity: float
        Light intensity at time t
    """
    time = t % daylength
    day = t // daylength
    base = LD(t, intensity, off_time, daylength)

    is_during_pulse = (day == pulse_day) & (pulse_time < time) & (time < pulse_time + pulse_length)

    # if not in pulse, return the base signal; if in pulse return the inverted one
    # done a little weirdly so that the function works when vectorized
    return is_during_pulse * (intensity - base) + (1 - is_during_pulse) * base
        
# -- DIFFERENTIAL EQUATION SOLVING --

def xy_lights(t, p, l, A, tau, light_func):
    """
    Derivative functions on x and y for a simple Poincare oscillator; include effect of light

    Parameters:
    t: array[float]
        Time points (hrs)
    p: [float, float]
        Current values of x and y
    l: float
        Rate of return from a disturbance (hrs^-1)
    A: float
        Amplitude of base oscillation
    tau: float
        Period of base oscillation i.e. free-running period (hrs)
    light_func: (t: float) -> float
        Light intensity as a function of t

    Returns:
    [dx_dt: float, dy_dt: float]
        dx_dt -- derivative of x with respect to t
        dy_dt -- derivative of y with respect to t
    """
    x, y = p
    r = np.sqrt(x**2 + y**2)
    
    dx = l * x * (A - r) - 2 * np.pi * y / tau - light_func(t)
    dy = l * y * (A - r) + 2 * np.pi * x / tau
    
    return [dx, dy]

def get_2var_simulation_result(l, tau, hours, light_func, timestep=1/60, A=1):
    """
    Get the solution of a simple 2-variable oscillator. 

    Parameters:
    p0: [float, float]
        Initial conditions x and y
    hours: int
        Number of hours to run the simulation for
    derivatives: (t: float, p: [float, float], ...args) -> [float, float]
        Function taking in t, initial conditions, and args returning the derivatives of x, y, ...
    timestep: float
        Timestep of ODE solver (hrs)
    A: float
        Amplitude of base oscillation

    Returns:
    (t, (x, y))
        t: [float...] -- times for solutions
        x, y, ...: [float...] -- solution values
    """
    tspan = [0, hours]
    t = np.arange(*tspan, timestep)

    result = solve_ivp(xy_lights, tspan, p0, args=(l, A, tau, light_func), t_eval=t)

    return t, result.y

def get_2var_simulation_period(l, tau, intensity, hours=144):
    """
    Uses a lomb-scargle periodogram to get the period of the second half of a simulation

    Parameters:
    l: float
        Rate of return from a disturbance (hrs^-1)
    tau: float
        Period of base oscillation i.e. free-running period (hrs)
    intensity: float
        Value when light is on
    hours: int
        Number of hours to run the simulation for

    Returns:
    peak_freq: float
        Period with the highest power peak
    """
    light_func = lambda t: LD(t, intensity)
    
    t, (x, y) = get_simulation_result(l, tau, intensity, hours)
    
    periods = np.arange(1, 10, .1)
    powers = lombscargle(t[len(x)//2:], x[len(x)//2:], freqs=1/periods)
    peak_freq = periods[powers.argmax()] * 6.25

    return peak_freq


def generate_arnold_tongue(size_x, size_y, tau_range, light_range, l=.1):
    """
    Generates an arnold tongue entrainment graph with free running period on the x-axis, light intensity on 
    the y-axis. Shows the region of entrainment by the difference from the ZT period (24hrs)

    Parameters:
    size_x: int
        Number of points for tau
    size_y: int
        Number of points for light intensity
    l: float
        Rate of return from a disturbance (hrs^-1)
    """
    def ranges(i, j, tau_range, light_range):
        tau = np.interp(i, [0, size_x], tau_range)
        light = np.interp(j, [0, size_y], light_range)
        
        return np.array([tau, light])

    # first generate an array of parameters (tau, light)
    im_shape = (size_x, size_y)
    
    param_array = np.fromfunction(lambda i, j: ranges(i, j, tau_range, light_range), (size_x + 1, size_y + 1))
    
    def generator(x):
        sys.stdout.write("\r%f, %f" % (x[0], x[1]))
        sys.stdout.flush()
        return get_simulation_period(l, x[0], x[1]) - 24

    # then apply the simulation period to each element of the parameter array
    new = np.apply_along_axis(generator, 0, param_array)

    fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
    
    ax.set_xticks([0, size_x / 2, size_x], labels=np.round(np.interp([0, size_x / 2, size_x], [0, size_x], tau_range), decimals=3), rotation='vertical')
    ax.set_yticks([0, size_y / 2, size_y], labels=np.round(np.interp([0, size_y / 2, size_y], [0, size_y], light_range), decimals=3))
    
    ax.set_xlabel('Free-running period (hours)')
    ax.set_ylabel('Light intensity')
    
    data = ax.imshow(new.T, cmap='RdBu', origin='lower', vmin=-5, vmax=5)
    
    fig.colorbar(data, ax=ax)
    fig.suptitle('Entrainment region (circadian clock period - ZT period)')

    return ax