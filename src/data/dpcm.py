# dpcm.py

class DPCM:
    ''' Data type holding DPCM sample information '''

    def __init__(self, 
        _index: int,
        _size: int, 
        _name: str
    ):
        self.index = _index
        self.size = _size 
        self.name = _name

        self.data = []
    
    def __str__(self):
        ''' Make printable type '''
        return "<{}>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()
