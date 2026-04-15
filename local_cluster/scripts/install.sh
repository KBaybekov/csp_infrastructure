source .venv/bin/activate # активируем питон >=3.11
pip install ansible-core
git submodule update --init --recursive

ansible-playbook playbooks/01-kubespray.yml -i inventory/inventory.yml

cd ..

git clone https://github.com/kubernetes-sigs/kubespray.git

pip install -r kubespray/requirements.txt

