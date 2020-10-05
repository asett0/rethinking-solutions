import sys
import argparse
import pyro
import pyro.distributions as dist
import torch
import pyro.ops.stats as stats
from matplotlib import pyplot as plt

pyro.set_rng_seed(100)


def get_samples(grid, posterior, sample_size):

    samples = dist.Empirical(grid, posterior.log()).sample(
        torch.Size(sample_size)
    )

    return samples


def easy():

    lam_grid = torch.linspace(0, 1, 1000)
    prior = torch.tensor(1).repeat(1000)
    likelihood = (
        dist.Binomial(total_count=9, probs=lam_grid)
        .log_prob(torch.tensor(6.0))
        .exp()
    )
    posterior = likelihood * prior
    posterior = posterior / sum(posterior)

    return posterior


def globe(n, grid_type):

    lam_grid = torch.linspace(0, 1, n)

    if grid_type == "uniform":
        prior = torch.tensor(1).repeat(n)
    elif grid_type == "step":
        prior = torch.tensor([0 if lam < 0.5 else 2 for lam in lam_grid])
    else:
        raise ValueError("Invalid grid type")

    likelihood = (
        dist.Binomial(total_count=15, probs=lam_grid)
        .log_prob(torch.tensor(8.0))
        .exp()
    )

    posterior = likelihood * prior
    posterior = posterior / sum(posterior)

    return posterior


def compute_pi_width(N, true_lam):
    n = 100
    lam_grid = torch.linspace(0, 1, n)
    prior = torch.tensor([0 if lam < 0.5 else 2 for lam in lam_grid])
    likelihood = (
        dist.Binomial(total_count=N, probs=lam_grid)
        .log_prob(torch.tensor(N * true_lam))
        .exp()
    )

    posterior = likelihood * prior

    posterior = posterior / sum(posterior)

    samples = get_samples(torch.linspace(0, 1, 1000), posterior, 10000)

    interval = stats.hdpi(samples, prob=0.99)

    return interval[1] - interval[0]


def main(args):

    # Easy Questions

    easy_samples = get_samples(torch.linspace(0, 1, 1000), easy(), 10000)

    sum(easy_samples < 0.2).float() / len(easy_samples)

    sum(easy_samples > 0.8).float() / len(easy_samples)

    sum((easy_samples > 0.2) & (easy_samples < 0.8)) / len(easy_samples)

    stats.quantile(easy_samples, 0.2)

    stats.quantile(easy_samples, 0.8)

    stats.hpdi(easy_samples, prob=0.66)

    stats.quantile(easy_samples, [0.17, 0.83])

    # Medium questions
    n = 100
    # Uniform prior

    posterior = globe(n, "uniform")

    fig, ax = plt.subplots()

    plt.plot(torch.linspace(0, 1, n), posterior)

    plt.savefig(
        "figures/gridType="
        + "uniform"
        + "_numGrid="
        + str(n)
        + "_nW="
        + str(8)
        + "_nL="
        + str(7)
        + ".png"
    )

    medium_samples = get_samples(torch.linspace(0, 1, n), posterior, 10000)

    stats.hpdi(medium_samples, prob=0.9)

    prediction_samples = dist.Binomial(
        total_count=15, probs=medium_samples
    ).sample(torch.Size([10000]))

    sum(prediction_samples == 8) / len(prediction_samples)

    prediction_samples = dist.Binomial(
        total_count=9, probs=medium_samples
    ).sample(torch.Size([10000]))

    sum(prediction_samples == 6) / len(prediction_samples)

    # Step prior
    posterior = globe(n, "step")

    fig, ax = plt.subplots()

    plt.plot(torch.linspace(0, 1, n), posterior)

    plt.savefig(
        "figures/gridType="
        + "step"
        + "_numGrid="
        + str(n)
        + "_nW="
        + str(8)
        + "_nL="
        + str(7)
        + ".png"
    )

    medium_samples = get_samples(torch.linspace(0, 1, n), posterior, 10000)

    stats.hpdi(medium_samples, prob=0.9)

    prediction_samples = dist.Binomial(
        total_count=15, probs=medium_samples
    ).sample(torch.Size([10000]))

    sum(prediction_samples == 8) / len(prediction_samples)

    prediction_samples = dist.Binomial(
        total_count=9, probs=medium_samples
    ).sample(torch.Size([10000]))

    sum(prediction_samples == 6) / len(prediction_samples)

    compute_pi_width(100, 0.7)
    # Hard questions


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
