# csp_infrastructure

### Data for creating HPC

### Установка Slurm

 ! Перед установкой на всех машинах необходимо создать пользователей slurm & munge в одноимённых группах, у которых uid & gid будут одинаковы на всех машинах. Для Munge в целях безопасности должно быть отключено логгирование.

 Установка производится с помощью Ansible (ansible/munge_setup.yml & ansible/slurm_build_install.yml), а также файла инвентаря с перечислением узлов будущего кластера:
 ansible-playbook -i inventory.ini `<playbook>`.yml

 Проверка работы узлов производится с помощью:
   sinfo -N -r -l
   srun -N<количество узлов> hostname

!!After downloading nextflow, its deps & worflows for nanopore modify nextflow configs (located in configs). Paths for placing configs are shown in the 1st row of config.

All configs are modified in way of parallel running x4 samples per machine (256 threads, 2 TB RAM).

#### Установка pySlurm

Для работы в Slurm через Python реализован API, обеспечиваемый библиотекой [pyslurm](https://github.com/PySlurm/pyslurm).

Установка:
