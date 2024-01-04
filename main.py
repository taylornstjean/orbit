from orbit.core import CelestialObject

if __name__ == "__main__":

    earth = CelestialObject(name="earth", i=0.00005, e=0.01671022, a=1, node_long=-11.26064, peri_long=102.94719, L=100.464, n=0.98564787, epoch="K0011")
    mercury = CelestialObject(name="mercury", i=7.00487, e=0.20563069, a=0.38709893, node_long=48.33167, peri_long=77.45645, L=252.25084, n=4.0923507, epoch="K0011")
    venus = CelestialObject(name="venus", i=3.39471, e=0.00677323, a=0.72333199, node_long=76.68069, peri_long=131.53298, L=181.97973, n=1.602129051, epoch="K0011")
    mars = CelestialObject(name="mars", i=1.85061, e=0.09341233, a=1.52366, node_long=49.57854, peri_long=336.04084, L=355.45332, n=0.524038, epoch="K0011")
    saturn = CelestialObject(name="saturn", i=2.48446, e=0.05415060, a=9.53707032, node_long=113.71504, peri_long=92.43194, L=49.94432, n=0.0334979073, epoch="K0011")
    jupiter = CelestialObject(name="jupiter", i=1.30530, e=0.04839266, a=5.20336301, node_long=100.55615, peri_long=14.75385, L=34.40438, n=0.0831294545, epoch="K0011")
    FO97O01 = CelestialObject(name="FO97O01", i=2.80896, e=0.7756225, a=4.7041536, node_long=301.46745, peri_arg=159.39498, M=359.38340, n=0.09660105, epoch="K23CP")

    earth.plot_params(orbit=True, position=True, color="green", width=3, size=4)
    venus.plot_params(orbit=True, position=True)
    mars.plot_params(orbit=True, position=True)
    mercury.plot_params(orbit=True, position=True)
    saturn.plot_params(orbit=True, position=True)
    jupiter.plot_params(orbit=True, position=True)
    FO97O01.plot_params(orbit=True, position=True, color="red", width=3)

    CelestialObject.plot()
