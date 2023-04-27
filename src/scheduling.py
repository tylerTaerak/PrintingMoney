"""
My implementation of scheduling algorithms for my final project

- First Come, First Serve (FCFS)
- Shortest Job First (SJF)
- Shortest Time-To-Completion First (STCF)
- Round Robin




I don't think we need to implement priority schedulers, since
we're dealing with user orders, where they would all put their
orders at high priority
- Priority Scheduling
- Earliest Deadline First (EDF)
- Multilevel Queue (MLQ)
- Multilevel Feedback Queue (MLFQ)
"""
import copy
from userConfigs import Order


class Scheduler:
    def __init__(self, copyList=True):
        self.queue = []
        self.copy = copyList
        self.time = 0
        self.reportData = {}
        self.incomingTimes = {}
        self.fulfilled = {}
        self.failedCount = 0

    def addOrder(self,
                 order: Order
                 ) -> None:
        if self.copy:
            order = copy.deepcopy(order)
        self.queue.append(order)
        self.incomingTimes[order] = self.time

    def update(self, empty=False):
        raise NotImplementedError

    def _updateRecursive(self, numParts):
        if len(self.queue) == 0:
            return
        order = self.queue[0]
        order.numParts -= order.part.printsPerDay
        if not order.numParts > 0:
            self.fulfilled[order] = self.time
            self.queue.remove(order)
            self.reportData[self.time].append(f"Order {order.orderId} - \
{order.part.printsPerDay - (-order.numParts)}")
            if len(self.queue) == 0:
                return

            if order.part == self.queue[0].part:
                self._updateRecursive(numParts=-order.numParts)
        else:
            self.reportData[self.time].append(f"Order {order.orderId} - \
{order.part.printsPerDay}")

    def hasOrders(self):
        return bool(len(self.queue))

    def avgTurnaround(self):
        turnaround = []
        for order in self.incomingTimes.keys():
            turnaround.append(self.fulfilled[order] -
                              self.incomingTimes[order])
        return sum(turnaround)/len(turnaround)

    def report(self):
        for i in self.reportData.keys():
            joinedStr = ", ".join(self.reportData[i])
            print(f"Time {i}: {joinedStr}")

        print(f"Average Turnaround Time: {self.avgTurnaround()}")


class FCFS_Scheduler(Scheduler):
    def update(self, partsMissing='none'):
        if len(self.queue) == 0:
            return 0
        self.reportData[self.time] = []
        order = self.queue[0]
        if partsMissing == 'none':
            self.failedCount += min(self.queue[0].part.printsPerDay,
                                    self.queue[0].numParts)
            self._updateRecursive(self.queue[0].part.printsPerDay)
        elif partsMissing == 'one':
            self.failedCount += 1
            self._updateRecursive(self.queue[0].part.printsPerDay-1)
        elif partsMissing == 'all':
            self._updateRecursive(0)
        self.time += 1

        return order.part.printsPerDay * order.part.filamentUsed


class SJF_Scheduler(Scheduler):
    def update(self, partsMissing='none'):
        self.queue.sort(key=lambda x: x.numParts)
        if len(self.queue) == 0:
            return 0
        self.reportData[self.time] = []
        order = self.queue[0]
        if partsMissing == 'none':
            self.failedCount += min(self.queue[0].part.printsPerDay,
                                    self.queue[0].numParts)
            self._updateRecursive(self.queue[0].part.printsPerDay)
        elif partsMissing == 'one':
            self.failedCount += 1
            self._updateRecursive(self.queue[0].part.printsPerDay-1)
        elif partsMissing == 'all':
            self._updateRecursive(0)
        self.time += 1

        return order.part.printsPerDay * order.part.filamentUsed


class RR_Scheduler(Scheduler):
    def __init__(self, copyList=True, quantum=2):
        super().__init__(copyList)
        self.quantum = quantum

    def update(self, partsMissing='none'):
        if len(self.queue) == 0:
            return 0
        if self.time % self.quantum == 0:
            self.queue.append(self.queue[0])
            self.queue.pop(0)
        self.reportData[self.time] = []
        order = self.queue[0]
        if partsMissing == 'none':
            self.failedCount += min(self.queue[0].part.printsPerDay,
                                    self.queue[0].numParts)
            self._updateRecursive(self.queue[0].part.printsPerDay)
        elif partsMissing == 'one':
            self.failedCount += 1
            self._updateRecursive(self.queue[0].part.printsPerDay-1)
        elif partsMissing == 'all':
            self._updateRecursive(0)
        self.time += 1

        return order.part.printsPerDay * order.part.filamentUsed


if __name__ == "__main__":
    numOrders = 50
    schedulers = {
            "FCFS": FCFS_Scheduler(),
            "SJF": SJF_Scheduler(),
            "RR": RR_Scheduler()
            }
    for _ in range(numOrders):
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

    for s in schedulers.values():
        s.report()
        print('\n\n\n')

    for s in schedulers.keys():
        print(f"Avg turnaround time for {s}: {schedulers[s].avgTurnaround()}")
