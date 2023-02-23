from dataclasses import dataclass


@dataclass
class Vehicle:
    name: str
    max_speed: int
    mileage: int


car1 = Vehicle("Volvo", 200, 150000)
print(car1)


@dataclass
class Bus(Vehicle):
    color: str


bus1 = Bus("Volkswagen", 100, 5000, "Geel")
print(bus1)
