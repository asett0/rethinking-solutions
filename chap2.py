import pyro.distributions as dist
import seaborn as sns
from matplotlib import pyplot as plt
import sys
import argparse
import torch

datas = [
    ["W", "W", "W"],
    ["W", "W", "W", "L"],
    ["L", "W", "W", "L", "W", "W", "W"],
]


def get_posterior(data, prior_type, n_grid):

    p_grid = torch.linspace(0.0, 1.0, n_grid)

    if prior_type == "uniform":
        prior = torch.tensor(1.0).repeat(n_grid)
    elif prior_type == "step":
        prior = torch.tensor([0.0 if p < 0.5 else 2.0 for p in p_grid])
    else:
        raise ValueError("Invalid prior_type={} provided".format(prior_type))

    nW = data.count("W")
    nL = data.count("L")

    likelihood = (
        dist.Binomial(total_count=float(nW + nL), probs=p_grid)
        .log_prob(torch.tensor(float(nW)))
        .exp()
    )

    posterior = likelihood * prior
    posterior = posterior / torch.sum(posterior)

    return posterior, nW, nL


def main(args):

    parser = argparse.ArgumentParser(
        description="Compute posterior distributions for globe tossing model"
    )

    parser.add_argument(
        "-n", "--grid_cells", dest="n_grid", default=20, type=int
    )
    parser.add_argument(
        "-t", "--prior_type", dest="prior_type", default="uniform"
    )

    inputs = parser.parse_args(args)

    for data in datas:
        fig, ax = plt.subplots()
        posterior, nW, nL = get_posterior(
            data, inputs.prior_type, inputs.n_grid
        )
        sns.lineplot(
            x=torch.linspace(0.0, 1.0, inputs.n_grid), y=posterior, ax=ax
        )
        plt.savefig(
            "figures/chap2_priorType="
            + inputs.prior_type
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
