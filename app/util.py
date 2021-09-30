import datetime
import calendar

from .models import Drink


def filterDrinks(drinks, fromDate, toDate):
    drinkList = []

    for drink in drinks:
        if fromDate <= drink.date.date() <= toDate:
            drinkList.append(drink)

    return drinkList


def getDrinksOfUser(user, fromDate, toDate):
    drinks = Drink.objects.filter(user=user).order_by("date")

    drinkData = []

    if fromDate and toDate:
        fromDate = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
        toDate = datetime.datetime.strptime(toDate, "%Y-%m-%d").date()

        drinks = filterDrinks(drinks, fromDate, toDate)

    for drink in drinks:
        drinkData.append({
            "beer": drink.beer.name,
            "date": drink.date,
            "count": drink.count
        })

    return drinkData


def getTotal(drinks):
    total = 0

    for drink in drinks:
        total += drink.count

    return total


def getWeekTotal(drinks):
    now = datetime.date.today()
    weekStart = now - datetime.timedelta(days=now.weekday())
    weekEnd = weekStart + datetime.timedelta(days=6)

    drinks = filterDrinks(drinks, weekStart, weekEnd)

    return getTotal(drinks)


def getMonthTotal(drinks):
    now = datetime.date.today()
    monthStart = datetime.date(year=now.year, month=now.month, day=1)
    monthEnd = monthStart + \
        datetime.timedelta(days=calendar.monthrange(now.year, now.month)[1])

    drinks = filterDrinks(drinks, monthStart, monthEnd)

    return getTotal(drinks)


def getYearTotal(drinks):
    now = datetime.date.today()
    yearStart = datetime.date(year=now.year, month=1, day=1)
    yearEnd = datetime.date(year=now.year, month=12, day=31)

    drinks = filterDrinks(drinks, yearStart, yearEnd)

    return getTotal(drinks)


def DEBUG(*args, **kwargs):
    with open(r"C:\Users\Hannes\Documents\Github\Django-Liquity\debug.txt", "a") as file:
        file.write("====\n")

        for arg in args:
            file.write(f"[{datetime.datetime.now()}]: {arg}\n")

        file.write(f"[{datetime.datetime.now()}]: {kwargs}\n")

        file.write("====\n")
