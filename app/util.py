import datetime


def filterDrinks(entries, fromDate, toDate):
    drinkList = []

    for entry in entries:
        if fromDate <= entry.date.date() <= toDate:
            drinkList.append(entry)

    return drinkList


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


def get7DayAverage(drinks, end=datetime.date.today()):
    start = end - datetime.timedelta(days=7)

    drinks = filterDrinks(drinks, start, end)
    return getAverage(drinks)


def getToday(drinks, today):
    result = 0
    for entry in drinks:
        if entry.date.date() == today:
            result += entry.count * entry.volume

    return result
