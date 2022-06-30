import numpy as np
import scipy.linalg


def costfunlsq(fun, theta, xx, yy, sigmax, sigmay, wfft):
    """

    Parameters
    ----------
    fun
    theta
    xx
    yy
    sigmax
    sigmay
    wfft

    Returns
    -------

    """
    N = len(sigmax)
    H = np.conj(fun(theta, wfft))
    if N % 2 == 0:
        kNy = N // 2
        H[kNy] = np.real(H[kNy])

    ry = yy - np.real(np.fft.ifft(np.fft.fft(xx) * H))
    Vy = np.diag(sigmay**2)

    Htilde = np.fft.ifft(H)

    Uy = np.zeros((N, N))
    for k in np.arange(N):
        a = np.reshape(np.roll(Htilde, k), (N,1))
        b = np.reshape(np.conj(np.roll(Htilde, k)), (1, N))
        Uy = Uy + np.real(np.dot(a, b)) * sigmax[k]**2

    W = np.dot(np.eye(N), scipy.linalg.inv(scipy.linalg.sqrtm(Uy + Vy)))
    res = np.dot(W, ry)

    return res
