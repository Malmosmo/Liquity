import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import FriendList

from app.forms import (DrinkCreateForm, DrinkEntryForm, GroupCreateForm, GroupRenameForm)
from app.models import Drink, DrinkEntry, Group

from .util import getMonthTotal, getTotal, getWeekTotal, getYearTotal


def homepage(request):
    return render(request, 'app/home.html')


@login_required
def groups(request):
    groups_own = Group.objects.filter(creator=request.user)
    groups_oth = Group.objects.filter(members=request.user)

    form = GroupCreateForm()

    context = {
        "groups_own": groups_own,
        "groups_oth": groups_oth,
        "form": form
    }

    return render(request, 'app/groups.html', context)


@login_required
def group_single(request, pk):
    group = Group.objects.filter(pk=pk).first()

    if group:
        if request.user == group.creator:
            form = GroupRenameForm()

            context = {
                "group": group,
                "creator": True,
                "form": form
            }

        elif request.user in group.members.all():
            context = {
                "group": group,
                "creator": False
            }

        else:
            messages.info(request, "You are not in this group!")
            return redirect('groups')

        return render(request, 'app/group.html', context)

    messages.info(request, "Group does not exist!")
    return redirect('groups')


###############################################################################################
# Drinks
###############################################################################################
@login_required
def drinks(request):
    # own drinks
    drinks_own = Drink.objects.filter(creator=request.user)

    # Friends drinks
    friends = FriendList.objects.get(user=request.user).friends.all()
    drink_friends = Drink.objects.filter(creator__in=friends)

    # DrinkEntry Form
    form_drink = DrinkEntryForm(initial={'count': 1, "date": datetime.date.today().strftime("%Y-%m-%d")})

    # Drink Form
    form_beer = DrinkCreateForm()

    context = {
        "drinks": drink_friends | drinks_own,
        "form_drink": form_drink,
        "form": form_beer
    }

    return render(request, 'app/drinks.html', context)


@login_required
def overview(request):
    drinkEntries = DrinkEntry.objects.filter(user=request.user).order_by("date")

    context = {
        "drinkEntries": drinkEntries,
        "total": getTotal(drinkEntries),
        "week": getWeekTotal(drinkEntries),
        "month": getMonthTotal(drinkEntries),
        "year": getYearTotal(drinkEntries)
    }

    return render(request, 'app/overview.html', context)
