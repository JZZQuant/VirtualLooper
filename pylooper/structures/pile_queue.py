class Queue(object):
    def __init__(self, max_size=-1):
        self.data = []
        self.head = 0
        self.tail = -1

    def pre_padding(self, data):
        self.data = data + self.data

    def post_padding(self, data):
        self.data = self.data + data

    def put(self, val):
        self.data.append(val)

    def counter(self, addendum=None, back_vol=1):
        self.head = (self.head + 1) % (len(self.data))
        self.tail = self.head - 1
        if addendum is not None:
            self.data[self.tail] = addendum + self.data[self.tail]
            return addendum*back_vol + self.data[self.tail]
        return self.data[self.tail]*back_vol

    def extend_loop(self):
        self.post_padding(self.data)

    def empty(self):
        return len(self.data) == 0

    def slice(self,size):
        self.data=self.data[:size]
        return self

