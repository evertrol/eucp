# EUCP Notebook

31-08-2018

A notebook system for climate research.

Note: this document is work in progress.
This README will be shortened in the near future to provide a summary, with other documents providing details for the different sections.

## Goals

This repository documents a notebook system for possible use within the European Climate Prediction (EUCP) system project.
This notebook system allows scientists to use a uniform interface to perform their analysis on climate data sets, without the need to download the required data sets locally.
In addition, the analysis steps are to be saved (including history versioning) for reproducibility.
The use of notebooks also allows easy sharing, for example with peers (direct collaborators, referees etc.) and a more general audience.

The development of the notebook system will be through use cases and feedback from scientists directly involved in the EUCP project.
This should lead to a development system with rapid fixes and extensions in an iterative procedure.

In a worse-case scenario, the feedback may be such that the suggested system will have to be abandoned and replaced by something else.
On the other hand, the system may work well enough that its can be extended to several other areas of research.
In fact, notebook systems are already developed and used in related areas.

## Implementation

The notebook implementation to use is the Jupyter notebook.
This started originally as an extended Python interactive interpreter, and has evolved with a variety of extensions.
One of its main uses is in data analysis, since it includes output, including visualisations, directly in the notebook.
In addition, Python is widely used in the sciences for analysis, and nowadays a wide variety of packages (libraries) exist to help with that.
Note that, while the Jupyter notebook comes from the Python world and is largely programmed in Python (with lots of JavaScript on the user interface side), it allows a variety of "kernels" to run in the notebooks.
This includes kernels for R and Julia, as well as various Python versions (notably, versions 2.x versus 3.x).
In all cases, the notebook simply functions as an mediator, passing input from the user to the relevant interpreter or compiler behind the scenes, and output from the interpreter or compiler back to the user.

The widespread use of the Jupyter notebook should help with its usage: many users may not have to learn a new interface, or they may easily find help (either from (local) colleagues or on the internet) with its use.

### Lab environment

