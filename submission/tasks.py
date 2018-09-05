import os
from celery.task import task

from judge.language import LANGUAGE
from judge.status import ComputingStatus
from submission.constants import SubmissionStatus
from submission.models import Submission
from judge.machine import Machine
from config import settings


def compare(userout, stdout):
    std_lines = stdout.split('\n')
    user_lines = userout.readlines()

    while std_lines and std_lines[-1].replace('\n', '') == '':
        std_lines.pop()

    while user_lines and user_lines[-1].replace('\n', '') == '':
        user_lines.pop()

    if len(std_lines) != len(user_lines):
        return False

    for i in range(len(std_lines)):
        if std_lines[i].strip() != user_lines[i].strip():
            return False

    return True


@task()
def judge(submission_id):
    submission = Submission.objects.get(id=submission_id)
    problem = submission.problem
    test_data_list = problem.testdata_set.all()

    max_time = 15
    max_memory = 200

    os.makedirs('tmp', 0o755, True)
    for test_data in test_data_list:
        prefix = 'judge_%s_%s' % (submission.id, test_data.id)
        src_path = os.path.join(settings.BASE_DIR, 'tmp', '%s_src' % prefix)
        stdin_path = os.path.join(settings.BASE_DIR, 'tmp', '%s_stdin' % prefix)
        output_path = os.path.join(settings.BASE_DIR, 'tmp', '%s_output' % prefix)
        error_path = os.path.join(settings.BASE_DIR, 'tmp', '%s_error' % prefix)

        f = open(stdin_path, mode='w')
        f.write(test_data.input_data)
        f.close()

        f = open(src_path, 'w')
        f.write(submission.code)
        f.close()

        f = open(output_path, 'w')
        f.write('')
        f.close()

        f = open(error_path, 'w')
        f.write('')
        f.close()

        machine = Machine()
        machine.create(
            LANGUAGE.PYTHON,
            src_path=src_path,
            stdin_path=stdin_path,
            output_path=output_path,
            error_path=error_path,
        )
        machine.start()
        data = machine.wait_for_computing()

        if data['status'] == ComputingStatus.ERROR:
            submission.status = SubmissionStatus.SE
            submission.save()
            return

        time_cost = data['cpu_usage']
        memory_cost = data['memory_usage']
        if data['result'] and data['status'] == ComputingStatus.FINISHED:
            start = data['result'].get('start', 0)  # s
            end = data['result'].get('end', 2147483647)  # s
            memory = data['result'].get('memory', 2147483647)  # kbyte

            memory_cost = memory * 1024
            time_cost = (end - start) * 1000
            if memory > 256 * 1024:
                data['status'] = ComputingStatus.MEMORY_LIMIT_EXCEED

            if end - start > 1:
                data['status'] = ComputingStatus.TIME_LIMIT_EXCEED

        if data['status'] == ComputingStatus.TIME_LIMIT_EXCEED:
            submission.status = SubmissionStatus.TLE
            submission.save()
            return

        if data['status'] == ComputingStatus.MEMORY_LIMIT_EXCEED:
            submission.status = SubmissionStatus.MLE
            submission.save()
            return

        if data['status'] == ComputingStatus.FINISHED:
            if not compare(data['output'], test_data.output_data):
                submission.status = SubmissionStatus.WA
                submission.save()
                return

            max_time = max(max_time, time_cost)
            max_memory = max(max_memory, memory_cost)

    submission.time_cost = max_time
    submission.memory_cost = max_memory
    submission.status = SubmissionStatus.AC
    submission.save()
