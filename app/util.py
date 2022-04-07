import datetime


def filterDrinks(entries, fromDate, toDate):
    return entries.filter(date__range=[fromDate, toDate])


def getTotal(drinks):
    total = 0

    for drink in drinks:
        total += drink.count * drink.volume

    return total


def get7DayAverage(drinks, end=datetime.date.today()):
    start = end - datetime.timedelta(days=7)

    drinks = filterDrinks(drinks, start, end)

    mean = 0

    for drink in drinks:
        mean += drink.count * drink.volume

    return mean / 7


def getToday(drinks, today):
    result = 0
    for entry in drinks:
        if entry.date.date() == today:
            result += entry.count * entry.volume

    return result


def getMonthTotal(drinks, today):
    month_start = datetime.date(today.year, today.month, 1)

    return getTotal(filterDrinks(drinks, month_start, today))
