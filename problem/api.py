from urllib.parse import urlsplit, urlunsplit, parse_qs, urlencode
from rest_framework import viewsets, serializers, response, status, pagination
from rest_framework.decorators import action
from problem.models import Problem
from submission.models import Submission
from submission.serializers import SubmissionSerializer
from submission.tasks import judge
from utils.cursor_paginator import cursor_paginate


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def list(self, request, *args, **kwargs):
        return cursor_paginate(self, request, *args, **kwargs)

    @action(detail=True, methods=['POST'])
    def submit(self, request, **kwargs):
        problem = self.get_object()
        code = request.data.get('code', None)
        if code is None:
            return response.Response({}, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(problem=problem, code=code)
        judge.delay(submission.id)
        return response.Response(SubmissionSerializer(submission).data, status=status.HTTP_202_ACCEPTED)
