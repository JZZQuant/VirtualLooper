import copy

class IndexQueue(object):
    def __init__(self):
        self.data=[]
        self.head=0
        self.tail=-1
        self.len=0
        self.extend_flag =False
        self.buffer=[]
        self.buffer_len=0

    def put(self,val):
        self.data.append(val)
        self.len+=1

    def counter(self,addendum=None):
        if self.buffer==[]:
            self.buffer= copy.deepcopy(self.data)
            self.buffer_len = self.len
        self.head=(self.head+1)%self.len
        self.tail=self.head-1
        if self.extend_flag is True and self.head==0:
            self.data = self.data+self.buffer
            self.head +=self.buffer_len
            self.tail +=self.buffer_len
            self.len  +=self.buffer_len
            self.extend_flag =False
            print("doubled loop to length: %d current head at %d" % (self.len,self.head))
        if addendum is not None:
            self.data[self.tail] = addendum + self.data[self.tail]
        return self.data[self.tail]

    def extend_loop(self):
        self.extend_flag=True

    def empty(self):
        return self.len==0


