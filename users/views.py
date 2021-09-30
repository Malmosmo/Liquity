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
        delete = request.GET.get('delete')

        if delete:
            profile = Profile.objects.get(user=request.user)
            profile.delete()

            messages.info(request, "Your account has been deleted!")

            return redirect('logout')

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)

            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                # profile form is also saved because of signals.py
                user_form.save()

                messages.success(
                    request, 'Your account has been updated!')

                return redirect('profile', pk=pk)

        else:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'users/profile.html', context)

    elif request.user in friend_list.friends.all():
        remove = request.GET.get('remove')

        if remove:
            user = User.objects.filter(pk=pk).first()
            friend_list = FriendList.objects.get(user=request.user)

            if user in friend_list.friends.all():
                friend_list.unfriend(user)

                messages.success(request, f"Friend successfully removed!")
                return redirect('friends')

            else:
                messages.info(request, "You are not friends")

        context = {
            "profile_user": user
        }

        return render(request, 'users/profile_friend.html', context)

    else:
        add = request.GET.get('add')

        if add:
            user = User.objects.filter(pk=pk).first()

            if user:

                if FriendRequest.objects.filter(receiver=user, sender=request.user).exists():
                    messages.info(
                        request, "You have already send a friend request")

                elif FriendRequest.objects.filter(receiver=request.user, sender=user).exists():
                    messages.info(
                        request, "The User already send you a request")

                else:
                    FriendRequest.objects.create(
                        receiver=user, sender=request.user)

                    messages.success(
                        request, "successfully send friend request")

                    return redirect('friends')

            else:
                messages.info(request, "User could not be found")

        context = {
            "profile_user": user,
            "profile": Profile.objects.get(user=user)
        }

        return render(request, 'users/profile_stranger.html', context)


@login_required
def friends(request) -> HttpResponse:
    pk = request.GET.get('pk')
    method = request.GET.get('method')

    if pk and method:
        friend_request = FriendRequest.objects.filter(pk=pk).first()

        if friend_request:
            if friend_request.receiver == request.user:
                if method == "accept":
                    friend_request.accept()
                    messages.success(request, f"Accepted Friend Request")

                elif method == "decline":
                    friend_request.decline()
                    messages.info(request, f"Declined Friend Request")

                else:
                    messages.info(request, f"Unknown Method")

            elif friend_request.sender == request.user:
                if method == "cancel":
                    friend_request.cancel()
                    messages.info(request, f"Canceled Friend Request")

            else:
                messages.info(request, f"This is not your friend request")

        else:
            messages.info(request, f"This Friend Request does not exist" +
                          str(method) + str(pk))

        return redirect('friends')

    elif pk:
        user = User.objects.filter(pk=pk).first()

        if user:
            friend_list = FriendList.objects.get(user=request.user)
            if user in friend_list.friends.all():
                friend_list.unfriend(user)

                messages.success(request, f"Friend successfully removed!")
                return redirect('friends')

            else:
                messages.info(request, f"User is not your Friend!")
                return redirect('friends')

        else:
            messages.info(request, f"User does not exist!")
            return redirect('friends')

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

    return render(request, 'users/profile_search.html', context)
