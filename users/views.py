from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import FriendList, FriendRequest, Profile


def register(request) -> HttpResponse:
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request, 'Your account has been created! You are now able to log in!')

            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def profile(request, pk: int) -> HttpResponse:
    user = User.objects.filter(pk=pk).first()

    if not user:
        messages.info(request, "User does not exist")
        return redirect('home')

    friend_list = FriendList.objects.get(user=user)

    if request.user == user:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'users/profile.html', context)

    elif request.user in friend_list.friends.all():
        context = {
            "profile_user": user
        }

        return render(request, 'users/profile/friend.html', context)

    else:
        context = {
            "profile_user": user,
            "profile": Profile.objects.get(user=user)
        }

        return render(request, 'users/profile/stranger.html', context)


@login_required
def friends(request) -> HttpResponse:
    friend_list = FriendList.objects.get(user=request.user)

    incoming = FriendRequest.objects.filter(receiver=request.user)
    outgoing = FriendRequest.objects.filter(sender=request.user)

    context = {
        "friends": friend_list.friends.all(),
        "incoming": incoming,
        "outgoing": outgoing
    }

    return render(request, 'users/friends.html', context)


@login_required
def password_change(request) -> HttpResponse:
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')

            return redirect('profile', pk=request.user.pk)

        else:
            messages.error(request, form.errors)

    form = PasswordChangeForm(request.user)

    context = {
        "form": form
    }

    return render(request, 'users/password_change.html', context)


@login_required
def search(request) -> HttpResponse:
    name = request.GET.get('name')
    profiles = []

    if name:
        profiles = Profile.objects.filter(name__icontains=name)

    else:
        name = ""

    context = {
        "profiles": profiles,
        "name": name
    }

    return render(request, 'users/search.html', context)
