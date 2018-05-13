from rest_framework import viewsets, pagination, response
from django_filters.rest_framework import DjangoFilterBackend

from submission.models import Submission
from submission.serializers import SubmissionSerializer


class SubmissionPagination(pagination.CursorPagination):
    page_size = 15
    ordering = '-id'


class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission.objects.all().order_by('-id')
    serializer_class = SubmissionSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('problem',)
    pagination_class = SubmissionPagination
