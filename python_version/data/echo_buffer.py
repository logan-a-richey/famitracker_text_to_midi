# echo_buffer.py

class EchoBuffer:
    ''' 
    FIFO structure to contain token strings for EchoBuffer memoization 
    Contains methods `peek` and `push_front` for element access.
    In FamiTracker, the max size of an echo buffer is 4.

    Example:
    4 3 2 1         # contains 4 elements
    push_front(5)   # add a new element
    5 4 3 2         # (element '1' has been popped since it is the oldest element)
    '''

    def __init__(self):
        self.lst = []
        self.max_size = 4

    def peek(self, index: int) -> any:
        ''' Returns the item at a specified index. '''

        # if there are no times in the list, return None type
        if len(self.lst) == 0:
            return None

        # if the index is in the list, return that element
        if index >= 0 and index <= len(self.lst) - 1:
            return self.lst[index]
        
        # if the index is not in the list, but the list contains elements, return the last element
        return self.lst[-1]

    def push_front(self, item: any) -> None:
        ''' 
        Insert a new element to the front of the Stack. 
        Pop last item if larger than 4. 
        '''
        self.lst.insert(0, item)
        if len(self.lst) > self.max_size:
            self.lst.pop()
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
