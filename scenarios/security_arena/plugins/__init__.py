"""Scenario plugin system for Security Arena."""

from .base import ScenarioPlugin
from .portfolioiq import PortfolioIQPlugin
from .thingularity import ThingularityPlugin
from .example_medical import MedicalRecordsPlugin


def load_scenario(*args, **kwargs):
    from .registry import load_scenario as _load_scenario

    return _load_scenario(*args, **kwargs)


def list_scenarios(*args, **kwargs):
    from .registry import list_scenarios as _list_scenarios

    return _list_scenarios(*args, **kwargs)


def register_scenario(*args, **kwargs):
    from .registry import register_scenario as _register_scenario

    return _register_scenario(*args, **kwargs)


__all__ = [
    "ScenarioPlugin",
    "load_scenario",
    "list_scenarios",
    "register_scenario",
    "PortfolioIQPlugin",
    "ThingularityPlugin",
    "MedicalRecordsPlugin",
]
