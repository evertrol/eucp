# Docker notebook for climate analysis - European Climate Prediction project

FROM jupyter/datascience-notebook:45b8529a6bfc

LABEL maintainer="EUCP-NLESC <e.rol@esciencecenter.nl>"


ENV PCRASTER_DIR=/usr/local/pcraster

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    csh \
    tcsh \
    zsh \
    less \
    htop \
    grads \
    ncl-ncarg \
##    gfortran-8 \
    cmake \
    libgl1-mesa-dev \
##  qtdeclaratives5-dev
    qtbase5-dev \
    libncurses5-dev \
    libqwt-qt5-dev \
    libqt5opengl5-dev \
##    libxerces-c-dev \
    libboost-all-dev \
    libgdal-dev \
    python3-numpy \
    python3-docopt \
 && apt-get clean


RUN mkdir -p $PCRASTER_DIR \
 && chown $NB_UID $PCRASTER_DIR \
 && fix-permissions $PCRASTER_DIR


RUN cd /tmp \
 && curl -O http://pcraster.geo.uu.nl/pcraster/4.2.1/pcraster-4.2.1.tar.bz2 \
 && tar -jxvf pcraster-4.2.1.tar.bz2 \
 && cd pcraster-4.2.1 \
 && mkdir build \
 && cd build \
 && PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
 && cmake -Wno-dev -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 -DFERN_BUILD_ALGORITHM:BOOL=TRUE  -DCMAKE_INSTALL_PREFIX:PATH=$PCRASTER_DIR .. \
 && cmake --build . \
 && make install
RUN rm -r /tmp/pcraster*

USER $NB_UID

# Notes:
# - grads is not available under Conda
# - installing ncl under Conda messes up the notebook; for example, the R kernel disappears from the menu
RUN conda install --quiet --yes --channel conda-forge --override-channels \
    'ipyleaflet' \
    'ipywidgets' \
    'iris' \
    'nc-time-axis' \
    'iris-sample-data' \
    'h5py' \
    'netcdf4' \
    'pyproj' \
    'cartopy' \
    'dask' \
    'xarray' \
    'boost' \
    'gdal' \
    'cdo' \
    'pynio' \
 && conda clean -tipsy \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

RUN pip install jupyterlab_thredds
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install jupyter-leaflet
RUN jupyter labextension install @ewatercycle/jupyterlab_thredds


ENV PATH=${PATH}:${PCRASTER_DIR}/bin
ENV PYTHONPATH=${PCRASTER_DIR}/python
