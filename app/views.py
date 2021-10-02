from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import BeerCreateForm, DrinkForm, GroupCreateForm, GroupRenameForm
from .models import Beer, Drink, Group
from users.models import FriendList
from .util import getMonthTotal, getTotal, getWeekTotal, getYearTotal
import datetime


def homepage(request):
    return render(request, 'app/home.html')


@login_required
def groups(request):
    pk = request.GET.get('pk')

    if pk:
        group = Group.objects.filter(pk=pk).first()

        if group:
            if group.creator == request.user:
                group.delete()

                messages.success(
                    request, "Group successfully deleted")
                # return redirect('groups')

            else:
                messages.info(
                    request, "You are not the creator of this group!")
                # return redirect('groups')

        else:
            messages.info(
                request, "Group does not exist!")

        return redirect('groups')

    elif request.method == 'POST':
        form = GroupCreateForm(request.POST)

        if form.is_valid():
            # Group name
            name = form.cleaned_data.get("name")
            creator = request.user

            if Group.objects.filter(creator=creator, name=name).exists():
                messages.info(
                    request, "You already have created a group with this Name!")

            else:
                Group.objects.create(creator=creator, name=name)
                messages.success(request, "Group successfully created")

        return redirect('groups')

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
        del_pk = request.GET.get('pk')
        add = request.GET.get('add')

        if request.user == group.creator:
            if del_pk:
                user = User.objects.filter(pk=del_pk).first()

                if user:
                    if user in group.members.all():
                        group.members.remove(user)
                        group.save()

                        messages.success(request, "Successfully removed User")
                        return redirect('group-single', pk=pk)

                    else:
                        messages.info(request, "User not in Group")
                        return redirect('group-single', pk=pk)
                else:
                    messages.info(
                        request, "Cannot remove User. User does not exist!")
                    return redirect('group-single', pk=pk)

            if add:
                user_pks = add.split("-")

                fail = False

                for user_pk in user_pks:
                    user = User.objects.filter(pk=user_pk).first()

                    if user:
                        group.members.add(user)
                        group.save()

                    else:
                        fail = True

                if fail:
                    messages.info(request, "Could not add some users")

                else:
                    messages.success(request, "Added all users")

                return redirect('group-single', pk=pk)

            if request.method == 'POST':
                form_rename = GroupRenameForm(request.POST)

                if form_rename.is_valid():
                    name = form_rename.cleaned_data.get("name")
                    creator = request.user

                    if creator == group.creator:
                        group.name = name
                        group.save()

                        messages.success(
                            request, "Group successfully renamed")

                    else:
                        messages.info(
                            request, "Cannot rename group. You are not the creator of this Group")

                else:
                    messages.info(request, "Form is invalid")

                return redirect('group-single', pk=pk)

            form = GroupRenameForm()

            context = {
                "group": group,
                "creator": True,
                "form": form
            }

            return render(request, 'app/group_single.html', context)

        elif request.user in group.members.all():
            if del_pk:
                if int(del_pk) == request.user.pk:
                    group.members.remove(request.user)

                    messages.success(
                        request, f"Successfully left { group.name }")
                    return redirect('groups')

                else:
                    messages.info(
                        request, f"You cannot remove this Users from this group")
                    return redirect('group-single', pk=pk)

            context = {
                "group": group,
                "creator": False
            }

            return render(request, 'app/group_single.html', context)

        else:
            messages.info(request, "You are not in this group!")
            return redirect('groups')

    messages.info(request, "Group does not exist!")
    return redirect('groups')


#####
# Beer stuff
#####

def beers(request):
    # Default Beer
    beers_default = Beer.objects.filter(creator_id=1)

    if request.user.is_authenticated:
        delete_pk = request.GET.get('delete')

        if delete_pk:
            beer = Beer.objects.filter(
                pk=delete_pk, creator=request.user).first()

            if beer:
                beer.delete()
                messages.success(request, "Beer successfully deleted")

            else:
                messages.info(request, "Beer does not exist or was not created by yourself")

        # Own Beer
        beers_own = Beer.objects.filter(creator=request.user)

        # Friends Beer
        friends = FriendList.objects.get(user=request.user).friends.all()
        beers_friends = Beer.objects.filter(creator__in=friends)

        # Forms
        if request.method == 'POST':
            if "beerAdd" in request.POST:
                form = BeerCreateForm(request.POST, request.FILES)

                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.creator = request.user

                    if Beer.objects.filter(name=instance.name).count() == 0:
                        instance.save()

                        messages.success(request, "Successfully added Beer")

                    else:
                        messages.info(request, "Beer already exists with that name")

                else:
                    messages.info(request, request.POST)
                    messages.info(request, form.errors)

            else:
                form = DrinkForm(request.POST)

                if form.is_valid():
                    beer_pk = form.cleaned_data["beer"]
                    count = form.cleaned_data["count"]

                    date = form.cleaned_data["date"]
                    time = form.cleaned_data["time"]

                    dt = datetime.datetime.combine(date, time)
                    beer = Beer.objects.filter(pk=beer_pk).first()

                    if beer:
                        Drink.objects.create(beer=beer, user=request.user, count=count, date=dt)

                        messages.success(request, "Successfully added Drink")

                    else:
                        messages.success(request, "Beer does not exist")

                else:
                    messages.warning(request, request.POST)

            return redirect('beers')

        # Drink Form
        form_drink = DrinkForm(initial={'count': 1, "date": datetime.date.today()})

        # Beer Form
        form_beer = BeerCreateForm()

        context = {
            "beers": beers_friends | beers_default | beers_own,
            "form_drink": form_drink,
            "form": form_beer
        }

    else:
        context = {
            "beers": beers_default
        }

    return render(request, 'app/beers.html', context)


@login_required
def overview(request):
    deleteID = request.GET.get('delete')
    if deleteID:
        Drink.objects.filter(id=deleteID).delete()

        return redirect('overview')

    drinks = Drink.objects.filter(user=request.user).order_by("date")

    context = {
        "drinks": drinks,
        "fromDate": datetime.date(datetime.date.today().year, 1, 1).strftime("%Y-%m-%d"),
        "toDate": datetime.date.today().strftime("%Y-%m-%d"),
        "total": getTotal(drinks),
        "week": getWeekTotal(drinks),
        "month": getMonthTotal(drinks),
        "year": getYearTotal(drinks)
    }

    return render(request, 'app/overview.html', context)
