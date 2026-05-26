from dataclasses import dataclass

@dataclass
class Track:
    TrackId : int
    Name : str
    AlbumId : int
    UnitPrice : float

    def __hash__(self):
        return hash(self.TrackId)

    def __eq__(self, other):
        return self.TrackId == other.TrackId

    def __str__(self):
        return f"Nome: {self.Name} - ({self.TrackId})"