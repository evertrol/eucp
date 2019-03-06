# Use this bind_url when using Nginx as reverse proxy
c.JupyterHub.bind_url = 'http://127.0.0.1:8000'
c.Spawner.default_url = '/lab'

# Bunch of alternative spawners
c.JupyterHub.spawner_class='sudospawner.SudoSpawner'
#c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
#c.JupyterHub.spawner_class = 'dockerspawner.SystemUserSpawner'
#c.JupyterHub.spawner_class = 'systemgroupspawner.SystemGroupSpawner'
# Note: SystemGroupSpawner inherits from SystemUserSpawner, which in its turn
# inherits from DockerSpawner
#c.SystemUserSpawner.environment = {'JUPYTER_ENABLE_LAB': '1', 'GRANT_SUDO': '1'}
#c.SystemUserSpawner.host_homedir_format_string = '/mnt/data/users/{username}'
#c.DockerSpawner.image = '{{ docker_image }}'

# Turn off; minimize non-essential warnings & errors in the logs
c.PAMAuthenticator.open_sessions = False

# https://github.com/jupyterhub/dockerspawner/issues/198#issuecomment-404412344
#from jupyter_client.localinterfaces import public_ips
#c.JupyterHub.hub_ip = public_ips()[0]

# The following three settings are used when running JupyterHub by itself, without a proxy
#c.JupyterHub.bind_url = 'https://{{ servername }}:8088'
#c.JupyterHub.ssl_key = '/etc/letsencrypt/live/{{ servername }}/privkey1.pem'
#c.JupyterHub.ssl_cert = '/etc/letsencrypt/live/{{ servername }}/fullchain1.pem'

# Uncomment the following three debug settings when debugging
#c.Application.log_level = 'DEBUG'
#c.Spawner.debug = True
#c.SystemGroupSpawner.debug = True

# Set the following to True when debugging and testing new images
#c.DockerSpawner.remove = True