The Jupyter notebook environment has been extended to include a shell environment with a command line and a text editor, and the option to start multiple sessions and kernels (e.g., Python 2, Python 3, R, Julia) all from the same session.
This is now called [JupyterLab](http://jupyterlab.readthedocs.io/en/latest/).

Like the notebook, JupyterLab can be run locally (`python -m jupyter lab` from the command line), or, for the case here, remotely through a web browser.

### Hub

The JupyterHub is a system where multiple users can start a notebook (or lab) on the same server: each notebook is separate from the other notebooks.
JupyterHub is the underlying system for remote use of Jupyter notebooks / labs.


### Binders

A recent development are notebook binders.
These use (often very simple) repositories that lists required packages (how this is to be listed, depends on the language to be used in the notebook).
The binder interface will accept a link to the repository, and create a notebook environment with those packages installed.
This allows anyone to tweak their notebook to their needs.
In addition, notebook files (`*.ipynb`) can be saved in the same repository.
This makes it straightforward for others to recreate the environment, *and* load the relevant notebook.

For generic use, one or a few notebook environments will be given as an option to select from, so that users do not need to create a repository first.
In addition, notebooks also accept a `!pip install <package>` syntax (and similar for R and Julia), which escapes the notebook session (thanks to the `!`) and will install the relevant package.
This last option is more a quick-fix solution; binders allow for full Conda environments to be installed.

The main project for Jupyter notebooks binders is [BinderHub](https://binderhub.readthedocs.io/en/latest/).
As the name indicates, the actual underlying infrastructure is provided by JupyterHub; BinderHub adds the option of turning a repository into a Dockerfile that can be used to start a notebook environment.
The latter is done through a utility called `repo2docker`, which is developed within the larger [JupyterHub project](https://github.com/jupyterhub).

A demonstration page (that can actually be used already!) is at https://mybinder.org/.

### Example cases

Note: some of the mybinder examples may take some time to load.

See also https://mybinder.readthedocs.io/en/latest/sample_repos.html

- Julia and Python notebook: http://mybinder.org/v2/gh/binder-examples/julia_python/master

  Once loaded, change this example to a JupyterLab environment by changing the `tree` bit at the end of the URL into `lab`.

- R notebook: https://hub.mybinder.org/user/binder-examples-r-huwjm759/notebooks/index.ipynb

- R studio environment: https://mybinder.org/v2/gh/ha0ye/RainCloudPlots/master?urlpath=rstudio

- Pangeo data: http://pangeo.pydata.org/hub/login

  Requires a GitHub account to sign in.
  Provides a JupyterLab environment for geoscience.
  It allows to run multi-core processes using `dask` and `xarray` on a cloud system: this will fire off separate "pods" for the computation.

  For more information, see http://pangeo.io.

## Infrastructure

### Kubernetes

The underlying infrastructure used is Kubernetes.
This is a system that manages containerized applications.
In this particular case, every user will start a new notebook in its own container, or pods as they are called in Kubernetes' terms.
Kubernetes will take care of the resources allocated to that pod (maximum memory, disk and CPU usage, for example).
It will also create (deploy) and remove pod as necessary.

### Docker

Kubernetes itself relies on Docker for creating the containers.
This is why it is somewhat straightforward to create a specific notebook Binder: starting from a base Docker file, it will create a new container with relevant packages and libraries, then start that container (in isolation of other notebook containers) to be used.
The new containers will be hosted in a private registry.
BinderHub has options for hosting containers at https://gcr.io (Google Cloud Container Registry) or at https://hub.docker.com/, Docker Hub.

Note that a Kubernetes pod can actually contain multiple containers.
In most situations for BinderHub, a single pod runs a single container, but the Nginx and http-proxy-public containers share a pod.

### BinderHub architecture

The BinderHub system requires several containers to be run (whether on a single machine or a cluster does not really matter), which will all communicate with each other using the HTTP protocol.
Installation of this is detailed on the [Zero to JupyterHub with Kubernetes](https://zero-to-jupyterhub.readthedocs.io/en/latest/) and the [BinderHub](https://binderhub.readthedocs.io/en/latest/) documentation.

Once set up, there will be pods running

- BinderHub: this runs a webserver (using the Python Tornado package) that allows users to pick a repository and then build a notebook environment from it.
- JupyterHub: the actual hub that will spawn a new notebook for each new user, as detailed above.
- Nginx and http-proxy-public: intermediates between the actual outside world, and BinderHub and JupyterHub.

Once a user has chosen to build a new environment, a new pod will be created which runs `repo2docker`, a specialized tool to create a Docker container from a list of packages (this tool was written in the context of the BinderHub project).
Once the container has been built and uploaded to the container registry, this pod will be removed again.

A new pod will now be started (with a name relevant to the used repository; though the pod names are only relevant to administrators, as users will not see these), that runs the actual notebook.

Some further details can be found at the relevant [page of the BinderHub documentation](https://binderhub.readthedocs.io/en/latest/overview.html), from which the below figure is also taken:

![The BinderHub architecture. From https://binderhub.readthedocs.io/en/latest/overview.html](https://binderhub.readthedocs.io/en/latest/_static/images/architecture.png)


## Issues / to-do list

### Technical challenges

There are several technical challenges that need to be solved before this system can be used fully.
Note that these are essentially requirements for a proper EUCP notebook system.

- Binders & notebooks need to be login protected.
  This may be a login arranged by an administrator, but alternatively this is an external OpenID account.
  One reason for this is to limit the use by random people outside the project.
  A managed system-login is the probably the easiest to set which people have access; an external OpenID account may have some other advantages, mentioned below.

- A certain amount of (often used) data sets should be stored as "cache" data locally, on the same server that runs the notebook system, or directly next to it.
  This allows fast and easy access for users, compared to retrieving data sets from, for example, ESGF nodes elsewhere.

  This likely requires the containers inside the pods to access data on their host.

- Resources, in particular data sets, may be limited by permissions.
  Usually, this requires a person to log in to an ESGF system and select the relevant data sets for which they require access.
  This would mean the notebook system needs to be able to

  * request permission through the ESGF system for locally stored data sets

  * check that a user has the correct permissions

  This may mean the notebook system needs to run a permission system similar to that of ESGF nodes.
  It also requires checking with the ESGF that this can be done without problems.

  Alternatively, the notebook system could host only data sets that are approved for general, open access.
  In particular, if all users logging in to the notebook system do this through the ESGF OpenID system, this provides a minor guarantee for proper use of the data sets (though it is unclear how this would work, for example, with commercial parties logging in).

- Users need to be able to access each other data and notebooks, in a read-only fashion, similar to working on a standard (file) server.
  There is the standard option of sharing a notebook through an access token, but this allows anyone with the token to edit the notebook.
  Since everything is run through containers inside pods, and each users often starts up their own pod, this may require digging into how pods could connect in an invisible, easy and read-only way for users on a Kubernetes system.
  Optionally, users should be able to set who has read access, so that their direct colleagues can access their data, while others may not (in particular for intermediate data).

- Users need to be able to store intermediate data (derived data) on the system (within limits), such that it can be accessed again later, either by the same user or other users.

- Scripts, notebooks etcetera, should be easy to version.
  Potentially, this could be done directly by the user, by saving the notebook to their desktop and taking care of that themselves.
  This, however, requires the users to take all the necessary steps.
  It may be possible to make a Jupyter plugin (if this does not already exist), that allows for a one-click save-and-version of a notebook to a (private?) repository.

  In addition, where possible, scripts and data should be tied together, as far as versioning goes.
  Generally, this is implicit by use of file names of the data sets in the relevant scripts, which tend to be unique across different variables, slices or versions.


### Potential system configurations

#### Kubernetes

The default system configuration for BinderHub is a Kubernetes system: multiple pods, each pod with a specific Docker container for a specific user.
The Docker container is created with the `repo2docker`.

The advantage of this system is that it scales really simple, using the scaling capabilities and administration of Kubernetes.
The disadvantage is communication between pods.
Usually, this is not an issue, because the pods (and thus Docker containers and their users) should be able to work in isolation.
Given some of issues (requirements, really) listed before, however, direct communication between pods and containers may be required: read-only access to share data and scripts between different users, read-only access for (permanent) data on the server, read-and-write access for intermediate data.
Usually, such data access is through network protocol: http is the standard protocol between BinderHub and JupyterHub, for example.
Solutions for data access on a Kubernetes system exist, often through a specialized data store (like S3).
This, however, may be slow or generally inconvenient, especially in the case of transferring many or large files.

#### Single (virtual) machine, many containers

Using a single machine would allow for use of the usual Unix-style permissions: user, group and world read, write and execute.
This, however, would lose the possibility of running separate containers for each user.
The containers provide some safety of users impacting the system, as well as the option of creating a completely independent and specialized  environment for each user to work in.

It would still be possible to use BinderHub on this sytem: BinderHub would fire up a Docker container (with help of `repo2docker`) for each user that logs in.
The containers could then have optional connections (mounts) to the local file system, which makes local data access possible.
User data storage, for example a specific `/home/` directory, should also be possible, if users are logged in using accounts on the local system.
For the user storage to work, users should then write their files to a special directory inside their container, which connects to this home directory on the local system.

This would allow the full possibilities of a Unix-like system, including management of users, such as data use limitations (for example, maximum allowed storage in their home directory).



### Caveats with notebooks

Notebooks are not ideal for every situation.
In particular, cells can be executed out of order, causing state problems later in the notebook, and impeding reproducibility.
Tools are (slowly) being developed to help avoid this issue, but it is largely in the developer's and user's hands to use a notebook in order.
"Plain" programs (programs and scripts executed directly on the command line) do not have this issue.

Notebooks are not ideal for writing (and using) larger pieces of code that need to stick together, such as classes with several methods: such a class would have to be written inside one (large) cell.
Such pieces of code should be moved into their own module or package, and imported in the notebook.
This could be done using the binder system, where local code in a repository are added in addition to generic libraries and packages.
This, however, requires user's expertise which may not be available, or an effort that users may not be willing to make.

If the notebook interface is closed (that is, the browser page is closed), execution of a currently running cell will still continue, but the output will not be available; even when re-attaching to the notebook.
Thus, users have to learn to save all outputs from longer running task to a file *in the container image* (not to their local disk), and retrieve that later.
While this is similar to running a long-running job on, for example, a specialized cluster or high-performance machine, it may be somewhat unexpected in a notebook, where output is usually directly in the notebook.

For the above scenarios, using a plain program in a notebook Lab environment may be better: this program could be edited online (with the caveat that this editor is likely far from a user's favorite editor), and run on the command line provided by the lab terminal.
A Lab environment may also allow to combine several scripts in, for example, a bash script, so that a set of simple, task-specific, scripts can be run in a chain on the command line.
Since notebooks have not been set out for this task, it remains yet to be seen how well this workflow really works.
