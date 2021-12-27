import datetime

from app.forms import (DrinkCreateForm, DrinkEntryForm, GroupCreateForm,
                       GroupRenameForm)
from app.models import Drink, DrinkEntry, Group

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from users.forms import ProfileUpdateForm, UserUpdateForm
from users.models import FriendList, FriendRequest, Profile, User


##########################################################
# Drinks
##########################################################
@login_required
def drink_create(request):
    form = DrinkCreateForm(request.POST, request.FILES)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.creator = request.user

        if Drink.objects.filter(name=instance.name).count() == 0:
            instance.save()

            messages.success(request, _("Successfully added Drink"))

        else:
            messages.info(request, _("Drink already exists with that name"))

    else:
        # TODO: BOTH??
        messages.info(request, request.POST)
        messages.info(request, form.errors)

    return redirect('drinks')


@login_required
def drink_add(request):
    form = DrinkEntryForm(request.POST)

    if form.is_valid():
        pk = form.cleaned_data["drink"]
        count = form.cleaned_data["count"]

        date = form.cleaned_data["date"]
        volume = form.cleaned_data["volume"]
        time = form.cleaned_data["time"]

        dt = datetime.datetime.combine(date, time)
        drink = Drink.objects.filter(pk=pk).first()

        if drink:
            DrinkEntry.objects.create(drinkType=drink, user=request.user, count=count, date=dt, volume=volume)

            messages.success(request, _("Successfully added Drink"))
        else:
            messages.success(request, _("Drink does not exist"))

    else:
        messages.warning(request, form.errors)

    return redirect('drinks')


# @login_required
# def drink_delete(request):
#     # TODO: function does not work as intendet
#     delete_pk = request.GET.get('delete')

#     if delete_pk:
#         drink = Drink.objects.filter(
#             pk=delete_pk, creator=request.user).first()

#         if drink:
#             drink.delete()
#             # TODO: Translate
#             messages.success(request, "Beer successfully deleted")

#         else:
#             # TODO: Translate
#             messages.info(request, "Beer does not exist or was not created by yourself")

#     return redirect('drinks')


##########################################################
# overview
##########################################################
@login_required
def overview_delete(request, pk):
    DrinkEntry.objects.filter(pk=pk).delete()

    return redirect('overview')


##########################################################
# Groups
##########################################################
@login_required
def groups_delete(request, pk):
    group = Group.objects.filter(pk=pk).first()

    if group:
        if group.creator == request.user:
            group.delete()

            messages.success(request, _("Group successfully deleted"))

        else:
            messages.info(request, _("You are not the creator of this group"))

    else:
        messages.info(request, _("Group does not exist"))

    return redirect('groups')


@login_required
def groups_create(request):
    form = GroupCreateForm(request.POST)

    if form.is_valid():
        # Group name
        name = form.cleaned_data.get("name")

        if Group.objects.filter(creator=request.user, name=name).exists():
            messages.info(request, _("You already have created a group with this Name"))

        else:
            Group.objects.create(creator=request.user, name=name)
            messages.success(request, _("Group successfully created"))

    else:
        messages.info(request, _("Form invalid"))

    return redirect('groups')


##########################################################
# Group Single
##########################################################
@login_required
def group_rename(request, pk):
    group = Group.objects.filter(pk=pk).first()
    form = GroupRenameForm(request.POST)

    if group:
        if form.is_valid():
            name = form.cleaned_data.get("name")

            if request.user == group.creator:
                group.name = name
                group.save()

                messages.success(request, _("Group successfully renamed"))

            else:
                messages.info(request, _("Cannot rename group. You are not the creator of this Group"))

        else:
            messages.info(request, _("Form invalid"))

    else:
        messages.warning(request, _("Group does not exist"))

    return redirect('group-single', pk=pk)


@login_required
def group_user_remove(request, pk, user_pk):
    group = Group.objects.filter(pk=pk).first()

    if group:
        if request.user == group.creator:
            if user_pk:  # TODO: remove
                user = User.objects.filter(pk=user_pk).first()

                if user:
                    if user in group.members.all():
                        group.members.remove(user)
                        group.save()

                        messages.success(request, _("Successfully removed User"))

                    else:
                        messages.info(request, _("User not in Group"))

                else:
                    messages.info(request, _("Cannot remove User. User does not exist"))

            else:
                messages.info(request, _("No user provided to remove"))

        else:
            messages.info(request, _("You are not the creator of this group"))

    else:
        messages.warning(request, _("Group does not exist"))

    return redirect('group-single', pk=pk)


