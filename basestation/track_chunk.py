from helpers import HexArrayToDecimal
from track_data import TrackData

class TrackChunk(object):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.length = HexArrayToDecimal(raw_data[4:8])
        self.data = TrackData(raw_data[8:])
