import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from users.models import FriendList

# from django.core.paginator import Paginator

from app.forms import (DrinkCreateForm, DrinkEntryForm, GroupCreateForm,
                       GroupRenameForm, DrinkEditForm)
from app.models import Drink, DrinkEntry, Group

from .util import getTotal, get7DayAverage, getToday, getMonthTotal


def homepage(request):
    if request.user.is_authenticated:
        return redirect('drinks')

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
            total = [(member, getTotal(DrinkEntry.objects.filter(user=member))) for member in group.members.all()] + \
                [(group.creator, getTotal(DrinkEntry.objects.filter(user=group.creator)))]
            form = GroupRenameForm()

            context = {
                "group": group,
                "creator": True,
                "form": form,
                "users": reversed(sorted(total, key=lambda x: x[1]))
            }

        elif request.user in group.members.all():
            total = [(member, getTotal(DrinkEntry.objects.filter(user=member))) for member in group.members.all()] + \
                [(group.creator, getTotal(DrinkEntry.objects.filter(user=group.creator)))]
            context = {
                "group": group,
                "creator": False,
                "users": reversed(sorted(total, key=lambda x: x[1]))
            }

        else:
            messages.info(request, _("You are not in this group"))
            return redirect('groups')

        return render(request, 'app/group.html', context)

    messages.info(request, _("Group does not exist"))
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

    # Pagination
    # paginator = Paginator(drink_friends | drinks_own, 25)

    # page_number = request.GET.get('page')
    # drinks = paginator.get_page(page_number)

    context = {
        # "page_obj": drinks,
        "drinks": drink_friends | drinks_own,
        "form_drink": form_drink,
        "form": form_beer,
    }

    return render(request, 'app/drinks.html', context)


@login_required
def drink_edit(request, pk):
    drink = Drink.objects.filter(pk=pk).first()

    if drink:
        if drink.creator == request.user:
            form = DrinkEditForm(instance=drink)

            context = {
                "form": form,
                "drink": drink
            }

            return render(request, 'app/drinks/edit.html', context)

        else:
            messages.info(request, _("You cannot edit this drink"))

    else:
        messages.info(request, _("Drink does not exist"))

    return redirect('drinks')


@login_required
def overview(request):
    drinkEntries = DrinkEntry.objects.filter(user=request.user).order_by("date")

    _today = datetime.date.today()
    _yesterday = _today - datetime.timedelta(days=1)

    total = getTotal(drinkEntries)
    today = getToday(drinkEntries, _today)

    mean = get7DayAverage(drinkEntries, _today)
    mean_last = get7DayAverage(drinkEntries, _yesterday)

    month = getMonthTotal(drinkEntries, _today)

    total_average = 0
    if drinkEntries.count() > 0:
        totalDays = (drinkEntries.latest('date').date - drinkEntries.first().date).days
        if totalDays != 0:
            total_average = total / totalDays

    context = {
        "drinkEntries": drinkEntries,
        "total": total,
        "today": today,
        "mean": mean,
        "mean_growth": mean - mean_last,
        "month": month,
        "total_average": total_average
    }

    return render(request, 'app/overview.html', context)
