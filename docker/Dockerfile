FROM continuumio/anaconda3:5.0.1

# install sys requirements
RUN apt-get update
RUN apt-get install -y build-essential git

# clone in repo
RUN git clone https://github.com/DerThorsten/pybox2d

# update conda
RUN conda update --yes conda

# go into repo
RUN cd pybox2d && conda env create -f pybox2d-dev-requirements.yml

# activate
RUN echo "source activate pybox2d-dev-requirements" > ~/.bash
ENV PATH /opt/conda/envs/pybox2d-dev-requirements/bin:$PATH

# activate
#RUN conda activate pybox2d-dev-requirements

# make build dir
RUN cd pybox2d && mkdir build

# run cmake
RUN  cd pybox2d/build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=$(conda info --base)/envs/pybox2d-dev-requirements

# build and install project
RUN cd pybox2d/build && \
    make -j2 install