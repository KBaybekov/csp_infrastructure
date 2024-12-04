#!/usr/bin/env python3

"""
Script searches for sample folders in in_dir, then checks for .fast5 files in fast5_pass subdirectories of sample.
Task queue is created.
After converting all sample's .fast5 files to .pod5 on CPU nodes, basecalling starts on GPU.

Usage: t2.py in_dir
"""
import sys
import os
t = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(t)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import get_samples_in_dir
import pyslurm
import time


def ch_d(d):
    print(d)
    exit()



def submit_slurm_job(command, partition, nodes=1, job_name="slurm_job"):
    """Отправка задачи в SLURM через pyslurm"""
    job = {
        "job_name": job_name,
        "partition": partition,
        "command": command,
        "ntasks": 1,
        "nodes": nodes,
        "output": f"/tmp/{job_name}_%j.out"
    }
    job_id = pyslurm.job().submit_batch_job(job)
    print(f"Job {job_name} submitted with ID {job_id}")
    return job_id

def is_slurm_job_running(job_id):
    """Проверка статуса задачи через pyslurm"""
    job_info = pyslurm.job().find_id(job_id)
    if job_info:
        state = job_info.get('job_state', 'UNKNOWN')
        print(f"Job {job_id} state: {state}")
        return state in ['RUNNING', 'PENDING']
    return False

def get_idle_nodes(partition_name):
    """Получение списка простаивающих узлов"""
    nodes = pyslurm.node().get()
    idle_nodes = [node for node, data in nodes.items() if data['state'] == 'IDLE' and partition_name in data['partitions']]
    return idle_nodes

def convert_fast5_to_pod5(fast5_files, sample):
    """Запуск задачи конвертации fast5 -> pod5 на CPU"""
    command = f"convert_fast5_to_pod5 {fast5_files} --output-dir /data/pod5/{sample}"
    return submit_slurm_job(command, partition="cpu_nodes", job_name=f"convert_{sample}")

def basecalling(sample):
    """Запуск бейсколлинга на GPU"""
    command = f"basecalling /data/pod5/{sample} --output-dir /data/basecall/{sample}"
    return submit_slurm_job(command, partition="gpu_nodes", nodes=1, job_name=f"basecall_{sample}")

def main(in_dir:str):
    samples = get_samples_in_dir(dir=in_dir, extensions=('/'))
    ch_d(samples)
    pending_conversion_jobs = []
    pending_basecalling_jobs = []

    while samples or pending_conversion_jobs or pending_basecalling_jobs:
        # Step 2: Выбираем образец
        if samples:
            sample = samples.pop(0)
            fast5_files = get_fast5_files(sample)
            
            # Step 4: Конвертируем fast5 -> pod5
            job_id = convert_fast5_to_pod5(fast5_files, sample)
            pending_conversion_jobs.append((job_id, sample))
        
        # Check conversion jobs
        for job_id, sample in list(pending_conversion_jobs):
            if not is_slurm_job_running(job_id):
                pending_conversion_jobs.remove((job_id, sample))
                # Step 5.1.1: Отправляем бейсколлинг на GPU
                job_id = basecalling(sample)
                pending_basecalling_jobs.append((job_id, sample))

        # Check basecalling jobs
        for job_id, sample in list(pending_basecalling_jobs):
            if not is_slurm_job_running(job_id):
                pending_basecalling_jobs.remove((job_id, sample))
        
        # Пауза перед следующей проверкой
        time.sleep(10)

    print("All samples processed.")

in_dir = sys.argv[1]

if __name__ == "__main__":
    main(in_dir=in_dir)
