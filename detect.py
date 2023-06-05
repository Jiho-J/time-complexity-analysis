import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def constant(x, a):
    return x * 0 + a


def linear(x, a, b):
    return a * x + b


def quadratic(x, a, b, c):
    return a * x ** 2 + b * x + c


def binary_log(x, a, b):
    return a * np.log2(x) + b


def binary_exp(x, a, b):
    return a * 2 ** x + b


def nLogn(x, a, b):
    return a * x * np.log2(x) + b


def detect_trend(x, y):
    plt.clf()
    models = {
        'constant': constant,
        'linear': linear,
        'quadratic': quadratic,
        'binary_log': binary_log,
        'binary_exp': binary_exp,
        'nlogn': nLogn
    }

    best_model = None
    best_params = None
    best_r_squared = -np.inf

    for model_name, model_func in models.items():
        try:
            params, _ = curve_fit(model_func, x, y)
            residuals = y - model_func(x, *params)
            ss_residuals = np.sum(residuals ** 2)
            ss_total = np.sum((y - np.mean(y)) ** 2)
            print(ss_residuals, ss_total)
            r_squared = 1 - (ss_residuals / ss_total)
            plt.plot(x, models[model_name](x, *params), color='gray')
            print(model_name, ':', r_squared)

            if r_squared > best_r_squared:
                best_model = model_name
                best_params = params
                best_r_squared = r_squared
        except Exception as e:
            print(e)

    print("Best Model:", best_model)
    print("Best Parameters:", best_params)
    print("Best R-squared:", best_r_squared)

    plt.scatter(x, y, label='Data', linewidths=0.2)
    plt.plot(x, models[best_model](x, *best_params), color='red', label=best_model)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


