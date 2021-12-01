# pyb2d


[![Micromamba + CMake](https://github.com/pyb2d/pyb2d/actions/workflows/main.yml/badge.svg)](https://github.com/pyb2d/pyb2d/actions/workflows/main.yml)

[![Pip](https://github.com/pyb2d/pyb2d/actions/workflows/pip.yml/badge.svg)](https://github.com/pyb2d/pyb2d/actions/workflows/pip.yml)

[![Documentation Status](https://readthedocs.org/projects/pyb2d/badge/?version=latest)](https://pyb2d.readthedocs.io/en/latest/?badge=latest)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/pyb2d/pyb2d/main?urlpath=/lab/tree/examples/jupyter_integration.ipynb)


Warning, this is a work in progress and all APIs are subject to changes!
Nothing is stable yet.


### Installing from conda-forge

Then you can install in this environment `pyb2d` and its dependencies

```bash
mamba install pyb2d -c conda-forge
```

### Installing from source

Or you can install it from the sources, you will first need to install dependencies

```bash
mamba install cmake python numpy -c conda-forge
```

Then you can compile the sources (replace `$CONDA_PREFIX` with a custom installation
prefix if need be)

```bash



mkdir build && cd build
cmake .. -D CMAKE_PREFIX_PATH=$CONDA_PREFIX -D CMAKE_INSTALL_PREFIX=$CONDA_PREFIX -D CMAKE_INSTALL_LIBDIR=lib
make && make install
```

## Trying it online

To try out pyb2d interactively in your web browser, just click on the binder link:

[![Binder](docs/binder-logo.svg)](https://mybinder.org/v2/gh/pyb2d/pyb2d/main?urlpath=/lab/tree/examples/jupyter_integration.ipynb)



## Features:

* Liquidfun Integration

* Pygame Integration

* Jupyter Integration

![jupyter_integration](docs/img/jupyter_integration.gif)



## History

This project originated 2015 with the goal to create python bindings for liquidfun.
The original work can still be found here: https://github.com/DerThorsten/liquidfun/tree/master/liquidfun/Box2D/pybox2d
