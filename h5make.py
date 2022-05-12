"""
Convert Blensor-generated point clouds and query samples to hdf5 format.
"""

from pathlib import Path

import numpy as np
import h5py
from tqdm import tqdm
import hydra
from omegaconf import DictConfig


@hydra.main(config_path='./conf', config_name='hdf5')
def make_h5(cfg: DictConfig):
    """
    Make hdf5 data.
    """
    base_dir = Path(cfg.base_dir)
    for dataset_name in cfg.dataset_names:
        filenames_train = open(base_dir / dataset_name / 'trainset.txt').read().splitlines()

        # create empty hdf5 with placeholders
        hdf5_train = h5py.File(cfg.hdf5_train, 'w')

        hdf5_train.create_dataset("points", [len(filenames_train), cfg.num_points, 3], float, compression=9)
        hdf5_train.create_dataset("queries", [len(filenames_train), cfg.num_queries, 3], float, compression=9)
        hdf5_train.create_dataset("sdf", [len(filenames_train), cfg.num_queries, 1], float, compression=9)

        # collect point clouds, query points and query distance
        for i, filename_train in enumerate(tqdm(filenames_train)):
            points = np.load((base_dir / dataset_name / '04_pts' / filename_train).with_suffix('.xyz.npy'))
            queries = np.load((base_dir / dataset_name / '05_query_pts' / filename_train).with_suffix('.ply.npy'))
            distances = np.load((base_dir / dataset_name / '05_query_dist' / filename_train).with_suffix('.ply.npy'))

            choice = np.random.choice(points.shape[0], cfg.num_points, replace=False)
            choice.sort()
            points = points[choice, :]

            hdf5_train['points'][i] = points
            hdf5_train['queries'][i] = queries
            hdf5_train['sdf'][i] = np.expand_dims(distances, axis=1)

        hdf5_train.close()


if __name__ == '__main__':
    make_h5()
