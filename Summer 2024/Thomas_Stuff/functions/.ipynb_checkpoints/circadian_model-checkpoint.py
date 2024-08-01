import numpy as _np

# -- LIGHT INTENSITY FUNCTIONS --

# 12hrs light, 12hrs dark
def LD(t, intensity, off_time=12, daylength=24):
    """
    Light intensity as a function of t. Default: 12hrs light, 12hrs dark.

    Parameters:
    t: float -- input time
    intensity: float -- returns when light is on
    off_time: float -- time at which the lights turn off in hours; must be less than daylength
    daylength: float -- length of the day in hours

    Returns:
    float
    """
    time = t % daylength
    is_light = time < off_time
    
    return is_light * intensity



# LD function with a pulse of light or dark at the specified time and day, for the specified length (in hours)
def LD_pulse(t, intensity, pulse_day, pulse_time, pulse_length=2, off_time=12, daylength=24):
    """
    Light intensity as a function of t, with a pulse at the specified time. Default: 12hrs light, 12hrs dark;
    

    Parameters:
    t: float -- input time
    intensity: float -- returns when light is on
    pulse_day: int -- day of the simulation on which to add the pulse
    pulse_time: float -- ZT time of the start of the pulse in hours
    pulse_length: float -- length of the pulse in hours
    off_time: float -- time at which the lights turn off in hours; must be less than daylength
    daylength: float -- length of the day in hours

    Returns:
    float
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
    Derivative functions on x and y; include effect of light

    Parameters:
    t: float -- time (hrs)
    p: [float, float] -- current x and y
    l: float -- rate of return from a disturbance (hrs^-1)
    A: float -- amplitude of base oscillation
    tau: float -- period of base oscillation (hrs)
    light_func: (float) -> float -- light intensity as a function of t

    Returns:
    list [float, float]
    """
    x, y = p
    r = _np.sqrt(x**2 + y**2)
    
    dx = l * x * (A - r) - 2 * _np.pi * y / tau - light_func(t)
    dy = l * y * (A - r) + 2 * _np.pi * x / tau
    
    return [dx, dy]

def get_simulation_result(l, tau, hours, light_func, timestep=1/60, A=1):
    """
    Get the solution of a simple 2-variable oscillator. 

    Parameters:
    p0: [float...] -- initial conditions
    hours: int -- number of hours to run the simulation for
    derivatives: (float, [float...], ...args) -> [float...] -- function taking in t, initial conditions, and args returning the derivatives of x, y, ...
    timestep: float -- timestep of ODE solver
    A: float -- amplitude of base oscillation

    Returns:
    tuple (t, (x, y, ...))
    t: [float...] -- times for solutions
    x, y, ...: [float...] -- solution values
    """
    tspan = [0, hours]
    t = _np.arange(*tspan, timestep)

    result = solve_ivp(xy_lights, tspan, p0, args=(l, A, tau, light_func), t_eval=t)

    return t, result.y

# use a lomb-scargle periodogram to get the final period of a simulation; used to compare to the ZT period
def get_simulation_period(l, tau, intensity, hours=144):
    light_func = lambda t: LD(t, intensity)
    
    t, (x, y) = get_simulation_result(l, tau, intensity, hours)
    
    periods = _np.arange(1, 10, .1)
    powers = lombscargle(t[len(x)//2:], x[len(x)//2:], freqs=1/periods)
    peak_freq = periods[powers.argmax()] * 6.25

    return peak_freq


def generate_arnold_tongue(size_x, size_y, tau_range, light_range, l=.1):
    def ranges(i, j, tau_range, light_range):
        tau = _np.interp(i, [0, size_x], tau_range)
        light = _np.interp(j, [0, size_y], light_range)
        
        return _np.array([tau, light])
    
    im_shape = (size_x, size_y)
    
    param_array = _np.fromfunction(lambda i, j: ranges(i, j, tau_range, light_range), (size_x + 1, size_y + 1))
    
    def generator(x):
        sys.stdout.write("\r%f, %f" % (x[0], x[1]))
        sys.stdout.flush()
        return get_simulation_period(l, x[0], x[1]) - 24
    
    new = _np.apply_along_axis(generator, 0, param_array)
    
    fig, ax = plt.subplots(constrained_layout=True, figsize=(6, 4))
    
    ax.set_xticks([0, size_x / 2, size_x], labels=_np.round(_np.interp([0, size_x / 2, size_x], [0, size_x], tau_range), decimals=3), rotation='vertical')
    ax.set_yticks([0, size_y / 2, size_y], labels=_np.round(_np.interp([0, size_y / 2, size_y], [0, size_y], light_range), decimals=3))
    
    ax.set_xlabel('Free-running period (hours)')
    ax.set_ylabel('Light intensity')
    
    data = ax.imshow(new.T, cmap='RdBu', origin='lower', vmin=-5, vmax=5)
    
    fig.colorbar(data, ax=ax)
    fig.suptitle('Entrainment region (circadian clock period - ZT period)')

    return ax

def generate_pulse_sim_df(pulse_starts, periods, sim_hours, pulse_day: int, intensity=.15, l=.1):
    # first generate a list of dictionaries
    
    rows = []
    for pulse_time in pulse_starts:
        for period in periods:
            t, (ctrl_result, _) = get_simulation_result(l, period, sim_hours, intensity)
            _, (pulse_result, _) = get_pulse_simulation_result(l, period, sim_hours, intensity, pulse_day, pulse_time)
    
            pulse_time_absolute = (24 * pulse_day) + pulse_time
    
            measurement_interval = 2
            
            is_pulse = (pulse_time_absolute <= t) & (t < pulse_time_absolute + 1)
            ctrl_avg = ctrl_result[is_pulse].mean()
            pulse_avg = pulse_result[is_pulse].mean()
    
            rows.append({
                'zt': pulse_time,
                'tau': period,
                'ctrl_avg': ctrl_avg,
                'pulse_avg': pulse_avg
            })
    
    # compile the list of dictionaries into a dataframe
    df = _pd.DataFrame(rows)
    return df