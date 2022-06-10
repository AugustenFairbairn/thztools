import numpy as np


def epswater(f, t=25):
    """
    EPSWATER Complex relative permittivity of water
    Interpolation function taken from W. J. Ellison, doi:10.1063/1.2360986

    EPSWATER(F) computes the complex relative permittivity at frequency F
    (THz) and temperature T = 25 deg C

    EPSWATER(F,T) computes the complex relative permittivity at frequency F
    (THz) and temperature T (deg C)

    Parameters
    ----------
    f Frequency (THz)
    t Temperature (deg C) (optional)

    Returns
    -------
    epsilonr Complex relative permittivity of water

    """
    # Define relaxation parameters
    a = [79.23882, 3.815866, 1.634967]
    b = [0.004300598, 0.01117295, 0.006841548]
    c = [1.382264e-13, 3.510354e-16, 6.30035e-15]
    d = [652.7648, 1249.533, 405.5169]
    Tc = 133.1383

    # Define resonance parameters
    p0 = 0.8379692
    p = [-0.006118594, -0.000012936798, 4235901000000, -14260880000,
         273815700, -1246943, 9.618642e-14, 1.795786e-16, -9.310017e-18,
         1.655473e-19, 0.6165532, 0.007238532, -0.00009523366, 15983170000000,
         -74413570000, 497448000, 2.882476e-14, -3.142118e-16, 3.528051e-18]

    # Compute temperature - dependent functions
    eps0 = 87.9144 - 0.404399 * t + 9.58726e-4 * t ** 2 - 1.32802e-6 * t ** 3
    delta = a * np.exp(-b * t)
    tau = c * np.exp(d / (t + Tc))

    delta4 = p0 + p[0] * t + p[1] * t ** 2
    f0 = p[2] + p[3] * t + p[4] * t ** 2 + p[5] * t ** 3
    tau4 = p[6] + p[7] * t + p[8] * t ** 2 + p[9] * t ** 3
    delta5 = p[10] + p[11] * t + p[12] * t ** 2
    f1 = p[13] + p[14] * t + p[15] * t ** 2
    tau5 = p[16] + p[17] * t + p[18] * t ** 2

    # Put it all together
    epsilonr = (eps0 + 2 * 1j * np.pi * f * (delta[0] * tau[0] / (1 - 2 * 1j * np.pi * f * tau[0])
            + delta[1] * tau[1] / (1 - 2 * 1j * np.pi * f * tau[1])
            + delta[2] * tau[2] / (1 - 2 * 1j * np.pi * f * tau[2]))
            + 1j * np.pi * f * (delta4 * tau4 / (1 - 2 * 1j * np.pi * tau4 * (f0 + f))
            + delta4 * tau4 / (1 + 2 * 1j * np.pi * tau4 * (f0 - f)))
            + 1j * np.pi * f * (delta5 * tau5 / (1 - 2 * 1j * np.pi * tau5 * (f1 + f))
            + delta5 * tau5 / (1 + 2 * 1j * np.pi * tau5 * (f1 - f))))

    return epsilonr
