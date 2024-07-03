from dataclasses import dataclass

@dataclass
class Location:
    location: str
    latitude: float
    longitude: float

    def __hash__(self):
        return hash(self.location)

    def __str__(self):
        return self.location