from rest_framework import serializers

from submission.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    problem = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ('id', 'problem', 'status', 'time_cost', 'memory_cost')

    def get_problem(self, obj):
        return {
            'id': obj.problem.id,
            'title': obj.problem.title,
        }
