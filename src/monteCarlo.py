"""
This file contains the Monte Carlo simulation
algorithm. Research was quite sparse on what
sort of randomness to expect for sales, so I
guessed. Nearly all parameters are user-
configurable in config.yaml, so anyone with
a better understanding can edit those parameters
to their heart's content
"""
import numpy as np
import matplotlib.pyplot as plt

from userConfigs import Order, Filament, getUserData
from scheduling import Scheduler, SJF_Scheduler


def monte_carlo(
        salesMean: float,
        salesStddev: float,
        dailyExpenses: float,
        scheduler: Scheduler,
        filament: Filament,
        printFail: float,
        allFail: float,
        salesShift: float = 0.005
        ) -> list[float]:
    """
    monte_carlo: a Monte-Carlo simulation which showcases
    possible paths for earnings via a 3D printing business.
    This simulation assumes that the entrepreneur is not
    an industrial giant, and that the business is starting
    from basically nothing. It also assumes that the business
    owner has done their just work in marketing and setting
    up their business well.

    Params
    ------

    salesMean: the mean for the normal distribution of sales
    salesStddev: standard deviation for normal distribution of sales
    dailyExpenses: maintenence costs for running the printer (e.g. power)
    scheduler: type of scheduler for scheduling orders (see scheduling.py)
    printFail: percent chance of a print failing
    allFail: percent chance, given printFail, that all prints fail
    salesShift: how far the salesMean shifts on a day with successful sales

    Returns
    -------

    list[float] containing the value of the business at each day
    """

    T = 365
    dt = 1

    currentValue = 0
    businessGain = [currentValue]
    income = []
    expenses = []
    orders = []

    remainingFilament = filament.size

    while T - dt > 0:
        # find number of sales, normalizing negative values to 0
        numSales = max(int(np.random.normal(salesMean, salesStddev)), 0)

        dailyProfit = -dailyExpenses

        dailyIncome = 0
        dailyExpenditures = dailyExpenses

        for i in range(numSales):
            newOrder = Order.genRandomOrder()
            orders.append(newOrder)
            scheduler.addOrder(newOrder)

            dailyProfit += newOrder.part.price * newOrder.numParts
            dailyIncome += newOrder.part.price * newOrder.numParts

            # the more successful sales, the business may get more publicity
            salesMean += salesShift

        failChance = np.random.uniform()

        # check for part failure
        if failChance < allFail:
            fail = 'all'
        elif failChance < printFail:
            fail = 'one'
        else:
            fail = 'none'

        remainingFilament -= scheduler.update(partsMissing=fail)
        if remainingFilament <= 0:
            dailyProfit -= filament.price
            dailyExpenditures += filament.price
            remainingFilament += filament.size

        # if an order takes too long, sales may tend to dwindle
        for o in orders:
            if o not in scheduler.fulfilled:
                salesMean -= salesShift

        currentValue += dailyProfit

        businessGain.append(currentValue)
        income.append(dailyIncome)
        expenses.append(dailyExpenditures)

        T -= dt

    return businessGain, income, expenses


def main(numIterations=1):
    data = getUserData()

    for i in range(numIterations):
        sim = monte_carlo(
                data['Probabilities']['Sales Mean'],
                data['Probabilities']['Sales Stddev'],
                data['Power Cost'],
                Filament(data['Filament Price'], data['Meters Per Spool']),
                SJF_Scheduler(),
                data['Probabilities']['Print Failure'],
                data['Probabilities']['Other Failure']
                )
        plt.plot(sim)

    plt.show()


if __name__ == "__main__":
    main(numIterations=1)
