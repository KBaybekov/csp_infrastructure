local_cluster/
├── ansible.cfg                 # Конфиг Ansible (отключение проверки хостов, путь к inventory)
├── inventory/                  # Динамический или статический инвентарь для Kubespray
│   ├── hosts.ini               # Список серверов (master, worker, etcd) в формате ini
│   └── group_vars/             # Переменные для групп хостов (опционально)
│       └── all.yml
├── kubespray/                  # Git submodule или копия репозитория Kubespray
│   └── ...                     # (все файлы Kubespray, не требуется редактировать)
├── playbooks/
│   ├── 00-prerequisites.yml    # Предварительная настройка серверов (docker, python, ntp)
│   ├── 01-kubespray.yml        # Запуск Kubespray для установки K8s
│   └── 02-prefect-helm.yml     # Установка Helm и чартов Prefect
├── helm/
│   ├── prefect-server-values.yaml   # Настройки сервера Prefect (ресурсы, ingress, БД)
│   ├── prefect-worker-values.yaml   # Настройки worker'а Prefect (пул, образ, лимиты)
│   └── install-prefect.sh           # Скрипт для установки/обновления через Helm
├── scripts/
│   ├── generate-inventory.sh   # (опционально) Генерация inventory из вашего источника
│   └── check-cluster.sh        # Проверка работоспособности кластера
└── README.md                   # Инструкция по запуску
