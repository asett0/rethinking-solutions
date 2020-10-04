import sys
import argparse
import pyro
import pyro.distributions as dist
import torch
import pyro.ops.stats as stats

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

    return lam_grid, posterior


def globe(n):
    lam_grid = torch.linspace(0, 1, n)
    prior = torch.tensor(1).repeat(n)
    likelihood = (
        dist.Binomial(total_count=15, probs=lam_grid)
        .log_prob(torch.tensor(8.0))
        .exp()
    )
    posterior = likelihood * prior
    posterior = posterior / sum(posterior)

    return posterior


def main(args):

    # parser = argparse.ArgumentParser(
    #     description="Computer posterior distributions for globe tossing model"
    # )

    # parser.add_argument(
    #     "-n", "--grid_number", dest="n_grid", default=20, type=int
    # )
    # parser.add_argument(
    #     "-t", "--grid_type", dest="grid_type", default="uniform"
    # )

    # inputs = parser.parse_args(args)

    # Easy Questions

    samples = get_samples(*easy(), 1000)

    sum(samples < 0.2).float() / len(samples)

    sum(samples > 0.8).float() / len(samples)

    sum((samples > 0.2) & (samples < 0.8)) / len(samples)

    stats.quantile(samples, 0.2)

    stats.quantile(samples, 0.8)

    stats.hpdi(samples, prob=0.66)

    stats.quantile(samples, [0.17, 0.83])

    # Medium questions


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
