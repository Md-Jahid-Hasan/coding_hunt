from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import JudgeNameSerializer, UserOnlineJudgeSerializer, ProblemDetailsSerializer, \
    UserSolveProblemSerializer, ProblemSolvedByUsers
from ..models import JudgeName, UserOnlineJudge, ProblemDetails, Semester, UserSolveProblem


class JudgeNameList(generics.ListCreateAPIView):
    serializer_class = JudgeNameSerializer
    queryset = JudgeName.objects.all()


class JudgeNameDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JudgeNameSerializer
    queryset = JudgeName.objects.all()


class HandleUserOnlineJudge(generics.ListCreateAPIView):
    serializer_class = UserOnlineJudgeSerializer
    queryset = UserOnlineJudge.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user_link=self.request.user.link)

    def perform_create(self, serializer):
        serializer.save(user_link=self.request.user.link)


class UserOnlineJudgeDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserOnlineJudgeSerializer
    queryset = UserOnlineJudge.objects.all()


class ShowProblemDetails(generics.ListCreateAPIView):
    serializer_class = ProblemDetailsSerializer
    queryset = ProblemDetails.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProblemSolvedByUsers
        return self.serializer_class


class HandleProblemDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProblemDetailsSerializer
    queryset = ProblemDetails.objects.all()
    permission_classes = (IsAuthenticated, )


class UserAddProblem(generics.CreateAPIView):
    serializer_class = UserSolveProblemSerializer
    queryset = UserSolveProblem.objects.all()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        semester = Semester.objects.get(is_current=True)
        serializer.save(user=self.request.user, semester=semester)


class UserRemoveProblem(generics.DestroyAPIView):
    serializer_class = UserSolveProblemSerializer
    queryset = UserSolveProblem.objects.all()
