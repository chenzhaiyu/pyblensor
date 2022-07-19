""""
Script to filenames into [train, val, test]
"""

import glob
from pathlib import Path
import random

import hydra
from omegaconf import DictConfig


@hydra.main(config_path='./conf', config_name='split', version_base='1.2')
def get_filelist(cfg: DictConfig):
    mesh_names = glob.glob(cfg.mesh_dir + '/*.obj')
    filelist = []
    for mesh_name in mesh_names:
        filelist.append(Path(mesh_name).stem)
    with open(cfg.all_set, 'w') as f_out:
        f_out.write('\n'.join(filelist))


@hydra.main(config_path='./conf', config_name='split', version_base='1.2')
def purge_filelist(cfg: DictConfig):
    with open(cfg.test_set, 'r') as f_test:
        filenames_test = f_test.read().splitlines()
    with open(cfg.all_set, 'r') as f_all:
        filenames_all = f_all.read().splitlines()

    for filename in filenames_all[:]:
        if filename in filenames_test:
            filenames_all.remove(filename)

    # random samples from remaining filenames_all
    filenames_val = random.sample(filenames_all, cfg.num_val)

    for filename in filenames_val:
        filenames_all.remove(filename)

    filenames_train = filenames_all
    print('size of train set:', len(filenames_train))
    print('size of val set:', len(filenames_val))
    print('size of test set:', len(filenames_test))

    with open(cfg.train_set, 'w') as f_out:
        f_out.write('\n'.join(filenames_all))

    with open(cfg.val_set, 'w') as f_out:
        f_out.write('\n'.join(filenames_val))


if __name__ == '__main__':
    get_filelist()
    purge_filelist()
