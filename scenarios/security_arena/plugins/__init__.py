"""Scenario plugin system for Security Arena"""

from .base import ScenarioPlugin
from .portfolioiq import PortfolioIQPlugin
from .thingularity import ThingularityPlugin
from .example_medical import MedicalRecordsPlugin


def load_scenario(scenario_type: str, config: dict):
    from .registry import load_scenario as _load_scenario

    return _load_scenario(scenario_type, config)


def list_scenarios():
    from .registry import list_scenarios as _list_scenarios

    return _list_scenarios()


def register_scenario(name: str, plugin_class: type[ScenarioPlugin]) -> None:
    from .registry import register_scenario as _register_scenario

    _register_scenario(name, plugin_class)


__all__ = [
    "ScenarioPlugin",
    "load_scenario",
    "list_scenarios",
    "register_scenario",
    "PortfolioIQPlugin",
    "ThingularityPlugin",
    "MedicalRecordsPlugin",
]
