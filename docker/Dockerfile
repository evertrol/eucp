# Docker notebook for climate analysis - European Climate Prediction project

FROM jupyter/datascience-notebook:45b8529a6bfc

LABEL maintainer="EUCP-NLESC <e.rol@esciencecenter.nl>"


ENV PCRASTER_DIR=/usr/local/pcraster

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    grads \
    cdo \
    gfortran-8 \
    cmake \
	gcc \
	g++ \
	git \
	qtbase5-dev \
	libncurses5-dev \
	libqwt-qt5-dev \
	libqt5opengl5-dev \
	libxerces-c-dev \
	libboost-all-dev \
	libgdal-dev \
	python3-numpy \
	python3-docopt \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir -p $PCRASTER_DIR \
 && chown $NB_UID $PCRASTER_DIR \
 && fix-permissions $PCRASTER_DIR


RUN cd /tmp \
 && curl -O http://pcraster.geo.uu.nl/pcraster/4.2.1/pcraster-4.2.1.tar.bz2 \
 && tar -jxvf pcraster-4.2.1.tar.bz2 \
 && cd pcraster-4.2.1 \
# && sed -i.bck 's/python3/python36/g' environment/cmake/PCRasterConfiguration.cmake \
# && sed -i.bck 's/numpy3/numpy36/g' environment/cmake/PCRasterConfiguration.cmake \
 && mkdir build \
 && cd build \
 && PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
 && cmake -Wno-dev -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3 -DFERN_BUILD_ALGORITHM:BOOL=TRUE  -DCMAKE_INSTALL_PREFIX:PATH=$PCRASTER_DIR .. \
 && cmake --build . \
 && make install


USER $NB_UID

RUN conda install --quiet --yes --channel conda-forge --override-channels \
    'ipyleaflet' \
    'ipywidgets' \
    'iris' \
    'iris-sample-data' \
	'h5py' \
    'netcdf4' \
    'pyproj' \
    'dask' \
    'xarray' \
    'boost' \
    'gdal' \
 && conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER


ENV PATH=${PATH}:${PCRASTER_DIR}/bin
ENV PYTHONPATH=${PCRASTER_DIR}/python
