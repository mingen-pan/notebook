from math import exp
import matplotlib.pyplot as plt

class Hybrid:
    def __init__(self, n0, eps, delta):
        self.n0 = n0
        self.eps = eps
        self.delta = delta
        self.update_parameters()

    def update_parameters(self):
        self.p0 = (exp(self.eps) - 1 + self.delta*(1-exp(-self.eps))) / (exp(self.eps) - exp(-self.eps))
        self.p1 = exp(-self.eps) * self.p0 + 1 - exp(-self.eps) * (1 - self.delta)
        self.a = exp(-self.eps)
        self.b = - self.delta * exp(-self.eps) / (1 - exp(-self.eps))
        self.c = exp(-2 * self.eps)
        self.d = (1 - exp(-self.eps) * (1 - self.delta)) * (1 + exp(-self.eps)) / (1 - self.c)

    def prob(self, n):
        if n >= self.n0:
            if (n - self.n0) % 2:
                return self.c ** ((n - self.n0 - 1) / 2) * (self.p1 - self.d) + self.d
            else:
                return self.c ** ((n - self.n0) / 2) * (self.p0 - self.d) + self.d
        else:
            return self.a ** (self.n0 - n) * (self.p0 - self.b) + self.b



if __name__ == '__main__':
    h = Hybrid(0, 1e-3, 1e-3)
    p = 0
    print(h.p0)
    for n in range(0, -10001, -100):
        p = h.prob(n)
        if p <= 0.01:
            print("find one", n, p)
            break
    else:
        print("cannot find:", p)


    for n in range(0, 10000, 100):
        p = h.prob(n)
        if p >= 0.99:
            print("find one", n, p)
            break
    else:
        print("cannot find:", p)


    x = list(range(-4000, 4001, 10))
    y = [h.prob(i) for i in x]
    plt.plot(x, y)
    plt.show()
