import yaml
import numpy as np

with open("config.yaml", 'r') as handle:
    userData = yaml.load(handle, Loader=yaml.Loader)


def getUserData():
    return userData


class Filament:
    def __init__(self,
                 price: float,
                 size: float
                 ):
        self.price = price
        self.size = size


class Part:
    partId = 0
    instances = []

    def __init__(self,
                 name: str,
                 filament: float,
                 howMany: int,
                 price: float
                 ):
        self.name = name
        self.filamentUsed = filament
        self.printsPerDay = howMany
        self.price = price
        self.partId = Part.partId
        Part.partId += 1

        Part.instances.append(self)

    @classmethod
    def userParts(cls):
        return Part.instances

    def __eq__(self, other):
        return self.partId == other.partId

    def __ne__(self, other):
        return self.partId != other.partId

    def __hash__(self):
        return hash(self.partId)


class Order:
    orderId = 0

    def __init__(self,
                 part: Part,
                 numParts: int
                 ):
        self.orderId = Order.orderId
        Order.orderId += 1

        self.part = part
        self.numParts = numParts
        self.fulfilled = False

    @classmethod
    def genRandomOrder(cls):
        parts = Part.userParts()
        return Order(
                np.random.choice(parts),
                max(int(np.random.normal(userData['Probabilities']['Parts Per Order'],
                    userData['Probabilities']['Parts Std Dev'])), 1)
                )

    def __eq__(self, other):
        return self.orderId == other.orderId

    def __ne__(self, other):
        return self.orderId != other.orderId

    def __hash__(self):
        return hash(self.orderId)
