# Point cloud simulation with Blensor

This repository hosts the simulation code originally from [Points2Surf](https://github.com/ErlerPhilipp/points2surf/tree/master#dataset-from-meshes-for-training-and-reconstruction). It simulates point clouds from individual meshes with [BlenSor](https://www.blensor.org/), and generates sets of query points with known signed distance values in the meantime.

## Usage

### Configuration

Configure simulation runtime settings in `./conf/blensor.yaml`, and dataset-specific configuration in `./{dataset}/settings.ini`.

### Simulation

Three sensor perspective presets are available with the parameter `perspective`:
```
# simulate point clouds from upper part of meshes
python simulate perspective='upper'

# simulate point clouds from only top of meshes
python simulate perspective='top'

# simulte point clouds all around meshes
python simulate perspective='full'
```

### Misc

`./misc/hdf5.py` and `./misc/split.py` are two scripts for HDF5 file creation and filelist split, with configurations in `./conf/hdf5.yaml` and `./conf/split.yaml`, respectively.

## References

```bibtex
@inproceedings{erler2020points2surf,
  title={Points2surf learning implicit surfaces from point clouds},
  author={Erler, Philipp and Guerrero, Paul and Ohrhallinger, Stefan and Mitra, Niloy J and Wimmer, Michael},
  booktitle={European Conference on Computer Vision},
  pages={108--124},
  year={2020},
  organization={Springer}
}
```

```bibtex
@article{chen2022points2poly,
  title = {Reconstructing compact building models from point clouds using deep implicit fields},
  journal = {ISPRS Journal of Photogrammetry and Remote Sensing},
  volume = {194},
  pages = {58-73},
  year = {2022},
  issn = {0924-2716},
  doi = {https://doi.org/10.1016/j.isprsjprs.2022.09.017},
  url = {https://www.sciencedirect.com/science/article/pii/S0924271622002611},
  author = {Zhaiyu Chen and Hugo Ledoux and Seyran Khademi and Liangliang Nan}
}
```


