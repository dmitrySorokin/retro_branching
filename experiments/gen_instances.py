from retro_branching.utils import check_if_network_params_equal, seed_stochastic_modules_globally
from retro_branching.environments import EcoleBranching
from retro_branching.utils import generate_craballoc, generate_tsp

import ecole
import torch

import random
from tqdm import trange

import os
import argparse

import hydra
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf
import shutil

hydra.HYDRA_FULL_ERROR = 1


@hydra.main(config_path='configs', config_name='config.yaml')
def run(cfg: DictConfig):
    # seeding
    if 'seed' not in cfg.experiment:
        cfg.experiment['seed'] = random.randint(0, 10000)
    seed_stochastic_modules_globally(cfg.experiment.seed)

    # print info
    print('\n\n\n')
    print(f'~' * 80)
    print(f'Config:\n{OmegaConf.to_yaml(cfg)}')
    print(f'~' * 80)

    # initialise instance generator
    if cfg.instances.co_class == 'set_covering':
        instances = ecole.instance.SetCoverGenerator(**cfg.instances.co_class_kwargs)
    elif cfg.instances.co_class == 'combinatorial_auction':
        instances = ecole.instance.CombinatorialAuctionGenerator(**cfg.instances.co_class_kwargs)
    elif cfg.instances.co_class == 'capacitated_facility_location':
        instances = ecole.instance.CapacitatedFacilityLocationGenerator(**cfg.instances.co_class_kwargs)
    elif cfg.instances.co_class == 'maximum_independent_set':
        instances = ecole.instance.IndependentSetGenerator(**cfg.instances.co_class_kwargs)
    elif cfg.instances.co_class == 'crabs':
        instances = generate_craballoc(**cfg.instances.co_class_kwargs)
    elif cfg.instances.co_class == 'tsp':
        instances = generate_tsp(**cfg.instances.co_class_kwargs)
    else:
        raise Exception(f'Unrecognised co_class {cfg.instances.co_class}')
    print(f'Initialised instance generator.')

    print(cfg.environment.scip_params)

    # initialise branch-and-bound environment
    env = EcoleBranching(observation_function=cfg.environment.observation_function,
                         information_function=cfg.environment.information_function,
                         reward_function=cfg.environment.reward_function,
                         scip_params=cfg.environment.scip_params)
    print(f'Initialised environment.')

    # data generation
    for i in trange(1000):
        done = True
        while done:
            instance = next(instances)
            env.seed(cfg.experiment.seed)
            obs, act, rew, done, info = env.reset(instance.copy_orig())

        instance.write_problem(
            f'../../../retro_branching_paper_validation_instances/'
            f'tsp_n_nodes_20_planar_False'
            f'/instance_{i}.mps'
        )


if __name__ == '__main__':
    run()
