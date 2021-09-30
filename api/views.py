from app.models import Group
from app.util import getDrinksOfUser
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from users.models import Profile


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
def single(request):
    fromDate = request.GET.get('fromDate', None)
    toDate = request.GET.get('toDate', None)

    if fromDate and toDate:
        data = {
            "data": getDrinksOfUser(request.user, fromDate, toDate)
        }

        return JsonResponse(data)

    return JsonResponse({})


@login_required
def group(request):
    grouppk = request.GET.get('grouppk')

    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')

    if grouppk:
        group = Group.objects.filter(pk=grouppk).filter(Q(creator=request.user) | Q(
            members=request.user)).first()

        if group:
            data = {
                "data": {
                    "name": group.name,
                    "data": [{
                        "name": group.creator.username,
                        "drinks": getDrinksOfUser(group.creator, fromDate, toDate)
                    }] + [{
                        "name": member.username,
                        "drinks": getDrinksOfUser(member, fromDate, toDate)
                    } for member in group.members.all()]
                },
                "status": "Success"
            }

        else:
            data = {"status": "Error"}

    else:
        data = {"status": "Error"}

    return JsonResponse(data)
