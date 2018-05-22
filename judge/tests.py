from django.test import TestCase

from problem.models import TestData, Problem
from submission.constants import SubmissionStatus
from submission.models import Submission
from submission.tasks import judge


class JudgeTest(TestCase):
    def setUp(self):
        self.problem = Problem.objects.create(title='a+b problem')
        TestData.objects.create(problem=self.problem, input_data='1 2', output_data='3')

    def test_judge_ac(self):
        s = Submission.objects.create(problem=self.problem, code='''
print sum(map(int, raw_input().split(' ')))
        ''')
        judge(s.id)
        s.refresh_from_db()
        self.assertEqual(SubmissionStatus.AC, s.status)

    def test_judge_wa(self):
        s = Submission.objects.create(problem=self.problem, code='print 4')
        judge(s.id)
        s.refresh_from_db()
        self.assertEqual(SubmissionStatus.WA, s.status)

    def test_judge_tle(self):
        s = Submission.objects.create(problem=self.problem, code='''
a = 1
for i in xrange(2147483647):
    a += i

print 3
        ''')
        judge(s.id)
        s.refresh_from_db()
        self.assertEqual(SubmissionStatus.TLE, s.status)

    def test_judge_mle(self):
        s = Submission.objects.create(problem=self.problem, code='''
a = 1
b = range(9999999999)
for i in range(18446744073709551615):
    a += i

print 3
        ''')
        judge(s.id)
        s.refresh_from_db()
        self.assertEqual(SubmissionStatus.MLE, s.status)
