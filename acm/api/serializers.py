from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import JudgeName, UserOnlineJudge, UserSolveProblem, ProblemDetails, StudentDivision, Semester


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'name', 'email', 'student_id']


class JudgeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JudgeName
        fields = '__all__'


class UserOnlineJudgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserOnlineJudge
        fields = ['pk', 'name', 'link']


class ProblemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemDetails
        fields = '__all__'


class ProblemSolvedByUsers(ProblemDetailsSerializer):
    user = UserSerializer(many=True)


class UserSolveProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSolveProblem
        fields = ['problem']

    def create(self, validated_data):
        problem = validated_data['problem']
        user = validated_data['user']
        is_add = UserSolveProblem.objects.filter(user=user, problem=problem).first()
        if is_add:
            raise serializers.ValidationError("You add this problem already")
        user_solve = UserSolveProblem(**validated_data)
        user_solve.save()
        return user_solve
