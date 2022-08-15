from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, LoginForm
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Hi {username}! Your account has been created. You are now able to log in.')
            return redirect('login')

    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.method == 'POST':
        l_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'Welcome {username}.')
            return redirect('sportsbook-nba')
        else:
            messages.error(
                request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    else:
        l_form = LoginForm()

    context = {
        'form': l_form
    }
    return render(request, 'users/login.html', context)

#
# @login_required
# def profile(request):
#
#     num_checks = 0
#     if request.user.is_staff:
#         num_checks = User.objects.get(username=request.user.username).profile.num_checks
#         print(num_checks)
#
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         # p_form = ProfileUpdateForm(
#         #     request.POST, request.FILES, instance=request.user.profile)
#
#         if u_form.is_valid():
#             u_form.save()
#             # p_form.save()
#             messages.success(
#                 request, f'Your account has been updated.')
#             return redirect('profile')
#
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         # p_form = ProfileUpdateForm(instance=request.user.profile)
#
#     context = {
#         'num_checks': num_checks,
#         'u_form': u_form,
#         # 'p_form': p_form
#     }
#
#     return render(request, 'users/profile.html', context)