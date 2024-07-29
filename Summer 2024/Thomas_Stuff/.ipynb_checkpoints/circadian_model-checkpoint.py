# -- LIGHT INTENSITY FUNCTIONS --

# 12hrs light, 12hrs dark
def LD(t, intensity: float, off_time=12, daylength=24):
    time = t % daylength
    is_light = time < off_time
    
    return is_light * intensity

# LD function with a pulse of light or dark at the specified time and day, for the specified length (in hours)
def LD_pulse(t, intensity: float, pulse_day: int, pulse_time: int, pulse_length=2, off_time=12, daylength=24):
    time = t % daylength
    day = t // daylength
    base = LD(t, intensity, off_time, daylength)

    is_during_pulse = (day == pulse_day) & (pulse_time < time) & (time < pulse_time + pulse_length)

    # if not in pulse, return the base signal; if in pulse return the inverted one
    # done a little weirdly so that the function works when vectorized
    return is_during_pulse * (intensity - base) + (1 - is_during_pulse) * base
        
# -- DIFFERENTIAL EQUATION SOLVING --

# derivative functions on x and y; include effect of light
# t: time (hrs)
# l (lambda): rate of return from a disturbance (hrs^-1)
# A: amplitude of base oscillation
# tau: period of base oscillation (hrs)
# ifunc: light intensity as a function of t
def cartesian_lights(t, p, l, A, tau, ifunc):
    x, y = p
    r = np.sqrt(x**2 + y**2)
    
    # see equations 4 and 5 in the paper (section 4.1)
    dx = l * x * (A - r) - 2 * np.pi * y / tau - ifunc(t)
    dy = l * y * (A - r) + 2 * np.pi * x / tau
    
    return [dx, dy]

# get the solution of a simulated oscillator affected by the given light intensity function
# returns t, (x, y)
def get_simulation_result(l, tau, ifunc, hours, timestep=1/60, A=1):
    tspan = [0, hours]
    t = np.arange(*tspan, timestep)

    p0 = [A, 0]
    result = solve_ivp(cartesian_lights, tspan, p0, args=(l, A, tau, ifunc), t_eval=t)

    return t, result.y

# use a lomb-scargle periodogram to get the final period of a simulation; used to compare to the ZT period
def get_simulation_period(l, tau: float, max_intensity: float, hours=144):
    intensity = lambda x: LD_step(x) * max_intensity
    
    t, (x, y) = get_simulation_result(l, tau, intensity, hours)
    
    periods = np.arange(1, 10, .1)
    
    powers = lombscargle(t[len(x)//2:], x[len(x)//2:], freqs=1/periods)
    
    peak_freq = periods[powers.argmax()] * 6.25

    return peak_freq


def generate_arnold_tongue(size_x: int, size_y: int, tau_range: [float, float], light_range: [float, float], l=.1):
    def ranges(i, j, tau_range, light_range):
        tau = np.interp(i, [0, size_x], tau_range)
        light = np.interp(j, [0, size_y], light_range)
        
        return np.array([tau, light])
    
    im_shape = (size_x, size_y)
    
    param_array = np.fromfunction(lambda i, j: ranges(i, j, tau_range, light_range), (size_x + 1, size_y + 1))
    
    def generator(x):
        sys.stdout.write("\r%f, %f" % (x[0], x[1]))
        sys.stdout.flush()
        return get_simulation_period(l, x[0], x[1]) - 24
    
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

def generate_pulse_sim_df(pulse_starts: float[], periods: float[], sim_hours: int, pulse_day: int, intensity=.15, l=.1):
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
    df = pd.DataFrame(rows)
    return df