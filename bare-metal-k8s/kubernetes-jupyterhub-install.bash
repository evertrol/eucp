#! /bin/bash

# Set up a cluster (this uses the OpenNebula API through a Python interface):
python3 -m pip install oca
python3 create-new-cluster.py 3
# create-new-cluster also updates hosts.ini, ~/.ssh/config and ~/.ssh/known_hosts

# Give the cluster machines some time to really get started and update themselves
sleep 15

# Update intnet_vars.yml, to include the correct control machine IP for the firewall on the controller
clientip=$(ipconfig getifaddr en0)
sed "s/\${clientip}/${clientip}/" intnet_vars_local.yml > intnet_vars.yml

# Run the Ansible playbook to install the necessary software on the nodes, and open the necessary ports in the firewall.
# Turn off confirmation for ssh-ing into unknown hosts
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -i hosts.ini --become --user ubuntu playbook.yml -vv

# nodes are named knode0, knode1 etc in ~/.ssh/config
# Copy the kube config to the local machine:
scp knode0:.kube/config ~/.kube/config

# Install Helm & Tiller: helm-tiller-installation.txt
sh helm-tiller-install.sh

# Create some data dirs persistentvolumes as storage for pods:
# Note: /mnt/data/pv-user created in the ansible playbook
ssh knode2 sudo mkdir /mnt/data/pv-hub
kubectl apply -f storage.yaml


# Create and adjust JupyterHub configuration file: jupyterhub-config.yaml
# Install JupyterHub via Helm: helm-jupyterhub-install.txt
sh helm-jupyterhub-install.sh


# Find the internal IP JupyterHub's proxy-public
pp_internalIP=$(kubectl get svc -n jhub -lapp=jupyterhub,component=proxy-public -o=jsonpath="{.items[0]['spec']['clusterIP']}")

# Substitue this IP into the Nginx default template, copy it over, and restart nginx
sed "s/\${pp_internalIP}/${pp_internalIP}/" nginx_default_template > nginx_default
scp nginx_default knode0:/tmp/nginx_default
ssh knode0 sudo cp /tmp/nginx_default /etc/nginx/sites-available/default
ssh knode0 sudo systemctl restart nginx


frontendip=$(sed -n 's/^node0 ansible_host=\(..*\)$/\1/p' hosts.ini)
echo "Done. Find your JupyterHub at http://controller.eucp-nlesc.surf-hosted.nl or at http://${frontendip}"
