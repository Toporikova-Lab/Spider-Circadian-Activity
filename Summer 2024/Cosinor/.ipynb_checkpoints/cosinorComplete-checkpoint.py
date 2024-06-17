import numpy as np
import pandas as pd
import data_reading
import raster 

def cosinor_model(t, period, amplitude, phase, offset):
    """Cosinor model function"""
    return offset + amplitude * np.cos(2 * np.pi * (t / period) + phase)

def residuals(params, t, y):
    """Residuals between data and model"""
    period, amplitude, phase, offset = params
    return y - cosinor_model(t, period, amplitude, phase, offset)

def jacobian(params, t, y):
    """Jacobian matrix of partial derivatives"""
    period, amplitude, phase, offset = params
    n = len(t)
    jac = np.zeros((n, 4))
    jac[:, 0] = -2 * np.pi * amplitude * np.sin(2 * np.pi * (t / period) + phase) * (t / period**2)
    jac[:, 1] = np.cos(2 * np.pi * (t / period) + phase)
    jac[:, 2] = -amplitude * np.sin(2 * np.pi * (t / period) + phase)
    jac[:, 3] = 1
    return jac

def marquardt(t, y, p0, maxiter=100, tol=1e-6):
    """Marquardt algorithm for cosinor model fitting"""
    params = p0
    lambdas = 0.01
    for i in range(maxiter):
        r = residuals(params, t, y)
        J = jacobian(params, t, y)
        JtJ = J.T @ J
        JtR = J.T @ r
        lam_diag = lambdas * np.diag(np.diag(JtJ))
        dp = np.linalg.solve(JtJ + lam_diag, -JtR)
        new_params = params + dp
        r_new = residuals(new_params, t, y)
        if np.sum(r_new**2) < np.sum(r**2):
            params = new_params
            lambdas /= 10
        else:
            lambdas *= 10
        if np.linalg.norm(dp) < tol:
            break
    return params


def main():
    
    t = data['time'].values
    y = data['activity'].values
    p0 = [12, 5, 0, 10]  # Initial guesses for period, amplitude, phase, offset

    estimated_params = marquardt(t, y, p0)
    print(f"Estimated Period: {estimated_params[0]:.2f}")

if __name__ == "__main__":
    main()