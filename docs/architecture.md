# Architecture

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
