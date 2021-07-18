from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from . import models

"""get_user_model().objects.all().annotate(
    g=Count('problemdetails', filter=Q(problemdetails__division="G")),
    b=Count('problemdetails', filter=Q(problemdetails__division="B")),
    r=Count('problemdetails', filter=Q(problemdetails__division="R"))
)"""


def problem_list(request):
    """division = 'B'
    semesters = models.UserSolveProblem.objects.distinct('semester')
    problems = models.ProblemDetails.objects.all(). \
        annotate(user_solved=Count('user'),
                 semester_solved=Count('user', filter=Q(usersolveproblem__semester="Summer 2021")))"""
    try:
        semester = models.Semester.objects.get(is_current=True)
    except:
        return HttpResponse("There is no running semester")

    green_division = models.ProblemDetails.objects.filter(division="G"). \
        annotate(user_solved=Count('user'),
                 semester_solved=Count('user', filter=Q(usersolveproblem__semester=semester)))

    red_division = models.ProblemDetails.objects.filter(division="R"). \
        annotate(user_solved=Count('user'),
                 semester_solved=Count('user', filter=Q(usersolveproblem__semester=semester)))

    blue_division = models.ProblemDetails.objects.filter(division="B"). \
        annotate(user_solved=Count('user'),
                 semester_solved=Count('user', filter=Q(usersolveproblem__semester=semester)))

    context = {
        'green': green_division, 'blue': blue_division,
        'red': red_division

    }
    return render(request, 'acm/problem_list.html', context)


def user_by_problem(request, problem_id):
    problem = models.ProblemDetails.objects.get(id=problem_id)
    users = problem.user.all()
    context = {
        'users': users,
        'problem': problem
    }
    return render(request, 'acm/user_solved.html', context)


def user_by_division(request, semester=None):
    if not semester:
        try:
            semester = models.Semester.objects.get(is_current=True)
        except:
            return HttpResponse("There is no running semester")

    green_user = get_user_model().objects.filter(problemdetails__division="G", usersolveproblem__semester=semester). \
        annotate(total_solve=Count('usersolveproblem')).order_by('-total_solve')
    blue_user = get_user_model().objects.filter(problemdetails__division="B", usersolveproblem__semester=semester). \
        annotate(total_solve=Count('usersolveproblem')).order_by('-total_solve')
    red_user = get_user_model().objects.filter(problemdetails__division="R", usersolveproblem__semester=semester). \
        annotate(total_solve=Count('usersolveproblem')).order_by('-total_solve')

    if request.method == "POST":
        print("POsted")
        number = request.POST.get('number')
        condition = request.POST.get('condition')
        division = request.POST.get('division')
        if condition == "gt":
            if division == "G":
                green_user = green_user.filter(total_solve__gt=number)
            elif division == "B":
                blue_user = blue_user.filter(total_solve__gt=number)
            elif division == "R":
                red_user = red_user.filter(total_solve__gt=number)

        elif condition == 'lt':
            if division == "G":
                green_user = green_user.filter(total_solve__lt=number)
            elif division == "B":
                blue_user = blue_user.filter(total_solve__lt=number)
            elif division == "R":
                red_user = red_user.filter(total_solve__lt=number)

    green_user = green_user.filter(total_solve__gte=0)
    context = {
        'green_user': green_user,
        'blue_user': blue_user,
        'red_user': red_user
    }
    return render(request, 'acm/user_solved_by_division.html', context)


def problem_by_user(request, user_id):
    problems = models.UserSolveProblem.objects.filter(user=user_id).prefetch_related('problem').\
        order_by('problem__division')
    context = {'problems': problems}
    return render(request, 'acm/user_solved_problem.html', context)
