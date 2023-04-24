import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.sin(2*np.pi*x)


def u_exact(x):
    c = -f(x)/(4*np.pi**2 + 2)
    return c


def solve(N):
    h = 1/(N+1)
    x = np.linspace(0, 1, N+1)
    b = -f(x)
    A = np.zeros((N + 1, N + 1))
    np.fill_diagonal(A, 2 + 2 / h ** 2)
    np.fill_diagonal(A[1:], -1 / h ** 2)
    np.fill_diagonal(A[:, 1:], -1 / h ** 2)
    u = np.linalg.solve(A, b)
    return x, u


N_values = [10, 50, 100, 500]
for N in N_values:
    x, u = solve(N)
    plt.plot(x, u, '--',  label='N={}'.format(N))
x_exact = np.linspace(0, 1, 1000)
u_e = u_exact(x_exact)
plt.plot(x_exact, u_e, label='Exact')
plt.legend()
plt.show()
