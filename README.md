# Printing Money

This project is the final project for my CS5060 Algorithms in Uncertainty class. It covers several different uncertainty algorithms.
The purpose of this project is to apply these uncertainty algorithms to a small 3D printing business, such as one run on
Etsy, Shopify, or maybe even Shapeways.

## How to Run

The files all use the `config.yaml` file that is in the `src/` directory. So, it is suggested that everything is run from the
`src/` directory.

The `config.yaml` file contains parameters to change at your discretion. This includes all sorts of things, including probabilities,
filament statistics, and part information.

Each file can be run individually (except for `userConfigs.py`). In order to run all of the algorithms together, use the command
`python3 main.py` from the `src/` directory. This runs the main algorithm from each of the other files.

The `userConfigs.py` file doesn't have any functionality of its own. It only contains several data classes and the data access
function for `configs.yaml`.

## The Algorithms

This project covers 3 uncertainty algorithms:

* Scheduling
* Insurance
* Monte-Carlo Simulation

### Scheduling

The first algorithm utilized is scheduling. Typically, scheduling algorithms are applied to running CPU processes. In this project,
the same algorithms are utilized, but it uses orders as an input instead of processes. `scheduling.py` contains the algorithms for
scheduling. This file covers 3 specific scheduling algorithms: First Come First Serve, Shortest Job First, and Round Robin. For this
application, it was found that Shortest Job First is the best by a fair margin. This makes sense, since it is one of the algorithms
that guarantees shortest average turnaround time, which is the main desirable for scheduling orders.

### Insurance

Anyone who has tried their hand at 3D printing knows that it is difficult to get consistent results. Insurance algorithms are a method
that can be used to alleviate the lost potential when a print fails. In this project, we add the insurance into the price of each
print. We do this by insuring each part against the possible odds that a print fails, and against the odds that a failed print leads
to every other print on the bed failing. Adding the insurance in this way adds a pretty large percentage to the original price.

Another way insurance could be done is by using previous experience to determine the exact odds of any print failing in the whole of
projected sales throughout a period of time. Instead of insuring one against just the parts its printed with, this would insure a part
against every print printed througout that period of time. This would lower the cost of insurance and, in turn, lower the overall
price of any printed part.

### Monte-Carlo Simulation

A Monte-Carlo simulation is used to simulate the growth of the 3D printing business throughout the course of the year. This simulation
relies on several variables, including a sales per day median and standard deviation for a normal distribution random variable, and
a random percent chance that a print will fail and one for if all prints fail if a print fails. Each day, the simulation goes through
the following steps:

    * get a number of sales (`normal(salesMean, salesStddev)`)
    * add new orders to scheduler
    * add income for new orders
    * shift sales mean to the right for each new order
    * check if the prints that day fail
    * update the scheduler according to failed prints
    * reduce filament by number of prints that day
    * buy new filament if out

This simulation is not exhaustive by any means, but it showcases the growth possible through this business method. The volatility is
scaled by the shifting of the sales mean, which represents getting more sales as popularity increases, and getting less as the return
time on orders is too long. The function returns a list each for net worth, income, and expenses for each day of the year.
