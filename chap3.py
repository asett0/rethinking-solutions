import sys
import argparse
import pyro
import pyro.distributions as dist
import torch
import pyro.ops.stats as stats
from matplotlib import pyplot as plt
import pickle
import seaborn as sns
import os
import json


# pyro.set_rng_seed(100)


# def get_samples(grid, posterior, sample_size):

#     samples = dist.Empirical(grid, posterior.log()).sample(
#         torch.Size([sample_size])
#     )

#     return samples


# def easy():

#     lam_grid = torch.linspace(0, 1, 1000)
#     prior = torch.tensor(1).repeat(1000)
#     likelihood = (
#         dist.Binomial(total_count=9, probs=lam_grid)
#         .log_prob(torch.tensor(6.0))
#         .exp()
#     )
#     posterior = likelihood * prior
#     posterior = posterior / sum(posterior)

#     return posterior


# def globe(n, grid_type):

#     p_grid = torch.linspace(0, 1, n)

#     if grid_type == "uniform":
#         prior = torch.tensor(1).repeat(n)
#     elif grid_type == "step":
#         prior = torch.tensor([0 if lam < 0.5 else 2 for lam in p_grid])
#     else:
#         raise ValueError("Invalid grid type")

#     likelihood = (
#         dist.Binomial(total_count=15, probs=p_grid)
#         .log_prob(torch.tensor(8.0))
#         .exp()
#     )

#     posterior = likelihood * prior
#     posterior = posterior / torch.sum(posterior)

#     return posterior


# Metric values
# Inertvals of defined boundary
# Intervals of defined mass


def get_posterior_samples(n_water, n_tosses, prior_type, n_grid, sample_size):

    p_grid = torch.linspace(0.0, 1.0, n_grid)

    if prior_type == "uniform":
        prior = torch.tensor(1.0).repeat(n_grid)
    elif prior_type == "step":
        prior = torch.tensor([0.0 if p < 0.5 else 2.0 for p in p_grid])
    else:
        raise ValueError("Invalid value: prior_type={}".format(prior_type))

    likelihood = (
        dist.Binomial(total_count=float(n_tosses), probs=p_grid)
        .log_prob(torch.tensor(float(n_water)))
        .exp()
    )

    posterior = likelihood * prior
    posterior = posterior / torch.sum(posterior)

    samples = dist.Empirical(p_grid, posterior.log()).sample(
        torch.Size([sample_size])
    )

    return samples


def get_prediction_samples(n_tosses, posterior_samples, sample_size):

    prediction_samples = dist.Binomial(
        total_count=n_tosses, probs=posterior_samples
    ).sample(sample_size)

    return prediction_samples


def get_metric(metric, metric_type, value, samples):
    if metric == "mass":
        if metric_type == "HDPI":
            return stats.hpdi(samples, prob=value)
        elif metric_type == "PI":
            return stats.quantile(samples, [0.5 - value / 2, 0.5 + value / 2])
        elif metric_type == "PI_WIDTH":
            pi = stats.hpdi(samples, prob=value)
            return pi[1] - pi[0]
        else:
            ValueError(
                "For metric={}, invalid value: metric_type={}".format(
                    metric, metric_type
                )
            )
    elif metric == "boundaries":

        if metric_type == "LT":
            torch.sum(samples < value).float() / len(samples)
        elif metric_type == "GT":
            torch.sum(samples > value).float() / len(samples)

        elif metric_type == "BETWEEN":
            torch.sum(
                (samples > value[0]) & (samples < value[1])
            ).float() / len(samples)
        elif metric_type == "EQUAL":
            torch.sum(samples == value).float() / len(samples)
        else:
            ValueError(
                "For: metric={}, invalid value: metric_type={}".format(
                    metric, metric_type
                )
            )
    else:
        ValueError("Invalid value: metric={}".format(metric))


