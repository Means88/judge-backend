import json

from django.test import TestCase
from rest_framework.test import APIClient
from problem.models import Problem, TestData


class ProblemTest(TestCase):
    def test_problem(self):
        count = Problem.objects.count()
        p = Problem.objects.create(title='test')
        self.assertEqual(count + 1, Problem.objects.count())
        self.assertEqual('test', p.title)
        p.title = 'test2'
        p.save()
        p = Problem.objects.get(id=p.id)
        self.assertEqual('test2', p.title)
        p.delete()
        self.assertEqual(count, Problem.objects.count())

    def test_data(self):
        p = Problem.objects.create(title='test')
        data = TestData.objects.create(problem=p, input_data='in', output_data='out')
        self.assertEqual(1, p.testdata_set.count())
        self.assertEqual(data.problem.id, p.id)

    def test_retrieve(self):
        p = Problem.objects.create(title='retrieve')
        client = APIClient()
        response = client.get('/api/problem/%s/' % 2147483647)
        self.assertEqual(404, response.status_code)
        response = client.get('/api/problem/%s/' % p.id)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(p.id, data['id'])
        self.assertEqual('retrieve', data['title'])

    def test_list(self):
        for i in range(100):
            Problem.objects.create(title='title %s' % i)

        client = APIClient()
        response = client.get('/api/problem/')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(Problem.objects.count(), data['count'])
        self.assertEqual(15, len(data['results']))
        self.assertIsNotNone(data['next'])
