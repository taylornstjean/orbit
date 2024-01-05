from orbit.core import CelestialObject, StarSystem

if __name__ == "__main__":

    P21QfuV = CelestialObject(name="P21QfuV", a=1.6980943, e=0.6366116, i=5.61980, node_long=276.25089,
                              peri_arg=85.04585, M=26.23227, n=0.44541145, epoch="K2413")

    solar_system = StarSystem()

    solar_system.include(P21QfuV, color="red", width=3)

    solar_system.include_planet("earth", color="green", width=3, size=4)
    for planet in ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]:
        solar_system.include_planet(planet)

    solar_system.plot()