# def compute_pi_width(N, true_p):
#     n = 100
#     p_grid = torch.linspace(0, 1, n)
#     prior = torch.tensor([0 if p < 0.5 else 2 for p in p_grid])
#     likelihood = (
#         dist.Binomial(total_count=N, probs=p_grid)
#         .log_prob(torch.tensor(N * true_p))
#         .exp()
#     )

#     posterior = likelihood * prior

#     posterior = posterior / sum(posterior)

#     samples = get_samples(torch.linspace(0, 1, 1000), posterior, 10000)

#     interval = stats.hdpi(samples, prob=0.99)

#     return interval[1] - interval[0]


def main(args):

    parser = argparse.ArgumentParser(
        description="""Compute posterior distributions, prediction simulations, metrics and plots 
        for globe tossing model and birth model"""
    )

    parser.add_argument(
        "-m",
        "--model",
        dest="model",
        default={"type": "globe", "n_tosses": 9, "n_water": 6},
        type=json.loads,
    )

    parser.add_argument(
        "-n", "--grid_cells", dest="n_grid", default=1000, type=int
    )

    parser.add_argument(
        "-t", "--prior_type", dest="prior_type", default="uniform"
    )

    parser.add_argument(
        "-x",
        "--n_samples_posterior",
        dest="posterior_sample_size",
        default=10000,
        type=int,
    )

    parser.add_argument(
        "-y",
        "--n_samples_prediction",
        dest="prediction_sample_size",
        default=10000,
        type=int,
    )

    parser.add_argument(
        "-o", "--output", dest="output", default="posterior_plot"
    )

    parser.add_argument("-v", "--value", dest="value", default=None)

    inputs = parser.parse_args(args)

    if inputs.output == "posterior_plot":

        if not os.path.exists("figures"):
            os.mkdir("figures")

        posterior, nW, nL = get_posterior_samples(
            inputs.model.n_water, inputs.prior_type, inputs.n_grid
        )

        fig, ax = plt.subplots()

        sns.lineplot(
            x=torch.linspace(0.0, 1.0, inputs.n_grid), y=posterior, ax=ax
        )

    # get_posterior_samples(n_water, n_tosses, prior_type, n_grid, sample_size)

    # for data in datas:
    #     fig, ax = plt.subplots()
    #     posterior, nW, nL = get_posterior(
    #         data, inputs.prior_type, inputs.n_grid
    #     )
    #     sns.lineplot(
    #         x=torch.linspace(0.0, 1.0, inputs.n_grid), y=posterior, ax=ax
    #     )
    #     plt.savefig(
    #         "figures/chap2_priorType="
    #         + inputs.prior_type
    #         + "_numGrid="
    #         + str(inputs.n_grid)
    #         + "_nW="
    #         + str(nW)
    #         + "_nL="
    #         + str(nL)
    #         + ".png"
    #     )

    # # # Easy Questions

    # easy_samples = get_posterior_samples(
    #     torch.linspace(0, 1, 1000), easy(), 10000
    # )

    # # threeE1 = torch.sum(easy_samples < 0.2).float() / len(easy_samples)

    # # threeE2 = torch.sum(easy_samples > 0.8).float() / len(easy_samples)

    # # threeE3 = torch.sum(
    # #     (easy_samples > 0.2) & (easy_samples < 0.8)
    # # ).float() / len(easy_samples)

    # # threeE4 = stats.quantile(easy_samples, 0.2)

    # # threeE5 = stats.quantile(easy_samples, 0.8)

    # # threeE6 = stats.hpdi(easy_samples, prob=0.66)

    # # threeE7 = stats.quantile(easy_samples, [0.17, 0.83])

    # # # Medium questions
    # # n = 100

    # # # Uniform prior
    # # posterior = globe(n, "uniform")

    # # fig, ax = plt.subplots()

    # # sns.lineplot(x=torch.linspace(0.0, 1.0, n), y=posterior, ax=ax)

    # # plt.savefig(
    # #     "figures/chap3_priorType="
    # #     + "uniform"
    # #     + "_numGrid="
    # #     + str(n)
    # #     + "_nW="
    # #     + str(8)
    # #     + "_nL="
    # #     + str(7)
    # #     + ".png"
    # # )

    # # medium_samples = get_samples(torch.linspace(0, 1, n), posterior, 10000)

    # # threeM2 = stats.hpdi(medium_samples, prob=0.9)

    # # prediction_samples = dist.Binomial(
    # #     total_count=15, probs=medium_samples
    # # ).sample(torch.Size([10000]))

    # # threeM3 = torch.sum(prediction_samples == 8).float() / len(
    # #     prediction_samples
    # # )

    # # prediction_samples = dist.Binomial(
    # #     total_count=9, probs=medium_samples
    # # ).sample(torch.Size([10000]))

    # # threeM4 = torch.sum(prediction_samples == 6).float() / len(
    # #     prediction_samples
    # # )

    # # # Step prior
    # # posterior = globe(n, "step")

    # # fig, ax = plt.subplots()
    # # sns.lineplot(x=torch.linspace(0.0, 1.0, n), y=posterior, ax=ax)

    # # plt.savefig(
    # #     "figures/chap3_gridType="
    # #     + "step"
    # #     + "_numGrid="
    # #     + str(n)
    # #     + "_nW="
    # #     + str(8)
    # #     + "_nL="
    # #     + str(7)
    # #     + ".png"
    # # )

    # # medium_samples = get_samples(torch.linspace(0, 1, n), posterior, 10000)

    # # threeM5_2 = stats.hpdi(medium_samples, prob=0.9)

    # # prediction_samples = dist.Binomial(
    # #     total_count=15, probs=medium_samples
    # # ).sample(torch.Size([10000]))

    # # threeM5_3 = torch.sum(prediction_samples == 8).float() / len(
    # #     prediction_samples
    # # )

    # # prediction_samples = dist.Binomial(
    # #     total_count=9, probs=medium_samples
    # # ).sample(torch.Size([10000]))

    # # threeM5_4 = sum(prediction_samples == 6).float() / len(prediction_samples)

    # # compute_pi_width(100, 0.7)

    # # Hard questions

    # with open("data/birth1.pkl") as f:
    #     birth1 = torch.tensor(pickle.load(f))

    # with open("data/birth2.pkl") as f:
    #     birth2 = torch.tensor(pickle.load(f))

    # n = 100

    # lam_grid = torch.linspace(0, 1, n)
    # prior = torch.tensor(1).repeat(n)

    # likelihood = (
    #     dist.Binomial(
    #         total_count=torch.tensor(
    #             torch.size(birth1) + torch.size(birth2)
    #         ).item(),
    #         probs=lam_grid,
    #     )
    #     .log_prob(torch.sum(birth1) + torch.sum(birth2))
    #     .exp()
    # )

    # posterior = likelihood * prior
    # posterior = posterior / torch.sum(posterior)

    # threeH1 = lam_grid[torch.argmax(posterior)]

    # print(threeH1)

    # # samples = dist.Empirical(lam_grid, posterior.log()).sample(
    # #     torch.Size(10000)
    # # )

    # # stats.hpdi(medium_samples, prob=0.50)
    # # stats.hpdi(medium_samples, prob=0.89)
    # # stats.hpdi(medium_samples, prob=0.97)

    # # predictions = dist.Binomial(
    # #     total_count=torch.tensor(
    # #         torch.size(birth1) + torch.size(birth2)
    # #     ).item(),
    # #     probs=samples,
    # # ).sample(torch.Size([10000]))

    # # # compare to torch.sum(birth1) + torch.sum(birth2)

    # # predictions = dist.Binomial(
    # #     total_count=torch.tensor(torch.size(birth1)).item(), probs=samples
    # # ).sample(torch.Size([10000]))

    # # # compare to torch.sum(birth1) + torch.sum(birth2)

    # # predictions = dist.Binomial(
    # #     total_count=torch.tensor(torch.sum(birth1 == 0)).item(), probs=samples
    # # ).sample(torch.Size([10000]))

    # # # Compare to torch.sum(birth2[birth1 == 0])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
