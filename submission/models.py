from django.db import models

from problem.models import Problem
from submission.constants import SUBMISSION_STATUS_CHOICE, SubmissionStatus


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.IntegerField(choices=SUBMISSION_STATUS_CHOICE, default=SubmissionStatus.PENDING)
    time_cost = models.IntegerField(null=True, blank=True)  # ms
    memory_cost = models.IntegerField(null=True, blank=True)  # byte
