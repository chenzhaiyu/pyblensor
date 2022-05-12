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
        for split in cfg.splits:
            filenames = open(base_dir / dataset_name / (split + 'set.txt')).read().splitlines()

            # create empty hdf5 with placeholders
            hdf5_file = h5py.File((split + '.hdf5'), 'w')

            hdf5_file.create_dataset("points", [len(filenames), cfg.num_points, 3], float, compression=9)
            hdf5_file.create_dataset("queries", [len(filenames), cfg.num_queries, 3], float, compression=9)
            hdf5_file.create_dataset("sdf", [len(filenames), cfg.num_queries, 1], float, compression=9)

            # collect point clouds, query points and query distance
            for i, filename in enumerate(tqdm(filenames)):
                points = np.load((base_dir / dataset_name / '04_pts' / filename).with_suffix('.xyz.npy'))
                queries = np.load((base_dir / dataset_name / '05_query_pts' / filename).with_suffix('.ply.npy'))
                distances = np.load((base_dir / dataset_name / '05_query_dist' / filename).with_suffix('.ply.npy'))

                choice = np.random.choice(points.shape[0], cfg.num_points, replace=False)
                choice.sort()
                points = points[choice, :]

                hdf5_file['points'][i] = points
                hdf5_file['queries'][i] = queries
                hdf5_file['sdf'][i] = np.expand_dims(distances, axis=1)

            hdf5_file.close()


if __name__ == '__main__':
    make_h5()
