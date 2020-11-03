import torch
import pyro.distributions as dist


def sample_binomial(n, k, n_steps, n_samples):
    """Generate samples from a binomial distribution.
    Assumes a flat prior distribution.

    Args:
        n (int):        Binomial distribution total count
        k (int):        Binomial distribution total success
        n_steps (int):  Resolution of probability grid (number of steps
                        between 0 and 1)
        n_sample (int): Number of items to sample

    """
    p_grid = torch.linspace(start=0, end=1, steps=n_steps)
    prior = torch.tensor(1.).repeat(n_steps)
    likelihood = dist.Binomial(
        total_count=n,
        probs=p_grid
    ).log_prob(torch.tensor(float(k))).exp()
    posterior = likelihood * prior
    posterior = posterior / sum(posterior)
    samples = dist.Empirical(
        p_grid,
        posterior.log()
    ).sample(torch.Size([n_samples]))
    return samples


def posterior_predictive_binomial(n, posterior, n_samples):
    """Sample from each value of p in the posterior distribution.

    Args:
        n (int):            Binomial distribution total count
        posterior (array):  Posterior distribution
        samples (int)       Number of samples to generate

    """
    return dist.Binomial(
        total_count=n,
        probs=posterior
    ).sample(torch.Size([int(n_samples)])).long()
