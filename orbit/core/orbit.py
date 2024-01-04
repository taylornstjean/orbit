import numpy as np
import scipy.special as sp
from datetime import datetime, date, time
from config import char_map
from .renderer import generate_plot


class CelestialObject:

    __plot = {}

    def __init__(self, **kwargs):

        self.__name__ = kwargs.get("name")

        self.i = kwargs.get("i") * np.pi / 180
        self.e = kwargs.get("e")
        self.n = kwargs.get("n") * np.pi / 180
        self.a = kwargs.get("a")

        self.node_long = kwargs.get("node_long") * np.pi / 180
        self.epoch = kwargs.get("epoch")

        peri_arg = kwargs.get("peri_arg")
        peri_long = kwargs.get("peri_long")

        self.peri_long = peri_long * np.pi / 180 if peri_long else peri_arg * np.pi / 180 + self.node_long + np.pi / 2

        L = kwargs.get("L")
        M = kwargs.get("M")

        self.M = M * np.pi / 180 if M else L * np.pi / 180 - self.peri_long

    @property
    def perihelion(self):
        return np.float64(self.a * (1 + self.e))

    @property
    def aphelion(self):
        return np.float64(self.a * (1 - self.e))

    def _get_foci_dist(self):
        return self.perihelion * self.e

    def _get_rotation_matrix(self, theta, ux, uy, uz):

        rotation_array = np.array([
            [
                np.cos(theta) + ux ** 2 * (1 - np.cos(theta)),
                ux * uy * (1 - np.cos(theta)) - uz * np.sin(theta),
                ux * uz * (1 - np.cos(theta)) + uy * np.sin(theta)
            ], [
                ux * uy * (1 - np.cos(theta)) + uz * np.sin(theta),
                np.cos(theta) + uy ** 2 * (1 - np.cos(theta)),
                uy * uz * (1 - np.cos(theta)) - ux * np.sin(theta)
            ], [
                ux * uz * (1 - np.cos(theta)) - uy * np.sin(theta),
                uy * uz * (1 - np.cos(theta)) + ux * np.sin(theta),
                np.cos(theta) + uz ** 2 * (1 - np.cos(theta))
            ]
        ])

        return rotation_array

    def _get_ellipse(self, theta):

        aphelion = self.aphelion
        perihelion = self.perihelion
        foci_dist = self._get_foci_dist()

        ellipse_flat = np.array([
            perihelion * np.cos(theta) - foci_dist,
            aphelion * np.sin(theta),
            0 * theta
        ])

        ux = np.cos(self.node_long)
        uy = np.sin(self.node_long)
        uz = 0

        peri_rotation_array = self._get_rotation_matrix(self.peri_long, 0, 0, 1)

        ellipse_rotated = np.matmul(peri_rotation_array, ellipse_flat)

        incl_rotation_array = self._get_rotation_matrix(self.i, ux, uy, uz)

        ellipse = np.matmul(incl_rotation_array, ellipse_rotated)

        return ellipse

    def ellipse_points(self):

        theta = np.linspace(0, 2 * np.pi, 100)

        ellipse = self._get_ellipse(theta)

        return ellipse

    def _get_days_since_epoch(self):

        epoch = self.epoch

        current_date = datetime.utcnow().timestamp()

        year = int(str(char_map[epoch[0]]) + epoch[1] + epoch[2])
        month = char_map[epoch[3]] if not epoch[3].isdigit() else int(epoch[3])
        day = char_map[epoch[4]] if not epoch[4].isdigit() else int(epoch[4])

        epoch_date = datetime.combine(date(year=year, month=month, day=day), time(hour=12))

        days_since_epoch = (current_date - datetime.timestamp(epoch_date)) / 86400

        return days_since_epoch

    def position(self):

        theta = self._get_true_anomaly(50)

        pos = self._get_ellipse(theta + self.n * self._get_days_since_epoch())

        return np.array([[v] for v in pos])

    def _get_eccentric_anomaly(self, order):

        def _n_sum():

            value = 0
            for i in range(1, order):
                value += (sp.jv(i, i * self.e) / i) * np.sin(i * self.M)

            return value

        eccentric_anomaly = self.M + 2 * _n_sum()

        return eccentric_anomaly

    def _get_true_anomaly(self, order):

        E = self._get_eccentric_anomaly(order)
        beta = np.sqrt(1 + self.e) / np.sqrt(1 - self.e)

        true_anomaly = 2 * np.arctan(beta * np.tan(E / 2))

        return true_anomaly

    def plot_params(self, **kwargs):

        CelestialObject.__plot[self] = {
            "orbit": kwargs.get("orbit", False),
            "position": kwargs.get("position", False),
            "size": int(kwargs.get("size", 3)),
            "width": int(kwargs.get("width", 2)),
            "color": kwargs.get("color", "grey")
        }

    @classmethod
    def plot(cls):
        generate_plot(cls.__plot)
