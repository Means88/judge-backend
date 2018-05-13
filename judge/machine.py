import json
import uuid
import os

import docker
import time
from celery.utils.log import get_task_logger
from config import settings

from .language import LANGUAGE
from .status import ComputingStatus

logger = get_task_logger(__name__)


class Machine:
    client = docker.from_env()

    def __init__(self):
        self.container = None
        self.src_path = None
        self.stdout_path = None
        self.output_path = None
        self.start_time = None  # s
        self.time_limit = None  # ms
        self.memory_limit = None  # byte
        self.uuid = str(uuid.uuid4())
        self.temp_file_path = os.path.join(settings.BASE_DIR, 'tmp', self.uuid + '.log')
        f = open(self.temp_file_path, 'w')
        f.write('')
        f.close()
        self.status = ComputingStatus.PENDING

    def create(self, language,
               src_path, stdin_path, output_path, error_path,
               time_limit=1000, memory_limit=256 * 1024 * 1024):

        if self.container:
            raise Exception('Container already exist')

        self.src_path = src_path
        self.output_path = output_path
        self.time_limit = time_limit
        self.memory_limit = memory_limit

        self.container = self.client.containers.create(
            LANGUAGE.get_image_name(language),
            volumes={
                src_path: {'bind': '/judge/{}'.format(LANGUAGE.get_source_name(language)), 'mode': 'ro'},
                stdin_path: {'bind': '/judge/stdin', 'mode': 'ro'},
                # stdout_path: {'bind': '/judge/stdout', 'mode': 'ro'},
                output_path: {'bind': '/judge/userout', 'mode': 'rw'},
                error_path: {'bind': '/judge/usererr', 'mode': 'rw'},
                self.temp_file_path: {'bind': '/judge/return', 'mode': 'rw'}
            },
            mem_limit=int(memory_limit / 0.95),
            memswap_limit=int(memory_limit / 0.95),
            oom_kill_disable=True,
        )

    def start(self):
        self.start_time = time.time()
        self.container.start()

    def stats(self):
        return self.container.stats(decode=True, stream=False)

    def container_status(self):
        self.container.reload()
        return self.container.status

    def _wait_for_computing(self):
        cpu_usage = 0
        memory_usage = 0

        logger.debug('judge machine compute: %s' % self.src_path)
        logger.debug('time_limit: %s', self.time_limit)

        for stats in self.container.stats(decode=True):
            time_used = time.time() - self.start_time
            cpu_usage = max(cpu_usage, time_used / 2 * 1000)
            logger.debug('time_used: %s', time_used)
            logger.debug('cpu_usage: %s', cpu_usage)

            # stats = self.stats()
            logger.debug(json.dumps(stats, indent=2, sort_keys=True))
            if self.container_status() == 'exited':
                self.status = ComputingStatus.FINISHED
                break

            cpu_usage = max(cpu_usage, stats['cpu_stats']['cpu_usage']['total_usage'] / 1e6)
            logger.debug('time_limit : %s' % self.time_limit)
            logger.debug('cpu_usage : %s' % cpu_usage)
            memory_usage = max(memory_usage, stats['memory_stats'].get('max_usage', 0))
            if cpu_usage > self.time_limit:
                self.status = ComputingStatus.TIME_LIMIT_EXCEED
                break

            logger.debug('memory_limit: %s' % self.memory_limit)
            logger.debug('memory_usage: %s' % memory_usage)
            if memory_usage >= self.memory_limit:
                self.status = ComputingStatus.MEMORY_LIMIT_EXCEED
                break

            if time_used > self.time_limit * 2 / 1000:
                self.status = ComputingStatus.TIME_LIMIT_EXCEED
                self.container.stop(timeout=0)
                break

            time.sleep(0.5)

        try:
            result = json.load(open(self.temp_file_path, mode='r'))
        except:
            result = None

        return {
            'status': self.status,
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'output': open(self.output_path, mode='r'),
            'result': result,
        }

    def wait_for_computing(self):
        try:
            return self._wait_for_computing()
        except Exception as e:
            logger.error(e)
            return {
                'status': ComputingStatus.ERROR,
                'cpu_usage': 0,
                'memory_usage': 0,
                'output': None,
                'result': None,
            }
        finally:
            self.destroy()

    def destroy(self):
        if self.container:
            self.container.stop(timeout=0)
            self.container.remove()
            self.container = None
