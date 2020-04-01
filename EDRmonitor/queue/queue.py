class Q:
    def __init__(self, maxsize=10):
        self.q = []
        self.maxsize = maxsize

    def enqueue(self, val):
        self.q.append(val)
        if len(self.q) > self.maxsize:
            self.q.pop(0)

    def dequeue(self):
        if len(self.q) == 0:
            raise IndexError("Queue is empty")
        return self.q.pop(0)

    def peek(self):
        if len(self.q) == 0:
            raise IndexError("Queue is empty")
        return self.q[0]

    @property
    def len(self):
        return len(self.q)

    def tolist(self):
        return self.q