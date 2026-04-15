sudo apt install git

pip install ansible-core

ansible-playbook playbooks/00-prerequisites.yml -i inventory/inventory.yml

cd ..

git clone https://github.com/kubernetes-sigs/kubespray.git

pip install -r kubespray/requirements.txt