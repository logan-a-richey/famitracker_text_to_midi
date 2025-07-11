# echo_buffer.py

class EchoBuffer:
    def __init__(self):
        self.lst = []
        self.max_size = 4

    def peek(self, index: int) -> any:
        if len(self.lst) == 0:
            return None

        if index >= 0 and index <= len(self.lst) - 1:
            return self.lst[index]
        return self.lst[-1]

    def push_front(self, item: any) -> None:
        self.lst.insert(0, item)
        if len(self.lst) > self.max_size:
            self.lst.pop()