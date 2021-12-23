from app.models import Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from users.models import Profile

from app.models import DrinkEntry


def getDrinkData(user):
    drinks = DrinkEntry.objects.filter(user=user).order_by("date")
    drinkData = []
    for drink in drinks:
        drinkData.append({
            "beer": drink.drinkType.name,
            "date": drink.date,
            "count": drink.count
        })

    return drinkData


@login_required
def profile(request):
    name = request.GET.get('name', None)

    if name:
        profiles = Profile.objects.filter(name__icontains=name)

        return JsonResponse({
            "profiles": [
                {
                    "pk": profile.user.pk,
                    "name": profile.name,
                    "image": profile.image.url
                } for profile in profiles
            ]
        })

    return JsonResponse({})


@login_required
def _all(request):
    data = {
        "data": getDrinkData(request.user)
    }

    return JsonResponse(data)


# @login_required
# def single(request):
#     fromDate = request.GET.get('fromDate', None)
#     toDate = request.GET.get('toDate', None)

#     if fromDate and toDate:
#         data = {
#             "data": getDrinksOfUser(request.user, fromDate, toDate)
#         }

#         return JsonResponse(data)

#     return JsonResponse({})


@login_required
def group(request, pk):
    group = Group.objects.filter(pk=pk).filter(Q(creator=request.user) | Q(members=request.user)).first()

    if group:
        data = {
            "data": {
                "name": group.name,
                "data": [{
                    "name": group.creator.username,
                    "drinks": getDrinkData(group.creator)
                }] + [{
                    "name": member.username,
                    "drinks": getDrinkData(member)
                } for member in group.members.all()]
            },
            "status": "Success"
        }

    else:
        data = {"status": "Error"}

    return JsonResponse(data)
