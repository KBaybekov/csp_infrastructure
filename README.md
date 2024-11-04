# csp_infrastructure
 Data for creating HPC
 Установка
 ! Перед установкой на всех машинах необходимо создать пользователей slurm & munge в одноимённых группах, у которых uid & gid будут одинаковы на всех машинах. Для Munge в целях безопасности должно быть отключено логгирование.
 
 Установка производится с помощью Ansible (ansible/munge_setup.yml & ansible/slurm_build_install.yml), а также файла инвентаря с перечислением узлов будущего кластера:
 ansible-playbook -i inventory.ini <playbook>.yml

 Проверка работы узлов производится с помощью:
   sinfo -N -r -l
   srun -N<количество узлов> hostname
