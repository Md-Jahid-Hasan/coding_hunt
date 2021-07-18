from django.contrib import admin
from .models import UserOnlineJudge, JudgeName, ProblemDetails, UserSolveProblem,\
    Semester

admin.site.register(UserOnlineJudge)
admin.site.register(JudgeName)
admin.site.register(ProblemDetails)
admin.site.register(UserSolveProblem)
admin.site.register(Semester)
