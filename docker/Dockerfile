# Docker notebook for climate analysis - European Climate Prediction project

FROM jupyter/datascience-notebook:45b8529a6bfc

LABEL maintainer="EUCP-NLESC <e.rol@esciencecenter.nl>"


USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    grads \
    cdo \
    gfortran-8 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER $NB_UID

RUN conda install --quiet --yes --channel conda-forge --override-channels \
    'ipyleaflet' \
	'ipywidgets' \
    'iris' \
    'iris-sample-data' \
	'netcdf4' \
	'pyproj' \
    'dask' \
    'xarray' && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
