import pytest

from bloptools import devices, test_functions
from bloptools.bayesian import Agent


@pytest.mark.test_func
def test_acq_funcs_single_task(RE, db):
    dofs = [
        {"device": devices.DOF(name="x1"), "limits": (-8, 8), "kind": "active"},
        {"device": devices.DOF(name="x2"), "limits": (-8, 8), "kind": "active"},
    ]

    tasks = [
        {"key": "himmelblau", "kind": "minimize"},
    ]

    agent = Agent(
        dofs=dofs,
        tasks=tasks,
        digestion=test_functions.constrained_himmelblau_digestion,
        db=db,
    )

    RE(agent.learn("qr", n=64))

    RE(agent.learn("qei", n=2))
    RE(agent.learn("qpi", n=2))