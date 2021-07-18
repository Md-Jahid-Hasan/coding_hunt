from django.urls import path

from . import views
from .api.views import JudgeNameList, JudgeNameDetails, HandleUserOnlineJudge, UserOnlineJudgeDetails, \
    ShowProblemDetails, HandleProblemDetails, UserAddProblem, UserRemoveProblem

app_name = 'acm'

urlpatterns = [
    path('problems/', views.problem_list, name="problem_list"),
    path('problems/<int:problem_id>/users/', views.user_by_problem, name="user_by_problem"),
    path('user/solve/', views.user_by_division, name="user_by_division"),
    path('<int:user_id>/solve/', views.problem_by_user, name="problem_by_user"),

    # URL for API

    path('api/judge_name/', JudgeNameList.as_view(), name="create_list_judgeName"),
    path('api/judge_name/<int:pk>/', JudgeNameDetails.as_view(), name="delete_update_judgeName"),
    path('api/userJudge_name/', HandleUserOnlineJudge.as_view(), name="create_update_userJudgeName"),
    path('api/userJudge_name/<int:pk>/', UserOnlineJudgeDetails.as_view(), name="delete_update_userJudgeName"),
    path('api/all-problem/', ShowProblemDetails.as_view(), name="all_problem_details"),
    path('api/user-add-problem/', UserAddProblem.as_view(), name="all_problem_details"),
    path('api/all-problem/<int:pk>/', HandleProblemDetails.as_view(), name="all_problem_details"),
    path('api/user-remove-problem/<int:pk>/', UserRemoveProblem.as_view(), name="all_problem_details"),
]