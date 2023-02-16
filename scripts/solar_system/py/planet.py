from dataclasses import dataclass


@dataclass
class Planet:
    name: str
    type: str
    mass: float
    lengthOfDay: int
    lengthOfYear: int
    averageDistanceToStar: int = 0


earth = Planet("Earth", "Round", 1, 24, 365)
print(earth)
