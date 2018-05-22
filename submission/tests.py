import json

from django.test import TestCase
from rest_framework.test import APIClient

from problem.models import Problem, TestData
from submission.constants import SubmissionStatus
from submission.models import Submission
from submission.tasks import judge


class SubmissionTest(TestCase):
    def test_submission(self):
        p = Problem.objects.create(title='test')
        c = Submission.objects.count()
        s = Submission.objects.create(problem=p, code='')
        self.assertEqual(1, p.submission_set.count())
        self.assertEqual(SubmissionStatus.PENDING, s.status)

    def test_retrieve(self):
        p = Problem.objects.create(title='retrieve')
        s = Submission.objects.create(problem=p, code='retrieve')
        client = APIClient()
        response = client.get('/api/submission/%s/' % 2147483647)
        self.assertEqual(404, response.status_code)
        response = client.get('/api/submission/%s/' % s.id)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(s.id, data['id'])
        self.assertEqual('retrieve', data['problem']['title'])

    def test_list(self):
        p = Problem.objects.create(title='submission')
        for i in range(100):
            Submission.objects.create(problem=p, code='')

        client = APIClient()
        response = client.get('/api/submission/')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(15, len(data['results']))
        self.assertIsNotNone(data['next'])

    def test_submit(self):
        p = Problem.objects.create(title='submit')
        client = APIClient()
        c = Submission.objects.count()
        response = client.post('/api/problem/%s/submit/' % p.id)
        self.assertEqual(400, response.status_code)
        response = client.post('/api/problem/%s/submit/' % p.id, {'code': 'test'})
        self.assertEqual(202, response.status_code)
        self.assertEqual(c + 1, Submission.objects.count())
        submission = Submission.objects.last()
        self.assertEqual('test', submission.code)

