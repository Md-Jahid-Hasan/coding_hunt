from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from user.models import Link

DIVISION = [
    ('B', "Blue"),
    ("G", "Green"),
    ("R", "Red"),
]


class JudgeName(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=50)

    def __str__(self):
        return self.name


class UserOnlineJudge(models.Model):
    name = models.ForeignKey(JudgeName, on_delete=models.CASCADE)
    link = models.URLField(max_length=100)
    user_link = models.ForeignKey(Link, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.name


class ProblemDetails(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=255)
    division = models.CharField(max_length=1, choices=DIVISION)
    user = models.ManyToManyField(get_user_model(), through='UserSolveProblem')

    def __str__(self):
        return self.name + " " + self.division


class UserSolveProblem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    problem = models.ForeignKey(ProblemDetails, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    semester = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.email + " " + self.problem.name

    def clean(self):
        is_add = UserSolveProblem.objects.filter(user=self.user, problem=self.problem).first()
        if is_add:
            raise ValidationError("You add this problem already")


class StudentDivision(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    division = models.CharField(max_length=1, choices=DIVISION)
    semester = models.CharField(max_length=50)


class Semester(models.Model):
    semester = models.CharField(max_length=50)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.semester

    def clean(self):
        print("Clean called")
        if self.is_current:
            current = Semester.objects.filter(is_current=True).first()
            if current:
                raise ValidationError(f"Now {current} semester is running. If {current} semester is end first mark"
                                      f" it as finish")
