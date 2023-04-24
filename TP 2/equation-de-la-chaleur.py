import matplotlib.pyplot as plt
import numpy as np
import time

# valeurs d'entrées
m = 1000
# petit
# m = 100
n = 10
X = 10
T = 5
dt = T / m
h = 0.1
# grand
# h = 1
# petit
# h = 0.01

# intervalle de temps et d'espace
x = np.linspace(0, X, n+2)
t = np.linspace(0, T, m+1)

# matrice A
A = np.zeros((n+2, n+2))
np.fill_diagonal(A, 2)
np.fill_diagonal(A[1:], -1)
np.fill_diagonal(A[:, 1:], -1)

# données de l'exercice
alpha = 50*(1+t)**2
beta = 50*(1-t)**2
f = 50*np.ones(x.shape)

# matrcice V^j
V = np.zeros((m+1, n+2))
V[:, 0] = alpha
V[:, -1] = beta

# programme principal
t0 = time.time()
U = np.zeros((m+1, n+2))
U[0] = f

for i in range(m):
    U[i+1] = U[i] - dt / h**2 * A @ U[i] + dt / h**2 * V[i]
t1 = time.time()
print('Temps : {}'.format(round((t1-t0), 2)) + ' secondes')

for i in range(0, m+1, m//10):
    plt.plot(x, U[i], label='t = {}'.format(round((i*dt), 2)))
plt.xlabel('x')
plt.ylabel('Temperature')
plt.title('Propagation de la chaleur')
# plt.title('Propagation de la chaleur avec h grand')
# plt.title('Propagation de la chaleur avec h petit')
plt.legend()
plt.show()

# Programme principal 2
t0 = time.time()
U2 = np.zeros((m+1, n+2))
U2[0] = f
Id = np.eye(n+2)

for j in range(1, m+1):
    U2[j] = np.linalg.inv(Id + dt / h**2 * A) @ (U2[j-1] + dt / h**2 * V[j])

for j in range(0, m+1, m//10):
    plt.plot(x, U2[j], label='t = {}'.format(round((j*dt), 2)))
t1 = time.time()
print('Temps : {}'.format(round((t1-t0), 2)) + ' secondes')

plt.xlabel('x')
plt.ylabel('Temperature')
plt.title('Propagation de la chaleur 2')
# plt.title('Propagation de la chaleur 2 avec h grand')
# plt.title('Propagation de la chaleur 2 avec h petit')
plt.legend()
plt.show()

# On remarque que la méthode 1 est plus rapide mais moins stable pour un h ou m petit
# Pour un m très grand le programme 2 est 'infini'
