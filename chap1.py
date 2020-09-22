import numpy as np
import math
from matplotlib import pyplot as plt
import sys
import argparse

datas = [
    ["W", "W", "W"],
    ["W", "W", "W", "L"],
    ["L", "W", "W", "L", "W", "W", "W"],
]


def get_pgrid(grid_type, grid):
    if grid_type == "uniform":
        p_grid = [1 / len(grid)] * len(grid)
    elif grid_type == "step":
        raw_p_grid = [0 if lam < 0.5 else 1 for lam in grid]
        grid_norm = np.sum(raw_p_grid)
        p_grid = [p / grid_norm for p in raw_p_grid]

    return p_grid


def binomial(n, k, p):
    comb = math.factorial(n) / (math.factorial(k) * math.factorial(n - k))
    return comb * p ** k * (1 - p) ** (n - k)


def get_posterior(WLs, p_grid, grid):
    nW = WLs.count("W")
    nL = WLs.count("L")
    likelihoods = [binomial(nW + nL, nW, p) for p in grid]
    raw_posterior = [
        likelihood * p for (likelihood, p) in zip(likelihoods, p_grid)
    ]
    norm = np.sum(raw_posterior)
    posterior = [p / norm for p in raw_posterior]
    return posterior, nW, nL


def main(args):

    parser = argparse.ArgumentParser(
        description="Computer posterior distributions for globe tossing model"
    )

    parser.add_argument(
        "-n", "--grid_number", dest="n_grid", default=20, type=int
    )
    parser.add_argument(
        "-t", "--grid_type", dest="grid_type", default="uniform"
    )

    inputs = parser.parse_args(args)

    grid = np.linspace(0, 1, inputs.n_grid)
    p_grid = get_pgrid(inputs.grid_type, grid)

    for data in datas:
        fig, ax = plt.subplots()
        posterior, nW, nL = get_posterior(data, p_grid, grid)
        plt.plot(grid, posterior)
        plt.savefig(
            "figures/gridType="
            + inputs.grid_type
            + "_numGrid="
            + str(inputs.n_grid)
            + "_nW="
            + str(nW)
            + "_nL="
            + str(nL)
            + ".png"
        )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
