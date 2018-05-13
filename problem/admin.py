from django.contrib import admin

from problem.models import Problem, TestData


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(TestData)
class TestDataAdmin(admin.ModelAdmin):
    pass