@login_required
def group_leave(request, pk):
    group = Group.objects.filter(pk=pk).first()

    if group:
        if request.user in group.members.all():
            group.members.remove(request.user)

            messages.success(request, _("Successfully left") + f" { group.name }")

        else:
            messages.info(request, _("You are not in this group"))

        return redirect('group-single', pk=pk)

    else:
        messages.info(request, _("Group does not exist"))

    return redirect('groups')


@login_required
def group_user_add(request, pk):
    group = Group.objects.filter(pk=pk).first()

    if group:
        if request.user == group.creator:
            add = request.GET.get('add')
            if add:  # TODO: remove
                user_pks = add.split("_")
                fail = False

                for user_pk in user_pks:
                    user = User.objects.filter(pk=user_pk).first()

                    # TODO: CAUTION... if users does not exist and second condition gets executed
                    if user and not user in group.members.all():
                        group.members.add(user)
                        group.save()

                    else:
                        fail = True

                if fail:
                    messages.info(request, _("Could not add some users"))

                else:
                    messages.success(request, _("Added all users"))

            # else:
            #     messages.info(request, "No Users to add")

        else:
            messages.info(request, _("You cannot add users"))

        return redirect('group-single', pk=pk)

    else:
        messages.info(request, _("Group does not exist"))

    return redirect('groups')


##########################################################
# Profile
##########################################################
@login_required
def profile_delete(request, pk):
    user = User.objects.filter(pk=pk).first()

    if user:
        if request.user == user:
            profile = Profile.objects.get(user=request.user)
            profile.delete()

            messages.info(request, _("Your account has been deleted"))

            return redirect('logout')

        else:
            messages.info(request, _("You cannot delete someones other account"))

    else:
        messages.info(request, _("User does not exist"))

    return redirect("home")


@login_required
def profile_update(request, pk):
    user_form = UserUpdateForm(request.POST, instance=request.user)
    profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
        # profile form is also saved because of signals.py
        user_form.save()

        messages.success(request, _("Your account has been updated"))

    else:
        messages.info(request, _("Form invalid"))

    return redirect("profile", pk=pk)


@login_required
def friend_remove(request, pk):
    user = User.objects.filter(pk=pk).first()
    my_friend_list = FriendList.objects.get(user=request.user)

    if user:
        if user in my_friend_list.friends.all():
            my_friend_list.unfriend(user)

            messages.success(request, _("Friend successfully removed"))

        else:
            messages.info(request, _("You are not friends"))

    else:
        messages.info(request, _("User does not exist"))

    return redirect('friends')


@login_required
def friend_add(request, pk):
    user = User.objects.filter(pk=pk).first()

    if user:
        if FriendRequest.objects.filter(receiver=user, sender=request.user).exists():
            messages.info(request, _("You have already send a friend request"))

        elif FriendRequest.objects.filter(receiver=request.user, sender=user).exists():
            messages.info(request, _("The User already send you a request"))

        else:
            FriendRequest.objects.create(receiver=user, sender=request.user)

            messages.success(request, _("successfully send friend request"))

    else:
        messages.info(request, _("User could not be found"))

    return redirect('friends')


##########################################################
# Friends
##########################################################
@login_required
def friend_rq_accept(request, pk):
    friend_request = FriendRequest.objects.filter(pk=pk).first()

    if friend_request:
        if friend_request.receiver == request.user:
            friend_request.accept()

            messages.success(request, _("Accepted Friend Request"))

        else:
            messages.info(request, _("This friend request is not for you"))

    else:
        messages.info(request, _("No friend request found"))

    return redirect('friends')


@login_required
def friend_rq_decline(request, pk):
    friend_request = FriendRequest.objects.filter(pk=pk).first()

    if friend_request:
        if friend_request.receiver == request.user:
            friend_request.decline()

            messages.success(request, _("Declined Friend Request"))

        else:
            messages.info(request, _("This friend request is not for you"))

    else:
        messages.info(request, _("No friend request found"))

    return redirect('friends')


@login_required
def friend_rq_cancel(request, pk):
    friend_request = FriendRequest.objects.filter(pk=pk).first()

    if friend_request:
        if friend_request.sender == request.user:
            friend_request.cancel()

            messages.success(request, _("Canceled Friend Request"))

        else:
            messages.info(request, _("This friend request is not from you"))

    else:
        messages.info(request, _("No friend request found"))

    return redirect('friends')
