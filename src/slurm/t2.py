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
from utils import get_dirs_in_dir, get_fast5_dirs
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

def convert_fast5_to_pod5(fast5_dir:list, sample:str, pod5_name:str, out_dir:str):
    """
    Запуск задачи конвертации fast5 -> pod5 на CPU
    :param fast5_dir: папка с файлами для конвертации
    :param sample: наименование образца
    :param pod5_name: имя выходного файла
    :param out_dir: папка для результатов
    :return: id задачи Slurm
    """

    command = f"pod5 convert fast5 {fast5_dir}*.fast5 --output {out_dir}{sample}.pod5 --threads 256"
    return submit_slurm_job(command, partition="cpu_nodes", job_name=f"convert_{sample}")

def basecalling(sample):
    """Запуск бейсколлинга на GPU"""
    command = f"basecalling /data/pod5/{sample} --output-dir /data/basecall/{sample}"
    return submit_slurm_job(command, partition="gpu_nodes", nodes=1, job_name=f"basecall_{sample}")

def main(in_dir:str):
    sample_dirs = get_dirs_in_dir(dir=in_dir)
    # Create dict with sample_name:[sample_fast5s_dirs] as key:val
    sample_data = {os.path.basename(os.path.normpath(s)):get_fast5_dirs(dir=s) for s in sample_dirs}
    # Create list of samples for iteration
    samples = list(sample_data.keys())
    samples.sort()
    for sample in samples:
        ch_d(sample_data[sample])
        
    # Create list for slurm jobs (each for one type of jobs)
    pending_conversion_jobs = []
    pending_basecalling_jobs = []

    # Loop will proceed until we're out of jobs or samples to process
    while samples or pending_conversion_jobs or pending_basecalling_jobs:
        # Choose sample
        if samples:
            sample = samples.pop(0)
            fast5_dirs = sample_data[sample]
            
            # Start converting to pod5. One subdir per CPU node
            for idx,fast5_d in enumerate(fast5_dirs):
                job_id = convert_fast5_to_pod5(fast5_dir=fast5_d, sample=sample, pod5_name=str(idx), out_dir=out_dir)
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

in_dir = os.path.normpath(os.path.join(sys.argv[1], '/'))
out_dir = os.path.normpath(os.path.join(sys.argv[2], '/'))
ch_d((in_dir, out_dir))

if __name__ == "__main__":
    main(in_dir=in_dir)
