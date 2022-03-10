import datetime
import calendar
from unittest import result

from .models import DrinkEntry


def filterDrinks(entries, fromDate, toDate):
    drinkList = []

    for entry in entries:
        if fromDate <= entry.date.date() <= toDate:
            drinkList.append(entry)

    return drinkList


# def getDrinksOfUser(user, fromDate, toDate):
#     drinkEntries = DrinkEntry.objects.filter(user=user).order_by("date")
#     drinkData = []

#     if fromDate and toDate:
#         fromDate = datetime.datetime.strptime(fromDate, "%Y-%m-%d").date()
#         toDate = datetime.datetime.strptime(toDate, "%Y-%m-%d").date()

#         drinks = filterDrinks(drinkEntries, fromDate, toDate)

#     for drink in drinks:
#         drinkData.append({
#             "drink": drink.drink.name,
#             "date": drink.date,
#             "count": drink.count
#         })

#     return drinkData


def getTotal(drinks):
    total = 0

    for drink in drinks:
        total += drink.count * drink.volume

    return total


def getAverage(drinks):
    mean = 0

    for drink in drinks:
        mean += drink.count * drink.volume

    return mean / 7


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


def get7DayAverage(drinks, end=datetime.date.today()):
    # end = datetime.date.today()
    # end = datetime.date(2022, 3, 1)
    start = end - datetime.timedelta(days=7)

    drinks = filterDrinks(drinks, start, end)

    # for drink in drinks:
    #     print(drink.date)

    return getAverage(drinks)


def getToday(drinks, today):
    # today = datetime.date.today()
    # today = datetime.date(2022, 2, 28)
    result = 0
    for entry in drinks:
        if entry.date.date() == today:
            result += entry.count * entry.volume

    return result


# def getPerformance(drinks):
#     mean = get7DayAverage(drinks, datetime.date(2022, 3, 1))
#     mean_1 = get7DayAverage(drinks, datetime.date(2022, 3, 1) - datetime.timedelta(days=3))

#     return (mean - mean_1) / mean


def DEBUG(*args, **kwargs):
    with open(r"C:\Users\Hannes\Documents\Github\Django-Liquity\debug.txt", "a") as file:
        file.write("====\n")

        for arg in args:
            file.write(f"[{datetime.datetime.now()}]: {arg}\n")

        file.write(f"[{datetime.datetime.now()}]: {kwargs}\n")

        file.write("====\n")
