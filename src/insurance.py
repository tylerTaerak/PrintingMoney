import math
from userConfigs import getUserData


def insurance(
        probabilities: list[float],
        losses: list[int]
        ) -> tuple[float, float]:
    """
    insurance: calculate an insurance premium based on an expected loss and
    taking the standard deviation given probabilities

    Parameters
    ----------
    probabilities: a list of probabilities of each loss event occurring
    losses: a list of losses indexed the same as each probability

    NOTE: probabilities and losses must have the same length

    Returns
    -------
    tuple(float, float): tuple[0] is the expected loss and tuple[1] is
    the standard deviation (or the insurance premium)
    """

    assert len(probabilities) == len(losses)

    expectedLoss = 0
    for i in range(len(probabilities)):
        expectedLoss += probabilities[i] * losses[i]

    # now that we have calculated our expected loss, calculate insurance
    # using the standard deviation
    sigma = 0
    for i in range(len(probabilities)):
        sigma += probabilities[i] * (losses[i] - expectedLoss) ** 2

    sigma = math.sqrt(sigma)

    return expectedLoss, sigma


def getInsurancePremium(
        partPrice: float,
        partsPerPrint: int,
        printFailure: float,
        allFailure: float
        ) -> float:

    lossProbs = [1-printFailure, printFailure - allFailure, allFailure]
    losses = [0, partPrice, partPrice * partsPerPrint]

    return insurance(lossProbs, losses)[1]


def main():
    """
    main: uses user-defined configurations in config.yaml to determine
    final pricing of 3D printed parts by applying the above-defined
    insurance algorithm to the generated price
    """
    data = getUserData()

    # define price per meter
    ppm = data['Filament Price'] / data['Meters Per Spool']

    # define user-defined configuration variables
    for part in data['Parts']:
        # material cost
        basePartPrice = part['Filament Used'] * ppm

        # plus profit margin
        profit = basePartPrice + (basePartPrice * data['Profit Margin'])
        print(f"Price before insurance premium: ${round(profit, 2)}")

        partsPerPrint = part['Parts Per Day']

        printFail = data['Probabilities']['Print Failure']
        allFail = printFail * data['Probabilities']['Other Failure']

        lossProbs = [1-printFail, printFail - allFail, allFail]
        losses = [0, profit, profit * partsPerPrint]

        print(f"Expected loss per print: ${round(insurance(lossProbs, losses)[0], 2)}")
        print(f"Price per print after insurance: ${round(profit + insurance(lossProbs, losses)[1], 2)}")
        print('\n\n')


if __name__ == "__main__":
    main()
