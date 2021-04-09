class MyQueue:
    def __init__(self, maxsize):
        self.queue = [0] * maxsize




    def EnQueue(self, data):
        self.queue.pop(0)
        self.queue.append(data)

    def getQueue(self):
        return self.queue