from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.views.generic.detail import DetailView
from django.forms import formset_factory

from . import models
from . import forms


def login_view(request):
    """Make a user login in the system. If already login redirect to the home"""
    if request.user.is_authenticated:
        return redirect('user:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            error = {'info': "Email Password doesn't match"}
            try:                                                           # Check If user exists
                _ = get_user_model().objects.get(email=email)
            except:
                error['info'] = "User with this email doesn't exists"
            return render(request, 'account/login.html', error)
        login(request, user)
        return redirect('user:home')
    return render(request, 'account/login.html')


def home(request):
    link = models.Link.objects.get(pk=1)
    print(link)
    formset = forms.TestForm(instance=link)
    if request.method == 'POST':
        print("POST")
        formset = forms.TestForm(request.POST, instance=link)
        print(formset)
        if formset.is_valid():
            formset.save()
            print(formset.cleaned_data)
    return render(request, 'home.html', {'formset': formset})


def logout_view(request):
    logout(request)
    return redirect('user:home')


def account_details(request):
    try:
        email = request.session['email']
        new_user = get_user_model().objects.get(email=email)
        is_new = True
    except:
        if request.user.is_anonymous:
            return redirect('user:login')
        new_user = request.user
        is_new = False
    print(is_new)
    user_form = forms.UserProfileUpdateForm(request.POST or None, instance=new_user)
    user_link = forms.LinkForm(request.POST or None, instance=new_user.link)

    if request.method == 'POST':
        if user_form.is_valid() and user_link.is_valid():
            user = user_form.save(is_new=is_new)
            link = user_link.save(commit=False)
            if is_new:
                link.user = user
                link.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['email']
                return redirect('user:home')
            link.save()

    context = {
        'profile': new_user,
        'user_form': user_form,
        'user_link': user_link,
    }

    return render(request, 'account/user_details_update.html', context)


class UserDetailView(DetailView):
    models = get_user_model
    queryset = get_user_model().objects.all()
    template_name = 'account/user_details.html'

    def get_queryset(self):
        print("get queryset")
        return self.queryset.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        link = self.get_object()
        form = forms.TestForm(instance=link.link)
        print("get context")
        data['formset'] = form
        return data

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(UserDetailView, self).get_context_data(**kwargs)
        form = forms.TestForm(request.POST, instance=self.object.link)

        if form.is_valid():
            form.save()

        return self.render_to_response(context)

