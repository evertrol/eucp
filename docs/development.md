# Development

The development of the notebook system will be through use cases and feedback from scientists directly involved in the EUCP project.
This should lead to a development system with rapid fixes and extensions in an iterative procedure.


In a worse-case scenario, the feedback may be such that the suggested system will have to be abandoned and replaced by something else.
On the other hand, the system may work well enough that its can be extended to several other areas of research.
In fact, notebook systems are already developed and used in related areas.

## Technical challenges

There are several technical challenges that need to be solved before this system can be used fully.
Note that these are essentially requirements for a proper EUCP notebook system.

- Binders & notebooks need to be login protected.
  This may be a login arranged by an administrator, but alternatively, this is an external OpenID account.
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

