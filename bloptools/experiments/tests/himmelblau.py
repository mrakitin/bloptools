import bluesky.plan_stubs as bps
import bluesky.plans as bp
import numpy as np

from .. import BaseTask
from . import get_dofs

dofs = get_dofs(n=2)
bounds = np.array([[-10.0, +10.0], [-10.0, +10.0]])


class MinHimmelblau(BaseTask):
    name = "minimize_himmelblau"

    def get_fitness(entry):
        return -np.log(1 + 1e-2 * getattr(entry, "himmelblau"))


def initialize():
    yield from bps.null()  # do nothing


def acquisition(dofs, inputs, dets):
    uid = yield from bp.list_scan(dets, *[_ for items in zip(dofs, np.atleast_2d(inputs).T) for _ in items])
    return uid


def digestion(db, uid):
    """
    Evaluates Himmelblau's function (https://en.wikipedia.org/wiki/Himmelblau%27s_function) on the inputs.
    """

    table = db[uid].table()
    products = {"himmelblau": []}

    for index, entry in table.iterrows():
        for param in ["x1", "x2"]:
            if not hasattr(entry, param):
                setattr(entry, param, 0)

        x1_squared = entry.x1**2
        x2_squared = entry.x2**2

        # reject if the inputs are farther than some distance from the origin
        bad = False
        bad |= np.sqrt(x1_squared + x2_squared) > 8

        if not bad:
            himmelblau = (x1_squared + entry.x2 - 11) ** 2 + (entry.x1 + x2_squared - 7) ** 2
        else:
            himmelblau = np.nan

        products["himmelblau"].append(himmelblau)

    return products