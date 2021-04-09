from collections import deque
class MyQueue:
    def __init__(self, maxsize):
        self.queue = deque([0]*maxsize)






    def EnQueue(self, data):
        self.queue.popleft()
        self.queue.append(data)

    def getQueue(self):
        return self.queue