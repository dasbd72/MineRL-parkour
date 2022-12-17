
# Installation

## Macos

### Conda

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* xcode-select --install
* conda install ipykernel --update-deps --force-reinstall

### [Tensorflow](https://developer.apple.com/metal/tensorflow-plugin/)

* conda install -c apple tensorflow-deps
* python -m pip install tensorflow-macos==2.10.0
* python -m pip install tensorflow-metal==0.6.0

### Torch
* conda install pytorch torchvision torchaudio -c pytorch

### Minerl
* pip install git+https://github.com/minerllabs/minerl@v0.4
* pip install pyglet==1.5.27 --user
* pip install numpy --force-reinstall

#### 1.0.0
* pip install git+https://github.com/minerllabs/minerl
* https://github.com/minerllabs/minerl/issues/374

### fix numpy
* ls /opt/miniconda3/envs/minerl-0.4.4/lib/python3.9/site-packages
* rm -r /opt/miniconda3/envs/minerl-0.4.4/lib/python3.9/site-packages/numpy-1.22.3.dist-info

## Windows

Condo env with python=3.10
### Cuda

* conda install -c "nvidia/label/cuda-11.7.1" cuda-toolkit

### Torch

* conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia

### Minerl

* conda install openjdk=8
* pip install git+https://github.com/minerllabs/minerl@v0.4
* pip install pyglet==1.5.27
* pip install numpy --force-reinstall

### Remote

* jupyter notebook --no-browser --port=8080
* ssh -L 8080:localhost:8080 \<Remote\>