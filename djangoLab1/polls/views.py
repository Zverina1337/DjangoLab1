from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Question, Choice, Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request,'index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(MyLoginView, self).form_valid(form)

@login_required
def profile(request):
    if request.method == 'GET':
        if not Profile.objects.filter(user=request.user.id).exists():
            print('work')
            profile = Profile()
            profile.user = request.user
            profile.save()

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)


    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    print(request.user.id)
    print(Profile.objects.get(user=request.user.id))
    profileVoted(Profile.objects.get(user=request.user.id))

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('results', args=(question.id,)))


def profileVoted(profile):

    profile.voted = True
    profile.save()

@login_required
def profileDelete(request):
    request.user.delete()
    return render(request, 'users/user_deleted.html')