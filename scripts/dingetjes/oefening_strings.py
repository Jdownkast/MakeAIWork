star = "Sun"
planet = "Mercury"
planetAdj = "Mercurian"
homePlanet = "Earth"

print("Since {0} is so much closer to the {1} than \
we are, in the {2} sky the {1} appears three \
times as big as from here on {3}".format(planet, star, planetAdj, homePlanet))

print(f"Since {planet} is so much closer to the {star} than \
we are, in the {planetAdj} sky the {star} appears three \
times as big as from here on {homePlanet}")
    
print("Since %s is so much closer to the %s than \
we are, in the %s sky the %s appears three \
times as big as from here on %s" %(planet, star, planetAdj, star, homePlanet))


object = "kbo"
distanceUnit = "au"
star = "SUN"

print(f"So far, {object.upper()}s have been seen from distances \
ranging from 30{distanceUnit.upper()} to 50{distanceUnit.upper()} \
from the {star.capitalize()} (for reference, Pluto's average orbit \
is at about 39{distanceUnit.upper()}).")