"""
This is the main driver code to showcase everything
in this project. This includes:
    * Using insurance calculations to determine pricing
    * Determining a best scheduling algorithm
    * Simulating business growth with Monte-Carlo
"""

# Change these constants to change experiment behavior
NUM_SCHEDULING_EXPERIMENTS = 100
NUM_SCHEDULING_ORDERS = 500

NUM_MONTECARLO_EXPERIMENTS = 500

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    from userConfigs import getUserData, Part, Order, Filament
    from insurance import getInsurancePremium
    from scheduling import FCFS_Scheduler, SJF_Scheduler, RR_Scheduler
    from monteCarlo import monte_carlo

    # Read user config from file
    print("Loading User Data...")

    data = getUserData()

    print("Done!\n")

    # Determine insurance price
    print("Determining Insurance Premium\n")

    # we'll keep a collection just so the parts don't get
    # garbage collected
    parts = []

    ppm = data['Filament Price'] / data['Meters Per Spool']

    for part in data['Parts']:
        basePrice = part['Filament Used'] * ppm
        profit = basePrice + (basePrice * data['Profit Margin'])
        print(f"{part['Name']}'s price before insurance: ${round(profit, 2)}")

        partsPerPrint = part['Parts Per Day']
        printFail = data['Probabilities']['Print Failure']
        allFail = printFail * data['Probabilities']['Other Failure']

        # calculate insured price
        insuredPrice = profit + getInsurancePremium(
                profit,
                partsPerPrint,
                printFail,
                allFail
                )

        print(f"{part['Name']}'s price after insurance:\
 ${round(insuredPrice, 2)}")

        parts.append(Part(
            part['Name'],
            part['Filament Used'],
            part['Parts Per Day'],
            insuredPrice
            ))
        print('\n')

    print("Insurance Calculations Finished\n")

    # determine best scheduling algorithm for turnaround time
    print("Determining Best Scheduler...\n")

    avgs = {
            "First Come First Serve": [],
            "Shortest Job First": [],
            "Round Robin (time quantum = 1 day)": [],
            "Round Robin (time quantum = 2 days)": [],
            "Round Robin (time quantum = 3 days)": [],
            "Round Robin (time quantum = 4 days)": [],
            "Round Robin (time quantum = 5 days)": [],
            }

    for _ in range(NUM_SCHEDULING_EXPERIMENTS):
        schedulers = {
                "First Come First Serve": FCFS_Scheduler(),
                "Shortest Job First": SJF_Scheduler(),
                "Round Robin (time quantum = 1 day)": RR_Scheduler(quantum=1),
                "Round Robin (time quantum = 2 days)": RR_Scheduler(quantum=2),
                "Round Robin (time quantum = 3 days)": RR_Scheduler(quantum=3),
                "Round Robin (time quantum = 4 days)": RR_Scheduler(quantum=4),
                "Round Robin (time quantum = 5 days)": RR_Scheduler(quantum=5),
                }

        for _ in range(NUM_SCHEDULING_ORDERS):
            order = Order.genRandomOrder()
            for s in schedulers.values():
                s.addOrder(order)

        keepGoing = True
        while keepGoing:
            keepGoing = False
            for s in schedulers.values():
                s.update()
                if s.hasOrders():
                    keepGoing = True

        for s in schedulers.keys():
            avgs[s].append(schedulers[s].avgTurnaround())

    print("Average Turnaround Times:")
    for a in avgs.keys():
        print(f"{a}: {round(sum(avgs[a])/len(avgs[a]), 5)} days")

    print("\nScheduling Calculations Complete")

    # simulate business venture
    print("\n\nCalculating Simulations for 365 Days' Worth of Business\n")

    incomes = []
    expenses = []
    for _ in range(NUM_MONTECARLO_EXPERIMENTS):
        # make a new scheduler for the simulation
        bestSched = min(avgs, key=lambda x: avgs[x])
        schedulers = {
                "First Come First Serve": FCFS_Scheduler(),
                "Shortest Job First": SJF_Scheduler(),
                "Round Robin (time quantum = 1 day)": RR_Scheduler(quantum=1),
                "Round Robin (time quantum = 2 days)": RR_Scheduler(quantum=2),
                "Round Robin (time quantum = 3 days)": RR_Scheduler(quantum=3),
                "Round Robin (time quantum = 4 days)": RR_Scheduler(quantum=4),
                "Round Robin (time quantum = 5 days)": RR_Scheduler(quantum=5),
                }
        newSched = schedulers[bestSched]

        filament = Filament(
                data['Filament Price'],
                data['Meters Per Spool']
                )

        sim = monte_carlo(
                data['Probabilities']['Sales Mean'],
                data['Probabilities']['Sales Stddev'],
                data['Power Cost'],
                newSched,
                filament,
                data['Probabilities']['Print Failure'],
                data['Probabilities']['Other Failure']
                )

        plt.plot(sim[0])
        incomes.append(sim[1])
        expenses.append(sim[2])

    avgIncomePaths = [sum(x) for x in incomes]
    avgIncome = sum(avgIncomePaths)/len(avgIncomePaths)

    avgExpensePaths = [sum(x) for x in expenses]
    avgExpense = sum(avgExpensePaths)/len(avgExpensePaths)

    print(f"Average Income: {round(avgIncome, 2)}")
    print(f"Average Expenses: {round(avgExpense, 2)}")

    profit = [avgIncomePaths[x] - avgExpensePaths[x] for x in
              range(len(avgIncomePaths))]
    avgProfit = sum(profit)/len(profit)
    profitPercent = avgProfit / (avgProfit + avgExpense)

    print(f"Average Profit: {round(avgProfit, 2)} ({profitPercent * 100}%)")

    plt.show()

    print("\nComplete!")
