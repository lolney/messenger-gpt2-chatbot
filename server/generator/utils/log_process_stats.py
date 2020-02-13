import os
import psutil
import logging
log = logging.getLogger('app.create_app')


def log_process_stats():
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]/2.**30
    log.info(f'memory use (GB): {memoryUse}')
    log.info(f'cpu use (%): {py.cpu_percent()}')
