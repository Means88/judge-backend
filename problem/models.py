from django.db import models


class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    picture = models.FileField(blank=True)
    input = models.TextField(blank=True)
    output = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    hint = models.TextField(blank=True)

    def __str__(self):
        return self.title


class TestData(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.TextField()
    output_data = models.TextField()

    def __str__(self):
        return 'data - %s' % self.problem.title
