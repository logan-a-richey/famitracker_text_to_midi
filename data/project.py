
class Project:
    def __init__(self):
        self.title = ""
        self.author = ""
        self.copyright = ""
        self.comment = ""
        
        self.machine = 0
        self.framerate= 0
        self.expansion= 0
        self.vibrato = 1
        self.split = 32
        self.n163channels = 0

        self.dpcm = {}
        self.grooves = {}
        self.usegroove = []
        self.macros = {}
        self.instruments = {}
        self.tracks = []

    def show(self):
        out = ""
        divider = "{}\n".format("*" * 80)

        out += "Project Data:\n"
        out += divider
        out += "--- Song Information ---\n"
        out += "{}\n".format(self.title)
        out += "{}\n".format(self.author)
        out += "{}\n".format(self.copyright)
        
        out += divider
        out += "--- Comment ---\n"
        out += "{}\n".format(self.comment)
        
        out += divider
        out += "--- Global Setting ---\n"
        out += "machine: {}\n".format(self.machine)
        out += "framerate: {}\n".format(self.framerate)
        out += "expansion: {}\n".format(self.expansion)
        out += "vibrato: {}\n".format(self.vibrato)
        out += "split: {}\n".format(self.split)
        out += "n163channels: {}\n".format(self.n163channels)
        out += "\n"

        out += divider
        out += "--- DPCM Samples ---\n"
        for sample in self.dpcm:
            out += "Sample {} : {}\n".format(sample.index, sample.name)
        out += "\n"

        out += divider
        out += "--- Grooves ---\n"
        for groove in self.grooves:
            out += "Groove {} : {}\n".format(groove.index, groove.data)
        out += "\n"
        
        out += divider
        out += "--- Tracks Using Default Groove ---\n"
        out += "{}\n".format(self.usegroove)        
        out += "\n"

        out += divider
        out += "--- Macros ---\n"
        for macro in self.macros:
            out += "{} {} : {}\n".format(macro.label, macro.name, macro.sequence)
        out += "\n"

        out += divider
        out += "--- Instruments ---\n"
        for inst in self.instruments:
            out += "{} : {}\n".format(inst.index, inst.name) 
        out += "\n"

        out += divider
        out += "--- Tracks ---"
        for track in self.tracks:
            out += "Track {} : {}\n".format(track.index, track.name)
        out += "\n"
        