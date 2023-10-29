from math import exp


def hPreciPow(x, power):
    result = 1
    for _ in range(power):
        result *= x
    return result


def f(x):
    return 1/4*hPreciPow(x[0], 4)


def fGradient(x):
    return [hPreciPow(x[0], 3)]


def g(x):
    return (1.5 - exp(-pow(x[0], 2) - pow(x[1], 2)) -
            0.5 * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2)))


def gGradient(x):
    return [2 * x[0] * exp(-pow(x[0], 2) - pow(x[1], 2))
            + (x[0] - 1) * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2)),

            2 * x[1] * exp(-pow(x[0], 2) - pow(x[1], 2))
            + (x[1] - 1) * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2))]
