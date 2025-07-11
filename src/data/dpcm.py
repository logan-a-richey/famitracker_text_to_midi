# dpcm.py

class DPCM:
    def __init__(self, 
        index: int,
        size: int, 
        name: str
    ):
        self.index = index
        self.size = size 
        self.name = name

        self.data = []
    
    def __str__(self):
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
